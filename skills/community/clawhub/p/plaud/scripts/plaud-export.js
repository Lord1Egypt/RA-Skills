#!/usr/bin/env node
import { mkdir, writeFile } from 'fs/promises';
import { spawnSync } from 'child_process';
import { join } from 'path';

const id = process.argv[2];
const outDir = process.argv[3] || `plaud-export-${id || 'recording'}`;

if (!id) {
  console.error('Usage: plaud-export.js <recording-id> [output-dir]');
  process.exit(2);
}

function run(args) {
  const result = spawnSync('plaud', args, { encoding: 'utf8' });
  if (result.status !== 0) {
    throw new Error(`plaud ${args.join(' ')} failed: ${result.stderr || result.stdout}`);
  }
  return result.stdout;
}

await mkdir(outDir, { recursive: true });

const metadata = run(['file', id]);
await writeFile(join(outDir, 'metadata.txt'), metadata, 'utf8');

try {
  const summary = run(['summary', id]);
  await writeFile(join(outDir, 'summary.md'), summary, 'utf8');
} catch (err) {
  await writeFile(join(outDir, 'summary.md'), `No summary available.\n\n${String(err.message || err)}\n`, 'utf8');
}

try {
  const transcript = run(['transcript', id]);
  await writeFile(join(outDir, 'transcript.txt'), transcript, 'utf8');
} catch (err) {
  await writeFile(join(outDir, 'transcript.txt'), `No transcript available.\n\n${String(err.message || err)}\n`, 'utf8');
}

console.log(`Exported Plaud recording ${id} to ${outDir}`);
