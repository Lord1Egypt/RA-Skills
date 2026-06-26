#!/usr/bin/env node
// Build a ClawHub-ready skill bundle using only Node built-ins.
// Pipeline: read clawhub.ignore.txt, walk deterministically, write USTAR, gzip, verify archive entries.

import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

function parseIgnore(file) {
  if (!fs.existsSync(file)) return [];
  return fs.readFileSync(file, 'utf8')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));
}

function getArg(flag, fallback) {
  const idx = process.argv.indexOf(flag);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return process.argv.slice(2).find((arg) => !arg.startsWith('-')) || fallback;
}

function globToRegex(pattern) {
  let rx = '';
  for (let i = 0; i < pattern.length; i++) {
    const ch = pattern[i];
    const next = pattern[i + 1];
    const prev = pattern[i - 1];
    const afterNext = pattern[i + 2];
    if (ch === '*' && next === '*' && (prev === undefined || prev === '/') && (afterNext === undefined || afterNext === '/')) {
      rx += afterNext === '/' ? '(?:[^/]+/)*' : '.*';
      if (afterNext === '/') i += 2;
      else i += 1;
    } else if (ch === '*') rx += '[^/]*';
    else if (ch === '?') rx += '[^/]';
    else if ('.+^${}()|[]\\'.includes(ch)) rx += '\\' + ch;
    else rx += ch;
  }
  return new RegExp('^' + rx + '$');
}

function isIgnored(relPath, patterns) {
  const segments = relPath.split('/');
  for (const raw of patterns) {
    const pattern = raw.replace(/\/$/, '');
    if (pattern.includes('/')) {
      if (globToRegex(pattern).test(relPath)) return true;
    } else if (pattern.includes('*') || pattern.includes('?')) {
      if (segments.some((seg) => globToRegex(pattern).test(seg))) return true;
    } else if (segments.includes(pattern)) return true;
  }
  return false;
}

function walk(root, ignorePatterns) {
  const out = [];
  function recurse(relDir) {
    const absDir = path.join(root, relDir);
    const entries = fs.readdirSync(absDir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      const rel = relDir ? `${relDir}/${entry.name}` : entry.name;
      if (isIgnored(rel, ignorePatterns)) continue;
      if (entry.isDirectory()) {
        out.push({ rel, type: 'dir' });
        recurse(rel);
      } else if (entry.isFile()) {
        out.push({ rel, type: 'file' });
      }
    }
  }
  recurse('');
  return out;
}

function octal(value, width) {
  return Math.floor(value).toString(8).padStart(width - 1, '0') + '\0';
}

function writeAscii(buf, str, offset, length) {
  const bytes = Buffer.from(str, 'utf8');
  if (bytes.length > length) throw new Error(`field overflow (${bytes.length} > ${length}): ${str}`);
  bytes.copy(buf, offset, 0, bytes.length);
}

function makeTarHeader({ name, size, mode, mtime, typeflag }) {
  let prefix = '';
  let filename = name;
  if (filename.length > 100) {
    const cut = filename.lastIndexOf('/', filename.length - 101);
    if (cut < 0 || filename.length - cut - 1 > 100 || cut > 155) throw new Error(`path too long for USTAR: ${name}`);
    prefix = filename.slice(0, cut);
    filename = filename.slice(cut + 1);
  }

  const header = Buffer.alloc(512);
  writeAscii(header, filename, 0, 100);
  writeAscii(header, octal(mode & 0o7777, 8), 100, 8);
  writeAscii(header, octal(0, 8), 108, 8);
  writeAscii(header, octal(0, 8), 116, 8);
  writeAscii(header, octal(size, 12), 124, 12);
  writeAscii(header, octal(mtime, 12), 136, 12);
  writeAscii(header, '        ', 148, 8);
  writeAscii(header, typeflag, 156, 1);
  writeAscii(header, 'ustar\0', 257, 6);
  writeAscii(header, '00', 263, 2);
  if (prefix) writeAscii(header, prefix, 345, 155);

  let sum = 0;
  for (let i = 0; i < 512; i++) sum += header[i];
  writeAscii(header, sum.toString(8).padStart(6, '0') + '\0 ', 148, 8);
  return header;
}

