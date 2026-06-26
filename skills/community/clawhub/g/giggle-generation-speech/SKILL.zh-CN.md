---
name: giggle-generation-speech
description: "当用户希望生成语音、配音或文字转音频时使用此技能。通过 Giggle.pro 文转音 API 将文本合成为 AI 语音。触发词：生成语音、文转音、文字转语音、配音、TTS、朗读这段文字、把这段文字读出来、合成语音、我需要一段配音。"
version: "0.0.10"
license: MIT
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": {
          "bins": ["python3"],
          "env": ["GIGGLE_API_KEY"],
          "pip": ["requests"]
        },
        "primaryEnv": "GIGGLE_API_KEY",
        "runtimeBehaviors": {
          "writes": ["~/.openclaw/skills/giggle-generation-speech/logs/"],
          "cron": "用户发起语音生成时注册轮询任务（30秒间隔）"
        }
      }
  }
---

简体中文 | [English](./SKILL.md)

# 文转音（Text-to-Audio）

通过 giggle.pro 平台将文本合成为 AI 语音/配音。支持多种音色、情绪和语速。

## ⚠️ 安装前请阅读

**安装前请确认以下内容。** 本技能将：

1. **写入** `~/.openclaw/skills/giggle-generation-speech/logs/` – 任务状态文件，用于 Cron 去重
2. **注册 Cron**（30 秒间隔） – 用户发起语音生成时的异步轮询；任务完成后移除
3. **原样转发 stdout** – 脚本输出（音频链接、状态）直接呈现给用户

**依赖要求**：`python3`、`GIGGLE_API_KEY`（系统环境变量）、pip 包：`requests`

---

**API Key**：设置系统环境变量 `GIGGLE_API_KEY`。若未配置，脚本会提示配置。

> **禁止内联 Python**：所有命令必须通过 `exec` 工具直接执行。**切勿**使用 heredoc 内联代码。

> **报错禁止重试**：调用脚本如果出现报错，**禁止重试**。直接将错误信息报告给用户并停止执行。

## 执行流程（阶段 1 提交 + 阶段 2 Cron + 阶段 3 同步兜底）

语音生成通常需要 10–30 秒。采用「快速提交 + Cron 轮询 + 同步兜底」三阶段架构。

> **重要**：**切勿**在 exec 的 `env` 参数中传递 `GIGGLE_API_KEY`。API Key 从系统环境变量读取。

---

### 阶段 0：引导用户选择音色与情绪（必须）

**在提交任务前，必须先引导用户选择音色和情绪，不要使用默认值。**

1. 执行 `--list-voices` 获取可用音色列表：

```bash
python3 scripts/text_to_audio_api.py --list-voices
```

2. 将音色列表以易读的方式展示给用户（包含 voice_id、name、style、gender 等信息），引导用户选择一个音色
3. 询问用户期望的情绪（如 joy、sad、neutral、angry、surprise 等），如用户无特殊要求可选 neutral
4. 用户确认音色和情绪后，再进入阶段 1 提交任务

---

### 阶段 1：提交任务（exec 在 10 秒内完成）

**先向用户发送消息**：「语音生成进行中，通常需要 10–30 秒，结果将自动发送。」

```bash
# 必须指定用户选择的音色和情绪
python3 scripts/text_to_audio_api.py \
  --text "今天天气真好" \
  --voice-id "Calm_Woman" \
  --emotion "joy" \
  --speed 1.2 \
  --no-wait --json

# 查看可用音色列表
python3 scripts/text_to_audio_api.py --list-voices
```

响应示例：

```json
{"status": "started", "task_id": "xxx"}
```

**立即将 task_id 存入记忆**（`addMemory`）：

