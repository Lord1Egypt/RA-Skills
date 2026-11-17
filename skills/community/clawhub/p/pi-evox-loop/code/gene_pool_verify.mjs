#!/usr/bin/env node
// 0.42 O02：池验签工具。读取分发池 genes.jsonl，逐条 verifyGene；
// tampered 必须显式报警并 exit 1（不得静默判绿），供发布后 C67 调用。
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const __here = path.dirname(new URL(import.meta.url).pathname);
const { verifyGene } = await import(pathToFileURL(path.join(__here, 'engine/light/identity.mjs')).href);
const file = process.argv[2];
if (!file || !fs.existsSync(file)) { console.error('用法: node gene_pool_verify.mjs <pool/genes.jsonl>'); process.exit(2); }
const rows = fs.readFileSync(file, 'utf8').split('\n').filter(x => x.trim()).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
const stat = {}; const bad = [];
for (const g of rows) { const s = verifyGene(g).status; stat[s] = (stat[s] || 0) + 1; if (s === 'tampered' || s === 'bad-format') bad.push(g.id || g.asset_id); }
console.log('[pool-verify] 共 ' + rows.length + ' 条：' + JSON.stringify(stat));
if (bad.length) { console.error('[pool-verify] BLOCKED tampered/bad-format: ' + bad.slice(0, 10).join(', ')); process.exit(1); }
console.log('[pool-verify] OK：无 tampered');
