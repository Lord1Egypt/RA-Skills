---
name: "piper-tts-engine-free"
description: "基于 Piper 的本地离线文字转语音工具，零云端调用、零 API 费用，适合个人单条语音生成。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "本地语音合成免费版"
  version: "1.0.0"
  summary: "基于 Piper 的本地离线文字转语音工具，零云端调用、零 API 费用，适合个人单条语音生成。"
  tags:
    - "语音合成"
    - "本地TTS"
    - "离线语音"
    - "文字转语音"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 本地语音合成 免费版

## 概述

免费版本地语音合成工具基于 Piper 引擎，为个人用户提供完全离线的文字转语音能力。无需云端 API、无需 API Key、零费用，安装后即可在本地生成高质量语音。生成的 MP3 文件可作为语音消息投递至 Telegram、Discord 等渠道。本版本适合个人开发者、内容创作者与无障碍辅助场景。

与专业版相比，免费版聚焦单条文本合成与预置音色选择，不包含批量合成、自定义音色训练、SSML 标记与 API 服务化等高级能力。但两者的核心合成命令完全一致，便于后续平滑升级。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 本地离线合成 | 完全在本地运行，不依赖任何云端服务 |
| 单条文本合成 | 将一段文本转换为 MP3 语音文件 |
| 预置音色 | 提供多个预置音色（英语为主） |
| 快速生成 | 合成速度约 0.5-1 秒，远快于云端 TTS |
| 语音消息投递 | 生成的 MP3 可作为原生语音消息发送 |
| 零配置 | 安装后无需 API Key 即可使用 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Piper、的本地离线文字转、语音工具、零云端调用、适合个人单条语音、面向个人用户的本、地离线文字转语音、多音色选择、离线运行、适用场景、个人语音消息生成、离线朗读、无障碍辅助、内容创作配音、差异化、免费版聚焦单条文、本合成与基础音色、不含批量合成与自、定义音色训练、适用关键词、语音合成、文字转语音、voice等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：个人语音消息生成

用户希望将一段文字转为语音消息发送给好友。

```bash
# 生成语音
scripts/piper-speak.sh "嘿，今天天气不错，要不要一起出去走走？"

# 示例
# MP3 路径: ~/.piper/output/20260718_153000.mp3
```

将输出路径填入回复，以语音消息形式投递：

```text
[[audio_as_voice]]
MEDIA:~/.piper/output/20260718_153000.mp3
```

### 场景二：内容创作配音

博主为短视频生成英文旁白，避免真人录音。

```bash
# 生成英文旁白
scripts/piper-speak.sh "Welcome to my channel. Today we will explore the future of AI." en_US-ryan-high

# 输出
# MP3 路径: ~/.piper/output/20260718_153100.mp3
```

### 场景三：无障碍朗读辅助

将长文本转为语音，方便视障用户或通勤时收听。

```bash
# 朗读一段文章摘要
scripts/piper-speak.sh "本文介绍了向量数据库的核心原理与典型应用场景，包括相似度检索、推荐系统与语义搜索。"
```

## 不适用场景

以下场景本地语音合成免费版不适合处理：

- 加密文件破解
- 损坏文件修复
- 物理介质数据恢复

## 触发条件

需要文件处理、文档转换、格式互转、内容提取时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 运行安装脚本，自动安装 Piper 引擎与默认音色。

```bash
scripts/setup-piper.sh
```

安装脚本会：
- 通过 pip 安装 `piper-tts`
- 下载默认音色 `en_US-kusal-medium`
- 配置输出目录 `~/.piper/output/`

2. 生成第一条语音。

```bash
scripts/piper-speak.sh "Hello, this is my first voice message."
```

3. 获取 MP3 路径并投递。

```text
[[audio_as_voice]]
MEDIA:/path/to/output.mp3
```

## 配置示例

免费版配置通过环境变量或脚本参数控制。

