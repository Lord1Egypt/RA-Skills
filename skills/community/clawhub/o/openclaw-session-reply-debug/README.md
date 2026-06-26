# OpenClaw Session 异常排查、模型切换与多模型备选

本 README 用于处理以下问题：

- 会话中「消息已发送但助手无回复」
- 模型不可用导致的运行失败
- 需要在多个模型间按优先级自动切换（Primary + Fallback）

## 1. 仓库内容

- `SKILL.md`: 会话无回复的排查主流程
- `openclaw-model-connectivity-test.md`: 模型可用性探针手册（切换前后都要跑）
- `scripts/switch-model-to-gpt-5.2.js`: 固定回滚脚本（`gpt-5.3 -> gpt-5.2`）
- `scripts/switch-model-with-fallback.js`: 通用脚本（支持目标模型 + 多备选）

## 1.1 怎么使用这个 skill（教程）

你可以直接用自然语言提需求，不需要先自己拼命令。

例如，你可以这样说：

- `OpenClaw，为我切换到 gpt-5.4，备用 gpt-5.3 和 gpt-5.2。`
- `帮我把主模型设为 gpt-5.4，降级顺序是 gpt-5.3、gpt-5.2。`
- `我希望 heartbeat 自动探测 gpt-5.4，不可用就降级到 gpt-5.3，再不行就 gpt-5.2；恢复后自动切回最高模型。`

上面这类请求，等价于下面这组优先级：

- Primary: `gpt-5.4`
- Fallback 1: `gpt-5.3`
- Fallback 2: `gpt-5.2`

系统最终会使用这条脚本命令来执行切换：

```bash
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

### 这个 skill 会帮你做什么

当你像上面那样提出需求后，这个 skill 的推荐流程是：

1. 检查当前 session / config / logs，确认是不是模型可用性问题
2. 跑 Provider 探针，按优先级检查 `gpt-5.4 -> gpt-5.3 -> gpt-5.2`
3. 选择第一个可用模型
4. 调用现有脚本切换活动模型引用
5. 如果你要接入 heartbeat，就把同一组参数挂到 OpenClaw 的 heartbeat / cron
6. 用同一会话做一次回归验证，确认助手回复非空

### 一个完整例子

用户说：

```text
OpenClaw，为我切换 gpt-5.4，备用 gpt-5.3、gpt-5.2；如果 gpt-5.4 恢复可用，heartbeat 自动切回去。
```

这个 skill 会理解为：

- 首选模型：`gpt-5.4`
- 降级顺序：`gpt-5.3 -> gpt-5.2`
- 切换执行器：`scripts/switch-model-with-fallback.js`
- 定时恢复机制：复用 OpenClaw 自带 `heartbeat / cron`

如果你只是想做紧急回滚，也可以直接说：

- `OpenClaw，先把 gpt-5.3 回滚到 gpt-5.2。`

## 2. 会话异常排查（快速路径）

### 2.1 找到当前 session JSONL

已知 key（示例 `agent:main:main`）：

```bash
rg -n '"agent:main:main"' "$HOME/.openclaw/agents/main/sessions/sessions.json" -S
node -e 'const d=require(process.env.HOME+"/.openclaw/agents/main/sessions/sessions.json"); console.log(d["agent:main:main"])'
```

未知 key：

```bash
ls -lt "$HOME/.openclaw/agents/main/sessions" | head -n 20
tail -n 80 "$HOME/.openclaw/agents/main/sessions/<candidate>.jsonl"
```

### 2.2 检查异常特征

```bash
tail -n 120 "$HOME/.openclaw/agents/main/sessions/<session-id>.jsonl"
```

重点字段：

- `"content":[]`
- `"stopReason":"error"`
- `"errorMessage":"..."`

### 2.3 检查模型引用

```bash
rg -n "openai/gpt-5\\.4|openai/gpt-5\\.3|openai/gpt-5\\.2|\"model\"\s*:\s*\"gpt-5\\.[432]\"" \
  "$HOME/.openclaw/openclaw.json" \
  "$HOME/.openclaw/agents/main/sessions/sessions.json" -S
```

### 2.4 检查运行日志

```bash
rg -n "unknown provider|Unknown provider|api key|embedded run start|agent model" \
  "$HOME/.openclaw/logs/gateway.log" \
  "$HOME/.openclaw/logs/gateway.err.log" \
  "/tmp/openclaw/openclaw-$(date +%F).log" -S
```

## 3. 模型可用性验证（切换前后都必须做）

请按 `openclaw-model-connectivity-test.md` 执行：

- Provider 直连探针
- OpenClaw Agent 端到端探针

只有双探针都通过，才算模型可用。

## 4. 模型切换方案

### 4.1 固定回滚（原有脚本）

适合明确要把 `gpt-5.3` 回滚到 `gpt-5.2`：

```bash
node scripts/switch-model-to-gpt-5.2.js
node scripts/switch-model-to-gpt-5.2.js --apply
```

### 4.2 目标模型 + 多备选（推荐）

新脚本：`scripts/switch-model-with-fallback.js`

能力：

- 指定 `--primary`（目标模型）
- 支持多个 `--fallback`（按顺序降级）
- 默认先做 Provider 探针，自动选第一个可用模型
- 自动将会话/配置中的候选模型引用统一替换为最终选中模型
- 每次重新运行都会从最高优先级重新探测，因此天然支持“高优先级模型恢复后自动切回”
- `--apply` 前自动备份原文件（`.bak.<timestamp>`）

命令格式：

```bash
node scripts/switch-model-with-fallback.js \
  --primary <model> \
  --fallback <model> \
  [--fallback <model> ...] \
  [--provider openai] \
  [--root "$HOME/.openclaw"] \
  [--apply]
