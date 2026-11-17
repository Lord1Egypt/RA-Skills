---
name: lipvoice-tts
description: "LipVoice 语音克隆和文本转语音合成：上传参考音频创建声音模型、列出已有模型、文本转语音合成下载"
metadata: {"author": "lipvoice", "version": "1.0.0"}
user-invocable: true
allowed-tools: ["exec", "read", "write"]
---

# LipVoice TTS 语音合成技能

使用 LipVoice 企业 API 实现声音克隆和高质量文本转语音。需要企业会员 API Key。

## 使用前准备

**配置 API Key（二选一）：**
1. 设置环境变量 `LIPVOICE_API_KEY` 为你的 API Key
2. 调用时通过 `--api-key YOUR_KEY` 参数传入

## 常用命令

脚本路径：`scripts/lipvoice_tts.py`（相对于本技能目录）

**注意：Windows 下使用 `py` 命令启动 Python，Linux/macOS 使用 `python3`。**

### 1. 列出所有声音模型
```bash
py scripts/lipvoice_tts.py list
```
查看已上传的所有声音模型及其ID，合成语音时需要用到 `audio-id`。

### 2. 上传音频创建声音克隆模型
```bash
py scripts/lipvoice_tts.py upload --file <音频文件路径> --name "<模型名称>" [--describe "<描述>"]
```
- 支持格式：mp3/wav/m4a
- 建议使用 30s-2min 清晰无背景噪音的音频，效果更佳

### 3. 文本转语音合成（自动等待完成并下载）
```bash
py scripts/lipvoice_tts.py tts --text "<要合成的文本>" --audio-id <模型ID> [--style 1] [--output <输出路径.wav>]
```
- `--style`: 合成模式
  - `1`: 参考原音频风格（默认，克隆效果更贴近原声）
  - `2`: 大模型通用风格（更稳定）
- `--output/-o`: 自定义输出 wav 文件路径

### 4. 删除模型
```bash
py scripts/lipvoice_tts.py delete --audio-id <模型ID>
```

## 典型工作流

1. **首次使用**：先调用 `list` 查看已有模型，或用 `upload` 上传自己的参考音频创建模型
2. **合成语音**：使用 `tts` 命令传入文本和模型ID，自动合成并下载到本地wav文件
3. **返回结果**：合成完成后将音频文件作为附件回复给用户

## 输出说明

合成成功会返回：
- 本地保存的wav文件路径（绝对路径）
- 原始音频URL

## Windows 兼容性

已修复Windows控制台GBK编码问题，所有输出直接支持中文。
