---
name: modelcli
description: 使用本地 ModelCLI 完成目标检测、OCR、语音识别、语音合成、模型管理与运行诊断。 Use when the user asks to detect objects in an image, extract Chinese or English text from an image, transcribe WAV/FLAC/MP3 audio, synthesize or clone speech, inspect local model capabilities, or manage ModelCLI models.
---

# ModelCLI

通过本 skill 的包装器调用本地 ModelCLI。不要解析人类模式的富文本输出，也不要绕过包装器自行拼接 Agent 协议。

## 工作流

1. 根据请求选择能力：
   - 图片中的常见物体、类别、置信度或坐标：`detect`。
   - 图片文字：`ocr`。
   - 音频转文字、时间段、情绪或声音事件：`asr`。
   - 文本转语音或参考音克隆：`tts`。
   - 环境、模型状态或故障检查：`capabilities`、`doctor` 或 `models`。
2. 推理前检查输入文件存在且可读。所有路径都转换为绝对路径。
3. 使用 `{baseDir}/scripts/invoke.py` 执行。包装器会确保 CLI 可用，并加入全局 `--json --allow-download`：

   ```bash
   python3 {baseDir}/scripts/invoke.py -- detect /absolute/path/photo.jpg
   python3 {baseDir}/scripts/invoke.py -- ocr /absolute/path/screenshot.png
   python3 {baseDir}/scripts/invoke.py -- asr /absolute/path/audio.wav --lang auto
   python3 {baseDir}/scripts/invoke.py -- tts "要合成的文本" --out /absolute/path/speech.wav
   ```

4. 解析 stdout 中唯一的 JSON 信封：
   - `ok: true`：使用 `result` 回答，并指出生成文件的绝对路径。
   - `ok: false`：使用 `error.code`、`message` 和 `retryable` 处理失败；stderr 仅作诊断。
5. `retryable: true` 或 `MODEL_BUSY` 最多重试一次。不要重试输入错误、输出冲突或不可重试错误。
6. 向用户简洁报告结果。除非用户要求，不要倾倒完整 JSON 或依赖日志。

## 安全边界

包装器会自动安装缺失的 ModelCLI，也允许推理时下载缺失模型。以下操作必须先获得用户明确确认，然后才加入 `--approve-sensitive`：

- 使用任何 `--force` 覆盖已有输出。
- `models install ... --refresh`。
- `models remove ...` 或 `models clean`。
- `doctor --deep`。

确认后这样执行：

```bash
python3 {baseDir}/scripts/invoke.py --approve-sensitive -- tts "新内容" --out /absolute/path/existing.wav --force
```

不要主动刷新模型、删除缓存或覆盖文件。普通推理、`models install`、`models verify`、`models list`、`capabilities` 和静态 `doctor` 不需要额外确认。

## 能力选择约束

- `detect` 只识别 COCO 80 类，类别名使用英文，例如 `person`、`car`；它不是开放词汇或 UI 元素检测模型。
- OCR 返回逐行文本、置信度和四点坐标；需要可视化时使用 `--draw-boxes`。
- ASR 语言可选 `auto|zh|en|yue|ja|ko`；长音频默认启用 VAD。
- TTS 在 Agent 模式必须有 `--out`；需要克隆声音时用可读音频传 `--prompt-audio`。
- 调用方拥有墙钟超时。包装器默认 900 秒，可用 `--timeout` 调整。

需要具体参数或返回字段时读取 [references/commands.md](references/commands.md)。需要错误码、信封或重试细节时读取 [references/protocol.md](references/protocol.md)。
