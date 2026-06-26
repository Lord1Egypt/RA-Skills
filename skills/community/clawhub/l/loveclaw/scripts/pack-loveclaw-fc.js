#!/usr/bin/env node
/**
 * 打包阿里云函数计算可上传目录/zip：HTTP 入口 exports.handler（来自 index_deployed_fixed.js）。
 *
 *   node scripts/pack-loveclaw-fc.js [输出zip路径，默认可略]
 *
 * 默认 zip 写到项目上级 Desktop：loveclaw-fc-aliyun-full-YYYY-MM-DD-HHMM.zip
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const FC = path.join(ROOT, 'deploy', 'loveclaw-fc');
const FIXED = path.join(FC, 'index_deployed_fixed.js');
const PKG = path.join(FC, 'package.json');

const desktop = path.join(require('os').homedir(), 'Desktop');
const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '').slice(0, 12);
const defaultZip = path.join(desktop, `loveclaw-fc-aliyun-full-${stamp}.zip`);
const outZip = process.argv[2] ? path.resolve(process.argv[2]) : defaultZip;

const STAGE = path.join(ROOT, '.loveclaw-fc-release');

function rmrf(p) {
  fs.rmSync(p, { recursive: true, force: true });
}

function main() {
  if (!fs.existsSync(FIXED)) {
    console.error('missing', FIXED);
    process.exit(1);
  }
  rmrf(STAGE);
  fs.mkdirSync(STAGE, { recursive: true });

  fs.copyFileSync(FIXED, path.join(STAGE, 'index.js'));
  fs.copyFileSync(PKG, path.join(STAGE, 'package.json'));

  const envReadme = [
    '# LoveClaw 云函数部署包（完整版，含 node_modules）',
    '',
    '- 运行时：Node.js（与当前 FC 所选大版本一致即可，建议 Node 18/20）',
    '- 入口：index.handler（HTTP 触发器）',
    '',
    '## 必填/常用环境变量',
    '',
    '- LOVECLAW_API_TOKEN 或 API_TOKEN：Bearer 与技能侧一致',
    '- LOVECLAW_MATCH_COMPARE / LOVECLAW_TOP_K_CANDIDATES：可选匹配调优',
    '- ACCESS_KEY_ID / ACCESS_KEY_SECRET：TableStore + OSS',
    '- TABULSTORE_INSTANCE（默认 loveclaw）、TABULSTORE_REGION（如 cn-hangzhou）',
    '- TABULSTORE_TABLE（默认 profiles）',
    '- OSS_BUCKET、OSS_REGION（如 oss-cn-shanghai 与桶地域一致）',
    '',
    '上传本 zip 后在控制台解压部署；或上传 zip 由平台解压。',
    '',
  ].join('\n');
  fs.writeFileSync(path.join(STAGE, 'FC-DEPLOY-README.txt'), envReadme, 'utf8');

  execSync('npm install --omit=dev', { cwd: STAGE, stdio: 'inherit' });
  rmrf(outZip);

  const parent = path.dirname(outZip);
  fs.mkdirSync(parent, { recursive: true });
  execSync(`zip -rq "${outZip}" .`, { cwd: STAGE, stdio: 'inherit' });

  console.log('OK zip ->', outZip);
}

main();
