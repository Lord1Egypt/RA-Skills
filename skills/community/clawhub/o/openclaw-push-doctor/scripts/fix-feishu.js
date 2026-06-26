#!/usr/bin/env node
/**
 * openclaw-healthcheck — fix-feishu.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Guides the agent through Feishu/lark-cli re-authentication.
 * Handles both token refresh (quick) and full OAuth re-login (browser step).
 *
 * Usage:
 *   node scripts/fix-feishu.js
 *   node scripts/fix-feishu.js --lang en
 *   node scripts/fix-feishu.js --full    # force full OAuth re-login
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const fullReauth = args.includes('--full');

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — Fix Feishu Auth ===
Mode: ${fullReauth ? 'Full OAuth re-login' : 'Try token refresh first, fall back to re-login'}

Feishu (lark-cli) tokens expire and must be refreshed or re-issued.
This guide covers both the quick refresh path and the full browser OAuth path.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — Diagnose current auth state
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status

Outcomes:
  A) Shows "Logged in as <user>" with no expiry warning → auth is fine, no action needed
  B) Shows "Token expires in <N> days"                  → proceed to STEP 2 (refresh)
  C) Shows "Token expired" or "Unauthorized"            → proceed to STEP 2 (refresh)
  D) Command not found                                  → lark-cli not installed, run feishu-cli-setup skill first

${fullReauth ? '' : `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — Try token refresh (no browser needed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth refresh

  → If succeeds: run lark-cli auth status to confirm new expiry date
  → If fails with "refresh token expired" or "invalid_grant": proceed to STEP 3 (full re-login)
  → If fails with network error: check internet connection and retry

`}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP ${fullReauth ? '2' : '3'} — Full OAuth re-login  ⚠️ BROWSER STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run in background and capture output:
  lark-cli auth login --recommend --no-wait

⚠️ EXTRACT THE AUTHORIZATION URL from the output. It looks like:
  "Please open the following URL to authorize: https://accounts.feishu.cn/..."

Send this message to the user:
  "Your Feishu token has expired and needs to be renewed.
   Please open this URL in your browser to re-authorize lark-cli:
   [paste URL here]
   Log in to Feishu and click Authorize. Tell me when done."

After user confirms:
  lark-cli auth status   # Must show: Logged in as <user>

If still failing (device code expired):
  lark-cli auth login --device-code <DEVICE_CODE from earlier output>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP ${fullReauth ? '3' : '4'} — Verify and test push
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status   # confirm logged in
  lark-cli im +messages-send --chat-id oc_xxx --text "✅ lark-cli reconnected at $(date)" --dry-run

  → If --dry-run succeeds, remove --dry-run for a real test message (optional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT — Update data/health-report.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Update the feishu entry:
  "feishu": { "status": "OK", "detail": "Re-authenticated at <timestamp>. Token valid." }
`);
} else {
  console.log(`=== openclaw-healthcheck — 修复飞书认证 ===
模式：${fullReauth ? '强制完整 OAuth 重新登录' : '先尝试 token 刷新，失败再重新登录'}

飞书 lark-cli token 会过期，需要刷新或重新授权。
本指南覆盖快速刷新和完整浏览器 OAuth 两条路径。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 1 步 — 诊断当前认证状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status

结果判断：
  A) 显示 "Logged in as <用户>" 且无过期警告 → auth 正常，无需操作
  B) 显示 "Token expires in <N> days"         → 进入第 2 步（刷新）
  C) 显示 "Token expired" 或 "Unauthorized"   → 进入第 2 步（刷新）
  D) 命令未找到                               → lark-cli 未安装，先运行 feishu-cli-setup skill

${fullReauth ? '' : `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 2 步 — 尝试 token 刷新（无需浏览器）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth refresh

  → 成功：运行 lark-cli auth status 确认新的过期日期
  → 失败（"refresh token expired" / "invalid_grant"）：进入第 3 步（完整重新登录）
  → 失败（网络错误）：检查网络后重试

`}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 ${fullReauth ? '2' : '3'} 步 — 完整 OAuth 重新登录  ⚠️ 浏览器步骤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

在后台运行并捕获输出：
  lark-cli auth login --recommend --no-wait

⚠️ 立即从输出中提取授权 URL，格式类似：
  "Please open the following URL to authorize: https://accounts.feishu.cn/..."

向用户发送此消息：
  "您的飞书 token 已过期，需要重新授权。
   请在浏览器中打开这个链接：
   [粘贴 URL]
   登录飞书并点击"授权"，完成后告诉我。"

用户确认后：
  lark-cli auth status   # 必须显示：已登录为 <用户>

如仍失败（device code 过期）：
  lark-cli auth login --device-code <上面输出中的 DEVICE_CODE>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 ${fullReauth ? '3' : '4'} 步 — 验证并测试推送
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli auth status   # 确认已登录
  lark-cli im +messages-send --chat-id oc_xxx --text "✅ lark-cli 已重新连接 $(date)" --dry-run

  → --dry-run 成功后，去掉 --dry-run 发送真实测试消息（可选）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出 — 更新 data/health-report.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

更新飞书条目：
  "feishu": { "status": "OK", "detail": "已于 <时间戳> 重新认证。Token 有效。" }
`);
}
