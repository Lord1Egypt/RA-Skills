#!/usr/bin/env node
// The store CLI: reading, and editing the fields the user owns. Adding and
// refreshing belong to scrape.ts, which writes the store itself. Between them
// they are the only writers — nothing hand-edits data.js, which is what keeps
// every write atomic and scraped values honest about where they came from.
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { emptyStoreText, readStore, removeProperty, setMine, writeStore, MINE_FIELDS } from './store.ts';
import type { Property } from './store.ts';

const BUNDLE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const FRONTEND_TEMPLATE = path.join(BUNDLE_ROOT, 'references', 'frontend');

const USAGE = `property-hunt store

  init                              scaffold the properties folder (idempotent)
  list [--json]                     every property
  get <id>                          one property as JSON
  set <id> <field> <value>          ${MINE_FIELDS.join(' | ')}
  rm <id>                           delete the property and its photo
  where                             print the folder being used

Adding and refreshing a property is a separate command — see SKILL.md.

The data folder is $PROPERTY_HUNT_DIR, else /workspace/host/properties inside
the agent VM, else ~/Plow/properties on a Mac.

A single-quoted value cannot contain an apostrophe, and notes do ("don't love
the kitchen"). Replace each ' with '\\'' before quoting.`;

/**
 * Resolve the data folder. The same code runs inside the agent container and on
 * the host during smoke tests, and those see the same bytes under two names.
 */
export function resolveDataDir(env: NodeJS.ProcessEnv = process.env): string {
  const override = env.PROPERTY_HUNT_DIR?.trim();
  if (override) return path.resolve(override);
  if (fs.existsSync('/workspace/host')) return '/workspace/host/properties';
  return path.join(os.homedir(), 'Plow', 'properties');
}

function copyTree(from: string, to: string): void {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const src = path.join(from, entry.name);
    const dest = path.join(to, entry.name);
    if (entry.isDirectory()) copyTree(src, dest);
    else fs.copyFileSync(src, dest);
  }
}

function init(dir: string): void {
  fs.mkdirSync(path.join(dir, 'photos'), { recursive: true });

  if (!fs.existsSync(FRONTEND_TEMPLATE)) {
    throw new Error(`bundle is incomplete: no frontend template at ${FRONTEND_TEMPLATE}`);
  }
  // The frontend is bundle-owned, so refresh it on every init to pick up skill
  // upgrades. data.js is user-owned and must survive untouched.
  copyTree(FRONTEND_TEMPLATE, dir);

  const store = path.join(dir, 'data.js');
  if (fs.existsSync(store)) {
    process.stdout.write(`ready: ${dir} (kept ${readStore(dir).length} existing properties)\n`);
    return;
  }
  fs.writeFileSync(store, emptyStoreText());
  process.stdout.write(`ready: ${dir}\n`);
}

function requireArg(value: string | undefined, name: string): string {
  if (value === undefined || value === '') throw new Error(`missing <${name}>\n\n${USAGE}`);
  return value;
}

function findOrThrow(rows: Property[], id: string): Property {
  const row = rows.find((candidate) => candidate.id === id);
  if (!row) {
    const known = rows.map((r) => r.id).join('\n  ') || '(store is empty)';
    throw new Error(`no property with id ${JSON.stringify(id)}. Known ids:\n  ${known}`);
  }
  return row;
}

function summarize(row: Property): string {
  const s = row.scraped;
  const money = s.price === null ? '?' : `$${s.price.toLocaleString('en-US')}`;
  const facts = [s.beds && `${s.beds}bd`, s.baths && `${s.baths}ba`, s.sqft && `${s.sqft}sqft`]
    .filter(Boolean)
    .join(' · ');
  const stars = row.mine.rating === null ? '' : ` ${'★'.repeat(row.mine.rating)}`;
  const note = row.mine.notes ? ` — ${row.mine.notes}` : '';
  return `${row.id}\n  ${s.address}, ${s.city} ${s.state}  ${money}  ${facts}\n  [${row.mine.status}]${stars}${note}`;
}

function main(argv: string[]): void {
  const [verb, ...rest] = argv;
  const dir = resolveDataDir();

  if (!verb || verb === '--help' || verb === '-h') {
    process.stdout.write(`${USAGE}\n`);
    return;
  }
  if (verb === 'where') {
    process.stdout.write(`${dir}\n`);
    return;
  }
  if (verb === 'init') {
    init(dir);
    return;
  }

  const rows = readStore(dir);

  switch (verb) {
    case 'list': {
      if (rest.includes('--json')) {
        process.stdout.write(`${JSON.stringify(rows, null, 2)}\n`);
      } else if (rows.length === 0) {
        process.stdout.write('no properties yet\n');
      } else {
        const label = rows.length === 1 ? 'property' : 'properties';
        process.stdout.write(`${rows.map(summarize).join('\n\n')}\n\n${rows.length} ${label}\n`);
      }
      return;
    }
    case 'get': {
      process.stdout.write(`${JSON.stringify(findOrThrow(rows, requireArg(rest[0], 'id')), null, 2)}\n`);
      return;
    }
    case 'set': {
      const id = requireArg(rest[0], 'id');
      const field = requireArg(rest[1], 'field');
      const value = rest.slice(2).join(' ');
      const next = setMine(rows, id, field, value);
      writeStore(dir, next);
      process.stdout.write(`${id}: ${field} = ${JSON.stringify(value)}\n`);
      return;
    }
    case 'rm': {
      const id = requireArg(rest[0], 'id');
      const row = findOrThrow(rows, id);
      writeStore(dir, removeProperty(rows, id));
      if (row.scraped.photo) fs.rmSync(path.join(dir, row.scraped.photo), { force: true });
      process.stdout.write(`removed ${id}\n`);
      return;
    }
    default:
      throw new Error(`unknown verb ${JSON.stringify(verb)}\n\n${USAGE}`);
  }
}

// Only run when invoked directly, so tests can import resolveDataDir.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    main(process.argv.slice(2));
  } catch (err) {
    process.stderr.write(`${(err as Error).message}\n`);
    process.exit(1);
  }
}
