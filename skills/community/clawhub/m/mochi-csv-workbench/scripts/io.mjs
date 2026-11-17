import fs from 'node:fs';
import path from 'node:path';
import { TextDecoder } from 'node:util';

export function checkedPath(value, type = 'file') {
  if (typeof value !== 'string' || !value || value.includes('\0') || /^(?:\\\\|\/\/)/.test(value)) throw new Error('Use an explicit local path.');
  const full = path.resolve(value), root = path.parse(full).root;
  let current = root;
  for (const part of full.slice(root.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    const stat = fs.lstatSync(current);
    if (stat.isSymbolicLink()) throw new Error('Symlink/reparse paths are refused: ' + current);
  }
  const stat = fs.lstatSync(full);
  if (type === 'file' ? !stat.isFile() : !stat.isDirectory()) throw new Error('Expected a regular ' + type + '.');
  return full;
}
export function openRegular(value) {
  const full = checkedPath(value), before = fs.lstatSync(full);
  const fd = fs.openSync(full, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  const after = fs.fstatSync(fd);
  if (!after.isFile() || after.dev !== before.dev || after.ino !== before.ino) { fs.closeSync(fd); throw new Error('Input changed while opening.'); }
  return { fd, full, stat: after };
}
export async function readText(input, maxBytes = 8 * 1024 * 1024) {
  let bytes;
  if (input === '-') {
    const chunks = []; let total = 0;
    for await (const chunk of process.stdin) { total += chunk.length; if (total > maxBytes) throw new Error('Input exceeds byte limit.'); chunks.push(chunk); }
    bytes = Buffer.concat(chunks);
  } else {
    const opened = openRegular(input);
    try {
      if (opened.stat.size > maxBytes) throw new Error('Input exceeds byte limit.');
      const buffer = Buffer.alloc(maxBytes + 1); let total = 0, count;
      while ((count = fs.readSync(opened.fd, buffer, total, buffer.length - total, null)) > 0) { total += count; if (total > maxBytes) throw new Error('Input exceeds byte limit.'); }
      const end = fs.fstatSync(opened.fd);
      if (end.size !== opened.stat.size || end.mtimeMs !== opened.stat.mtimeMs) throw new Error('Input changed while reading.');
      bytes = buffer.subarray(0, total);
    } finally { fs.closeSync(opened.fd); }
  }
  return new TextDecoder('utf-8', { fatal: true }).decode(bytes).replace(/^\uFEFF/, '');
}
export function newOutput(value) {
  if (typeof value !== 'string' || !value || /^(?:\\\\|\/\/)/.test(value)) throw new Error('Use a new local output directory.');
  const full = path.resolve(value);
  checkedPath(path.dirname(full), 'directory');
  if (fs.existsSync(full)) throw new Error('Output directory already exists; choose a new name.');
  fs.mkdirSync(full, { mode: 0o700 });
  return full;
}
export function writeNew(folder, name, content) {
  if (path.basename(name) !== name) throw new Error('Output filenames must be local.');
  fs.writeFileSync(path.join(folder, name), content, { flag: 'wx', mode: 0o600 });
}
export function md(value) { return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\\`*_{}\[\]#|~]/g, '\\$&').replace(/(^|\n)([ \t]*)([-+>])/g, '$1$2\\$3').replace(/(^|\n)([ \t]*[0-9]+)([.)])(?=\s)/g, '$1$2\\$3'); }
export function csvCell(value) {
  let text = String(value ?? '');
  if (/^[\s\p{Cc}\p{Cf}]*[=+\-@]/u.test(text) || /^[\p{Cc}\p{Cf}]/u.test(text)) text = "'" + text;
  return '"' + text.replace(/"/g, '""') + '"';
}
export function isWithin(parent, child) { const relative = path.relative(parent, child); return relative === '' || (!relative.startsWith('..' + path.sep) && relative !== '..' && !path.isAbsolute(relative)); }
