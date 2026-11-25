#!/usr/bin/env node

/**
 * IMAP Email CLI
 * Works with any standard IMAP server (Gmail, ProtonMail Bridge, Fastmail, etc.)
 * Supports IMAP ID extension (RFC 2971) for 163.com and other servers
 */

const Imap = require('imap');
const { simpleParser } = require('mailparser');
const path = require('path');
const fs = require('fs');
const os = require('os');
const net = require('net');
const config = require('./config');

function validateWritePath(dirPath) {
  if (!config.allowedWriteDirs.length) {
    throw new Error('ALLOWED_WRITE_DIRS not set in .env. Attachment download is disabled.');
  }

  const resolved = path.resolve(dirPath.replace(/^~/, os.homedir()));

  const allowedDirs = config.allowedWriteDirs.map(d =>
    path.resolve(d.replace(/^~/, os.homedir()))
  );

  const allowed = allowedDirs.some(dir =>
    resolved === dir || resolved.startsWith(dir + path.sep)
  );

  if (!allowed) {
    throw new Error(`Access denied: '${dirPath}' is outside allowed write directories`);
  }

  return resolved;
}

function sanitizeFilename(filename) {
  return path.basename(filename).replace(/\.\./g, '').replace(/^[./\\]/, '') || 'attachment';
}

// IMAP ID information for 163.com compatibility
const IMAP_ID = {
  name: 'openclaw',
  version: '0.0.1',
  vendor: 'netease',
  'support-email': 'kefu@188.com'
};

