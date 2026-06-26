#!/usr/bin/env node
/**
 * Pack this skill directory into publish/<name>-<version>.zip.
 *
 * Writes a plain ZIP archive directly so Windows Explorer, PowerShell
 * Expand-Archive, and agent installers all see the same contents.
 */

import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from 'fs';
import { join, relative, resolve, sep } from 'path';
import { tmpdir } from 'os';

const skillRoot = resolve(process.cwd());
const pkgPath = join(skillRoot, 'package.json');

if (!existsSync(pkgPath)) {
  console.error(`pack-skill: run from the skill root containing package.json (cwd=${skillRoot})`);
  process.exit(1);
}

const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
const { name, version } = pkg;

if (!name || !version) {
  console.error('pack-skill: package.json must contain name and version');
  process.exit(1);
}

const publishDir = join(skillRoot, 'publish');
const zipFile = `${name}-${version}.zip`;
const zipPath = join(publishDir, zipFile);
const tmpZip = join(tmpdir(), `mofang-skill-pack-${name}-${version}-${process.pid}.zip`);

const excludedDirs = new Set(['.git', 'node_modules', 'docs', 'publish', 'skillsbackup']);
const excludedFiles = new Set(['.env', '.DS_Store', 'tsconfig.json']);

function toZipPath(absPath) {
  return relative(skillRoot, absPath).split(sep).join('/');
}

function shouldSkip(relPath, isDir) {
  const parts = relPath.split('/');
  if (parts.some((part) => excludedDirs.has(part) || part === '__MACOSX')) return true;
  const base = parts[parts.length - 1];
  if (excludedFiles.has(base)) return true;
  if (!isDir && (base.endsWith('.zip') || base.endsWith('.map') || base.endsWith('.vue'))) return true;
  return false;
}

function collectEntries(dir) {
  const entries = [];
  for (const name of readdirSync(dir).sort((a, b) => a.localeCompare(b))) {
    const absPath = join(dir, name);
    const relPath = toZipPath(absPath);
    const st = statSync(absPath);
    if (shouldSkip(relPath, st.isDirectory())) continue;
    if (st.isDirectory()) {
      entries.push({ name: `${relPath}/`, data: Buffer.alloc(0), isDir: true });
      entries.push(...collectEntries(absPath));
    } else if (st.isFile()) {
      entries.push({ name: relPath, data: readFileSync(absPath), isDir: false });
    }
  }
  return entries;
}

const crcTable = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[i] = c >>> 0;
  }
  return table;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (const byte of buf) c = crcTable[(c ^ byte) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function dosTimeDate(date = new Date()) {
  const year = Math.max(1980, date.getFullYear());
  return {
    dosTime: (date.getHours() << 11) | (date.getMinutes() << 5) | Math.floor(date.getSeconds() / 2),
    dosDate: ((year - 1980) << 9) | ((date.getMonth() + 1) << 5) | date.getDate(),
  };
}

function u16(n) {
  const b = Buffer.alloc(2);
  b.writeUInt16LE(n & 0xffff, 0);
  return b;
}

function u32(n) {
  const b = Buffer.alloc(4);
  b.writeUInt32LE(n >>> 0, 0);
  return b;
}

function makeZip(entries) {
  const chunks = [];
  const central = [];
  let offset = 0;
  const { dosTime, dosDate } = dosTimeDate();

  for (const entry of entries) {
    const nameBuf = Buffer.from(entry.name, 'utf8');
    const data = entry.data;
    const crc = entry.isDir ? 0 : crc32(data);
    const size = data.length;

    const local = Buffer.concat([
      u32(0x04034b50),
      u16(20),
      u16(0x0800),
      u16(0),
      u16(dosTime),
      u16(dosDate),
      u32(crc),
      u32(size),
      u32(size),
      u16(nameBuf.length),
      u16(0),
      nameBuf,
    ]);
    chunks.push(local, data);

    central.push(Buffer.concat([
      u32(0x02014b50),
      u16(20),
      u16(20),
      u16(0x0800),
      u16(0),
      u16(dosTime),
      u16(dosDate),
      u32(crc),
      u32(size),
      u32(size),
      u16(nameBuf.length),
      u16(0),
      u16(0),
      u16(0),
      u16(0),
      u32(entry.isDir ? 0x10 : 0),
      u32(offset),
      nameBuf,
    ]));

    offset += local.length + data.length;
  }

  const centralStart = offset;
  const centralDir = Buffer.concat(central);
  const eocd = Buffer.concat([
    u32(0x06054b50),
    u16(0),
    u16(0),
    u16(entries.length),
    u16(entries.length),
    u32(centralDir.length),
    u32(centralStart),
    u16(0),
  ]);

  return Buffer.concat([...chunks, centralDir, eocd]);
}

try {
  const entries = collectEntries(skillRoot);
  const required = ['SKILL.md', 'package.json', 'scripts/', 'references/', 'assets/', 'examples/', 'agents/'];
  const names = new Set(entries.map((entry) => entry.name));
  const missing = required.filter((entry) => !names.has(entry));
  if (missing.length) {
    throw new Error(`required package entries missing: ${missing.join(', ')}`);
  }

  mkdirSync(publishDir, { recursive: true });
  writeFileSync(tmpZip, makeZip(entries));
  if (existsSync(zipPath)) unlinkSync(zipPath);
  try {
    renameSync(tmpZip, zipPath);
  } catch (e) {
    if (e && e.code === 'EXDEV') {
      copyFileSync(tmpZip, zipPath);
      unlinkSync(tmpZip);
    } else {
      throw e;
    }
  }
  console.log(`pack-skill: wrote ${zipPath}`);
} catch (e) {
  if (existsSync(tmpZip)) {
    try {
      unlinkSync(tmpZip);
    } catch {
      /* ignore */
    }
  }
  console.error('pack-skill: failed to create zip');
  console.error(e.message || e);
  process.exit(1);
}
