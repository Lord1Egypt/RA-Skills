#!/usr/bin/env node
/**
 * outlook-mail-fetch.mjs — Fetch the signed-in user's Outlook mail via an MSAL refresh token.
 * Zero external deps. Uses Microsoft Graph with a short-lived access token supplied on stdin.
 * NOT read-only — the accurate statement of what this file can change:
 *   - NEVER SENDS. There is no send/reply/forward call anywhere in this file, by design.
 *   - WRITES: it can CREATE and PATCH (overwrite) message drafts via Microsoft Graph.
 *     `saveDraft` issues PATCH /me/messages/{id}, which replaces an existing draft's body.
 *   - NEVER PERSISTS CREDENTIALS: a short-lived access token is read from stdin for one run.
 *   - EXPORTS: --fetch-all writes a local mailbox archive and requires an explicit --yes.
 * An earlier version of this header said "READ-ONLY + DRAFT-ONLY". That was wrong and is
 * exactly the kind of claim a reviewer would rely on: PATCH has been in this file the whole
 * time. Corrected 2026-09-07.
 * --fetch-all writes a local mailbox archive to disk and requires an explicit --yes.
 * 
 * Usage:
 *   printf '%s' "$TOKEN" | node outlook-mail-fetch.mjs --test --access-token-stdin
 *   printf '%s' "$TOKEN" | node outlook-mail-fetch.mjs --test --access-token-stdin
 *   printf '%s' "$TOKEN" | node outlook-mail-fetch.mjs --fetch-all --yes --access-token-stdin [--months 6]
 */
import { readFileSync, writeFileSync, mkdirSync, appendFileSync, existsSync, chmodSync, lstatSync } from 'fs';
import { dirname, join, resolve } from 'path';
import { homedir } from 'os';

const OUTPUT_DIR = join(homedir(), '.openclaw/workspace/data/outlook-emails');
const GRAPH = 'https://graph.microsoft.com/v1.0';

function ensurePrivateDir(dir) {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  if (lstatSync(dir).isSymbolicLink()) throw new Error(`Refusing symlink output directory: ${dir}`);
  chmodSync(dir, 0o700);
}

function preparePrivateFile(file) {
  if (existsSync(file) && lstatSync(file).isSymbolicLink()) throw new Error(`Refusing symlink output file: ${file}`);
  writeFileSync(file, '', { mode: 0o600 });
  chmodSync(file, 0o600);
}

function writePrivateFile(file, data) {
  if (existsSync(file) && lstatSync(file).isSymbolicLink()) throw new Error(`Refusing symlink output file: ${file}`);
  writeFileSync(file, data, { mode: 0o600 });
  chmodSync(file, 0o600);
}

ensurePrivateDir(OUTPUT_DIR);

function assertAllowedUrl(raw) {
  const u = new URL(raw);
  if (u.protocol !== 'https:' || u.hostname !== 'graph.microsoft.com' || u.username || u.password || u.port) {
    throw new Error(`Refusing credentialed request outside https://graph.microsoft.com: ${u.origin}`);
  }
  const path = u.pathname;
  const allowed = [
    /^\/v1\.0\/me\/messages(?:\/|$)/,
    /^\/v1\.0\/me\/mailFolders\/drafts\/messages$/,
  ];
  if (!allowed.some((re) => re.test(path))) {
    throw new Error(`Refusing Graph path outside mail/drafts: ${path}`);
  }
}

function assertGraphId(id) {
  if (typeof id !== 'string' || !id) throw new Error('Missing Graph message id');
  if (id.length > 512) throw new Error('Graph message id too long');
  if (!/^[A-Za-z0-9=_-]+$/.test(id)) throw new Error('Graph message id contains disallowed characters');
}

let currentToken = null;
async function readAccessTokenFromStdin() {
  if (!process.argv.includes('--access-token-stdin')) {
    throw new Error('Pass a short-lived Graph access token on stdin with --access-token-stdin; this skill never stores credentials');
  }
  if (process.stdin.isTTY) throw new Error('Pipe the access token on stdin; command-line tokens are refused');
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const token = Buffer.concat(chunks).toString('utf8').trim();
  if (!token) throw new Error('No access token received on stdin');
  return token;
}

// --- Graph API helpers ---

