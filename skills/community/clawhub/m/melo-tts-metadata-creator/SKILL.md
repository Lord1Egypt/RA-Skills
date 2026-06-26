---
name: melo-tts-metadata-creator
description: |
  当用户需要为 **MeloTTS** 训练或微调生成 metadata.list 文件时自动触发。
  专门处理 .wav 音频文件和对应的 .txt 转录文本，自动生成符合 MeloTTS 官方最新标准的 metadata.list（格式：音频路径|speaker|语言|文本）。
  支持单音色和多音色模式：
  - wav 和 txt 文件可以放在不同目录（目录结构一致）
  - 多音色时自动按第一级子目录名称提取 speaker
  - 单音色时可用 --speaker 参数强制指定说话人名称
  - 无 txt 文件时可自动调用 Whisper 进行转录（支持 ZH/EN 等语言）
  常见触发口语：
  - “帮我生成 MeloTTS 的 metadata.list”
  - “为 MeloTTS 训练准备 metadata”
  - “把这些 wav 和 txt 生成 metadata.list”
  - “MeloTTS 多音色 metadata”
  - “用 Whisper 转录音频生成 metadata”
  - “MeloTTS 数据集 metadata 生成器”
  - “处理 wav 文件夹生成 MeloTTS 训练文件”
  - “单音色/多音色 metadata.list”
  只处理 MeloTTS 相关的 metadata 生成，其他 TTS 或音频处理一律不触发。
metadata:
  openclaw:
    requires:
      bins:
        - python
    user-invocable: true
---

# melo-tts-metadata-creator

**功能**：专为 **MeloTTS** 训练/微调设计的 metadata.list 生成工具。支持单音色与多音色模式，特别适配 wav 文件和 txt 转录文件位于两个不同目录、每个子目录代表一个说话人的场景。

### 触发时机（Triggers）
- 用户提到 “MeloTTS”“metadata.list”“训练数据准备”“微调数据集”
- 用户有 wav 音频文件夹和对应 txt 转录，需要生成训练所需的 metadata 文件
- 需要自动转录（无 txt 时用 Whisper）
- 想处理多说话人（多音色）数据集

### 核心优势
- 支持 wav 和 txt 分离存放（目录结构完全一致）
- 自动按第一级子目录名称提取 speaker（多音色模式）
- 支持 `--speaker` 参数强制统一说话人（单音色模式）
- 内置 Whisper 自动转录功能（无 txt 时自动生成）
- Whisper 模型下载到 `./models/` 目录
- 生成完全符合 MeloTTS 官方最新标准的 `metadata.list`（UTF-8 无 BOM）
- 转录失败时优雅跳过，继续处理其他文件

### 支持的模型（推荐顺序）
1. **openai/whisper-base**（平衡速度与准确率）

## 参数提取指南
当决定调用此技能时，请从用户消息中提取以下参数：

1. **`--wav_dir`** (必填): 音频文件所在目录
2. **`--txt_dir`** (选填): 文本转录文件所在目录（若不提供且启用 Whisper，则自动转录）
3. **`--speaker`** (选填): 强制指定统一说话人名称（单音色模式）
4. **`--lang`** (选填): 语言代码，如 `ZH`、`EN` 等
5. **`--output`** (选填): 输出 metadata.list 的路径（默认当前目录）
6. **`--recursive`** (选填): 是否递归处理子目录
7. **`--use_whisper`** (选填): 是否强制使用 Whisper 转录

### 执行步骤
1. **解析目录**：自动识别 --wav_dir 和 --txt_dir，支持多级子目录结构。
2. **默认目标**：若未指定 --output，默认在当前工作目录生成 `metadata.list`。
3. **调用命令**：使用以下兼容性命令启动脚本（优先 `python3`，失败则 `python`）。脚本会自动检测 Whisper 依赖。

   ```bash
   (python3 scripts/generate_metadata_list.py --wav_dir "<音频目录>" --txt_dir "<文本目录>" [--speaker <姓名>] [--lang {ZH,EN}] [--output <路径>] [--recursive] [--use_whisper]) || (python scripts/generate_metadata_list.py --wav_dir "<音频目录>" --txt_dir "<文本目录>" [--speaker <姓名>] [--lang {ZH,EN}] [--output <路径>] [--recursive] [--use_whisper])