```

你的示例（完整）：

```bash
# 先 dry-run
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2

# 再 apply
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

如果你要强制使用 primary（不做可用性探针）：

```bash
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --no-probe \
  --apply
```

### 4.3 通过 OpenClaw heartbeat / cron 做自动降级与自动恢复

这次需求的关键点是：

- **不要自己写常驻心跳服务**
- **复用 OpenClaw 自带 heartbeat / cron**
- **heartbeat 只负责触发**
- **真正的模型选择与切换，直接调用现有 `scripts/switch-model-with-fallback.js`**

推荐链路：

`cron job -> wakeMode: next-heartbeat -> heartbeat -> node scripts/switch-model-with-fallback.js ...`

#### 为什么这能自动恢复到更高优先级模型

因为脚本每次运行都会按以下顺序重新探测：

1. `primary`
2. `fallback 1`
3. `fallback 2`
4. ...

所以如果当前因为故障已经降级到 `gpt-5.2`，后续 heartbeat 再次运行时：

- 只要 `gpt-5.4` 恢复可用，就会直接切回 `gpt-5.4`
- 如果 `gpt-5.4` 不可用但 `gpt-5.3` 可用，就切到 `gpt-5.3`
- 如果都不可用，则保持当前配置不变并报错

#### 任务参数怎么传

本仓库当前稳定支持的是 **CLI 参数契约**，因此 heartbeat 任务参数应直接映射为脚本参数：

- `primary` -> `--primary`
- `fallbacks[]` -> 多次传 `--fallback`
- `provider` -> `--provider`
- `probeTimeoutMs` -> `--probe-timeout-ms`
- `apply=true` -> `--apply`

例如，你想要：

- 主模型：`gpt-5.4`
- 一级降级：`gpt-5.3`
- 二级降级：`gpt-5.2`

heartbeat 最终执行的命令就是：

```bash
node scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

#### 当前 OpenClaw cron 只支持文本 payload 时怎么做

如果你当前的 cron payload 只能传文本，最稳妥的方式是把参数直接展开进命令模板，而不是依赖模糊自然语言解析。

可参考任务文本：

```text
模型心跳巡检：执行 node /absolute/path/to/scripts/switch-model-with-fallback.js --primary gpt-5.4 --fallback gpt-5.3 --fallback gpt-5.2 --apply 。若高优先级模型恢复可用，直接切回最高可用模型；若全部不可用，保持当前模型并汇报错误。
```

#### 推荐的 cron job 形态

本地已可见的 OpenClaw cron 结构通常类似：

```json
{
  "name": "model fallback heartbeat",
  "schedule": { "kind": "every", "everyMs": 600000 },
  "sessionTarget": "main",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "systemEvent",
    "text": "模型心跳巡检：执行 node /absolute/path/to/scripts/switch-model-with-fallback.js --primary gpt-5.4 --fallback gpt-5.3 --fallback gpt-5.2 --apply"
  }
}
```

这里的重点不是 payload 的文案，而是：

- 由 `OpenClaw cron` 负责周期触发
- 由 `heartbeat` 负责接收这次任务
- 由现有 JS 脚本负责真正的探测、降级、回切

## 5. 切换后验证（必须）

在同一会话做回归验证：

```bash
openclaw agent \
  --session-id <session-id> \
  --message "connectivity check: reply OK only" \
  --json \
  --timeout 120
```

成功标准：

- exit code = `0`
- `"status":"ok"`
- assistant 内容非空
- `agentMeta.model` 为你选中的最终模型

## 6. 推荐备选优先级

常用顺序：

1. `openai/gpt-5.4`（Primary）
2. `openai/gpt-5.3`（Fallback 1）
3. `openai/gpt-5.2`（Fallback 2）

建议每次切换都跑双探针，避免仅凭配置判断可用性。

## 7. 当前环境实测（2026-03-06）

- `gpt-5.4`: `OK 200`
- `gpt-5.3`: `ERROR 502 unknown provider for model gpt-5.3`
- `gpt-5.2`: `OK 200`

据此，在当前环境下建议：

- Primary 设为 `gpt-5.4`
- Fallback 至少包含 `gpt-5.2`
- 避免将 `gpt-5.3` 设为唯一可用模型

## 8. 常见误区

- UI 有记录不等于助手回复成功，JSONL + logs 才是准确信号。
- 未做切换后复测就宣称修复，容易复发。
- 只改一个配置文件，不改会话缓存引用，可能导致继续命中旧模型。
