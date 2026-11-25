#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = relative => fs.readFileSync(path.join(root, relative), 'utf8');
const fail = message => { throw new Error(message); };
const requireText = (relative, pattern, label) => {
  const text = read(relative);
  if (!pattern.test(text)) fail(`${relative}: missing ${label}`);
  return text;
};
const pngSize = relative => {
  const data = fs.readFileSync(path.join(root, relative));
  const signature = '89504e470d0a1a0a';
  if (data.subarray(0, 8).toString('hex') !== signature) fail(`${relative}: not a PNG`);
  return [data.readUInt32BE(16), data.readUInt32BE(20)];
};

const skill = requireText('SKILL.md', /^---[\s\S]*?^name: novel-pov-repair-cn$/m, 'required frontmatter name');
if (!/^description: .{80,240}$/mu.test(skill.match(/^---[\s\S]*?---/m)?.[0] ?? '')) fail('SKILL.md: description must be 80–240 characters');
const manifest = read('manifest.yaml');
for (const line of ['name: novel-pov-repair-cn', 'slug: novel-pov-repair-cn', 'display_name: 叙事视角诊断与修订', 'self_test: node scripts/self-test.mjs']) {
  if (!manifest.includes(line)) fail(`manifest.yaml: missing ${line}`);
}
if (!/short_description: .{25,64}/u.test(manifest)) fail('manifest.yaml: short_description must be 25–64 characters');
const manifestDescription = manifest.match(/^description: (.+)$/m)?.[1] ?? '';
if ([...manifestDescription].length < 80 || [...manifestDescription].length > 240) fail('manifest.yaml: description must be 80–240 characters');
if (!/allow_implicit_invocation: true/.test(manifest)) fail('manifest.yaml: policy boolean missing');
if ((manifest.match(/^  - /gm) ?? []).length < 7) fail('manifest.yaml: expected at least 4 tags and 3 triggers');
const agent = read('agents/openai.yaml');
for (const line of ['interface:', 'display_name: "叙事视角诊断与修订"', 'icon_small: "./icon-512.png"', 'icon_large: "./icon-512.png"', 'policy:', 'allow_implicit_invocation: true']) {
  if (!agent.includes(line)) fail(`agents/openai.yaml: missing ${line}`);
}
if (!/short_description: .{25,64}/u.test(agent)) fail('agents/openai.yaml: short_description must be 25–64 characters');
for (const field of ['display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large']) {
  const value = agent.match(new RegExp(`^  ${field}: "([^"\\n]+)"$`, 'm'))?.[1];
  if (!value) fail(`agents/openai.yaml: ${field} must be quoted`);
  if (field === 'default_prompt' && !value.includes('$novel-pov-repair-cn')) fail('default_prompt must refer to this Skill');
  if (field === 'short_description' && ([...value].length < 25 || [...value].length > 64)) fail('invalid actual short description length');
  if (field.startsWith('icon_')) {
    const resolved = path.resolve(root, value), relative = path.relative(root, resolved);
    if (relative.startsWith('..') || path.isAbsolute(relative) || !fs.existsSync(resolved)) fail('agent icon must exist inside Skill directory');
  }
}
for (const file of ['README.md', 'README.en.md', 'fixtures/success.md', 'fixtures/failure.md', 'fixtures/forward-success.md', 'fixtures/forward-failure.md', 'fixtures/failure-missing-viewpoint.md', 'fixtures/failure-missing-text.md', 'LICENSE']) {
  if (!fs.existsSync(path.join(root, file))) fail(`missing ${file}`);
}
const successFixture = read('fixtures/success.md');
for (const text of [
  '发现 2 处明确视角越界',
  '“陈默强装镇定”',
  '“心里其实害怕她会追问那笔钱的去向”',
  '只删除第 2 句',
  '陈默没有新增发言',
]) {
  if (!successFixture.includes(text)) fail(`fixtures/success.md: missing POV regression check: ${text}`);
}
// The revised passage must preserve every observable event and the original dialogue.
// Removing inaccessible narration is allowed; converting it into a new event is not.
const inputPassage = successFixture.split('## 参考交付')[0].split('\n> ')[1]?.trim();
const outputPassage = successFixture.split('合并最小修订（完整片段）：')[1]?.split('\n> ')[1]?.split('\n')[0]?.trim();
const inaccessibleSentence = '陈默强装镇定，心里其实害怕她会追问那笔钱的去向。';
if (!inputPassage || !inputPassage.includes(inaccessibleSentence)) fail('success input must retain its original inaccessible narration');
if (outputPassage !== inputPassage.replace(inaccessibleSentence, '')) fail('success output changed observable events, dialogue, or character knowledge');
if (read('fixtures/forward-success.md') !== successFixture.split('## 参考交付\n\n')[1]) fail('forward success and reference delivery disagree');
if (read('fixtures/forward-failure.md') !== read('fixtures/failure.md').split('## 参考交付\n\n')[1]) fail('forward failure and reference delivery disagree');
const missingViewpoint = read('fixtures/failure-missing-viewpoint.md').split('## 参考交付')[1]?.match(/缺项：([^\n]+)/)?.[1] ?? '';
const missingText = read('fixtures/failure-missing-text.md').split('## 参考交付')[1]?.match(/缺项：([^。]+)/)?.[1] ?? '';
if (!missingViewpoint.startsWith('视角人物') || missingViewpoint.split('。')[0].includes('场景文本')) fail('viewpoint-only failure reports supplied text as missing');
if (missingText !== '场景文本') fail('text-only failure reports supplied viewpoint as missing');
for (const rule of ['不把未说出口的内心活动改成台词', '已经收到的材料不得重复列为缺失', '章节、单场景和短文均属处理范围']) {
  if (!skill.includes(rule)) fail(`SKILL.md: missing behavior rule: ${rule}`);
}
if (skill.includes('超出单次场景的文本')) fail('SKILL.md contradicts chapter scope');
if (!manifest.includes('icon: icon-512.png')) fail('manifest.yaml: missing root icon reference');
for (const [file, dimensions] of [['icon-512.png', [512, 512]], ['assets/icon-512.png', [512, 512]], ['assets/promo-1600x900.png', [1600, 900]]]) {
  const got = pngSize(file);
  if (got[0] !== dimensions[0] || got[1] !== dimensions[1]) fail(`${file}: expected ${dimensions.join('×')}, got ${got.join('×')}`);
}
if (!read('README.md').includes('fixtures/success.md') || !read('README.md').includes('fixtures/failure.md')) fail('README.md: fixture links missing');
console.log('PASS: metadata, assets, exact observable-event preservation, and actual missing-field contracts.');
console.log('NOTE: fixture contract checks do not replace executing diagnosis on new user text.');
