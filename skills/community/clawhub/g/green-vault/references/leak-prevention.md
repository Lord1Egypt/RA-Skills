# Leak Prevention — 泄露防护

> 源自 OpenClaw/Bagman，适配 Green Vault 安全模块。

## 概述

三层防护体系：输出净化 → Pre-commit Hook → .gitignore 兜底。

---

## 1. 输出净化

所有 Agent 输出（聊天、日志、文件写入）在发送前必须扫描密钥模式：

```python
import re

KEY_PATTERNS = [
    r'0x[a-fA-F0-9]{64}',                    # ETH 私钥
    r'sk-[a-zA-Z0-9]{48,}',                  # OpenAI 密钥
    r'sk-ant-[a-zA-Z0-9\-_]{80,}',           # Anthropic 密钥
    r'gsk_[a-zA-Z0-9]{48,}',                 # Groq 密钥
    r'hf_[a-zA-Z0-9]{30,}',                  # HuggingFace token
    r'AKIA[0-9A-Z]{16}',                     # AWS Access Key
    r'[A-Za-z0-9+/]{40,}={0,2}',             # Base64 可疑长串
]

def sanitize_output(text: str) -> str:
    """从输出中移除潜在密钥。"""
    for pattern in KEY_PATTERNS:
        text = re.sub(pattern, '[REDACTED]', text)
    return text

# 在所有输出通道应用
def send_message(content: str):
    content = sanitize_output(content)
    # ... 发送到聊天/日志/文件
```

## 2. Pre-commit Hook

安装到 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
PATTERNS=(
    '0x[a-fA-F0-9]{64}'
    'sk-[a-zA-Z0-9]{48,}'
    'sk-ant-api'
    'PRIVATE_KEY='
    'gsk_[a-zA-Z0-9]{48,}'
    'hf_[a-zA-Z0-9]{30,}'
    'AKIA[0-9A-Z]{16}'
)

for pattern in "${PATTERNS[@]}"; do
    if git diff --cached | grep -qE "$pattern"; then
        echo "❌ Potential secret detected matching: $pattern"
        echo "   Remove secrets before committing!"
        exit 1
    fi
done

echo "✅ No secrets detected in staged changes."
```

## 3. .gitignore 必备项

```gitignore
# 密钥文件
.env
.env.*
*.pem
*.key
secrets/
credentials/

# Agent 状态（可能包含密钥）
memory/*.json
wallet-state.json
session-keys/

# 1Password 模板输出
*.1pux
```

## 4. 常见泄露场景与修复

### 4.1 记忆文件中的密钥

```markdown
# ❌ BAD — memory/2026-03-23.md
## Wallet
- Private key: 0x9f01dad551039daad3a8c4e43a...

# ✅ GOOD — 只存引用
## Wallet
- Private key: [1Password: agent-session-20260323]
```

### 4.2 .env.example 中的真实密钥

```bash
# ❌ BAD
PRIVATE_KEY=sk-ant-api03-real-key-here

# ✅ GOOD
PRIVATE_KEY=your-key-here
```

### 4.3 错误消息中的密钥

```python
# ❌ BAD
logger.error(f"Failed with key {private_key}: {e}")

# ✅ GOOD
logger.error(f"Key operation failed: {e}")
```

### 4.4 测试代码中的硬编码密钥

```python
# ❌ BAD
TEST_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# ✅ GOOD — 使用环境变量或测试 vault
TEST_KEY = os.environ.get("TEST_SESSION_KEY", "")
```
