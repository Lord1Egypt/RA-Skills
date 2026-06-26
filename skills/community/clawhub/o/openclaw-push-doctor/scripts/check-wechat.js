#!/usr/bin/env node
/**
 * openclaw-healthcheck — check-wechat.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 *
 * Usage:
 *   node scripts/check-wechat.js
 *   node scripts/check-wechat.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — WeChat Bridge Status ===

Run the following checks:

  # Check for WeChat bridge process
  pgrep -f "wechat|wx-bridge|wechaty" 2>/dev/null && echo "BRIDGE_RUNNING" || echo "BRIDGE_DOWN"

  # Check session file
  test -f ~/.openclaw/wechat/session.json && echo "SESSION_EXISTS" || echo "NO_SESSION"

  # Check openclaw wechat config
  cat ~/.openclaw/wechat/config.json 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "NO_CONFIG"

Interpret results:
  → BRIDGE_DOWN + NO_SESSION   wechat: NOT_CONFIGURED
  → BRIDGE_DOWN + SESSION_EXISTS  wechat: BRIDGE_DOWN — restart bridge manually
  → BRIDGE_RUNNING             wechat: OK (verify by checking recent message log)

If BRIDGE_DOWN and session exists:
  Tell user: "WeChat bridge is down. Restart it with your usual startup command,
  or re-scan the QR code if the session has expired."

Output:
  "wechat": { "status": "OK | BRIDGE_DOWN | NOT_CONFIGURED", "detail": "..." }
`);
} else {
  console.log(`=== openclaw-healthcheck — 微信 Bridge 状态检查 ===

运行以下检查：

  # 检查微信 bridge 进程
  pgrep -f "wechat|wx-bridge|wechaty" 2>/dev/null && echo "BRIDGE_RUNNING" || echo "BRIDGE_DOWN"

  # 检查 session 文件
  test -f ~/.openclaw/wechat/session.json && echo "SESSION_EXISTS" || echo "NO_SESSION"

  # 检查 openclaw 微信配置
  cat ~/.openclaw/wechat/config.json 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "NO_CONFIG"

结果判断：
  → BRIDGE_DOWN + NO_SESSION      wechat: NOT_CONFIGURED
  → BRIDGE_DOWN + SESSION_EXISTS  wechat: BRIDGE_DOWN — 手动重启 bridge
  → BRIDGE_RUNNING                wechat: OK（通过检查最近消息日志确认）

如 BRIDGE_DOWN 且 session 存在：
  告知用户："微信 bridge 已断开。请用您平时的启动命令重启，
  如果 session 已过期，需要重新扫描二维码。"

输出：
  "wechat": { "status": "OK | BRIDGE_DOWN | NOT_CONFIGURED", "detail": "..." }
`);
}