const DEFAULT_MAILBOX = config.imap.mailbox;

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
      if (value !== undefined && !value.startsWith('--')) {
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

// Create IMAP connection config
function createImapConfig() {
  return {
    user: config.imap.user,
    password: config.imap.pass,
    host: config.imap.host,
    port: config.imap.port,
    tls: config.imap.tls,
    tlsOptions: {
      rejectUnauthorized: config.imap.rejectUnauthorized,
      // node-imap hands tls.connect() its own socket, so Node does not derive
      // SNI from the host. Without it, multi-tenant hosts such as Gmail
      // present a default certificate and verification fails.
      ...(net.isIP(config.imap.host) ? {} : { servername: config.imap.host }),
    },
    connTimeout: 10000,
    authTimeout: 10000,
  };
}

// Connect to IMAP server with ID support
async function connect() {
  const imapConfig = createImapConfig();

  if (!imapConfig.user || !imapConfig.password) {
    throw new Error('Missing IMAP user or password. Check your config at ~/.config/imap-smtp-email/.env');
  }

  return new Promise((resolve, reject) => {
    const imap = new Imap(imapConfig);

    imap.once('ready', () => {
      // Send IMAP ID (RFC 2971) for 163.com compatibility, but only when the
      // server advertises it. Maddy and other valid servers do not, and
      // node-imap throws synchronously if ID is sent anyway.
      if (imap.serverSupports('ID')) {
        imap.id(IMAP_ID, (err) => {
          if (err) {
            console.warn('Warning: IMAP ID command failed:', err.message);
          }
          resolve(imap);
        });
      } else {
        resolve(imap);
      }
    });

    imap.once('error', (err) => {
      reject(new Error(`IMAP connection failed: ${err.message}`));
    });

    imap.connect();
  });
}

// Open mailbox and return promise
function openBox(imap, mailbox, readOnly = false) {
  return new Promise((resolve, reject) => {
    imap.openBox(mailbox, readOnly, (err, box) => {
      if (err) reject(err);
      else resolve(box);
    });
  });
}

// Search and return UIDs only (node-imap search is UID SEARCH, ascending)
function searchUids(imap, criteria) {
  return new Promise((resolve, reject) => {
    imap.search(criteria, (err, results) => {
      if (err) reject(err);
      else resolve(results || []);
    });
  });
}

// Fetch messages by UID. The server returns them in ascending UID order
// whatever the order of the input array.
function fetchByUids(imap, uids, fetchOptions) {
  return new Promise((resolve, reject) => {
    const fetch = imap.fetch(uids, fetchOptions);
    const messages = [];

    fetch.on('message', (msg) => {
      const parts = [];

      msg.on('body', (stream, info) => {
        let buffer = '';

        stream.on('data', (chunk) => {
          buffer += chunk.toString('utf8');
        });

        stream.once('end', () => {
          parts.push({ which: info.which, body: buffer });
        });
      });

      msg.once('attributes', (attrs) => {
        parts.forEach((part) => {
          part.attributes = attrs;
        });
      });

      msg.once('end', () => {
        if (parts.length > 0) {
          messages.push(parts[0]);
        }
      });
    });

    fetch.once('error', (err) => {
      reject(err);
    });

    fetch.once('end', () => {
      resolve(messages);
    });
  });
}

// Search, then fetch every match
async function searchMessages(imap, criteria, fetchOptions) {
  const uids = await searchUids(imap, criteria);
  if (uids.length === 0) return [];
  return fetchByUids(imap, uids, fetchOptions);
}

// Fetch the newest `limit` matches, newest first. Uses UID order, which
// matches arrival order for mail delivered over SMTP.
async function fetchNewest(imap, criteria, limit, fetchOptions) {
  const uids = await searchUids(imap, criteria);
  if (uids.length === 0) return [];
  return (await fetchByUids(imap, uids.slice(-limit), fetchOptions)).reverse();
}

// Sort by INTERNALDATE, newest first
function byInternalDateDesc(a, b) {
  const dateA = a.attributes.date ? new Date(a.attributes.date) : new Date(0);
  const dateB = b.attributes.date ? new Date(b.attributes.date) : new Date(0);
  return dateB - dateA;
}

// Shape one fetched message for output
async function toResult(item) {
  const parsed = await parseEmail(item.body);
  return {
    uid: item.attributes.uid,
    ...parsed,
    date: item.attributes.date, // INTERNALDATE: when the server received it
    flags: item.attributes.flags,
  };
}

// Parse email from raw buffer
async function parseEmail(bodyStr, includeAttachments = false) {
  const parsed = await simpleParser(bodyStr);

  return {
    from: parsed.from?.text || 'Unknown',
    to: parsed.to?.text,
    subject: parsed.subject || '(no subject)',
    headerDate: parsed.date, // sender's Date header, can be wrong or forged
    text: parsed.text,
    html: parsed.html,
    snippet: parsed.text
      ? parsed.text.slice(0, 200)
      : (parsed.html ? parsed.html.slice(0, 200).replace(/<[^>]*>/g, '') : ''),
    attachments: parsed.attachments?.map((a) => ({
      filename: a.filename,
      contentType: a.contentType,
      size: a.size,
      content: includeAttachments ? a.content : undefined,
      cid: a.cid,
    })),
  };
}

// Check for new/unread emails
async function checkEmails(mailbox = DEFAULT_MAILBOX, limit = 10, recentTime = null, unreadOnly = false) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    // Build search criteria
    const searchCriteria = unreadOnly ? ['UNSEEN'] : ['ALL'];

    if (recentTime) {
      const sinceDate = parseRelativeTime(recentTime);
      searchCriteria.push(['SINCE', sinceDate]);
    }

    const fetchOptions = {
      bodies: [''],
      markSeen: false,
    };

    // Fetch only the newest `limit` messages, not the whole mailbox
    const messages = await fetchNewest(imap, searchCriteria, limit, fetchOptions);

    const results = [];
    for (const item of messages) {
      results.push(await toResult(item));
    }

    return results;
  } finally {
    imap.end();
  }
}

// Fetch full email by UID
async function fetchEmail(uid, mailbox = DEFAULT_MAILBOX) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    const searchCriteria = [['UID', uid]];
    const fetchOptions = {
      bodies: [''],
      markSeen: false,
    };

    const messages = await searchMessages(imap, searchCriteria, fetchOptions);

    if (messages.length === 0) {
      throw new Error(`Message UID ${uid} not found`);
    }

    return toResult(messages[0]);
  } finally {
    imap.end();
  }
}

