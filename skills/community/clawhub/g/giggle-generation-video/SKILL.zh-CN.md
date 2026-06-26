---
name: giggle-generation-video
description: "支持文生视频和图生视频（首帧/尾帧）。当用户需要生成视频、制作短视频、文字转视频时使用。使用场景：(1) 根据文字描述生成视频，(2) 使用参考图作为首帧/尾帧生成视频，(3) 自定义模型、画幅比例、时长、分辨率。触发词：生成视频、文生视频、图生视频、AI 视频、text-to-video、image-to-video。"
version: "0.0.10"
license: MIT
author: giggle-official
homepage: https://github.com/giggle-official/skills
repository: https://github.com/giggle-official/skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      },
      "primaryEnv": "GIGGLE_API_KEY",
      "installSpec": {
        "bins": ["python3"],
        "env": ["GIGGLE_API_KEY"],
        "pip": ["requests"]
      }
    }
  }
---

简体中文 | [English](./SKILL.md)

# Giggle 视频生成

**来源**：[giggle-official/skills](https://github.com/giggle-official/skills) · API：[giggle.pro](https://giggle.pro/)

通过 giggle.pro 平台的 Generation API 生成 AI 视频，支持文生视频和图生视频。提交任务 → 需要时查询。无轮询、无 Cron、无文件写入，所有操作通过 exec 执行。

---

## 安装要求

| 要求 | 值 |
|------|-----|
| **二进制** | `python3` |
| **环境变量** | `GIGGLE_API_KEY`（必填；可从 https://giggle.pro/ 获取） |
| **Pip** | `requests` |

使用前请设置 `GIGGLE_API_KEY`。若未配置，脚本会提示配置。

**API Key**：设置系统环境变量 `GIGGLE_API_KEY`。若未配置，脚本会提示配置。

> **报错禁止重试**：调用脚本如果出现报错，**禁止重试**。直接将错误信息报告给用户并停止执行。

---

## 支持的模型

| 模型                      | 支持时长（秒）  | 默认时长 | 说明                  |
| ----------------------- | -------- | ---- | ------------------- |
| grok                    | 6, 10    | 6    | 综合能力强，推荐            |
| grok-fast               | 6, 10    | 6    | grok 快速版            |
| sora2                   | 4, 8, 12 | 4    | OpenAI Sora 2       |
| sora2-pro               | 4, 8, 12 | 4    | Sora 2 Pro 版        |
| sora2-fast              | 10, 15   | 10   | Sora 2 快速版          |
| sora2-pro-fast          | 10, 15   | 10   | Sora 2 Pro 快速版      |
| kling25                 | 5, 10    | 5    | 快影视频模型              |
| seedance15-pro          | 4, 8, 12 | 4    | Seedance Pro（含音频）   |
| seedance15-pro-no-audio | 4, 8, 12 | 4    | Seedance Pro（无音频）   |
| veo31                   | 4, 6, 8  | 4    | Google Veo 3.1（含音频） |
| veo31-no-audio          | 4, 6, 8  | 4    | Google Veo 3.1（无音频） |
| minimax23               | 6        | 6    | MiniMax 模型          |
| wan25                   | 5, 10    | 0    | 万象模型                |

**注意**：`--duration` 必须从对应模型的「支持时长」中选择，否则 API 会报错。

---

## 帧引用方式（图生视频）

图生视频的 `--start-frame` 和 `--end-frame` 支持三种互斥方式：

| 方式       | 格式              | 示例                                |
| -------- | --------------- | --------------------------------- |
| asset_id | `asset_id:<ID>` | `asset_id:lkllv0yv81`             |
| url      | `url:<URL>`     | `url:https://example.com/img.jpg` |
| base64   | `base64:<DATA>` | `base64:iVBORw0KGgo...`           |

每个帧参数只能选择其中一种方式。

---

## 执行流程：提交与查询

视频生成为异步（通常 60–300 秒）。**提交**任务获取 `task_id`，用户询问时再**查询**状态。所有命令通过 `exec` 执行；API Key 从系统环境变量读取。

---

### 步骤 1：提交任务

**先向用户发送消息**：「视频已提交，通常需要 1–5 分钟。您可以随时问我进度。」

```bash
# 文生视频（默认 grok-fast）
python3 scripts/generation_api.py \
  --prompt "相机缓缓向前推进，人物在画面中微笑" \
  --model grok-fast --duration 6 \
  --aspect-ratio 16:9 --resolution 720p

# 图生视频 - 使用 asset_id 作为首帧
python3 scripts/generation_api.py \
  --prompt "人物缓缓转身" \
  --start-frame "asset_id:lkllv0yv81" \
  --model grok-fast --duration 6 \
  --aspect-ratio 16:9 --resolution 720p

# 图生视频 - 使用 URL 作为首帧
python3 scripts/generation_api.py \
  --prompt "风景从静止到运动" \
  --start-frame "url:https://example.com/img.jpg" \
  --model grok-fast --duration 6

# 图生视频 - 同时指定首帧和尾帧
python3 scripts/generation_api.py \
  --prompt "场景过渡" \
  --start-frame "asset_id:abc123" \
  --end-frame "url:https://example.com/end.jpg" \
  --model grok --duration 6
```

响应示例：
```json
{"status": "started", "task_id": "55bf24ca-e92a-4d9b-a172-8f585a7c5969"}
```

**将 task_id 存入记忆**（`addMemory`）：
```
giggle-generation-video task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### 步骤 2：用户询问时查询

当用户询问视频进度时（如「视频好了吗？」「进度怎样？」），执行：

```bash
python3 scripts/generation_api.py --query --task-id <task_id>
```

**输出处理**：

| stdout 模式 | 动作 |
|-------------|------|
| 含视频链接的纯文本（视频已就绪） | 原样转发给用户 |
| 含错误的纯文本 | 原样转发给用户 |
| JSON `{"status": "processing", "task_id": "..."}` | 告知用户「进行中，请稍后再问」 |

**链接返回规范**：结果中的视频链接必须为**完整签名 URL**。转发时保持原样。

---

## 新请求 vs 查询旧任务

**当用户发起新的视频生成请求**时，**必须执行步骤 1 提交新任务**，不要复用记忆中的旧 task_id。

**仅当用户明确询问之前任务的进度**时，才从记忆中查询旧 task_id。

---

## 参数速查

| 参数               | 默认值  | 说明                                                |
| ---------------- | ---- | ------------------------------------------------- |
| `--prompt`       | 必填   | 视频描述 prompt                                       |
| `--model`        | grok | 见「支持的模型」表                                         |
| `--duration`     | 模型默认 | 必须从模型支持的时长中选择                                     |
| `--aspect-ratio` | 16:9 | 16:9、9:16、1:1、3:4、4:3                             |
| `--resolution`   | 720p | 分辨率：480p、720p、1080p                               |
| `--start-frame`  | -    | 图生视频首帧，格式：`asset_id:ID`、`url:URL` 或 `base64:DATA` |
| `--end-frame`    | -    | 图生视频尾帧，格式同首帧                                      |

注：base64 参数支持 base64 编码图片。请直接传递 Base64 编码字符串，勿添加 data:image/xxx;base64 前缀。

---

## 交互引导流程

**当用户请求较模糊时，按以下步骤引导。若用户已提供足够信息，可直接执行命令。**

### 步骤 1：选择模型（必须）

在生成前，**必须先向用户介绍可用模型**，再让用户选择。展示「支持的模型」表中的模型列表。等待用户明确选择后再继续。

### 步骤 2：视频时长

根据用户选择的模型，展示该模型支持的时长选项让用户选择。默认使用模型的默认时长。

### 步骤 3：生成模式

```
问题：「需要使用参考图片作为首帧/尾帧吗？」
选项：不需要 - 仅文生视频 / 需要 - 图生视频（设置首帧/尾帧）
```

### 步骤 4：画幅比例

```
问题：「需要什么画幅比例？」
选项：16:9 - 横屏（推荐）/ 9:16 - 竖屏 / 1:1 - 方形
```

### 步骤 5：执行并展示

按流程：发送消息 → 步骤 1 提交 → 用户询问 → 步骤 2 查询。将 exec stdout 原样转发给用户。
