#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const MB = 1024 * 1024;
const SIZE_LIMITS = { 5: 10*MB, 7: 10*MB, 13: 10*MB, 14: 10*MB, 9: 30*MB };
const DEFAULT_LIMIT = 200 * MB;
const UNSUPPORTED = new Set(['mp4','avi','mov','mkv','wmv','flv','webm','m4v','rmvb','rm','3gp']);

const EXT_MAP = {
  pdf: { t: 1, c: 'application/pdf' },
  doc: { t: 3, c: 'application/msword' },
  docx: { t: 3, c: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' },
  ppt: { t: 4, c: 'application/vnd.ms-powerpoint' },
  pptx: { t: 4, c: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' },
  xls: { t: 5, c: 'application/vnd.ms-excel' },
  xlsx: { t: 5, c: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' },
  csv: { t: 5, c: 'text/csv' },
  md: { t: 7, c: 'text/markdown' },
  markdown: { t: 7, c: 'text/markdown' },
  png: { t: 9, c: 'image/png' },
  jpg: { t: 9, c: 'image/jpeg' },
  jpeg: { t: 9, c: 'image/jpeg' },
  webp: { t: 9, c: 'image/webp' },
  txt: { t: 13, c: 'text/plain' },
  xmind: { t: 14, c: 'application/x-xmind' },
  mp3: { t: 15, c: 'audio/mpeg' },
  m4a: { t: 15, c: 'audio/x-m4a' },
  wav: { t: 15, c: 'audio/wav' },
  aac: { t: 15, c: 'audio/aac' },
};

const CT_MAP = {};
for (const [k, v] of Object.entries(EXT_MAP)) {
  if (!CT_MAP[v.c]) CT_MAP[v.c] = v.t;
}
Object.assign(CT_MAP, { 'text/x-markdown': 7, 'application/md': 7, 'application/markdown': 7, 'application/vnd.xmind.workbook': 14, 'application/zip': 14 });

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith('--') && i + 1 < process.argv.length) {
    args[process.argv[i].replace(/^--/, '')] = process.argv[++i];
  }
}

if (!args.file) {
  console.error('Usage: node preflight-check.cjs --file <path> [--content-type <mime>]');
  process.exit(2);
}

const filePath = path.resolve(args.file);
const fileName = path.basename(filePath);
const ext = fileName.match(/\.([^.]+)$/)?.[1]?.toLowerCase() || '';
const inputCt = args['content-type'] || '';

let stat;
try { stat = fs.statSync(filePath); }
catch (e) { console.error(`File not found: ${filePath}`); process.exit(2); }

if (UNSUPPORTED.has(ext)) fail({ file_path: filePath, file_name: fileName, file_ext: ext }, `Video files (.${ext}) are not supported. Only supported in IMA desktop app.`);
if (inputCt && inputCt.startsWith('video/')) fail({ file_path: filePath, file_name: fileName, file_ext: ext }, `Video files (${inputCt}) are not supported.`);

let mediaType, contentType;
const ctMt = inputCt ? CT_MAP[inputCt] : null;
const extMap = ext ? EXT_MAP[ext] : null;

if (ctMt != null) {
  mediaType = ctMt;
  contentType = inputCt;
} else if (inputCt) {
  if (extMap) { mediaType = extMap.t; contentType = extMap.c; }
  else fail({ file_path: filePath, file_name: fileName, file_ext: ext }, `Unrecognized content type ${inputCt}${ext ? ` and extension .${ext}` : ''}.`);
} else {
  if (extMap) { mediaType = extMap.t; contentType = extMap.c; }
  else if (ext) fail({ file_path: filePath, file_name: fileName, file_ext: ext }, `Unrecognized file extension .${ext}.`);
  else fail({ file_path: filePath, file_name: fileName, file_ext: ext }, 'File has no extension and no --content-type provided.');
}

const sizeLimit = SIZE_LIMITS[mediaType] || DEFAULT_LIMIT;
if (stat.size > sizeLimit) {
  const fmt = b => b < MB ? `${(b/1024).toFixed(1)} KB` : `${(b/MB).toFixed(1)} MB`;
  fail({ file_path: filePath, file_name: fileName, file_ext: ext, file_size: stat.size, media_type: mediaType, content_type: contentType }, `File size ${fmt(stat.size)} exceeds ${fmt(sizeLimit)} limit.`);
}

console.log(JSON.stringify({ pass: true, file_path: filePath, file_name: fileName, file_ext: ext, file_size: stat.size, media_type: mediaType, content_type: contentType }));
process.exit(0);

function fail(base, reason) {
  console.log(JSON.stringify({ pass: false, ...base, reason }));
  process.exit(1);
}
