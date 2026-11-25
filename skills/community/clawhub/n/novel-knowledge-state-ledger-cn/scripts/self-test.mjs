#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const run = (file) => spawnSync(process.execPath, [path.join(root, 'scripts/ledger.mjs')], { cwd:root, input:fs.readFileSync(path.join(root, file)), encoding:'utf8' });
const ok = run('fixtures/success-input.json');
if (ok.status !== 0) throw new Error(ok.stderr);
const result = JSON.parse(ok.stdout);
const yi = result.knowledge_matrix.find(x => x.character === '乙').facts.find(x => x.fact === 'F-密钥');
const jia = result.knowledge_matrix.find(x => x.character === '甲').facts.find(x => x.fact === 'F-密钥');
if (jia.status !== '确信' || jia.first_known_scene !== 'S1' || yi.status !== '确信' || yi.first_known_scene !== 'S3' || result.early_information_uses.length !== 1 || result.early_information_uses[0]?.scene !== 'S2' || !result.early_information_uses[0]?.evidence.includes('钟楼')) throw new Error('成功样例账本结果缺少提前使用事实的原文证据');
const sameScene = spawnSync(process.execPath, [path.join(root, 'scripts/ledger.mjs')], { cwd:root, input:JSON.stringify({characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[{character:'甲',fact:'F1',type:'used',quote:'甲使用F1。'},{character:'甲',fact:'F1',type:'told',quote:'甲获告知F1。'}]}]}), encoding:'utf8' });
if (sameScene.status !== 0 || JSON.parse(sameScene.stdout).early_information_uses.length !== 0) throw new Error('同场景 evidence 数组顺序不应决定先后');
const noQuote = spawnSync(process.execPath, [path.join(root, 'scripts/ledger.mjs')], { cwd:root, input:JSON.stringify({characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[{character:'甲',fact:'F1',type:'told'}]}]}), encoding:'utf8' });
if (noQuote.status === 0 || !noQuote.stderr.includes('quote')) throw new Error('缺少 quote 的证据未被拒绝');
const emptyEvidence = spawnSync(process.execPath, [path.join(root, 'scripts/ledger.mjs')], { cwd:root, input:JSON.stringify({characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[]}]}), encoding:'utf8' });
if (emptyEvidence.status === 0 || !emptyEvidence.stderr.includes('缺少')) throw new Error('空 evidence 未被拒绝');
for (const malformed of [
  {characters:['甲'],facts:[{}],scenes:[{id:'S1',evidence:[{character:'甲',type:'told',quote:'甲得知某事。'}]}]},
  {characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[{character:'甲',fact:'',type:'told',quote:'甲得知某事。'}]}]},
  {characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[{character:'甲',type:'told',quote:'甲得知某事。'}]}]},
  {characters:['甲'],facts:[{id:' F1 '}],scenes:[{id:'S1',evidence:[{character:'甲',fact:'F1',type:'told',quote:'甲得知某事。'}]}]},
  {characters:['甲'],facts:[{id:'F1'}],scenes:[{id:'S1',evidence:[{character:'甲',fact:' F1 ',type:'told',quote:'甲得知某事。'}]}]}
]) {
  const result = spawnSync(process.execPath, [path.join(root, 'scripts/ledger.mjs')], { cwd:root, input:JSON.stringify(malformed), encoding:'utf8' });
  if (result.status === 0) throw new Error('缺失事实编号或证据 fact 的输入被错误接受');
}
const bad = run('fixtures/failure-input.json');
if (bad.status === 0 || !bad.stderr.includes('缺少')) throw new Error('失败样例未被真实拒绝');
const manifest = fs.readFileSync(path.join(root, 'manifest.yaml'), 'utf8');
for (const term of ['tags:', '小说连续性', '人物设定', 'trigger_words:', '人物什么时候知道', 'triggers:', '按场景核对每个人物何时得知事实']) {
  if (!manifest.includes(term)) throw new Error(`manifest 缺少真实标签或触发词：${term}`);
}
console.log('self-test passed: success ledger and missing-evidence failure were executed.');
