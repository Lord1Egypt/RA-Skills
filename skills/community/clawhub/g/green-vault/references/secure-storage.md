# Secure Storage — 1Password Integration Patterns

> 源自 OpenClaw/Bagman，适配 Green Vault 安全模块。

## 概述

AI Agent 处理密钥的唯一安全途径是通过专用密钥管理器（如 1Password CLI `op`）在运行时获取凭证，绝不持久化到磁盘。

---

## 1. 创建专用 Vault

```bash
# 为 Agent 创建隔离的 vault
op vault create "Agent-Wallets" --description "AI agent wallet credentials"

# 添加凭证
op item create \
  --vault "Agent-Wallets" \
  --category "API Credential" \
  --title "llm-inference-api-key" \
  --field "api-key[password]=sk-..." \
  --field "service=inference-cluster" \
  --field "expires=2026-06-01T00:00:00Z"
```

## 2. 环境注入模式

创建模板文件 `.env.tpl`（不含实际密钥）：

```bash
# .env.tpl — 模板文件，安全提交到 Git
OPENAI_API_KEY=op://Agent-Wallets/openai-key/api-key
HF_TOKEN=op://Agent-Wallets/hf-token/token
WANDB_API_KEY=op://Agent-Wallets/wandb/api-key
```

运行时注入：

```bash
# 密钥在进程内存中，不落盘
op run --env-file=.env.tpl -- python inference_server.py
```

## 3. Python 集成

```python
import subprocess
import json

def op_read(reference: str) -> str:
    """从 1Password 读取单个值。"""
    result = subprocess.run(
        ["op", "read", reference],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def op_get_item(item_name: str, vault: str = "Agent-Wallets") -> dict:
    """获取完整条目。"""
    result = subprocess.run(
        ["op", "item", "get", item_name, "--vault", vault, "--format", "json"],
        capture_output=True, text=True, check=True
    )
    item = json.loads(result.stdout)
    return {f["label"]: f.get("value") for f in item.get("fields", [])}

# 使用示例
api_key = op_read("op://Agent-Wallets/openai-key/api-key")
```

## 4. 权限最小化

- 每个 Agent 只能访问其专用 vault
- 使用 1Password Service Account 而非个人账户
- 定期轮换 Service Account token
- 启用审计日志监控异常访问
