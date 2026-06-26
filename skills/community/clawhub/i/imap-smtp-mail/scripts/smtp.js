#!/usr/bin/env node

/**
 * SMTP Email CLI
 * Send email via SMTP protocol. Works with Gmail, Outlook, 163.com, and any standard SMTP server.
 * Supports attachments, HTML content, and multiple recipients.
 */

const nodemailer = require('nodemailer');
const Imap = require('imap');
const MailComposer = require('nodemailer/lib/mail-composer');
const path = require('path');
const os = require('os');
const fs = require('fs');
const util = require('util');
const { randomUUID } = require('crypto');
const EMAIL_ENV_DEFAULT = path.join(os.homedir(), '.openclaw', 'credentials', 'imap-smtp-mail.env');
const EMAIL_ENV_FILE = process.env.EMAIL_ENV_FILE || EMAIL_ENV_DEFAULT;
require('dotenv').config({ path: EMAIL_ENV_FILE });
const { fetchEmail } = require('./imap');

const WORKSPACE_ROOT = (() => {
  if (process.env.OPENCLAW_WORKSPACE) return path.resolve(process.env.OPENCLAW_WORKSPACE);
  let dir = path.resolve(__dirname);
  while (dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, '.openclaw')) || fs.existsSync(path.join(dir, 'AGENTS.md'))) return dir;
    dir = path.dirname(dir);
  }
  return path.resolve(__dirname, '../../..');
})();

function getDomainFromEmail(value) {
  const email = String(value || '').trim();
  const atIndex = email.lastIndexOf('@');
  if (atIndex === -1 || atIndex === email.length - 1) {
    return '';
  }
  return email.slice(atIndex + 1).trim();
}

function getTransportClientName() {
  const explicit = String(process.env.SMTP_CLIENT_NAME || '').trim();
  if (explicit) {
    return explicit;
  }

  const derivedDomain = getDomainFromEmail(process.env.SMTP_FROM || process.env.SMTP_USER);
  if (derivedDomain) {
    return derivedDomain;
  }

  return os.hostname();
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function textToHtml(value) {
  const normalized = String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  const paragraphs = normalized
    .split(/\n{2,}/)
    .map(part => part.trim())
    .filter(Boolean);

  if (paragraphs.length === 0) {
    return '';
  }

  return paragraphs
    .map(part => `<p>${escapeHtml(part).replace(/\n/g, '<br>')}</p>`)
    .join('\n');
}

function resolveWorkspacePath(inputPath) {
  const expanded = inputPath.replace(/^~/, os.homedir());
  let realPath;
  try {
    realPath = fs.realpathSync(expanded);
  } catch {
    realPath = path.resolve(expanded);
  }

  if (realPath !== WORKSPACE_ROOT && !realPath.startsWith(WORKSPACE_ROOT + path.sep)) {
    throw new Error(`Path must stay inside workspace: '${inputPath}'`);
  }

  return realPath;
}

function validateReadPath(inputPath) {
  const expanded = inputPath.replace(/^~/, os.homedir());
  let realPath;
  try {
    realPath = fs.realpathSync(expanded);
  } catch {
    realPath = path.resolve(expanded);
  }

  const allowedDirsStr = process.env.ALLOWED_READ_DIRS;
  if (!allowedDirsStr) {
    throw new Error('ALLOWED_READ_DIRS not set in credentials file. File read operations are disabled.');
  }

  const allowedDirs = allowedDirsStr.split(',').map(d =>
    path.resolve(d.trim().replace(/^~/, os.homedir()))
  );

  const allowed = allowedDirs.some(dir =>
    realPath === dir || realPath.startsWith(dir + path.sep)
  );

  if (!allowed) {
    throw new Error(`Access denied: '${inputPath}' is outside allowed read directories`);
  }

  return realPath;
}

function normalizeLookupValue(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function decodeEscapedText(value) {
  if (typeof value !== 'string') {
    return value;
  }

  return value
    .replace(/\\r\\n/g, '\n')
    .replace(/\\n/g, '\n')
    .replace(/\\r/g, '\n')
    .replace(/\\t/g, '\t');
}

function getContactsFilePath() {
  const configuredPath = process.env.EMAIL_CONTACTS_FILE
    || path.join(WORKSPACE_ROOT, 'contacts', 'email-contacts.json');
  return resolveWorkspacePath(configuredPath);
}

function loadContacts() {
  const contactsPath = getContactsFilePath();

  if (!fs.existsSync(contactsPath)) {
    return { contactsPath, contacts: [] };
  }

  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(contactsPath, 'utf8'));
  } catch (err) {
    throw new Error(`Invalid contacts file '${contactsPath}': ${err.message}`);
  }

  if (!parsed || !Array.isArray(parsed.contacts)) {
    throw new Error(`Contacts file '${contactsPath}' must contain a 'contacts' array`);
  }

  const contacts = parsed.contacts
    .filter(contact => contact && contact.email)
    .map((contact, index) => ({
      id: String(contact.id || `contact-${index + 1}`).trim(),
      name: String(contact.name || '').trim(),
      email: String(contact.email || '').trim(),
      phone: String(contact.phone || '').trim(),
      aliases: Array.isArray(contact.aliases)
        ? contact.aliases.map(alias => String(alias || '').trim()).filter(Boolean)
        : [],
      tags: Array.isArray(contact.tags)
        ? contact.tags.map(tag => String(tag || '').trim()).filter(Boolean)
        : [],
      notes: String(contact.notes || '').trim(),
    }));

  return { contactsPath, contacts };
}

