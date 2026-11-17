#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'fixtures/success-input.json', 'fixtures/failure-input.json'];
const errors = required.filter((file) => !existsSync(resolve(root, file))).map((file) => `缺少 ${file}`);
let success, failure;
try { success = JSON.parse(readFileSync(resolve(root, 'fixtures/success-input.json'), 'utf8')); } catch { errors.push('成功样例不是有效 JSON'); }
try { failure = JSON.parse(readFileSync(resolve(root, 'fixtures/failure-input.json'), 'utf8')); } catch { errors.push('失败样例不是有效 JSON'); }
if (!success?.opening?.trim()) errors.push('成功样例必须提供 opening');
if (failure?.opening?.trim()) errors.push('失败样例必须缺少 opening，以覆盖资料缺失');
const png = readFileSync(resolve(root, 'icon-512.png'));
if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') errors.push('图标不是 PNG');
if (png.readUInt32BE(16) !== 512 || png.readUInt32BE(20) !== 512) errors.push('图标必须是 512×512');
if (errors.length) { console.error(`self-test failed:\n- ${errors.join('\n- ')}`); process.exit(1); }
console.log('self-test passed: required files, fixtures, and 512×512 PNG icon are valid.');