async function graphGet(url, retried = false) {
  assertAllowedUrl(url);
  if (!currentToken) currentToken = await readAccessTokenFromStdin();
  const resp = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${currentToken}`,
      'Prefer': 'outlook.body-content-type="text"'
    }
  });
  if (resp.status === 401 && !retried) {
    throw new Error('Access token expired; obtain a new short-lived token and retry');
  }
  if (!resp.ok) throw new Error(`Graph API ${resp.status}: ${await resp.text()}`);
  return resp.json();
}

// Generic Graph request with method/body control + optional HTML body preference.
async function graphReq(method, url, { json, preferHtml = false } = {}, retried = false) {
  assertAllowedUrl(url);
  if (!currentToken) currentToken = await readAccessTokenFromStdin();
  const headers = { 'Authorization': `Bearer ${currentToken}` };
  if (preferHtml) headers['Prefer'] = 'outlook.body-content-type="html"';
  let body;
  if (json !== undefined) { headers['Content-Type'] = 'application/json'; body = JSON.stringify(json); }
  const resp = await fetch(url, { method, headers, body });
  if (resp.status === 401 && !retried) {
    throw new Error('Access token expired; obtain a new short-lived token and retry');
  }
  if (!resp.ok) throw new Error(`Graph API ${resp.status}: ${await resp.text()}`);
  const text = await resp.text();
  return text ? JSON.parse(text) : {};
}

const htmlToText = (html) => (html || '')
  .replace(/<[^>]*>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/\s{2,}/g, ' ').trim();

// --- Drafts & single-message access ---

async function listDrafts(limit = 15) {
  const sel = 'id,subject,toRecipients,ccRecipients,createdDateTime,lastModifiedDateTime,hasAttachments';
  const data = await graphGet(`${GRAPH}/me/mailFolders/drafts/messages?$top=${limit}&$select=${sel}&$orderby=lastModifiedDateTime desc`);
  for (const m of data.value || []) {
    const to = (m.toRecipients || []).map(r => r.emailAddress.address).join(', ');
    const cc = (m.ccRecipients || []).map(r => r.emailAddress.address).join(', ');
    console.log(`\n[${m.lastModifiedDateTime}] ${m.subject || '(no subject)'}${m.hasAttachments ? ' 📎' : ''}`);
    console.log(`  to: ${to}`);
    if (cc) console.log(`  cc: ${cc}`);
    console.log(`  id: ${m.id}`);
  }
}

// Full single message (any folder), incl. complete body. raw=true prints HTML.
async function getMessage(id, raw = false) {
  assertGraphId(id);
  const m = await graphReq('GET', `${GRAPH}/me/messages/${encodeURIComponent(id)}?$select=subject,from,toRecipients,ccRecipients,receivedDateTime,sentDateTime,hasAttachments,body`, { preferHtml: raw });
  const addrs = (a) => (a || []).map(r => `${r.emailAddress.name || ''} <${r.emailAddress.address}>`).join(', ');
  console.log('SUBJECT:', m.subject);
  console.log('FROM:', m.from ? `${m.from.emailAddress.name} <${m.from.emailAddress.address}>` : '(draft)');
  console.log('TO:', addrs(m.toRecipients));
  console.log('CC:', addrs(m.ccRecipients));
  console.log('DATE:', m.sentDateTime || m.receivedDateTime || '(unsent)');
  console.log('---BODY---');
  console.log(raw ? (m.body?.content || '') : htmlToText(m.body?.content));
}

// Replace a draft's body. keepSignature splices new HTML before the Outlook
// signature block, preserving signature (incl. cid logo) + quoted thread.
// NEVER sends — only updates the draft in place.
async function patchDraftBody(id, bodyFilePath, keepSignature) {
  assertGraphId(id);
  const newInner = readFileSync(bodyFilePath, 'utf8');
  let content;
  if (keepSignature) {
    const cur = await graphReq('GET', `${GRAPH}/me/messages/${encodeURIComponent(id)}?$select=body`, { preferHtml: true });
    const raw = cur.body?.content || '';
    const bodyTag = '<body dir="ltr">';
    const bStart = raw.indexOf(bodyTag);
    const sigIdx = raw.indexOf('<div id="Signature"');
    if (bStart < 0 || sigIdx < 0) throw new Error('keep-signature: <body> or <div id="Signature"> markers not found — aborting (use without --keep-signature to replace whole body)');
    const head = raw.slice(0, bStart + bodyTag.length);
    const tail = raw.slice(sigIdx); // signature + hr + quoted thread, verbatim
    content = head + newInner + tail;
  } else {
    content = newInner;
  }
  await graphReq('PATCH', `${GRAPH}/me/messages/${encodeURIComponent(id)}`, { json: { body: { contentType: 'html', content } } });
  console.log(`✅ Draft ${id.slice(0, 12)}… body updated (NOT sent).`);
}

// --- Email Fetching ---

async function fetchAllEmails(months) {
  const since = new Date();
  since.setMonth(since.getMonth() - months);
  const sinceISO = since.toISOString();

  console.error(`Fetching emails since ${sinceISO} (${months} months)...`);

  const rawFile = join(OUTPUT_DIR, 'raw-emails.jsonl');
  preparePrivateFile(rawFile); // truncate safely

  const select = 'id,subject,from,toRecipients,receivedDateTime,hasAttachments,bodyPreview,body,importance,isRead,categories,conversationId';
  let url = `${GRAPH}/me/messages?$filter=receivedDateTime ge ${sinceISO}&$orderby=receivedDateTime desc&$top=50&$select=${select}`;
  let page = 0, total = 0;

  while (url) {
    page++;
    process.stderr.write(`  Page ${page}...`);
    const data = await graphGet(url);
    const emails = data.value || [];
    if (emails.length === 0) break;

    for (const m of emails) {
      const line = JSON.stringify({
        id: m.id,
        subject: m.subject,
        from: m.from?.emailAddress?.address,
        fromName: m.from?.emailAddress?.name,
        to: (m.toRecipients || []).map(r => r.emailAddress?.address),
        date: m.receivedDateTime,
        hasAttachments: m.hasAttachments,
        importance: m.importance,
        isRead: m.isRead,
        categories: m.categories,
        conversationId: m.conversationId,
        preview: m.bodyPreview,
        bodyText: m.body?.content ? m.body.content.replace(/\r\n/g, '\n').replace(/\n{3,}/g, '\n\n').replace(/<[^>]*>/g, ' ').replace(/\s{2,}/g, ' ').slice(0, 3000) : null
      });
      appendFileSync(rawFile, line + '\n');
    }

    total += emails.length;
    console.error(` ${emails.length} emails (total: ${total})`);
    url = data['@odata.nextLink'] || null;
  }

  console.error(`Total emails fetched: ${total}`);
  return rawFile;
}

async function fetchAttachmentsIndex() {
  const rawFile = join(OUTPUT_DIR, 'raw-emails.jsonl');
  const attFile = join(OUTPUT_DIR, 'attachments-index.jsonl');
  preparePrivateFile(attFile);

  const lines = readFileSync(rawFile, 'utf8').split('\n').filter(Boolean);
  const withAtt = lines.map(l => JSON.parse(l)).filter(e => e.hasAttachments);

  console.error(`Indexing attachments for ${withAtt.length} emails...`);
  let count = 0;

  for (const email of withAtt) {
    try {
      assertGraphId(email.id);
      const data = await graphGet(`${GRAPH}/me/messages/${encodeURIComponent(email.id)}/attachments?$select=id,name,contentType,size,isInline`);
      for (const att of (data.value || [])) {
        appendFileSync(attFile, JSON.stringify({
          messageId: email.id,
          subject: email.subject,
          date: email.date,
          name: att.name,
          contentType: att.contentType,
          size: att.size,
          isInline: att.isInline,
          attachmentId: att.id
        }) + '\n');
      }
    } catch (e) {
      console.error(`  Failed for ${email.subject}: ${e.message}`);
    }
    count++;
    if (count % 20 === 0) console.error(`  Indexed ${count}/${withAtt.length}...`);
  }

  console.error(`Attachment index complete: ${count} messages`);
  return attFile;
}

function generateSummary(months) {
  const rawFile = join(OUTPUT_DIR, 'raw-emails.jsonl');
  const attFile = join(OUTPUT_DIR, 'attachments-index.jsonl');
  const summaryFile = join(OUTPUT_DIR, 'email-summary.md');

  const emails = readFileSync(rawFile, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l));
  const attachments = existsSync(attFile)
    ? readFileSync(attFile, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l))
    : [];

  // Build attachment lookup
  const attByMsg = {};
  for (const a of attachments) {
    if (!attByMsg[a.messageId]) attByMsg[a.messageId] = [];
    attByMsg[a.messageId].push(a);
  }

  const total = emails.length;
  const unread = emails.filter(e => !e.isRead).length;
  const withAtt = emails.filter(e => e.hasAttachments).length;

  // Top senders
  const senderCounts = {};
  for (const e of emails) {
    const addr = e.from || 'unknown';
    senderCounts[addr] = (senderCounts[addr] || 0) + 1;
  }
  const topSenders = Object.entries(senderCounts).sort((a, b) => b[1] - a[1]).slice(0, 25);

  let md = `# Outlook Email Analysis — Last ${months} Months\n\n`;
  md += `_Generated: ${new Date().toISOString()}_\n`;

  md += `## Stats\n`;
  md += `- **Total emails:** ${total}\n`;
  md += `- **Unread:** ${unread}\n`;
  md += `- **With attachments:** ${withAtt}\n`;
  md += `- **Unique senders:** ${Object.keys(senderCounts).length}\n\n`;

  md += `## Top 25 Senders\n\n`;
  md += `| Sender | Count |\n|--------|-------|\n`;
  for (const [addr, count] of topSenders) {
    md += `| ${addr} | ${count} |\n`;
  }
  md += `\n`;

  md += `## Email Digest (newest first)\n\n`;
  for (const e of emails) {
    const att = e.hasAttachments ? ' 📎' : '';
    const read = e.isRead ? '' : ' 🔴';
    const d = new Date(e.date).toISOString().slice(0, 16).replace('T', ' ');
    const attList = attByMsg[e.id];

    md += `### ${e.subject || '(no subject)'}${att}${read}\n`;
    md += `**From:** ${e.fromName || ''} <${e.from}> | **Date:** ${d}\n`;
    if (attList && attList.length > 0) {
      md += `**Attachments:** ${attList.map(a => `${a.name} (${(a.size / 1024).toFixed(0)}KB)`).join(', ')}\n`;
    }
    md += `> ${(e.preview || '').slice(0, 250).replace(/\n/g, ' ')}\n\n`;
  }

  writePrivateFile(summaryFile, md);
  console.error(`Summary written: ${summaryFile} (${(md.length / 1024).toFixed(0)}KB)`);
  return summaryFile;
}