function formatContact(contact) {
  return {
    id: contact.id,
    name: contact.name,
    email: contact.email,
    phone: contact.phone || null,
    aliases: contact.aliases,
    tags: contact.tags,
    notes: contact.notes,
  };
}

function getContactNeedles(contact) {
  return [
    contact.id,
    contact.name,
    contact.email,
    contact.phone,
    ...contact.aliases,
  ].map(normalizeLookupValue).filter(Boolean);
}

function formatCandidates(contacts) {
  return contacts
    .slice(0, 5)
    .map(contact => `${contact.name || contact.id} <${contact.email}>`)
    .join(', ');
}

function resolveContact(query) {
  const { contactsPath, contacts } = loadContacts();
  const lookup = normalizeLookupValue(query);

  if (!lookup) {
    throw new Error('Missing required option: --contact <name>');
  }

  const exactMatches = contacts.filter(contact => getContactNeedles(contact).includes(lookup));
  if (exactMatches.length === 1) {
    return { contactsPath, contact: exactMatches[0] };
  }
  if (exactMatches.length > 1) {
    throw new Error(`Contact query is ambiguous: ${formatCandidates(exactMatches)}`);
  }

  const partialMatches = contacts.filter(contact =>
    getContactNeedles(contact).some(value => value.includes(lookup))
  );
  if (partialMatches.length === 1) {
    return { contactsPath, contact: partialMatches[0] };
  }
  if (partialMatches.length > 1) {
    throw new Error(`Multiple contacts match '${query}': ${formatCandidates(partialMatches)}`);
  }

  throw new Error(`No contact found for '${query}' in ${contactsPath}`);
}

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        options[key] = value;
        i++;
      } else {
        options[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }

  return { command, options, positional };
}

function isTruthy(value) {
  return value === true || value === 'true' || value === '1' || value === 'yes';
}

function createDebugLogger() {
  const levels = ['trace', 'debug', 'info', 'warn', 'error', 'fatal'];
  const logger = {};

  for (const level of levels) {
    logger[level] = (data, message, ...args) => {
      const renderedMessage = args.length > 0
        ? util.format(message, ...args)
        : message;
      const meta = data && typeof data === 'object' ? { ...data } : {};
      delete meta.src;
      delete meta.tnx;

      const payload = {
        level,
        message: renderedMessage,
      };

      if (Object.keys(meta).length > 0) {
        payload.meta = meta;
      }

      console.error(`[smtp-debug] ${JSON.stringify(payload)}`);
    };
  }

  return logger;
}