// Download attachments from email
async function downloadAttachments(uid, mailbox = DEFAULT_MAILBOX, outputDir = '.', specificFilename = null) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    const searchCriteria = [['UID', uid]];
    const fetchOptions = {
      bodies: [''],
      markSeen: false,
    };

    const messages = await searchMessages(imap, searchCriteria, fetchOptions);

    if (messages.length === 0) {
      throw new Error(`Message UID ${uid} not found`);
    }

    const item = messages[0];
    const parsed = await parseEmail(item.body, true);

    if (!parsed.attachments || parsed.attachments.length === 0) {
      return {
        uid,
        downloaded: [],
        message: 'No attachments found',
      };
    }

    // Create output directory if it doesn't exist
    const resolvedDir = validateWritePath(outputDir);
    if (!fs.existsSync(resolvedDir)) {
      fs.mkdirSync(resolvedDir, { recursive: true });
    }

    const downloaded = [];

    for (const attachment of parsed.attachments) {
      // If specificFilename is provided, only download matching attachment
      if (specificFilename && attachment.filename !== specificFilename) {
        continue;
      }
      if (attachment.content) {
        const filePath = path.join(resolvedDir, sanitizeFilename(attachment.filename));
        fs.writeFileSync(filePath, attachment.content);
        downloaded.push({
          filename: attachment.filename,
          path: filePath,
          size: attachment.size,
        });
      }
    }

    // If specific file was requested but not found
    if (specificFilename && downloaded.length === 0) {
      const availableFiles = parsed.attachments.map(a => a.filename).join(', ');
      return {
        uid,
        downloaded: [],
        message: `File "${specificFilename}" not found. Available attachments: ${availableFiles}`,
      };
    }

    return {
      uid,
      downloaded,
      message: `Downloaded ${downloaded.length} attachment(s)`,
    };
  } finally {
    imap.end();
  }
}

// Parse relative time (e.g., "2h", "30m", "7d") to Date
function parseRelativeTime(timeStr) {
  const match = timeStr.match(/^(\d+)(m|h|d)$/);
  if (!match) {
    throw new Error('Invalid time format. Use: 30m, 2h, 7d');
  }

  const value = parseInt(match[1]);
  const unit = match[2];
  const now = new Date();

  switch (unit) {
    case 'm': // minutes
      return new Date(now.getTime() - value * 60 * 1000);
    case 'h': // hours
      return new Date(now.getTime() - value * 60 * 60 * 1000);
    case 'd': // days
      return new Date(now.getTime() - value * 24 * 60 * 60 * 1000);
    default:
      throw new Error('Unknown time unit');
  }
}

// Search emails with criteria
async function searchEmails(options) {
  const imap = await connect();

  try {
    const mailbox = options.mailbox || DEFAULT_MAILBOX;
    await openBox(imap, mailbox);

    const criteria = [];

    if (options.unseen && options.seen) {
      throw new Error('--unseen and --seen cannot be used together');
    }
    if (options.unseen) criteria.push('UNSEEN');
    if (options.seen) criteria.push('SEEN');
    if (options.from) criteria.push(['FROM', options.from]);
    if (options.subject) criteria.push(['SUBJECT', options.subject]);

    // Handle relative time (--recent 2h)
    if (options.recent) {
      const sinceDate = parseRelativeTime(options.recent);
      criteria.push(['SINCE', sinceDate]);
    } else {
      // Handle absolute dates
      if (options.since) criteria.push(['SINCE', options.since]);
      if (options.before) criteria.push(['BEFORE', options.before]);
    }

    // Default to all if no criteria
    if (criteria.length === 0) criteria.push('ALL');

    const fetchOptions = {
      bodies: [''],
      markSeen: false,
    };
    const limit = parseInt(options.limit) || 20;

    // Default: newest by UID, fetching only `limit` messages. --sort date
    // fetches every match and orders by INTERNALDATE, for mailboxes holding
    // copied or imported mail whose UID order differs from arrival order.
    const messages = options.sort === 'date'
      ? (await searchMessages(imap, criteria, fetchOptions)).sort(byInternalDateDesc).slice(0, limit)
      : await fetchNewest(imap, criteria, limit, fetchOptions);

    const results = [];
    for (const item of messages) {
      results.push(await toResult(item));
    }

    return results;
  } finally {
    imap.end();
  }
}