// Download a message's file attachments (incl. the plans/photos suppliers send) to a folder.
// Read-only: it fetches bytes via Graph and writes them locally. Never sends or modifies mail.
function uniquePrivateDest(outDir, rawName) {
  const baseDir = resolve(outDir);
  const cleaned = String(rawName || 'attachment')
    .replace(/[^A-Za-z0-9._-]+/g, '_')
    .replace(/^\.+/, '_')
    .slice(0, 180) || 'attachment';
  for (let i = 0; i < 100; i++) {
    const name = i === 0 ? cleaned : `${cleaned.replace(/(\.[^.]+)?$/, '')}-${i}${(cleaned.match(/\.[^.]+$/) || [''])[0]}`;
    const dest = resolve(baseDir, name);
    if (dirname(dest) !== baseDir) throw new Error('Attachment destination escapes the output directory');
    if (existsSync(dest)) continue;
    return dest;
  }
  throw new Error('Could not allocate a unique attachment filename');
}

async function getAttachments(id, outDir) {
  assertGraphId(id);
  const data = await graphGet(`${GRAPH}/me/messages/${encodeURIComponent(id)}/attachments`);
  const atts = data.value || [];
  if (!atts.length) { console.log('No attachments on this message.'); return; }
  ensurePrivateDir(outDir);
  let saved = 0;
  for (const a of atts) {
    const type = a['@odata.type'] || '';
    if (type.includes('fileAttachment') && a.contentBytes) {
      const dest = uniquePrivateDest(outDir, a.name || `attachment-${a.id}`);
      writeFileSync(dest, Buffer.from(a.contentBytes, 'base64'), { flag: 'wx', mode: 0o600 });
      chmodSync(dest, 0o600);
      console.log(`✅ ${a.isInline ? '(inline) ' : ''}${dest} (${(a.size / 1024).toFixed(0)}KB)`);
      saved++;
    } else {
      console.log(`⏭️  skipped ${a.name || a.id} (${type || 'unknown type'})`);
    }
  }
  console.log(`\nSaved ${saved}/${atts.length} attachment(s) to ${outDir}`);
}

