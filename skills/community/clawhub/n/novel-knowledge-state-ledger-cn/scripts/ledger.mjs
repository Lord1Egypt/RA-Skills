#!/usr/bin/env node
import fs from 'node:fs';

const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const fail = (message) => { process.stderr.write(`${message}\n`); process.exit(2); };
if (!Array.isArray(input.scenes) || input.scenes.length === 0) fail('缺少按故事顺序排列的 scenes，无法建立知情账本。');
if (!Array.isArray(input.facts) || input.facts.length === 0) fail('缺少 facts（事实编号与说明），无法建立知情账本。');
for (const fact of input.facts) if (!fact || typeof fact.id !== 'string' || !fact.id.trim() || fact.id !== fact.id.trim()) fail(`事实 id 必须非空且不得含首尾空格：${JSON.stringify(fact)}`);
const factIds = new Set(input.facts.map(f => f.id));
const people = new Set(input.characters || []);
const states = new Map();
const earlyUses = [];
let evidenceCount = 0;
for (const scene of input.scenes) {
  if (!scene.id || !Array.isArray(scene.evidence)) fail(`场景缺少 id 或 evidence：${JSON.stringify(scene)}`);
  for (const e of scene.evidence) {
    if (typeof e.fact !== 'string' || !e.fact.trim() || e.fact !== e.fact.trim() || !factIds.has(e.fact) || typeof e.character !== 'string' || !e.character.trim() || !['experienced', 'told', 'inferred', 'used'].includes(e.type) || typeof e.quote !== 'string' || !e.quote.trim()) fail(`无效证据（必须含人物、无首尾空格且有效的事实编号、类型和非空原文 quote）：${JSON.stringify(e)}`);
    evidenceCount++;
    people.add(e.character);
  }
}
if (evidenceCount === 0) fail('缺少人物事实证据，无法建立可审计知情账本；请补充具体场景及原文 quote。');
// Establish first knowledge across the complete scene, then compare uses by scene index.
for (const [sceneIndex, scene] of input.scenes.entries()) for (const e of scene.evidence) {
  if (e.type === 'used') continue;
  const key = `${e.character}\u0000${e.fact}`;
  const prior = states.get(key);
  if (!prior) states.set(key, {status: e.type === 'inferred' ? '猜测' : '确信', first_known_scene:scene.id, first_known_scene_index:sceneIndex, evidence:e.quote, basis:e.type});
  else if (prior.status === '猜测' && e.type !== 'inferred') states.set(key, {...prior, status:'确信', confirmation_scene:scene.id, confirmation_evidence:e.quote});
}
for (const [sceneIndex, scene] of input.scenes.entries()) for (const e of scene.evidence) {
  if (e.type !== 'used') continue;
  const known = states.get(`${e.character}\u0000${e.fact}`);
  if (!known || known.first_known_scene_index > sceneIndex) earlyUses.push({ character:e.character, fact:e.fact, scene:scene.id, evidence:e.quote });
}
const matrix = [...people].sort().map(character => ({ character, facts: input.facts.map(f => ({ fact:f.id, ...(states.get(`${character}\u0000${f.id}`) || {status:'未知', first_known_scene:null, evidence:null, basis:null}) })) }));
for (const row of matrix) for (const cell of row.facts) delete cell.first_known_scene_index;
process.stdout.write(JSON.stringify({ knowledge_matrix:matrix, early_information_uses:earlyUses }, null, 2) + '\n');
