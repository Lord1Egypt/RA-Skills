---
name: oc-call
description: 通过 OpenClaw Gateway HTTP API 调用远程 OpenClaw 实例，支持多轮会话保持。
  当用户说"用 oc 回答"、"用 openclaw 回答"、"oc 回答"、或发送 /oc 命令时触发。
  用于调用内网另一台机器（192.168.123.106）上的 OpenClaw 进行问答，保持会话上下文。
---

# OpenClaw HTTP API Call Skill / OpenClaw HTTP API 调用技能

Call a remote OpenClaw instance via its Gateway OpenAI-compatible `/v1/chat/completions` endpoint,
with multi-turn conversation support via `x-openclaw-session-key`.

通过 OpenClaw Gateway 的 OpenAI 兼容端点调用远程 OpenClaw 实例，自动处理多轮会话保持。

## Configuration / 配置

| Variable / 变量 | Default / 默认值 | Description / 说明 |
|----------------|-----------------|-------------------|
| `OC_URL` | `http://192.168.123.106:28789/v1/chat/completions` | Remote Gateway address / 远程 Gateway 地址 |
| `OC_TOKEN` | `87654321` | Auth token / 认证 Token |
| `OC_SESSION_FILE` | `~/.oc_session` | Session key storage path / Session Key 存储路径 |

> **Note / 注意:** Sensitive values (URL, token) should be overridden via environment variables in production.
> 产品环境中请通过环境变量覆盖敏感配置。

## How to Trigger / 触发方式

### Command / 命令
```
/oc 你的问题
```

### Keywords in message / 消息中的关键词
- `用 oc 回答`
- `用 openclaw 回答`
- `oc 回答`

## Session Persistence / 会话保持机制

Only the `x-openclaw-session-key` HTTP header is used — no local history file needed.
The session key is stored in `~/.oc_session` and automatically reused for subsequent calls.

仅依赖 `x-openclaw-session-key` HTTP header 保持会话，无需本地历史文件。
Session Key 存放在 `~/.oc_session`，后续调用自动复用。

## Management Commands / 管理命令

```bash
python oc_call.py /clear   # Clear session (delete session key) / 清除会话
python oc_call.py /new     # Create new session / 新建会话
```

## Script Usage / 脚本调用

```python
import subprocess
result = subprocess.run(
    ["python", "oc_call.py", "Your question here"],
    capture_output=True, text=True,
    cwd="C:\\Users\\an\\.openclaw\\workspace\\skills\\oc-call\\scripts"
)
print(result.stdout)
```