// --- Main ---

const args = process.argv.slice(2);
const cmd = args[0];

try {
  if (cmd === '--test') {
    const data = await graphGet(`${GRAPH}/me/messages?$top=5&$select=subject,from,receivedDateTime,hasAttachments&$orderby=receivedDateTime desc`);
    for (const m of data.value || []) {
      console.log(`${m.receivedDateTime?.slice(0, 16)} | ${m.from?.emailAddress?.address} | ${m.subject}${m.hasAttachments ? ' 📎' : ''}`);
    }

  } else if (cmd === '--fetch-all') {
    const monthsIdx = args.indexOf('--months');
    const months = monthsIdx >= 0 ? parseInt(args[monthsIdx + 1]) : 6;
    // CONSENT GATE: --fetch-all writes your mail bodies + attachment index to
    // plaintext files on disk. That is a privacy-affecting export, so it does
    // not run without an explicit --yes. Say exactly what will be written.
    if (!args.includes('--yes')) {
      console.error('⚠️  --fetch-all will export the last ' + months + ' months of your mailbox to disk:');
      console.error('      ' + join(OUTPUT_DIR, 'raw-emails.jsonl') + '   (subjects, senders, body text)');
      console.error('      ' + join(OUTPUT_DIR, 'attachments-index.jsonl') + '   (attachment names/types/sizes)');
      console.error('      ' + join(OUTPUT_DIR, 'email-summary.md') + '   (digest + top senders)');
      console.error('   These are UNENCRYPTED. Re-run with --yes to confirm, or use --test / --list-drafts,');
      console.error('   which keep data in memory. Remove an old export with your normal recovery-aware file tool: ' + OUTPUT_DIR);
      process.exit(2);
    }
    await fetchAllEmails(months);
    await fetchAttachmentsIndex();
    generateSummary(months);

  } else if (cmd === '--list-drafts') {
    const li = args.indexOf('--limit');
    await listDrafts(li >= 0 ? parseInt(args[li + 1]) : 15);

  } else if (cmd === '--get') {
    if (!args[1]) throw new Error('--get requires a message id');
    await getMessage(args[1], args.includes('--raw'));

  } else if (cmd === '--get-attachments') {
    if (!args[1]) throw new Error('--get-attachments requires a message id');
    const oi = args.indexOf('--out');
    const outDir = oi >= 0 ? args[oi + 1] : join(OUTPUT_DIR, 'attachments', args[1].slice(0, 16));
    await getAttachments(args[1], outDir);

  } else if (cmd === '--patch-draft') {
    if (!args[1]) throw new Error('--patch-draft requires a draft id');
    const fi = args.indexOf('--body-file');
    if (fi < 0) throw new Error('--patch-draft requires --body-file <path> (HTML fragment for the message body)');
    await patchDraftBody(args[1], args[fi + 1], args.includes('--keep-signature'));

  } else {
    console.log('Usage:');
    console.log('  node outlook-mail-fetch.mjs --test');
    console.log('  node outlook-mail-fetch.mjs --fetch-all --yes --access-token-stdin [--months 6]   # bulk export to disk; --yes required');
    console.log('  node outlook-mail-fetch.mjs --list-drafts --access-token-stdin [--limit 15]');
    console.log('  node outlook-mail-fetch.mjs --get <id> --access-token-stdin [--raw]            # full body of any message/draft (--raw = HTML)');
    console.log('  node outlook-mail-fetch.mjs --get-attachments <id> --access-token-stdin [--out <dir>]  # download a message\'s file attachments (plans/photos)');
    console.log('  node outlook-mail-fetch.mjs --patch-draft <id> --body-file <path.html> --access-token-stdin [--keep-signature]');
  }
} catch (e) {
  console.error(`❌ ${e.message}`);
  process.exit(1);
}