function sanitizeTransportConfig(config) {
  return {
    host: config.host,
    port: config.port,
    secure: config.secure,
    name: config.name || null,
    authUser: config.auth?.user || null,
    tlsRejectUnauthorized: config.tls?.rejectUnauthorized !== false,
  };
}

function createImapConfig() {
  return {
    user: process.env.IMAP_USER,
    password: process.env.IMAP_PASS,
    host: process.env.IMAP_HOST || '127.0.0.1',
    port: parseInt(process.env.IMAP_PORT, 10) || 1143,
    tls: process.env.IMAP_TLS === 'true',
    tlsOptions: {
      rejectUnauthorized: process.env.IMAP_REJECT_UNAUTHORIZED !== 'false',
    },
    connTimeout: 10000,
    authTimeout: 10000,
  };
}

function hasImapConfig() {
  return Boolean(process.env.IMAP_HOST && process.env.IMAP_USER && process.env.IMAP_PASS);
}

function shouldSaveSentCopy(options) {
  if (!hasImapConfig()) {
    return false;
  }

  if (options.saveSent === false || options.saveSent === 'false') {
    return false;
  }

  return process.env.IMAP_SAVE_SENT !== 'false';
}

function connectImap() {
  const config = createImapConfig();

  if (!config.user || !config.password) {
    throw new Error('Missing IMAP_USER or IMAP_PASS environment variables');
  }

  return new Promise((resolve, reject) => {
    const imap = new Imap(config);

    imap.once('ready', () => resolve(imap));
    imap.once('error', (err) => reject(new Error(`IMAP connection failed: ${err.message}`)));

    imap.connect();
  });
}

function getMailboxes(imap) {
  return new Promise((resolve, reject) => {
    imap.getBoxes((err, boxes) => {
      if (err) reject(err);
      else resolve(boxes);
    });
  });
}

function normalizeMailboxName(value) {
  return String(value || '').trim().toLowerCase();
}

function flattenMailboxes(boxes, prefix = '') {
  const result = [];

  for (const [name, info] of Object.entries(boxes || {})) {
    const fullName = prefix ? `${prefix}${info.delimiter}${name}` : name;
    result.push({
      name: fullName,
      attribs: Array.isArray(info.attribs) ? info.attribs : [],
    });

    if (info.children) {
      result.push(...flattenMailboxes(info.children, fullName));
    }
  }

  return result;
}

function resolveSentMailboxName(boxes) {
  const configured = String(process.env.IMAP_SENT_MAILBOX || '').trim();
  if (configured) {
    return configured;
  }

  const flat = flattenMailboxes(boxes);
  const byAttr = flat.find(box =>
    box.attribs.some(attr => normalizeMailboxName(attr) === '\\sent')
  );
  if (byAttr) {
    return byAttr.name;
  }

  const candidates = [
    'Sent',
    'Sent Items',
    'Sent Mail',
    'Sent Messages',
    'INBOX.Sent',
    'INBOX.Sent Items',
    'Envoyés',
    'Messages envoyés',
  ];

  for (const candidate of candidates) {
    const match = flat.find(box => normalizeMailboxName(box.name) === normalizeMailboxName(candidate));
    if (match) {
      return match.name;
    }
  }

  return configured || 'Sent';
}

