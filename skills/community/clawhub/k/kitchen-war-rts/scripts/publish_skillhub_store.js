#!/usr/bin/env node
/**
 * 发布/更新 厨房战争 到 SkillHub 商店前台 (skillhub.cn / cloud.tencent.com)。
 *
 * 重要事实（2026-09-08 验证）：
 *  - `clawhub publish --site https://skillhub.cn` 只写 **clawhub 兼容注册表镜像**，
 *    并不会在 SkillHub **商店前台目录**建/更新条目。商店前台用独立的 store API。
 *  - SkillHub 商店目录 API 用独立的 `skh_...` token（存于 ~/.skillhub/credentials.json），
 *    不是 clawhub 的 `clh_...` token。
 *  - 本技能的商店条目 slug 是 `war-skill`（owner `user_98676efe`），不是 `kitchen-war-rts`。
 *    用同一 slug + 更高 version 提交即为"更新到新版"（upsert）。
 *  - 提交后 reviewStatus/contentAuditStatus/securityScanStatus 会进入 pending，
 *    审核通过后自动翻成最新版（与 clawhub 的 pending-publication 一致）。
 *
 * 真实接口（从 skillhub 网页前端 bundle 反查确认）：
 *  POST /api/v1/community/skills/publish
 *  multipart/form-data:
 *    payload : JSON { slug, displayName, version, summaryZh?, iconUrl? }
 *    files[] : 每个技能文件，filename = 相对路径
 *  Header: Authorization: Bearer <skh_token>
 */

const fs = require('fs');
const path = require('path');

const CRED = path.join(process.env.USERPROFILE || process.env.HOME, '.skillhub', 'credentials.json');
const SKILL_DIR = path.resolve(__dirname, '..');
// slug / 显示名可用环境变量覆盖：SKH_SLUG、SKH_DISPLAY
// 默认 war-skill（老条目）。发与 clawhub 一致的别名时：SKH_SLUG=kitchen-war-rts SKH_DISPLAY="厨房战争：红警风RTS"
const SLUG = (process.env.SKH_SLUG || 'war-skill').trim();
const DISPLAY = (process.env.SKH_DISPLAY || '《厨房战争》全面红警化，并在多个维度做了"超越"。').trim();
const VERSION = (process.argv[2] || '1.0.4').trim();

// 要纳入发布的文件（相对路径）。无二进制，纯文本。
const REL = [
  'SKILL.md',
  'assets/index.html',
  'references/testing.md',
  'scripts/verify_game.js',
  'scripts/_audit2.js',
  'scripts/_smoke_features.js',
  'scripts/_probe.js',
  'scripts/_power_logic.js',
  'scripts/_best_test.js',
];

function ct(p) {
  if (p.endsWith('.html')) return 'text/html';
  if (p.endsWith('.md')) return 'text/markdown';
  if (p.endsWith('.js')) return 'text/javascript';
  return 'application/octet-stream';
}

(async () => {
  let cred;
  try { cred = JSON.parse(fs.readFileSync(CRED, 'utf8')); }
  catch (e) { console.error('找不到 SkillHub 凭证:', CRED); process.exit(2); }
  const TOKEN = cred.user && cred.user.token;
  const BASE = (cred.user && cred.user.host) || 'https://api.skillhub.cn';
  if (!TOKEN) { console.error('凭证里没有 token'); process.exit(2); }

  const form = new FormData();
  form.append('payload', JSON.stringify({
    slug: SLUG,
    displayName: DISPLAY,
    version: VERSION,
    summaryZh: '红警风 RTS 厨房战争：单文件 HTML5 Canvas，零依赖，即开即玩。v' + VERSION +
      ' 含 10 兵种独特剪影+专属兵种色+阵营环、修复自行火炮贴脸卡死与退款精度漏洞、62 项真机门禁全绿。',
  }));
  for (const rel of REL) {
    const buf = fs.readFileSync(path.join(SKILL_DIR, rel));
    form.append('files', new Blob([buf], { type: ct(rel) }), rel);
  }

  const res = await fetch(BASE + '/api/v1/community/skills/publish', {
    method: 'POST',
    headers: { Authorization: `Bearer ${TOKEN}` },
    body: form,
  });
  const text = await res.text();
  console.log('STATUS:', res.status);
  console.log(text.slice(0, 1200));
  if (!res.ok) process.exit(1);
  console.log('\n✅ 已提交 ' + SLUG + ' v' + VERSION + ' 到 SkillHub 商店（审核中，通过后自动生效）。');
})();
