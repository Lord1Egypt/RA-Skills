# ModelCLI 命令参考

始终通过 `scripts/invoke.py -- COMMAND ...` 调用。包装器负责加入全局 `--json --allow-download`。

## 能力发现与诊断

```bash
python3 {baseDir}/scripts/invoke.py -- capabilities
python3 {baseDir}/scripts/invoke.py -- doctor
python3 {baseDir}/scripts/invoke.py --approve-sensitive -- doctor --deep
```

- `capabilities`：CLI/schema 版本、支持命令、运行设备、provider、缓存目录和模型状态。
- `doctor`：依赖、目录、模型文件、manifest 和 hash 的静态检查，不下载模型。
- `doctor --deep`：实际加载已安装模型，执行前要求确认。

## 目标检测

```bash
python3 {baseDir}/scripts/invoke.py -- detect IMAGE \
  [--confidence 0.5] \
  [--class person --class car] \
  [--draw-boxes OUTPUT]
```

`result` 字段：

- `width`、`height`：原图尺寸。
- `confidence_threshold`、`class_filter`：实际过滤条件。
- `detections[]`：`class_id`、`label`、`confidence`、`bbox{x1,y1,x2,y2}`。
- `annotated_image`：使用 `--draw-boxes` 时的绝对路径。

`--force` 覆盖标注图前要求确认。COCO 类别必须使用英文标准名称。

## OCR

```bash
python3 {baseDir}/scripts/invoke.py -- ocr IMAGE \
  [--out TEXT_FILE] \
  [--markdown] \
  [--draw-boxes OUTPUT]
```

`result.lines[]` 包含 `text`、`score`、`box` 四点坐标。指定 `--out` 时增加 `text_output`；指定 `--draw-boxes` 时增加 `annotated_image`。只有覆盖标注图的 `--force` 需要确认。

## 语音识别

```bash
python3 {baseDir}/scripts/invoke.py -- asr AUDIO \
  [--out TEXT_FILE] \
  [--lang auto|zh|en|yue|ja|ko] \
  [--no-vad] [--timestamps] [--emotion]
```

输入支持 WAV、FLAC、MP3。`result` 包含 `text`、`language` 和 `segments[]`；每段有 `start`、`end`、`text`、`emotion`、`events`。指定 `--out` 时增加 `text_output`。

## 语音合成

```bash
python3 {baseDir}/scripts/invoke.py -- tts TEXT \
  --out OUTPUT.wav \
  [--prompt-audio REFERENCE.wav] \
  [--max-duration 30]
```

TEXT 以 `@` 开头时从 UTF-8 文本文件读取。`result` 包含：

- `output`、`size_bytes`、`duration_seconds`。
- `sample_rate`（固定 48000）、`channels`（固定 2）。
- `prompt_source` 和 `reached_frame_cap`。

Agent 调用必须显式传 `--out`。输出已存在时先询问用户，确认后使用包装器 `--approve-sensitive` 并在命令尾部加入 `--force`。

## 模型管理

```bash
python3 {baseDir}/scripts/invoke.py -- models list
python3 {baseDir}/scripts/invoke.py -- models install detect|asr|tts|all
python3 {baseDir}/scripts/invoke.py -- models verify detect|asr|tts|all
python3 {baseDir}/scripts/invoke.py -- models prefetch
```

以下命令要求确认并传 `--approve-sensitive`：

```bash
python3 {baseDir}/scripts/invoke.py --approve-sensitive -- models install TARGET --refresh
python3 {baseDir}/scripts/invoke.py --approve-sensitive -- models remove TARGET
python3 {baseDir}/scripts/invoke.py --approve-sensitive -- models clean
```

`TARGET` 为 `detect|asr|tts|all`。OCR 与 VAD 随 Python 依赖提供，没有独立下载目标。
