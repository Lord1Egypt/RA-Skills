# melo-tts-metadata-creator

一个专为 **MeloTTS** 训练 / 微调设计的 `metadata.list` 生成工具。

支持 **单音色** 与 **多音色** 两种模式，特别适配：

> ✅ wav 文件和 txt 转录文件位于两个不同目录
> ✅ 且每个子目录代表一个说话人

---

## ✨ 主要特性

* 支持 wav 和 txt **分离存放**（目录结构完全一致）
* 自动按第一级子目录提取 speaker（多音色模式）
* 支持 `--speaker` 强制统一说话人（单音色模式）
* 内置 Whisper 自动转录（无 txt 自动生成）
* Whisper 模型下载到 `./models/` 目录（便于管理）
* 转录失败或下载失败自动跳过，不影响整体处理
* 生成完全符合 MeloTTS 官方标准的 `metadata.list`

---

## 📁 数据目录结构示例

```
voice_dataset/
├── wav/                    ← --wav_dir
│   ├── user001/
│   │   ├── 0001.wav
│   │   ├── 0002.wav
│   │   └── ...
│   ├── lao_voice/
│   │   └── test.wav
│   └── user002/
│       └── ...
│
├── txt/                    ← --txt_dir
│   ├── user001/
│   │   ├── 0001.txt
│   │   ├── 0002.txt
│   │   └── ...
│   ├── lao_voice/
│   └── user002/
│
└── metadata.list           ← 输出文件
```

---

## 🚀 安装依赖

```bash
pip install openai-whisper torch torchaudio torchvision
```

---

## 📌 参数说明

| 参数            | 类型     | 必填 | 默认值           | 说明                    |
| ------------- | ------ | -- | ------------- | --------------------- |
| --wav_dir     | string | ✅  | -             | wav 根目录               |
| --txt_dir     | string | ✅  | -             | txt 根目录（必须与 wav 结构一致） |
| --speaker     | string | ❌  | None          | 单音色模式（强制统一 speaker）   |
| --lang        | string | ❌  | ZH            | 语言：ZH / EN            |
| --output      | string | ❌  | metadata.list | 输出文件路径                |
| --recursive   | flag   | ❌  | False         | 递归搜索子目录（建议开启）         |
| --use_whisper | flag   | ❌  | False         | 缺失 txt 时自动转录          |

---

## 🚀 使用示例

### 示例 1：多音色（推荐）

```bash
python generate_metadata_list.py \
  --wav_dir ./dataset/wav \
  --txt_dir ./dataset/txt \
  --lang ZH \
  --output ./dataset/metadata.list \
  --use_whisper \
  --recursive
```

---

### 示例 2：单音色

```bash
python generate_metadata_list.py \
  --wav_dir ./dataset/wav \
  --txt_dir ./dataset/txt \
  --speaker lao_voice \
  --lang ZH \
  --output ./dataset/metadata.list \
  --use_whisper
```

---

### 示例 3：不使用 Whisper

```bash
python generate_metadata_list.py \
  --wav_dir ./dataset/wav \
  --txt_dir ./dataset/txt \
  --speaker lao_voice \
  --lang ZH \
  --output ./dataset/metadata.list
```

### **命令行启动**

python scripts/generate_metadata_list.py --wav_dir F:\命理学-音频-干声-切片 --txt_dir F:\命理学-音频-干声-切片-文本_corrected_punctuated  --lang ZH --output F:\命理学-数据集\metadata.list --recursive --use_whisper

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

帮我生成 MeloTTS 的 metadata.list

把我的 /home/ai-wmr/下载/猴哥说易 文件夹和 /home/ai-wmr/下载/猴哥说易_punctuated 生成 metadata，说话者：猴哥说易，输出到/home/ai-wmr/下载/猴哥说易-数据集/，中文，递归搜索

用 Whisper 为这些音频转录并生成 MeloTTS 训练文件

MeloTTS 多音色数据集准备 metadata

---

## 📄 输出格式（官方标准）

每行 **严格 4 个字段，用 `|` 分隔**：

```
/absolute/path/to/wav/user001/0001.wav|user001|ZH|你好，这是我的第一条测试音频。
/absolute/path/to/wav/lao_voice/test.wav|lao_voice|ZH|今天天气真不错。
```

---

## ⚠️ 常见问题

* ❌ 路径错误 → `file not found`
* ❌ UTF-8 BOM → `train.sh` 报错
* ❌ 文本含 `|` → 分隔错误（请替换为中文符号）
* ❌ 音频格式不规范 → 建议统一转换

### 🎧 音频转换（推荐）

```bash
ffmpeg -i input.mp3 -ar 44100 -ac 1 output.wav
```

---

## 📌 使用注意

* wav 必须为 `.wav`（推荐 44100Hz 单声道）
* txt 内容必须与音频 **完全一致**
* 首次使用 `--use_whisper` 会下载模型到 `./models/`
* 转录失败不会中断程序
* 输出为 **UTF-8 无 BOM**

---

## 📚 metadata.list 详解（官方标准）

### ✅ 格式

```
音频路径|speaker|语言|文本
```

---

### 📌 字段说明

#### 1️⃣ 音频路径

* 必须 `.wav`
* 推荐绝对路径
* 建议 44100Hz 单声道

#### 2️⃣ speaker

* 可自定义（中英文均可）
* 单音色：统一名称
* 多音色：不同目录不同 speaker

#### 3️⃣ 语言代码

* `ZH`：中文
* `EN`：英文
* 支持中英混读（但一行只能标一个）

#### 4️⃣ 文本

* 必须与音频完全一致
* 包含标点、停顿
* 推荐使用 Whisper 自动生成

---

## 📄 示例文件

```bash
cat > your_metadata.list << 'EOF'
/home/lao/my_voice/recording_001.wav|我的声音|ZH|你好，我正在录制自己的音色训练数据。
/home/lao/my_voice/recording_002.wav|我的声音|ZH|这是第二句测试文本，用普通话说的。
/home/lao/my_voice/recording_003.wav|我的声音|EN|Hello, this is an English test sentence.
/home/lao/my_voice/recording_004.wav|我的声音|ZH|第三句中文，测试语速和情感。
EOF
```

---

## 📊 数据建议

* 最少：50–100 条
* 推荐：1–3 小时音频（效果最佳）

---