function appendToMailbox(imap, mailbox, rawMessage) {
  return new Promise((resolve, reject) => {
    imap.append(rawMessage, {
      mailbox,
      flags: ['\\Seen'],
    }, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

async function saveSentCopy(rawMessage, mailOptions) {
  const imap = await connectImap();

  try {
    const boxes = await getMailboxes(imap);
    const mailbox = resolveSentMailboxName(boxes);
    await appendToMailbox(imap, mailbox, rawMessage);
    return {
      success: true,
      mailbox,
    };
  } finally {
    imap.end();
  }
}

function ensureStableMailIdentity(mailOptions) {
  if (!mailOptions.date) {
    mailOptions.date = new Date();
  }

  if (!mailOptions.messageId) {
    const domain = getDomainFromEmail(
      typeof mailOptions.from === 'string'
        ? mailOptions.from
        : (mailOptions.from?.address || process.env.SMTP_FROM || process.env.SMTP_USER)
    ) || 'localhost';
    mailOptions.messageId = `<${randomUUID()}@${domain}>`;
  }

  return mailOptions;
}

function buildRawMessage(mailOptions) {
  const composer = new MailComposer(mailOptions);
  return new Promise((resolve, reject) => {
    composer.compile().build((err, message) => {
      if (err) reject(err);
      else resolve(message);
    });
  });
}

// Create SMTP transporter
function createTransporter(options = {}) {
  const config = {
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT) || 587,
    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
    name: getTransportClientName(),
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
    tls: {
      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
    },
  };

  if (isTruthy(options.debug)) {
    config.logger = createDebugLogger();
    config.debug = true;
  }

  if (!config.host || !config.auth.user || !config.auth.pass) {
    throw new Error('Missing SMTP configuration. Please set SMTP_HOST, SMTP_USER, and SMTP_PASS in credentials file');
  }

  return nodemailer.createTransport(config);
}

function normalizeEmailAddress(value) {
  return String(value || '').trim().toLowerCase();
}

function dedupeAddressObjects(addresses, seen = new Set()) {
  const nextSeen = new Set(seen);
  const unique = [];

  for (const entry of Array.isArray(addresses) ? addresses : []) {
    const address = String(entry?.address || '').trim();
    const key = normalizeEmailAddress(address);
    if (!key || nextSeen.has(key)) {
      continue;
    }

    nextSeen.add(key);
    unique.push({
      name: String(entry?.name || '').trim() || undefined,
      address,
    });
  }

  return {
    addresses: unique,
    seen: nextSeen,
  };
}

function collectOwnAddresses(options = {}) {
  return new Set(
    [
      options.from,
      process.env.SMTP_FROM,
      process.env.SMTP_USER,
      process.env.SMTP_REPLY_TO,
    ]
      .map(normalizeEmailAddress)
      .filter(Boolean)
  );
}

function buildReplySubject(subject) {
  const trimmed = String(subject || '').trim();
  if (!trimmed) {
    return 'Re: (no subject)';
  }

  return /^\s*re\s*:/i.test(trimmed) ? trimmed : `Re: ${trimmed}`;
}

function buildReplyReferences(originalMessage) {
  const references = Array.isArray(originalMessage?.references)
    ? originalMessage.references.map((entry) => String(entry || '').trim()).filter(Boolean)
    : [];
  const messageId = String(originalMessage?.messageId || '').trim();

  if (messageId && !references.includes(messageId)) {
    references.push(messageId);
  }

  return references;
}

function buildReplyMetadata(originalMessage, options = {}) {
  const replyAll = isTruthy(options['reply-all']) || isTruthy(options.replyAll);
  const ownAddresses = collectOwnAddresses(options);
  const primarySource = Array.isArray(originalMessage?.replyToAddresses) && originalMessage.replyToAddresses.length > 0
    ? originalMessage.replyToAddresses
    : (Array.isArray(originalMessage?.fromAddresses) && originalMessage.fromAddresses.length > 0
        ? originalMessage.fromAddresses
        : (Array.isArray(originalMessage?.senderAddresses) ? originalMessage.senderAddresses : []));
  const primaryRecipients = dedupeAddressObjects(primarySource, ownAddresses);

  if (primaryRecipients.addresses.length === 0) {
    throw new Error(`Unable to resolve reply recipient(s) from message UID ${originalMessage?.uid ?? 'unknown'}`);
  }

  let toRecipients = primaryRecipients.addresses;
  let seen = primaryRecipients.seen;
  let ccRecipients = [];

  if (replyAll) {
    const extraToRecipients = dedupeAddressObjects(originalMessage?.toAddresses || [], seen);
    toRecipients = toRecipients.concat(extraToRecipients.addresses);
    seen = extraToRecipients.seen;

    const extraCcRecipients = dedupeAddressObjects(originalMessage?.ccAddresses || [], seen);
    ccRecipients = extraCcRecipients.addresses;
  }

  const references = buildReplyReferences(originalMessage);

  return {
    mode: replyAll ? 'reply-all' : 'reply',
    to: toRecipients,
    cc: ccRecipients,
    subject: buildReplySubject(originalMessage?.subject),
    inReplyTo: String(originalMessage?.messageId || '').trim() || undefined,
    references: references.length > 0 ? references : undefined,
    original: {
      uid: originalMessage?.uid ?? null,
      subject: originalMessage?.subject ?? null,
      from: originalMessage?.from ?? null,
      replyTo: originalMessage?.replyTo ?? null,
      to: originalMessage?.to ?? null,
      cc: originalMessage?.cc ?? null,
      messageId: originalMessage?.messageId ?? null,
    },
  };
}

async function applyReplyContext(options) {
  const replyUid = options['reply-uid'] || options.replyUid;
  if (!replyUid) {
    if (isTruthy(options['reply-all']) || isTruthy(options.replyAll)) {
      throw new Error('The --reply-all flag requires --reply-uid <uid>');
    }
    return null;
  }

  const originalMessage = await fetchEmail(replyUid, options.mailbox);
  const replyMetadata = buildReplyMetadata(originalMessage, options);

  if (!options.to) {
    options.to = replyMetadata.to;
  }
  if (!options.cc && replyMetadata.cc.length > 0) {
    options.cc = replyMetadata.cc;
  }
  if (!options.subject) {
    options.subject = replyMetadata.subject;
  }
  if (!options.inReplyTo && replyMetadata.inReplyTo) {
    options.inReplyTo = replyMetadata.inReplyTo;
  }
  if (!options.references && replyMetadata.references) {
    options.references = replyMetadata.references;
  }

  options.replyContext = replyMetadata;
  return replyMetadata;
}

function buildMailOptions(options) {
  const fromAddress = options.from || process.env.SMTP_FROM || process.env.SMTP_USER;
  const fromName = String(options.fromName || process.env.SMTP_FROM_NAME || '').trim();
  const replyTo = options.replyTo || process.env.SMTP_REPLY_TO || undefined;

  return {
    from: fromName
      ? { name: fromName, address: fromAddress }
      : fromAddress,
    to: options.to,
    cc: options.cc || undefined,
    bcc: options.bcc || undefined,
    replyTo,
    inReplyTo: options.inReplyTo || undefined,
    references: options.references || undefined,
    subject: options.subject || '(no subject)',
    text: options.text || undefined,
    html: options.html || undefined,
    attachments: options.attachments || [],
  };
}

function normalizeComposedContent(options) {
  if (options.subject) {
    options.subject = decodeEscapedText(options.subject).trim();
  }

  if (typeof options.text === 'string') {
    options.text = decodeEscapedText(options.text);
  }

  if (typeof options.body === 'string') {
    options.body = decodeEscapedText(options.body);
  }

  if (typeof options.html === 'string') {
    options.html = decodeEscapedText(options.html);
  }
}

function summarizeAttachments(attachments) {
  return (attachments || []).map(attachment => ({
    filename: attachment.filename,
    path: attachment.path,
  }));
}

async function prepareSendOptions(inputOptions) {
  const options = { ...inputOptions };
  let resolvedContact = null;

  if (!options.to && options.contact) {
    const resolved = resolveContact(options.contact);
    resolvedContact = resolved.contact;
    options.to = resolved.contact.email;
  }

  if (options['subject-file']) {
    validateReadPath(options['subject-file']);
    options.subject = fs.readFileSync(options['subject-file'], 'utf8').trim();
  }

  if (options['body-file']) {
    validateReadPath(options['body-file']);
    const content = fs.readFileSync(options['body-file'], 'utf8');
    if (options['body-file'].endsWith('.html') || options.html) {
      options.html = content;
    } else {
      options.text = content;
    }
  } else if (options['html-file']) {
    validateReadPath(options['html-file']);
    options.html = fs.readFileSync(options['html-file'], 'utf8');
  } else if (options.body) {
    options.text = options.body;
  }

  if (options.attach) {
    const attachFiles = options.attach.split(',').map(f => f.trim()).filter(Boolean);
    options.attachments = attachFiles.map(f => readAttachment(f));
  }

  normalizeComposedContent(options);
  await applyReplyContext(options);

  return {
    options,
    resolvedContact,
  };
}

// Send email
async function sendEmail(options) {
  const transporter = createTransporter(options);

  // Verify connection
  try {
    await transporter.verify();
    console.error('SMTP server is ready to send');
  } catch (err) {
    throw new Error(`SMTP connection failed: ${err.message}`);
  }

  const mailOptions = buildMailOptions(options);

  if (!mailOptions.text && !mailOptions.html) {
    mailOptions.text = options.body || '';
  }

  if (mailOptions.text && !mailOptions.html) {
    mailOptions.html = textToHtml(mailOptions.text);
  }

  ensureStableMailIdentity(mailOptions);
  const rawMessage = await buildRawMessage(mailOptions);

  const info = await transporter.sendMail(mailOptions);

  const result = {
    success: true,
    messageId: info.messageId,
    response: info.response,
    to: mailOptions.to,
    cc: mailOptions.cc || null,
    subject: mailOptions.subject,
    inReplyTo: mailOptions.inReplyTo || null,
    references: mailOptions.references || null,
  };

  if (options.replyContext) {
    result.reply = options.replyContext;
  }

  if (isTruthy(options.debug)) {
    result.debug = {
      transport: sanitizeTransportConfig(transporter.options || {}),
      envelope: info.envelope || null,
      accepted: info.accepted || [],
      rejected: info.rejected || [],
      pending: info.pending || [],
    };
  }

  if (shouldSaveSentCopy(options)) {
    try {
      const saveSentResult = await saveSentCopy(rawMessage, mailOptions);
      result.savedToSent = true;
      result.sentMailbox = saveSentResult.mailbox;
      if (result.debug) {
        result.debug.sentCopy = saveSentResult;
      }
    } catch (err) {
      result.savedToSent = false;
      result.sentMailbox = null;
      result.sentCopyError = err.message;
      if (result.debug) {
        result.debug.sentCopy = {
          success: false,
          error: err.message,
        };
      }
    }
  } else {
    result.savedToSent = false;
    result.sentMailbox = null;
  }

  return result;
}

// Read file content for attachments
function readAttachment(filePath) {
  validateReadPath(filePath);
  if (!fs.existsSync(filePath)) {
    throw new Error(`Attachment file not found: ${filePath}`);
  }
  return {
    filename: path.basename(filePath),
    path: path.resolve(filePath),
  };
}

function buildApprovalPreview(options) {
  const mailOptions = buildMailOptions(options);
  if (!mailOptions.text && !mailOptions.html) {
    mailOptions.text = options.body || '';
  }

  if (mailOptions.text && !mailOptions.html) {
    mailOptions.html = textToHtml(mailOptions.text);
  }

  return {
    success: true,
    approvalRequired: true,
    approved: false,
    draft: {
      from: mailOptions.from,
      to: mailOptions.to,
      cc: mailOptions.cc || null,
      bcc: mailOptions.bcc || null,
      replyTo: mailOptions.replyTo || null,
      inReplyTo: mailOptions.inReplyTo || null,
      references: mailOptions.references || null,
      subject: mailOptions.subject,
      text: mailOptions.text || null,
      html: mailOptions.html || null,
      attachments: summarizeAttachments(options.attachments),
      reply: options.replyContext || null,
    },
    message: 'Email draft ready. Re-run with --approve to send.',
  };
}

// Test SMTP connection
async function testConnection(options = {}) {
  const transporter = createTransporter(options);

  try {
    await transporter.verify();
    const info = await transporter.sendMail({
      from: String(process.env.SMTP_FROM_NAME || '').trim()
        ? {
            name: String(process.env.SMTP_FROM_NAME || '').trim(),
            address: process.env.SMTP_FROM || process.env.SMTP_USER,
          }
        : (process.env.SMTP_FROM || process.env.SMTP_USER),
      replyTo: process.env.SMTP_REPLY_TO || undefined,
      to: process.env.SMTP_USER, // Send to self
      subject: 'SMTP Connection Test',
      text: 'This is a test email from the IMAP/SMTP email skill.',
      html: '<p>This is a <strong>test email</strong> from the IMAP/SMTP email skill.</p>',
    });

    const result = {
      success: true,
      message: 'SMTP connection successful',
      messageId: info.messageId,
    };

    if (isTruthy(options.debug)) {
      result.debug = {
        transport: sanitizeTransportConfig(transporter.options || {}),
        envelope: info.envelope || null,
        accepted: info.accepted || [],
        rejected: info.rejected || [],
        pending: info.pending || [],
      };
    }

    return result;
  } catch (err) {
    throw new Error(`SMTP test failed: ${err.message}`);
  }
}

// Main CLI handler
async function main() {
  const { command, options, positional } = parseArgs();

  try {
    let result;

    switch (command) {
      case 'send': {
        const prepared = await prepareSendOptions(options);
        const sendOptions = prepared.options;

        if (!sendOptions.to) {
          throw new Error('Missing required option: --to <email> or --reply-uid <uid>');
        }
        if (!sendOptions.subject) {
          throw new Error('Missing required option: --subject <text>, --subject-file <file>, or --reply-uid <uid>');
        }

        if (sendOptions.approve !== true && sendOptions.approve !== 'true') {
          result = buildApprovalPreview(sendOptions);
        } else {
          result = await sendEmail(sendOptions);
          result.approved = true;
        }
        if (prepared.resolvedContact) {
          result.contact = formatContact(prepared.resolvedContact);
          if (result.draft) {
            result.draft.contact = formatContact(prepared.resolvedContact);
          }
        }
        break;
      }

      case 'test':
        result = await testConnection(options);
        break;

      case 'contacts': {
        const { contactsPath, contacts } = loadContacts();
        if (options.query) {
          const lookup = normalizeLookupValue(options.query);
          const matches = contacts.filter(contact =>
            getContactNeedles(contact).some(value => value.includes(lookup))
          );
          result = {
            success: true,
            contactsFile: contactsPath,
            query: options.query,
            matches: matches.map(formatContact),
          };
        } else {
          result = {
            success: true,
            contactsFile: contactsPath,
            contacts: contacts.map(formatContact),
          };
        }
        break;
      }

      case 'resolve-contact': {
        const query = options.contact || positional[0];
        const { contactsPath, contact } = resolveContact(query);
        result = {
          success: true,
          contactsFile: contactsPath,
          contact: formatContact(contact),
        };
        break;
      }

      default:
        console.error('Unknown command:', command);
        console.error('Available commands: send, test, contacts, resolve-contact');
        console.error('\nUsage:');
        console.error('  send   --to <email> --subject <text> [--body <text>] [--html] [--cc <email>] [--bcc <email>] [--attach <file>] [--approve] [--debug]');
        console.error('  send   --contact <name> --subject <text> [--body <text>] [--html] [--cc <email>] [--bcc <email>] [--attach <file>] [--approve] [--debug]');
        console.error('  send   --reply-uid <uid> [--reply-all] [--mailbox <name>] [--body <text>] [--attach <file>] [--approve] [--debug]');
        console.error('  send   --reply-uid <uid> [--reply-all] --body-file <file> [--html-file <file>] [--attach <file>] [--approve] [--debug]');
        console.error('  send   --to <email> --subject <text> --body-file <file> [--html-file <file>] [--attach <file>] [--approve] [--debug]');
        console.error('  test   Test SMTP connection [--debug]');
        console.error('  contacts [--query <text>]');
        console.error('  resolve-contact --contact <name>');
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = {
  buildMailOptions,
  buildReplyMetadata,
  buildReplyReferences,
  buildReplySubject,
  prepareSendOptions,
  sendEmail,
};

if (require.main === module) {
  main();
}