```
giggle-generation-speech task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### 阶段 2：注册 Cron（30 秒间隔）

使用 `cron` 工具注册轮询任务。**必须严格遵循参数格式**：

```json
{
  "action": "add",
  "job": {
    "name": "giggle-generation-speech-<task_id 前 8 位>",
    "schedule": {
      "kind": "every",
      "everyMs": 30000
    },
    "payload": {
      "kind": "systemEvent",
      "text": "语音任务轮询：执行 exec python3 scripts/text_to_audio_api.py --query --task-id <完整 task_id>，按 Cron 逻辑处理 stdout。若 stdout 为非 JSON 纯文本，发送给用户并移除 Cron。若 stdout 为 JSON，不发送消息，继续等待。若 stdout 为空，立即移除 Cron。"
    },
    "sessionTarget": "main"
  }
}
```

**Cron 触发处理**（根据 exec stdout 判断）：

| stdout 模式 | 动作 |
|------------|------|
| 非空纯文本（不以 `{` 开头） | **原样转发给用户**，**移除 Cron** |
| stdout 为空 | 已推送，**立即移除 Cron，不发送消息** |
| JSON（以 `{` 开头，含 `"status"` 字段） | 不发送消息，不移除 Cron，继续等待 |

---

### 阶段 3：同步等待（乐观路径，Cron 未触发时的兜底）

**无论 Cron 是否注册成功，都必须执行此步骤。**

```bash
python3 scripts/text_to_audio_api.py --query --task-id <task_id> --poll --max-wait 120
```

**处理逻辑**：

- 返回纯文本（语音就绪/失败消息） → **原样转发给用户**，移除 Cron
- stdout 为空 → Cron 已推送，移除 Cron，不发送消息
- exec 超时 → Cron 继续轮询

---

## 查看声音列表

当用户想查看可用音色时，执行：

```bash
python3 scripts/text_to_audio_api.py --list-voices
```

脚本会调用 `GET /api/v1/project/preset_tones`，将返回的 `voice_id`、`name`、`style`、`gender`、`age`、`language` 等字段展示给用户，方便用户选择。

---

## 链接返回规范

返回给用户的音频链接必须为**完整签名 URL**（含 Policy、Key-Pair-Id、Signature 等查询参数）。正确示例：`https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`。错误：不要返回仅含基础路径的未签名 URL（无查询参数）。脚本已自动处理 `~` 编码为 `%7E`，转发时保持原样。

---

## 新请求 vs 查询旧任务

**当用户发起新的语音生成请求**时，**必须执行阶段 1 提交新任务**，不要复用记忆中的旧 task_id。

**仅当用户明确询问之前任务的进度**时，才从记忆中查询旧 task_id。

---

## 参数速查

| 参数 | 必填 | 默认值 | 说明 |
|-----|------|--------|------|
| `--text` | 是 | - | 要合成的文本内容 |
| `--voice-id` | 是 | - | 音色 ID，必须通过 `--list-voices` 获取并引导用户选择 |
| `--emotion` | 是 | - | 情绪，如 joy、sad、neutral、angry、surprise 等，需引导用户选择 |
| `--speed` | 否 | 1 | 语速倍率 |
| `--list-voices` | - | - | 获取可用音色列表 |
| `--query` | - | - | 查询任务状态 |
| `--task-id` | 查询时必填 | - | 任务 ID |
| `--poll` | 否 | - | 配合 `--query` 同步轮询等待 |
| `--max-wait` | 否 | 120 | 最长等待秒数 |

---

## 交互引导

**每次生成语音前，必须完成以下交互**：

1. 若用户未提供文本，询问：「您想把哪段文字转换成语音？」
2. **必须引导用户选择音色**：执行 `--list-voices` 获取音色列表，展示给用户并让用户选择，**不要使用默认音色**
3. **必须引导用户选择情绪**：询问用户期望的情绪风格（如 joy、sad、neutral、angry、surprise 等）
4. 用户确认文本、音色、情绪后，再执行阶段 1 提交 → 阶段 2 注册 Cron → 阶段 3 同步等待
