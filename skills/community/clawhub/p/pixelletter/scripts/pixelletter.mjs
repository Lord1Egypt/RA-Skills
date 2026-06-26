#!/usr/bin/env node
import { existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { basename } from 'node:path';

const ENDPOINT = process.env.PIXELLETTER_ENDPOINT || 'https://www.pixelletter.de/xml/index.php';

function usage(exitCode = 0) {
  const text = `PixelLetter CLI

Usage:
  node scripts/pixelletter.mjs account [--dry-run]
  node scripts/pixelletter.mjs send-text --address-file FILE --message-file FILE --subject TEXT --destination DE [options]
  node scripts/pixelletter.mjs send-upload --file FILE [--file FILE...] --destination DE [options]

Options:
  --action 1|2|3              1=letter, 2=fax, 3=letter+fax (default: 1)
  --fax "+49 ..."             Required for action 2 or 3
  --destination CC            Required for letter actions 1 or 3 (e.g. DE, AT, CH)
  --location 1|2|3            1=München, 2=Hausleiten, 3=Hamburg (default: 1)
  --transaction ID            Optional caller transaction id
  --control VALUE             Optional control value
  --return-address TEXT       Optional return address
  --addoption LIST            Registered mail options: 27, 28, 29, 30
  --production                Disable test mode (requires safeguards below)
  --confirm-real-send         Required together with --production
  --dry-run                   Print sanitized XML and do not call PixelLetter
  --raw                       Also print raw XML response
  -h, --help                  Show help

Environment:
  PIXELLETTER_EMAIL           PixelLetter login email
  PIXELLETTER_PASSWORD        PixelLetter password
  PIXELLETTER_ALLOW_REAL_SEND Must be true for --production sends
`;
  console.log(text);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const command = argv[2];
  if (!command || command === 'help' || command === '-h' || command === '--help') usage(0);
  const args = { _: [] };
  for (let i = 3; i < argv.length; i++) {
    const token = argv[i];
    if (token === '-h' || token === '--help') usage(0);
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    if (['production', 'confirm-real-send', 'dry-run', 'raw'].includes(key)) {
      args[key] = true;
      continue;
    }
    const value = argv[++i];
    if (value === undefined || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`);
    }
    if (key === 'file') {
      args.file = args.file || [];
      args.file.push(value);
    } else {
      args[key] = value;
    }
  }
  args.command = command;
  return args;
}

function xmlEscape(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('>', '&gt;')
    .replaceAll('<', '&lt;');
}

function requireEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable ${name}`);
  return value;
}

function option(args, key, fallback = '') {
  return args[key] ?? fallback;
}

function validateCommon(args) {
  const action = String(option(args, 'action', '1'));
  if (!['1', '2', '3'].includes(action)) throw new Error('--action must be 1, 2, or 3');

  const location = String(option(args, 'location', '1'));
  if (!['1', '2', '3'].includes(location)) throw new Error('--location must be 1, 2, or 3');

  const destination = option(args, 'destination', '').toUpperCase();
  if (['1', '3'].includes(action) && !/^[A-Z]{2}$/.test(destination)) {
    throw new Error('--destination must be a two-letter ISO country code for postal letter actions');
  }

  const fax = option(args, 'fax', '');
  if (['2', '3'].includes(action) && !fax.trim()) throw new Error('--fax is required for fax actions');

  validateAddoption(option(args, 'addoption', ''));
  validateProductionSafeguards(args);

  return { action, location, destination, fax };
}

function validateAddoption(value) {
  if (!value) return;
  const parts = value.split(',').map(v => v.trim()).filter(Boolean);
  const allowed = new Set(['27', '28', '29', '30']);
  for (const part of parts) {
    if (!allowed.has(part)) throw new Error(`Unsupported --addoption ${part}; supported: 27,28,29,30`);
  }
  if (parts.includes('30') && parts.length > 1) throw new Error('--addoption 30 is not combinable');
  if ((parts.includes('28') || parts.includes('29')) && !parts.includes('27')) {
    throw new Error('--addoption 28 or 29 requires 27');
  }
}

function validateProductionSafeguards(args) {
  if (!args.production) return;
  if (!args['confirm-real-send']) throw new Error('--production requires --confirm-real-send');
  if (process.env.PIXELLETTER_ALLOW_REAL_SEND !== 'true') {
    throw new Error('--production requires PIXELLETTER_ALLOW_REAL_SEND=true');
  }
}

function authXml({ email, password, production }) {
  const testmodus = production ? '' : '1';
  return `<auth>
    <email>${xmlEscape(email)}</email>
    <password>${xmlEscape(password)}</password>
    <agb>ja</agb>
    <widerrufsverzicht>ja</widerrufsverzicht>
    <testmodus>${testmodus}</testmodus>
    <ref></ref>
  </auth>`;
}

function optionsXml(args, common) {
  return `<options>
      <action>${common.action}</action>
      <transaction>${xmlEscape(option(args, 'transaction'))}</transaction>
      <control>${xmlEscape(option(args, 'control'))}</control>
      <fax>${xmlEscape(common.fax)}</fax>
      <location>${common.location}</location>
      <destination>${xmlEscape(common.destination)}</destination>
      <addoption>${xmlEscape(option(args, 'addoption'))}</addoption>
      <returnaddress>${xmlEscape(option(args, 'return-address'))}</returnaddress>
    </options>`;
}

function envelope(commandXml, args) {
  const email = args['dry-run'] ? 'REDACTED@example.invalid' : requireEnv('PIXELLETTER_EMAIL');
  const password = args['dry-run'] ? 'REDACTED' : requireEnv('PIXELLETTER_PASSWORD');
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<pixelletter version="1.3">
  ${authXml({ email, password, production: Boolean(args.production) })}
  ${commandXml}
</pixelletter>`;
}

async function buildTextPayload(args) {
  if (!args['address-file']) throw new Error('send-text requires --address-file');
  if (!args['message-file']) throw new Error('send-text requires --message-file');
  if (!args.subject) throw new Error('send-text requires --subject');
  const common = validateCommon(args);
  const address = await readFile(args['address-file'], 'utf8');
  const message = await readFile(args['message-file'], 'utf8');
  const command = `<command>
  <order type="text">
    ${optionsXml(args, common)}
    <text>
      <address>${xmlEscape(address)}</address>
      <subject>${xmlEscape(args.subject)}</subject>
      <message>${xmlEscape(message)}</message>
    </text>
  </order>
</command>`;
  return { xml: envelope(command, args), files: [] };
}

function ensureFiles(files = []) {
  if (!files.length) throw new Error('send-upload requires at least one --file');
  for (const file of files) {
    if (!existsSync(file)) throw new Error(`File does not exist: ${file}`);
  }
}

async function buildUploadPayload(args) {
  ensureFiles(args.file);
  const common = validateCommon(args);
  const command = `<command>
  <order type="upload">
    ${optionsXml(args, common)}
  </order>
</command>`;
  return { xml: envelope(command, args), files: args.file };
}

function buildAccountPayload(args) {
  const command = `<command>
  <info>
    <account:info type="all" />
  </info>
</command>`;
  return { xml: envelope(command, args), files: [] };
}

function parseResponse(xml) {
  const code = xml.match(/<result\s+code="([^"]+)"/i)?.[1] || null;
  const msg = xml.match(/<msg>([\s\S]*?)<\/msg>/i)?.[1]?.trim() || null;
  const transaction = xml.match(/<transaction>([\s\S]*?)<\/transaction>/i)?.[1]?.trim() || null;
  const credit = xml.match(/<(?:customer|costumer):credit[^>]*currency="([^"]+)"[^>]*>([\s\S]*?)<\/(?:customer|costumer):credit>/i);
  return {
    ok: code === '100' || Boolean(credit),
    code,
    msg,
    transaction,
    credit: credit ? { currency: credit[1], amount: credit[2].trim() } : null,
  };
}

async function submit(payload) {
  const form = new FormData();
  form.append('xml', payload.xml);
  for (let i = 0; i < payload.files.length; i++) {
    const file = payload.files[i];
    const buffer = await readFile(file);
    form.append(`uploadfile${i}`, new Blob([buffer], { type: 'application/pdf' }), basename(file));
  }
  const response = await fetch(ENDPOINT, { method: 'POST', body: form });
  const body = await response.text();
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${body.slice(0, 500)}`);
  return body;
}

async function main() {
  const args = parseArgs(process.argv);
  let payload;
  if (args.command === 'send-text') payload = await buildTextPayload(args);
  else if (args.command === 'send-upload') payload = await buildUploadPayload(args);
  else if (args.command === 'account') payload = buildAccountPayload(args);
  else throw new Error(`Unknown command: ${args.command}`);

  if (args['dry-run']) {
    console.log(payload.xml);
    return;
  }

  const raw = await submit(payload);
  const parsed = parseResponse(raw);
  console.log(JSON.stringify(parsed, null, 2));
  if (args.raw) console.error(raw);
  if (!parsed.ok) process.exitCode = 2;
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
