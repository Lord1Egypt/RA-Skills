import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';
import { checkedPath, openRegular, newOutput, writeNew, md, isWithin } from './io.mjs';

const categories = {
  documents: ['.pdf','.doc','.docx','.txt','.md','.odt','.rtf'], images: ['.png','.jpg','.jpeg','.gif','.webp','.svg','.heic'],
  audio: ['.mp3','.wav','.m4a','.flac','.ogg'], video: ['.mp4','.mov','.mkv','.webm','.avi'],
  archives: ['.zip','.7z','.tar','.gz','.rar'], data: ['.csv','.tsv','.json','.xml','.xlsx','.ods'],
  code: ['.js','.mjs','.ts','.py','.cs','.html','.css','.sh','.ps1','.sql']
};
function category(name) { const extension = path.extname(name).toLowerCase(); return Object.keys(categories).find(key => categories[key].includes(extension)) || 'other'; }
export async function plan(rootValue, { maxFiles = 10000, maxBytes = 1073741824 } = {}) {
  const root = checkedPath(rootValue, 'directory'), files = [], skipped = []; let totalBytes = 0;
  async function walk(directory, depth) {
    if (depth > 40) throw new Error('Directory nesting exceeds40 levels.');
    checkedPath(directory, 'directory');
    for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a,b) => a.name.localeCompare(b.name, 'en'))) {
      const full = path.join(directory, entry.name), relative = path.relative(root, full).split(path.sep).join('/');
      const stat = fs.lstatSync(full);
      if (stat.isSymbolicLink()) { skipped.push({ path: relative, reason: 'symlink-or-junction' }); continue; }
      if (stat.isDirectory()) { await walk(full, depth + 1); continue; }
      if (!stat.isFile()) { skipped.push({ path: relative, reason: 'not-regular-file' }); continue; }
      if (files.length >= maxFiles || totalBytes + stat.size > maxBytes) throw new Error('Scan limit reached; choose a smaller directory or explicit higher limits.');
      const opened = openRegular(full), hash = createHash('sha256');
      try {
        const block = Buffer.alloc(65536); let count, read = 0;
        while ((count = fs.readSync(opened.fd, block, 0, block.length, null)) > 0) {
          read += count; if (totalBytes + read > maxBytes) throw new Error('Byte limit reached.'); hash.update(block.subarray(0,count));
        }
        const end = fs.fstatSync(opened.fd);
        if (read !== opened.stat.size || end.size !== opened.stat.size || end.mtimeMs !== opened.stat.mtimeMs) throw new Error('A file changed during hashing; rerun on a stable input.');
        files.push({ path: relative, bytes: read, sha256: hash.digest('hex'), category: category(entry.name) }); totalBytes += read;
      } finally { fs.closeSync(opened.fd); }
    }
  }
  await walk(root, 0);
  const buckets = new Map(), targets = new Set();
  for (const item of files) {
    const key = item.bytes + ':' + item.sha256;
    if (!buckets.has(key)) buckets.set(key, []); buckets.get(key).push(item.path);
    let name = path.posix.basename(item.path).replace(/[<>:"/\\|?*\u0000-\u001f]/g,'_').replace(/[. ]+$/g,'');
    if (!name || /^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(name)) name = '_' + name;
    let target = item.category + '/' + name, serial = 1;
    while (targets.has(target.toLowerCase())) target = item.category + '/' + (++serial) + '-' + name;
    targets.add(target.toLowerCase()); item.proposedRelativePath = target;
  }
  const duplicateGroups = [...buckets].filter(([,paths]) => paths.length > 1).map(([key,paths]) => ({ bytesPerFile: Number(key.split(':')[0]), sha256: key.split(':')[1], paths }));
  return { schemaVersion: 1, mode: 'read-only-plan', root, totalFiles: files.length, totalBytes, classification: 'extension-only', files, duplicateGroups, skipped, changedFiles: 0 };
}
export async function main(argv = process.argv.slice(2)) {
  const { values } = parseArgs({ args: argv, options: { root: { type:'string' }, out: { type:'string' }, 'max-files': {type:'string'}, 'max-bytes': {type:'string'}, help: {type:'boolean'} } });
  if (values.help) { console.log('node organize.mjs --root INPUT_DIRECTORY --out NEW_REPORT_DIRECTORY [--max-files 10000 --max-bytes 1073741824]'); return; }
  if (!values.root || !values.out) throw new Error('--root and --out are required.');
  const root = checkedPath(values.root, 'directory'), out = path.resolve(values.out);
  if (isWithin(root, out)) throw new Error('Report output must be outside the scanned directory.');
  const limits = { maxFiles: Number(values['max-files'] || 10000), maxBytes: Number(values['max-bytes'] || 1073741824) };
  if (!Number.isSafeInteger(limits.maxFiles) || limits.maxFiles < 1 || limits.maxFiles > 50000 || !Number.isSafeInteger(limits.maxBytes) || limits.maxBytes < 1 || limits.maxBytes > 53687091200) throw new Error('Invalid scan limits.');
  const result = await plan(root, limits), directory = newOutput(values.out);
  writeNew(directory, 'plan.json', JSON.stringify(result, null, 2) + '\n');
  const lines = ['# File organization plan', '', 'Read-only. No source file was moved, copied or deleted.', '', `Files: ${result.totalFiles}; bytes: ${result.totalBytes}. Categories use extensions only.`, '', '## Proposed paths', ...result.files.map(item => '- ' + md(item.path) + ' → ' + md(item.proposedRelativePath)), '', '## SHA256 duplicate groups', ...result.duplicateGroups.map(group => '- ' + group.bytesPerFile + ' bytes each: ' + group.paths.map(md).join('; ')), '', '## Skipped paths', ...result.skipped.map(item => '- ' + md(item.path) + ': ' + item.reason), '', 'Hash equality is evidence for review, not permission to remove a file. Keep a backup; content can change after scanning.'];
  writeNew(directory, 'report.md', lines.join('\n') + '\n'); console.log(JSON.stringify({ output: directory, files: result.totalFiles, duplicateGroups: result.duplicateGroups.length, changedFiles: 0 }));
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main().catch(error => { console.error('ERROR: ' + error.message); process.exitCode = 1; });