function padToBlock(size) {
  const rem = size % 512;
  return rem === 0 ? 0 : 512 - rem;
}

const pkg = JSON.parse(fs.readFileSync(path.join(repoRoot, 'package.json'), 'utf8'));
const stamp = new Date().toISOString().slice(0, 10);
const defaultOut = path.join(path.dirname(repoRoot), `${pkg.name}-${stamp}.tar.gz`);
const outPath = path.resolve(getArg('--out', defaultOut));
const sourceDateEpoch = Number.parseInt(process.env.SOURCE_DATE_EPOCH || '0', 10);
const archiveMtime = Number.isFinite(sourceDateEpoch) && sourceDateEpoch >= 0 ? sourceDateEpoch : 0;
const ignorePatterns = [
  ...parseIgnore(path.join(repoRoot, 'clawhub.ignore.txt')),
  '.git', '.DS_Store', 'node_modules', '.clawignore',
];

const packName = 'ifq-app-builder';
const entries = walk(repoRoot, ignorePatterns);
const chunks = [];
const archivedPaths = [];

for (const item of entries) {
  const absPath = path.join(repoRoot, item.rel);
  const stat = fs.statSync(absPath);
  const archivedName = `${packName}/${item.rel}${item.type === 'dir' ? '/' : ''}`;
  archivedPaths.push(archivedName);

  if (item.type === 'dir') {
    chunks.push(makeTarHeader({ name: archivedName, size: 0, mode: 0o755, mtime: archiveMtime, typeflag: '5' }));
    continue;
  }

  const data = fs.readFileSync(absPath);
  chunks.push(makeTarHeader({ name: archivedName, size: data.length, mode: stat.mode & 0o7777 || 0o644, mtime: archiveMtime, typeflag: '0' }));
  chunks.push(data);
  const pad = padToBlock(data.length);
  if (pad) chunks.push(Buffer.alloc(pad));
}

chunks.push(Buffer.alloc(1024));
fs.writeFileSync(outPath, zlib.gzipSync(Buffer.concat(chunks), { level: 9, mtime: archiveMtime }));

const forbidden = archivedPaths.filter((entry) => /(^|\/)\.git\//.test(entry)
  || /(^|\/)\.DS_Store$/.test(entry)
  || /(^|\/)\.env(?:\.|$)/.test(entry)
  || /(^|\/)[^/]+\.schema\.json$/.test(entry)
  || /(^|\/)\.openclaw[^/]*\//.test(entry)
  || /(^|\/)\.claude\//.test(entry)
  || /(^|\/)\.agents\//.test(entry)
  || /(^|\/)\.well-known\//.test(entry)
  || /(^|\/)personal-asset-index\.json$/.test(entry));

if (forbidden.length) {
  console.error('pack failed: forbidden entries escaped ignore manifest');
  for (const entry of forbidden.slice(0, 20)) console.error(`  - ${entry}`);
  process.exit(1);
}

const extensionlessRootFiles = archivedPaths
  .map((entry) => entry.startsWith(`${packName}/`) ? entry.slice(packName.length + 1) : entry)
  .filter((entry) => entry && !entry.endsWith('/') && !entry.includes('/') && !path.basename(entry).includes('.'));
if (extensionlessRootFiles.length) {
  console.error('pack failed: extensionless root files may be misclassified by ClawHub');
  for (const entry of extensionlessRootFiles) console.error(`  - ${entry}`);
  process.exit(1);
}

const size = fs.statSync(outPath).size;
console.log('✓ skill bundle ready');
console.log(`  path: ${path.relative(process.cwd(), outPath)}`);
console.log(`  size: ${(size / 1024).toFixed(1)} KiB`);
console.log(`  entries: ${archivedPaths.length}`);
console.log(`  mtime: ${archiveMtime}`);
