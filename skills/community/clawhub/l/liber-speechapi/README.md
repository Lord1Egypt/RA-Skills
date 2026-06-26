# liber-speechapi 技能使用说明

## 功能和目的

`liber-speechapi` 是一个集成了ASR（自动语音识别）和TTS（文本转语音）功能的语音处理工具。该技能提供了：

- **ASR（语音转文字）**：基于 [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)（Whisper），支持多语言、时间戳、说话人分离（diarization）
- **TTS（文字转语音）**：基于 [chatterbox-tts](https://github.com/resemble-ai/chatterbox)，支持 Turbo/Standard/Multilingual 模型、音色克隆
- **多输出格式**：
  - ASR：JSON、TXT、SRT、VTT
  - TTS：WAV、MP4、OGG/Opus（按 Telegram Voice Note 最佳实践）
- **部署灵活**：本地 CLI 命令 + 远程 FastAPI 服务
- **API 鉴权**：支持 API Key（Bearer Token）
- **设备自适应**：自动检测 CUDA，支持 CPU/GPU 切换

## 前置条件

### 部署后端要求

使用此技能前，必须先部署后端服务，具体要求如下：

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)**（Python 包管理器）
- **FFmpeg**（用于音频转码，TTS 多格式输出需要）
- **可选**：CUDA（GPU 加速）

### 配置优先级

环境配置按以下优先级顺序加载：

1. **环境变量**：`LIBER_API_BASE_URL` 和 `LIBER_API_KEY`（最高优先级）
2. **全局配置文件**：`~/.openclaw/.env`（用于跨项目共享配置）
3. **项目内配置**：技能目录下的 `.env` 文件
4. **当前工作目录**：当前工作目录下的 `.env` 文件（最低优先级）

这样可以灵活地在不同层级进行配置，满足全局、项目和个人需求。

### 配置文件存储

为了防止在更新技能时丢失用户配置，详细的配置参数存储在以下位置：

1. **首选位置**：`~/.openclaw/workspace/config/speechapi_config.json`（防止更新时被覆盖）
2. **备用位置**：本地的 `config.json`（用于兼容性）

### 部署步骤

1. 克隆项目：
   ```
   git clone https://github.com/liberalchang/Liber_SpeechAPI.git
   ```

2. 交互式安装：
   - Windows:
     ```powershell
     .\setup.ps1
     ```
   
   - Linux/macOS:
     ```bash
     ./setup.sh
     ```

3. 安装脚本将：
   - 交互式选择组件（ASR/TTS/API）、设备、模型、鉴权方式
   - 生成 `.env` 配置文件
   - 自动安装依赖（`uv sync [--extra api]`）
   - 验证 CLI 入口

4. 验证安装：
   ```bash
   # 查看 CLI 帮助
   uv run liber-speech --help
   
   # 诊断环境
   uv run liber-speech doctor
   ```

5. 配置 API 凭据：
   根据上述优先级规则，在合适的位置设置 `LIBER_API_BASE_URL` 和 `LIBER_API_KEY`，例如：
   - 在 `~/.openclaw/.env` 中设置全局凭据
   - 或在环境变量中设置特定会话的凭据

6. 配置详细参数：
   如需自定义ASR/TTS参数，创建 `~/.openclaw/workspace/config/speechapi_config.json` 文件以避免在技能更新时丢失配置

### Web 服务部署选项

如果需要额外的 Web 服务，可以部署 FastAPI 服务：

```bash
# 启动服务（默认 5555 端口）
uv run liber-speech serve

# 指定端口
uv run liber-speech serve --host 0.0.0.0 --port 8080
```

访问 API 文档：`http://localhost:5555/docs`

## 项目地址

- **主项目地址**：[https://github.com/liberalchang/Liber_SpeechAPI](https://github.com/liberalchang/Liber_SpeechAPI)

## 使用示例

### CLI 模式

#### ASR 转录
```bash
# 使用默认配置转录（输出 JSON）
uv run liber-speech asr transcribe audio.wav

# 指定模型与语言，输出 SRT 字幕
uv run liber-speech asr transcribe audio.wav \
  --model openai/whisper-large-v3 \
  --language zh \
  --out subs.srt
```

#### TTS 合成
```bash
# 使用默认配置合成（输出 WAV）
uv run liber-speech tts synthesize "你好世界"

# 多语模型 + OGG/Opus 输出（适合 Telegram）
uv run liber-speech tts synthesize "你好世界" \
  --language zh \
  --format ogg_opus \
  --out hello.ogg
```

### API 模式

通过 HTTP 请求调用，支持认证和多种输出格式，详细 API 文档请参见项目文档。

## Windows 用户特别注意

如果在 Windows 上遇到编码或模块加载问题，请使用修复版启动器：

```bash
# 使用修复版启动器（推荐）
python -S scripts/run_cli.py [命令]

# 或使用批处理文件
.\run_cli.bat [命令]
```

修复版启动器解决了以下问题：
- Windows GBK 编码问题
- Python site 模块加载冲突
- 缺失依赖（setuptools）
- 张量维度不匹配