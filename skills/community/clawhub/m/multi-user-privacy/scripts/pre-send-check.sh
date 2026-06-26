#!/bin/bash

# Pre-Send Privacy Check - 发送前隐私检查
# 用法：bash pre-send-check.sh "消息内容" "当前用户 ID"

MESSAGE="$1"
CURRENT_USER_ID="$2"
SKILL_DIR="$HOME/.openclaw/skills/multi-user-privacy"
AUDIT_LOG="$HOME/.openclaw/workspace/memory/privacy-audit.log"

# 检查参数
if [ -z "$MESSAGE" ] || [ -z "$CURRENT_USER_ID" ]; then
  echo "ERROR: 缺少参数"
  echo "用法：bash pre-send-check.sh \"消息内容\" \"当前用户 ID\""
  exit 1
fi

# 运行隐私检查
CHECK_RESULT=$(node "$SKILL_DIR/privacy-guard.js" check "$MESSAGE" "$CURRENT_USER_ID" 2>&1)
CHECK_EXIT=$?

# 解析结果
PASSED=$(echo "$CHECK_RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(d.passed)")
BLOCKED=$(echo "$CHECK_RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(d.blocked)")

# 记录审计日志
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] User: $CURRENT_USER_ID | Passed: $PASSED | Blocked: $BLOCKED" >> "$AUDIT_LOG"

if [ "$PASSED" = "true" ]; then
  echo "✅ PASS"
  echo "$MESSAGE"
  exit 0
else
  echo "❌ BLOCKED"
  echo "原因:"
  echo "$CHECK_RESULT" | node -e "
    const d = JSON.parse(require('fs').readFileSync(0, 'utf8'));
    d.issues.forEach(i => console.log('  - ' + i.message));
  "
  
  # 记录详细信息
  echo "  Issues:" >> "$AUDIT_LOG"
  echo "$CHECK_RESULT" | node -e "
    const d = JSON.parse(require('fs').readFileSync(0, 'utf8'));
    d.issues.forEach(i => console.log('    - ' + i.type + ': ' + i.value));
  " >> "$AUDIT_LOG"
  
  exit 1
fi
