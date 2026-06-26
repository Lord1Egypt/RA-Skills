# 集成指南 - 方案 A（Agent 层拦截）

## 概述

本方案通过在 Agent 回复生成后、发送前进行隐私检查，实现多用户隐私保护。

## 架构

```
┌─────────────────┐
│  Agent 生成回复  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ pre-send-check  │ ← 调用 privacy-guard.js check
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────┐
│ PASS │  │BLOCK │
└──┬───┘  └──┬───┘
   │         │
   │         ▼
   │   ┌─────────────┐
   │   │ auto-rewrite│ ← 尝试自动重写
   │   └──────┬──────┘
   │          │
   │     ┌────┴────┐
   │     │         │
   │     ▼         ▼
   │  ┌─────┐  ┌────────┐
   │  │ OK  │  │ 人工   │
   │  └──┬──┘  │ 审查   │
   │     │     └───┬────┘
   │     │         │
   ▼     ▼         ▼
┌────────────────────────┐
│    发送消息 + 记录日志   │
└────────────────────────┘
```

## 使用方式

### 方式 1: 手动调用（测试用）

```bash
# 检查消息
bash ~/.openclaw/skills/multi-user-privacy/scripts/pre-send-check.sh \
  "你好，有什么可以帮你的？" \
  "ou_f5618661cbdcc6f3abb79571db7ec604"

# 自动重写
node ~/.openclaw/skills/multi-user-privacy/scripts/auto-rewrite.js rewrite \
  "老刘的账号是 ou_b96f5424607baf3a0455b55e0f4a2213" \
  "ou_f5618661cbdcc6f3abb79571db7ec604"
```

### 方式 2: 集成到 Agent 工作流（推荐）

在 Agent 每次发送消息前，自动执行以下流程：

```bash
#!/bin/bash
# 发送前检查脚本

MESSAGE="$1"
USER_ID="$2"

# 运行检查
RESULT=$(bash ~/.openclaw/skills/multi-user-privacy/scripts/pre-send-check.sh "$MESSAGE" "$USER_ID")
STATUS=$?

if [ $STATUS -eq 0 ]; then
  # 检查通过，发送原消息
  echo "$MESSAGE"
else
  # 检查失败，尝试重写
  REWRITE=$(node ~/.openclaw/skills/multi-user-privacy/scripts/auto-rewrite.js rewrite "$MESSAGE" "$USER_ID")
  REWRITE_STATUS=$?
  
  if [ $REWRITE_STATUS -eq 0 ]; then
    # 重写成功，发送重写后的消息
    echo "$REWRITE" | node -e "const d=JSON.parse(require('fs').readFileSync(0)); console.log(d.rewritten)"
  else
    # 重写失败，需要人工审查
    echo "⚠️ 消息无法自动重写，请人工审查"
    exit 1
  fi
fi
```

### 方式 3: 在 OpenClaw 中自动加载（当前实现）

**步骤：**

1. **在 TOOLS.md 中添加强制规则**（已做）

2. **创建隐私规则提示词** - 在每次对话前加载

3. **自检流程** - Agent 在发送前自我检查

## 审计日志

所有检查记录在 `~/.openclaw/workspace/memory/privacy-audit.log`

```bash
# 查看最近的检查记录
tail -20 ~/.openclaw/workspace/memory/privacy-audit.log

# 查看违规记录
grep "Blocked: true" ~/.openclaw/workspace/memory/privacy-audit.log
```

## 测试用例

### 测试 1: 正常消息（应通过）

```bash
bash pre-send-check.sh "你好，有什么可以帮你的？" "ou_f5618661cbdcc6f3abb79571db7ec604"
# 预期：✅ PASS
```

### 测试 2: 泄露账号 ID（应拦截并重写）

```bash
bash pre-send-check.sh "老刘的账号是 ou_b96f5424607baf3a0455b55e0f4a2213" "ou_f5618661cbdcc6f3abb79571db7ec604"
# 预期：❌ BLOCKED
# 重写后："[管理员] 的账号是 [管理员]"
```

### 测试 3: 提及其他用户（应拦截）

```bash
bash pre-send-check.sh "蟹老板也问过这个问题" "ou_b96f5424607baf3a0455b55e0f4a2213"
# 预期：❌ BLOCKED（对老刘可以，对其他用户不行）
```

## 当前限制

1. **依赖 Agent 自觉遵守** - 如果 Agent 绕过检查，无法拦截
2. **需要手动调用** - 目前没有自动钩子集成到 OpenClaw 核心
3. **重写可能改变语义** - 自动重写可能影响消息原意

## 未来改进

- [ ] 集成到 OpenClaw `message` 工具（方案 B）
- [ ] 添加 Web UI 审查界面
- [ ] 支持自定义重写规则
- [ ] 添加实时通知（违规时通知管理员）