// Mark message(s) as read
async function markAsRead(uids, mailbox = DEFAULT_MAILBOX) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    return new Promise((resolve, reject) => {
      imap.addFlags(uids, '\\Seen', (err) => {
        if (err) reject(err);
        else resolve({ success: true, uids, action: 'marked as read' });
      });
    });
  } finally {
    imap.end();
  }
}

// Mark message(s) as unread
async function markAsUnread(uids, mailbox = DEFAULT_MAILBOX) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    return new Promise((resolve, reject) => {
      imap.delFlags(uids, '\\Seen', (err) => {
        if (err) reject(err);
        else resolve({ success: true, uids, action: 'marked as unread' });
      });
    });
  } finally {
    imap.end();
  }
}

// Create a mailbox if it does not already exist
async function createMailbox(mailbox) {
  const imap = await connect();

  try {
    const mailboxes = await new Promise((resolve, reject) => {
      imap.getBoxes((err, boxes) => {
        if (err) reject(err);
        else resolve(formatMailboxTree(boxes));
      });
    });

    const exists = mailboxes.some((box) => box.name === mailbox);
    if (exists) {
      return { success: true, mailbox, action: 'already exists' };
    }

    return new Promise((resolve, reject) => {
      imap.addBox(mailbox, (err) => {
        if (err) reject(err);
        else resolve({ success: true, mailbox, action: 'created' });
      });
    });
  } finally {
    imap.end();
  }
}

// Copy messages to another mailbox
async function copyMessages(uids, destinationMailbox, mailbox = DEFAULT_MAILBOX) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    return new Promise((resolve, reject) => {
      imap.copy(uids, destinationMailbox, (err, newUIDs) => {
        if (err) reject(err);
        else {
          resolve({
            success: true,
            sourceMailbox: mailbox,
            destinationMailbox,
            uids,
            newUIDs,
            action: 'copied',
          });
        }
      });
    });
  } finally {
    imap.end();
  }
}

// Move messages to another mailbox
async function moveMessages(uids, destinationMailbox, mailbox = DEFAULT_MAILBOX) {
  const imap = await connect();

  try {
    await openBox(imap, mailbox);

    return new Promise((resolve, reject) => {
      imap.move(uids, destinationMailbox, (err, newUIDs) => {
        if (err) reject(err);
        else {
          resolve({
            success: true,
            sourceMailbox: mailbox,
            destinationMailbox,
            uids,
            newUIDs,
            action: 'moved',
          });
        }
      });
    });
  } finally {
    imap.end();
  }
}

// List all mailboxes
async function listMailboxes() {
  const imap = await connect();

  try {
    return new Promise((resolve, reject) => {
      imap.getBoxes((err, boxes) => {
        if (err) reject(err);
        else resolve(formatMailboxTree(boxes));
      });
    });
  } finally {
    imap.end();
  }
}

// Format mailbox tree recursively
function formatMailboxTree(boxes, prefix = '') {
  const result = [];
  for (const [name, info] of Object.entries(boxes)) {
    const fullName = prefix ? `${prefix}${info.delimiter}${name}` : name;
    result.push({
      name: fullName,
      delimiter: info.delimiter,
      attributes: info.attribs,
    });

    if (info.children) {
      result.push(...formatMailboxTree(info.children, fullName));
    }
  }
  return result;
}

