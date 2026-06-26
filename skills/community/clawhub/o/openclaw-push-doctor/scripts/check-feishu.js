#!/usr/bin/env node
/**
 * openclaw-healthcheck — check-feishu.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 *
 * Usage:
 *   node scripts/check-feishu.js
 *   node scripts/check-feishu.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — Feishu Status Check ===

Run the following checks and report results:

  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

Interpret results:
  → NOT_INSTALLED            feishu: NOT_CONFIGURED
  → NOT_AUTHENTICATED        feishu: EXPIRED — run: node scripts/fix-feishu.js
  → "Token expired"          feishu: EXPIRED — run: node scripts/fix-feishu.js
  → "Logged in as <user>"    feishu: OK

If OK, run a quick smoke test:
  lark-cli calendar +agenda --dry-run 2>/dev/null && echo "SMOKE_OK" || echo "SMOKE_FAILED"

Output:
  "feishu": { "status": "OK | EXPIRED | NOT_CONFIGURED", "detail": "..." }
`);
} else {
  console.log(`=== openclaw-healthcheck — 飞书状态检查 ===

运行以下检查并报告结果：

  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

结果判断：
  → NOT_INSTALLED              feishu: NOT_CONFIGURED
  → NOT_AUTHENTICATED          feishu: EXPIRED — 运行：node scripts/fix-feishu.js
  → "Token expired"            feishu: EXPIRED — 运行：node scripts/fix-feishu.js
  → "Logged in as <用户>"      feishu: OK

如 OK，运行快速冒烟测试：
  lark-cli calendar +agenda --dry-run 2>/dev/null && echo "SMOKE_OK" || echo "SMOKE_FAILED"

输出：
  "feishu": { "status": "OK | EXPIRED | NOT_CONFIGURED", "detail": "..." }
`);
}
