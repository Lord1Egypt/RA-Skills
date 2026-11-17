/**
 * klik-import CLI
 * Usage: node dist/klik-import.mjs <subcommand> [options]
 *
 * Subcommands:
 *   submit   --input <json> --code <6-digit>   Redact + validate + upload
 *   validate --input <json>                    Schema check only (no upload)
 *   redact   --input <json> --output <json>    Redact only (offline preview)
 *   doctor                                     Check env: Node version, DNS
 */
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import dns from 'node:dns/promises';
import { fileURLToPath } from 'node:url';
import { validatePayload } from './schema.ts';
import { redactContent } from './redactor.ts';
import { verifyCode, uploadPayload } from './uploader.ts';
import type { ImportPayload } from './types.ts';

const [, , subcommand, ...args] = process.argv;

function parseArgs(args: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      out[args[i].slice(2)] = args[i + 1] ?? 'true';
      i++;
    }
  }
  return out;
}

function readPayload(inputPath: string): unknown {
  const content = fs.readFileSync(inputPath, 'utf8');
  return JSON.parse(content);
}

function applyRedactionToPayload(payload: ImportPayload, redactEmail: boolean): { payload: ImportPayload; totalRedacted: number } {
  let totalRedacted = 0;
  const redacted = structuredClone(payload);
  for (const collector of redacted.collectors) {
    for (const item of collector.items) {
      if (item.content) {
        const { result, count } = redactContent(item.content, { redactEmail });
        item.content = result;
        totalRedacted += count;
      }
      if (item.prompt) {
        const { result, count } = redactContent(item.prompt, { redactEmail });
        item.prompt = result;
        totalRedacted += count;
      }
    }
  }
  redacted.redaction.redacted_count = totalRedacted;
  redacted.redaction.email_redacted = redactEmail;
  return { payload: redacted, totalRedacted };
}

function printSummary(payload: ImportPayload): void {
  console.log('\n=== Import Summary ===');
  for (const c of payload.collectors) {
    console.log(`  ${c.name}: ${c.items.length} items from ${c.source_root}`);
  }
  const totalItems = payload.collectors.reduce((s, c) => s + c.items.length, 0);
  const bytes = Buffer.byteLength(JSON.stringify(payload), 'utf8');
  console.log(`  Total: ${totalItems} items, ${(bytes / 1024).toFixed(1)} KB`);
  if (payload.redaction.redacted_count > 0) {
    console.log(`  Redacted: ${payload.redaction.redacted_count} secret(s) replaced`);
  }
  console.log('');
}

async function cmdSubmit(flags: Record<string, string>): Promise<void> {
  if (!flags.input) { console.error('--input required'); process.exit(1); }
  if (!flags.code) { console.error('--code required'); process.exit(1); }

  const raw = readPayload(flags.input);
  const nonInteractive = flags.yes === 'true';

  let redactEmail = false;
  if (!nonInteractive) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const answer = await rl.question('Redact email addresses? [y/N]: ');
    rl.close();
    redactEmail = answer.trim().toLowerCase() === 'y';
  }

  const { payload } = applyRedactionToPayload(raw as ImportPayload, redactEmail);

  try {
    validatePayload(payload);
  } catch (e: any) {
    console.error('Validation failed:', e.message);
    process.exit(1);
  }

  printSummary(payload);

  if (!nonInteractive) {
    const rl2 = readline.createInterface({ input: process.stdin, output: process.stdout });
    const confirm = await rl2.question('Upload to Klik? [y/N]: ');
    rl2.close();
    if (confirm.trim().toLowerCase() !== 'y') {
      console.log('Upload cancelled.');
      process.exit(0);
    }
  }

  console.log('Verifying import code...');
  const { import_token, user_id } = await verifyCode(flags.code);
  console.log(`Authenticated as user ${user_id}`);

  console.log('Uploading...');
  const result = await uploadPayload(payload, import_token);
  console.log(`\nImport complete. ID: ${result.import_id}`);
  for (const a of result.accepted) {
    console.log(`  ${a.collector}: ${a.item_count} items`);
  }
}

async function cmdValidate(flags: Record<string, string>): Promise<void> {
  if (!flags.input) { console.error('--input required'); process.exit(1); }
  const raw = readPayload(flags.input);
  try {
    validatePayload(raw);
    console.log('Payload is valid');
  } catch (e: any) {
    console.error('Validation failed:', e.message);
    process.exit(1);
  }
}

async function cmdRedact(flags: Record<string, string>): Promise<void> {
  if (!flags.input) { console.error('--input required'); process.exit(1); }
  const raw = readPayload(flags.input) as ImportPayload;
  const { payload, totalRedacted } = applyRedactionToPayload(raw, flags['redact-email'] === 'true');
  const out = flags.output ?? '/dev/stdout';
  fs.writeFileSync(out, JSON.stringify(payload, null, 2), 'utf8');
  console.error(`Redacted ${totalRedacted} secret(s)`);
}

async function cmdDoctor(): Promise<void> {
  const nodeVer = parseInt(process.versions.node.split('.')[0]);
  console.log(`Node version: ${process.versions.node} ${nodeVer >= 18 ? 'ok' : 'FAIL (need >= 18)'}`);
  try {
    await dns.lookup('hiklik.ai');
    console.log('DNS hiklik.ai: ok');
  } catch {
    console.log('DNS hiklik.ai: FAIL (no network or wrong domain)');
  }
  const skillMd = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'SKILL.md');
  console.log(`SKILL.md present: ${fs.existsSync(skillMd) ? 'ok' : 'missing'}`);
}

(async () => {
  const flags = parseArgs(args);
  switch (subcommand) {
    case 'submit':   await cmdSubmit(flags); break;
    case 'validate': await cmdValidate(flags); break;
    case 'redact':   await cmdRedact(flags); break;
    case 'doctor':   await cmdDoctor(); break;
    default:
      console.log('Usage: node klik-import.mjs <submit|validate|redact|doctor> [options]');
      process.exit(1);
  }
})().catch(err => { console.error(err.message); process.exit(1); });