// Display accounts in a formatted table
function displayAccounts(accounts, configPath) {
  // Handle no config file case
  if (!configPath) {
    console.error('No configuration file found.');
    console.error('Run "bash setup.sh" to configure your email account.');
    process.exit(1);
  }

  // Handle no accounts case
  if (accounts.length === 0) {
    console.error(`No accounts configured in ${configPath}`);
    process.exit(0);
  }

  // Display header with config path
  console.log(`Configured accounts (from ${configPath}):\n`);

  // Calculate column widths
  const maxNameLen = Math.max(7, ...accounts.map(a => a.name.length)); // 7 = 'Account'.length
  const maxEmailLen = Math.max(5, ...accounts.map(a => a.email.length)); // 5 = 'Email'.length
  const maxImapLen = Math.max(4, ...accounts.map(a => a.imapHost.length)); // 4 = 'IMAP'.length
  const maxSmtpLen = Math.max(4, ...accounts.map(a => a.smtpHost.length)); // 4 = 'SMTP'.length

  // Table header
  const header = `  ${padRight('Account', maxNameLen)}  ${padRight('Email', maxEmailLen)}  ${padRight('IMAP', maxImapLen)}  ${padRight('SMTP', maxSmtpLen)}  Status`;
  console.log(header);

  // Separator line
  const separator = '  ' + '─'.repeat(maxNameLen) + '  ' + '─'.repeat(maxEmailLen) + '  ' + '─'.repeat(maxImapLen) + '  ' + '─'.repeat(maxSmtpLen) + '  ' + '────────────────';
  console.log(separator);

  // Table rows
  for (const account of accounts) {
    const statusIcon = account.isComplete ? '✓' : '⚠';
    const statusText = account.isComplete ? 'Complete' : 'Incomplete';
    const row = `  ${padRight(account.name, maxNameLen)}  ${padRight(account.email, maxEmailLen)}  ${padRight(account.imapHost, maxImapLen)}  ${padRight(account.smtpHost, maxSmtpLen)}  ${statusIcon} ${statusText}`;
    console.log(row);
  }

  // Footer
  console.log(`\n  ${accounts.length} account${accounts.length > 1 ? 's' : ''} total`);
}

// Helper: right-pad a string to a fixed width
function padRight(str, len) {
  return (str + ' '.repeat(len)).slice(0, len);
}

// Main CLI handler
async function main() {
  const { command, options, positional } = parseArgs();

  try {
    let result;

    switch (command) {
      case 'check':
        result = await checkEmails(
          options.mailbox || DEFAULT_MAILBOX,
          parseInt(options.limit) || 10,
          options.recent || null,
          !!options.unseen
        );
        break;

      case 'fetch':
        if (!positional[0]) {
          throw new Error('UID required: node imap.js fetch <uid>');
        }
        result = await fetchEmail(positional[0], options.mailbox);
        break;

      case 'download':
        if (!positional[0]) {
          throw new Error('UID required: node imap.js download <uid>');
        }
        result = await downloadAttachments(positional[0], options.mailbox, options.dir || '.', options.file || null);
        break;

      case 'search':
        result = await searchEmails(options);
        break;

      case 'mark-read':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js mark-read <uid> [uid2...]');
        }
        result = await markAsRead(positional, options.mailbox);
        break;

      case 'mark-unread':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js mark-unread <uid> [uid2...]');
        }
        result = await markAsUnread(positional, options.mailbox);
        break;

      case 'create-mailbox':
        if (!positional[0]) {
          throw new Error('Mailbox name required: node imap.js create-mailbox <name>');
        }
        result = await createMailbox(positional[0]);
        break;

      case 'copy':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js copy <uid> [uid2...] --to <mailbox>');
        }
        if (!options.to) {
          throw new Error('Destination mailbox required: --to <mailbox>');
        }
        result = await copyMessages(positional, options.to, options.mailbox || DEFAULT_MAILBOX);
        break;

      case 'move':
        if (positional.length === 0) {
          throw new Error('UID(s) required: node imap.js move <uid> [uid2...] --to <mailbox>');
        }
        if (!options.to) {
          throw new Error('Destination mailbox required: --to <mailbox>');
        }
        result = await moveMessages(positional, options.to, options.mailbox || DEFAULT_MAILBOX);
        break;

      case 'list-mailboxes':
        result = await listMailboxes();
        break;

      case 'list-accounts':
        {
          const { listAccounts } = require('./config');
          const { accounts, configPath } = listAccounts();
          displayAccounts(accounts, configPath);
        }
        return;  // Exit early, no JSON output

      default:
        console.error('Unknown command:', command);
        console.error('Available commands: check, fetch, download, search, mark-read, mark-unread, create-mailbox, copy, move, list-mailboxes, list-accounts');
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
