---
name: giggle-generation-music
description: "当用户希望创建、生成或创作音乐时使用此技能——无论是文字描述、自定义歌词，还是纯乐器背景音乐。触发词：生成音乐、写歌、创作歌曲、制作音乐、做一首歌、AI 音乐、背景音乐、为我作曲、带歌词的音乐、纯音乐、做 beats。"
version: "0.0.10"
license: MIT
author: storyclaw-official
homepage: https://github.com/storyclaw-official/storyclaw-skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins: [python3]
      env: [GIGGLE_API_KEY]
      pip: [requests]
    primaryEnv: GIGGLE_API_KEY
---

简体中文 | [English](./SKILL.md)

# Giggle 音乐

**来源**：[storyclaw-official/storyclaw-skills](https://github.com/storyclaw-official/storyclaw-skills) · API：[giggle.pro](https://giggle.pro/)

通过 giggle.pro 平台生成 AI 音乐。支持简化模式和自定义模式。提交任务 → 需要时查询。无轮询、无 Cron。

**API Key**：设置系统环境变量 `GIGGLE_API_KEY`。登录 [Giggle.pro](https://giggle.pro/) 在账号设置中获取 API Key。

> **重要**：**切勿**在 exec 的 `env` 参数中传递 `GIGGLE_API_KEY`。API Key 从系统环境变量读取。

> **报错禁止重试**：调用脚本如果出现报错，**禁止重试**。直接将错误信息报告给用户并停止执行。

---

## 交互指引

### 模式选择（优先级从高到低）

| 用户输入 | 模式 | 说明 |
|------------|------|-------|
| 用户提供完整**歌词文本** | 自定义模式 (B) | 必须是歌词，而非描述 |
| 用户要求纯音乐/背景音乐 | 纯音乐模式 (C) | 无人声 |
| 其他情况（描述、风格、人声等） | **简化模式 (A)** | 将用户描述原样作为 prompt，AI 作曲 |

> **关键规则**：若用户未提供歌词，始终使用**简化模式 A**。将用户描述原样作为 `--prompt`；**不要补充或改写**。例如用户说「女声、1 分钟、古风爱情」，则直接使用 `--prompt "女声，1 分钟，古风爱情"`。

### 信息不足时的引导

仅当用户输入非常模糊时（例如只说「生成音乐」无任何描述），可询问：

```
问题：「您想生成什么类型的音乐？」
选项：AI 作曲（描述风格）/ 使用我的歌词 / 纯音乐
```

---

## 执行流程：提交与查询

音乐生成为异步（通常 1–3 分钟）。**提交**任务获取 `task_id`，用户询问时再**查询**状态。

---

### 步骤 1：提交任务

**先向用户发送消息**：「音乐已提交，通常需要 1–3 分钟。您可以随时问我进度。」

#### A：简化模式
```bash
python3 scripts/giggle_music_api.py --prompt "用户描述"
```

#### B：自定义模式
```bash
python3 scripts/giggle_music_api.py --custom \
  --prompt "歌词内容" \
  --style "pop, ballad" \
  --title "歌曲标题" \
  --vocal-gender female
```

#### C：纯音乐
```bash
python3 scripts/giggle_music_api.py --prompt "用户描述" --instrumental
```

响应示例：
```json
{"status": "started", "task_id": "xxx"}
```

**将 task_id 存入记忆**（`addMemory`）：
```
giggle-generation-music task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### 步骤 2：用户询问时查询

当用户询问音乐进度时（如「音乐好了吗？」「进度怎样？」），执行：

```bash
python3 scripts/giggle_music_api.py --query --task-id <task_id>
```

**输出处理**：

| stdout 模式 | 动作 |
|-------------|------|
| 含音乐链接的纯文本（🎶 音乐已就绪） | 原样转发给用户 |
| 含错误的纯文本 | 原样转发给用户 |
| JSON `{"status": "processing", "task_id": "..."}` | 告知用户「进行中，请稍后再问」 |

**链接返回规范**：stdout 中的音频链接必须为**完整签名 URL**（含 Policy、Key-Pair-Id、Signature 等查询参数）。转发时保持原样。

---

## 恢复

当用户询问之前的音乐进度时：

1. **记忆中有 task_id** → 直接执行 `--query --task-id xxx`，**切勿重新提交**
2. **记忆中无 task_id** → 告知用户，询问是否要重新生成

---

## 参数速查

| 参数 | 说明 |
|-----------|-------------|
| `--prompt` | 音乐描述或歌词（简化模式必填） |
| `--custom` | 启用自定义模式 |
| `--style` | 音乐风格（自定义模式必填） |
| `--title` | 歌曲标题（自定义模式必填） |
| `--instrumental` | 生成纯音乐 |
| `--vocal-gender` | 人声性别：male / female（仅自定义模式） |
| `--query` | 查询任务状态 |
| `--task-id` | 任务 ID（与 --query 配合使用） |