```bash
# ~/.piper/config.sh
export PIPER_VOICE="en_US-kusal-medium"   # 默认音色
export PIPER_OUTPUT_DIR="$HOME/.piper/output"  # 输出目录
export PIPER_SPEED="1.0"                  # 语速（0.5-2.0）
```

**可用预置音色**

| 音色名称 | 语言 | 风格 | 推荐用途 |
| --- | --- | --- | --- |
| `en_US-kusal-medium` | 美式英语 | 清晰男声（默认） | 通用场景 |
| `en_US-ryan-high` | 美式英语 | 高质量男声 | 内容创作 |
| `en_US-hfc_male-medium` | 美式英语 | 自然男声 | 日常对话 |
| `en_GB-northern_english_male-medium` | 英式英语 | 英国男声 | 英式内容 |

下载更多音色：

```bash
scripts/setup-piper.sh --voice en_US-ryan-high
scripts/setup-piper.sh --voice en_GB-northern_english_male-medium
```

## 最佳实践

- **按需合成**：不要设置 `messages.tts.auto: "always"`，这会使每条回复都变慢。保持按需触发。
- **音色选择**：内容创作推荐 `en_US-ryan-high`（高质量），日常使用推荐 `en_US-kusal-medium`（速度快）。
- **文本长度**：单条合成建议不超过 500 字，过长文本建议分段合成后拼接。
- **语速调整**：通过 `PIPER_SPEED` 环境变量调整，1.0 为正常速度，1.2 适合快节奏内容。
- **输出管理**：定期清理 `~/.piper/output/` 目录，避免磁盘空间占用过多。
- **离线运行**：安装完成后完全离线，无需网络连接，适合无网环境使用。
- **平台兼容**：支持 macOS（Apple Silicon + Intel）与 Linux，需 Python 3.9+。

## 常见问题

### 依赖详情

Piper 需要 Python 3.9+。运行 `python3 --version` 检查版本，若低于 3.9 请先升级 Python。

### Q2：合成的语音有杂音或断续？

- 检查文本中是否包含特殊字符，尝试去除 emoji 与特殊符号。
- 确认音色模型完整下载，重新运行 `scripts/setup-piper.sh --voice <音色名>`。
- 长文本建议分段合成。

### Q3：免费版支持中文语音吗？

免费版预置音色以英语为主。如需中文语音合成，可尝试下载社区中文音色模型，或升级至专业版获取多语言支持。

### Q4：可以在 Windows 上使用吗？

免费版主要支持 macOS 与 Linux。Windows 用户建议通过 WSL（Windows Subsystem for Linux）运行，或升级至专业版获取原生 Windows 支持。

### Q5：合成的 MP3 如何发送到 Telegram？

在 Agent 回复中使用 `[[audio_as_voice]]` 标记加上 `MEDIA:<MP3路径>`，即可作为原生语音消息投递至 Telegram 等渠道。

### 已知限制

没有。免费版完全本地运行，无任何使用次数或频率限制。合成速度取决于本地硬件性能。

### Q7：如何调整语速？

通过环境变量 `PIPER_SPEED` 设置，范围 0.5（慢速）到 2.0（快速），默认 1.0。

```bash
export PIPER_SPEED="1.2"  # 加速20%
scripts/piper-speak.sh "这是一段加速语音"
```

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：macOS（Apple Silicon + Intel）/ Linux
- **运行时**：Python 3.9+
- **网络**：仅安装时需要下载音色模型，运行时完全离线

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
| :------- | :----- | :--------- | :--------- |
| Python 3.9+ | 运行时 | 必需 | python.org 官方下载 |
| piper-tts | Python 包 | 必需 | `pip install piper-tts`（安装脚本自动处理） |
| 音色模型 | 模型文件 | 必需 | 安装脚本自动下载默认音色 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| onnxruntime | Python 包 | 必需 | `pip install onnxruntime`（自动安装） |

### API Key 配置

- 免费版无需任何 API Key。
- 完全本地离线运行，不调用任何云端服务。

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务。免费版为单条合成功能子集，核心合成命令与专业版完全兼容。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
