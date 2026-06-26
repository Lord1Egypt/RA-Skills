#!/usr/bin/env bash
# ZeeLin Deep Research - 调用 desearch.zeelin.cn API
# 用法: research.sh "研究问题" [deep|major]
# 环境变量: DESEARCH_API_KEY

set -euo pipefail
BASE_URL="https://desearch.zeelin.cn"
API_KEY="${DESEARCH_API_KEY:-}"

if [[ -z "$API_KEY" ]]; then
  echo "错误: 请设置环境变量 DESEARCH_API_KEY。可前往 https://desearch.zeelin.cn/skill-activity 注册获取。"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "错误: 缺少 node 运行时，无法解析/构造 JSON。请在运行环境中安装 Node.js。"
  exit 1
fi

CONTENT="${1:-}"
THINKING="${2:-major}"

if [[ -z "$CONTENT" ]]; then
  echo "用法: $0 \"研究问题\" [deep|major]"
  echo "  deep  = 深度思考模式（全面分析，非万字报告）"
  echo "  major = 专家模式（深度系统、万字报告），默认"
  exit 1
fi

if [[ "$THINKING" != "deep" && "$THINKING" != "major" ]]; then
  THINKING="major"
fi

# 1) 创建会话（内容经 stdin 传入，避免引号/换行问题）
BODY=$(printf '%s' "$CONTENT" | node -e '
  const fs = require("fs");
  const content = fs.readFileSync(0, "utf8").trim();
  const thinking = process.argv[1];
  process.stdout.write(JSON.stringify({
    sessionId: "",
    content,
    thinking,
    workflow: "",
    needEditChapter: 0,
    moreSettings: {}
  }));
' "$THINKING")
RESP=$(curl -s -X POST "${BASE_URL}/api/conversation/anew" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${API_KEY}" \
  -d "$BODY")

SESSION_ID=$(printf '%s' "$RESP" | node -e '
  const fs = require("fs");
  try {
    const d = JSON.parse(fs.readFileSync(0, "utf8") || "{}");
    const sid = (d.data && d.data.sessionId) || d.sessionId || "";
    process.stdout.write(String(sid));
  } catch (_) {
    process.stdout.write("");
  }
')

if [[ -z "$SESSION_ID" ]]; then
  echo "创建会话失败。响应: $RESP"
  exit 1
fi

# 2) 轮询状态直到完成（status=2）或失败（4）
MAX_WAIT=600
INTERVAL=5
WAITED=0
while [[ $WAITED -lt $MAX_WAIT ]]; do
  STATUS_RESP=$(curl -s -X GET "${BASE_URL}/api/conversation/status?sessionId=${SESSION_ID}" -H "x-api-key: ${API_KEY}")
  STATUS=$(printf '%s' "$STATUS_RESP" | node -e '
    const fs = require("fs");
    try {
      const d = JSON.parse(fs.readFileSync(0, "utf8") || "{}");
      const status = (d.data && d.data.status) || 0;
      process.stdout.write(String(status));
    } catch (_) {
      process.stdout.write("0");
    }
  ')

  case "$STATUS" in
    2) break ;;
    4) echo "任务失败。"; exit 1 ;;
    3) echo "任务已结束。"; break ;;
  esac

  sleep "$INTERVAL"
  WAITED=$((WAITED + INTERVAL))
done

if [[ $WAITED -ge $MAX_WAIT ]]; then
  echo "等待超时，请稍后在网页查看: ${BASE_URL} (sessionId=${SESSION_ID})"
  exit 1
fi

# 3) 获取历史回答
HISTORY=$(curl -s -X GET "${BASE_URL}/api/conversation/history?sessionId=${SESSION_ID}&pageSize=10&pageNo=1" -H "x-api-key: ${API_KEY}")

printf '%s' "$HISTORY" | node -e '
  const fs = require("fs");
  const input = fs.readFileSync(0, "utf8") || "{}";
  let d;
  try { d = JSON.parse(input); } catch (e) {
    console.error("解析回答失败:", e && e.message ? e.message : e);
    process.exit(1);
  }
  const answers = (((d || {}).data || {}).answers) || [];
  if (!Array.isArray(answers) || answers.length === 0) {
    process.stdout.write("暂无回答内容。\\n");
    process.exit(0);
  }
  for (const a of answers) {
    const c = a && a.content ? String(a.content) : "";
    if (c) process.stdout.write(c + "\\n---\\n");
  }
'
