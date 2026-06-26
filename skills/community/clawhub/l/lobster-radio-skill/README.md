# 龙虾电台 (Lobster Radio) - OpenClaw Skill

个性化资讯电台生成服务，使用本地TTS模型，完全免费（上方文件有音频示例）

基于通义千问开源的Qwen3-TTS-12Hz 0.6b本地模型语音大模型，实现 **「资讯智能抓取→内容精编→个性化语音合成」** 全链路自动化的音频资讯系统。

1）资讯文本生成使用openclaw当前配置的LLM模型，目前测试安装到成功音频生产大概需要3百万token

2）音频生成无需付费 API 调用，是在本地TTS模型端到端运行，能用预设9个专业主播音色生成资讯播客，通勤、运动、居家等碎片化场景，都能无缝获取你关心的信息。


## 功能特性

- 🎙️ **个性化电台生成**: 根据用户输入感兴趣的主题或标签生成资讯音频
- ⏰ **定时推送**: 支持每日定时推送电台内容
- 🎨 **多音色选择**: 支持多种中文音色和情感表达
- 💰 **完全免费**: 使用本地TTS模型，无API调用费用
- 🐣 **自动下载安装模块**：skill 自动判断当前地址，自动检查环境从国内外下载模型
- 🔒 **数据隐私**: 所有处理在本地完成
- 📡 **多渠道支持**: 支持飞书、Telegram、微信等20+平台



## 系统要求（普通电脑都能跑）

### 最低配置
- CPU: 任意现代CPU
- 内存: 4GB RAM
- 存储: 2GB可用空间

### 推荐配置
- GPU: NVIDIA显卡（支持CUDA）
- 显存: 2GB以上
- 内存: 8GB RAM
- 存储: 5GB可用空间

## 安装

### 前置要求

**重要**: Qwen3-TTS模型**不在Ollama公共仓库中**，需要从HuggingFace或ModelScope下载。

#### 系统要求

**最低配置（Qwen3-TTS-12Hz-0.6B-Base）**:
- CPU: 任意现代CPU
- 内存: 8GB RAM
- 存储: 5GB可用空间
- GPU: 可选（推荐）

**推荐配置（Qwen3-TTS-12Hz-0.6B-Base）**:
- GPU: NVIDIA显卡（支持CUDA）
- 显存: 4GB以上
- 内存: 16GB RAM
- 存储: 10GB可用空间

### 方法一：一键安装（推荐）

```bash
# 进入Skill目录
cd lobster-radio-skill

# 运行安装脚本
bash scripts/install.sh
```

安装脚本会自动：
- ✅ 安装Python依赖
- ✅ 下载Qwen3-TTS模型（首次使用时）
- ✅ 配置TTS
- ✅ 集成到OpenClaw

### 方法二：手动安装

#### 1. 安装Python依赖

```bash
cd lobster-radio-skill
pip install -r requirements.txt
```

#### 2. 下载Qwen3-TTS模型

**方式A：从HuggingFace下载**

```bash
# 安装huggingface_hub
pip install huggingface_hub

# 下载模型（0.6B版本，推荐）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 或下载1.7B版本（性能更好，需要更多显存）
huggingface-cli download Qwen/Qwen3-TTS-1.7B --local-dir ./models/Qwen3-TTS-1.7B
```

**方式B：从ModelScope下载（国内用户推荐）**

```bash
# 安装modelscope
pip install modelscope

# 下载模型
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"
```

**方式C：使用Python脚本下载**

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    local_dir="./models/Qwen3-TTS-12Hz-0.6B-Base",
    local_dir_use_symlinks=False
)
```

#### 3. 验证模型下载

```bash
# 检查模型文件
ls -lh ./models/Qwen3-TTS-12Hz-0.6B-Base

# 应该看到以下文件：
# config.json
# pytorch_model.bin
# tokenizer.json
# tokenizer_config.json
```

#### 4. 集成到OpenClaw

**方式A：复制到工作区**
```bash
# 复制到OpenClaw工作区
cp -r lobster-radio-skill ~/.openclaw/workspace/skills/

# 重启OpenClaw
openclaw gateway restart
```

**方式B：使用符号链接（推荐开发使用）**
```bash
# 创建符号链接
ln -s $(pwd)/lobster-radio-skill ~/.openclaw/workspace/skills/lobster-radio-skill

# 重启OpenClaw
openclaw gateway restart
```

#### 5. 验证Skill安装

```bash
# 查看已安装的skills
openclaw skills list

# 应该能看到 lobster-radio 在列表中
```

### 详细安装指南

- 查看 [INSTALL.md](INSTALL.md) 获取详细的安装和配置说明
- 查看 [QWEN3TTS_GUIDE.md](QWEN3TTS_GUIDE.md) 获取Qwen3-TTS模型的详细使用说明

## 使用方法

### 通过OpenClaw使用

在OpenClaw支持的任意聊天平台中：

**生成电台**:
```
生成关于人工智能的电台
```

**设置定时推送**:
```
每天早上8点推送科技新闻电台
```

**配置音色**:
```
配置我的电台音色
```

### 命令行使用

**生成电台**:
```bash
python scripts/generate_radio.py --topics "人工智能" --tags "科技"
```

**配置TTS**:
```bash
python scripts/configure_tts.py --voice xiaoxiao
```

**查看历史电台**:
```bash
python scripts/list_radios.py
```

## 可用音色

### 中文音色
- **xiaoxiao** (晓晓): 女声，温柔，适合新闻播报
- **yunjian** (云健): 男声，沉稳，适合财经资讯
- **xiaochen** (晓辰): 女声，活泼，适合娱乐新闻

### 情感表达
- **neutral**: 中性，适合新闻播报
- **happy**: 开心，适合娱乐内容
- **sad**: 悲伤，适合严肃话题
- **excited**: 兴奋，适合科技突破

## 性能指标

- **CPU推理速度**: 1-2秒/100字
- **GPU推理速度**: 0.5-1秒/100字
- **内存占用**: 约500MB
- **模型大小**: 约600MB

## 成本优势

- ✅ **完全免费**: 无API调用费用
- ✅ **无使用限制**: 可无限次使用
- ✅ **数据隐私**: 所有处理在本地完成
- ✅ **可离线使用**: 无网络依赖

## 项目结构

```
lobster-radio-skill/
├── SKILL.md                 # Skill主定义文件
├── requirements.txt         # Python依赖
├── README.md               # 使用说明
├── __init__.py             # 包初始化
├── scripts/                # Python脚本
│   ├── generate_radio.py   # 电台生成脚本
│   ├── configure_tts.py    # TTS配置脚本
│   └── list_radios.py      # 列出历史电台
├── providers/              # TTS提供商实现
│   ├── __init__.py
│   ├── tts_base.py         # TTS基类
│   └── qwen3_tts.py        # Qwen3-TTS本地模型实现
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── content_generator.py # 内容生成器
│   ├── audio_manager.py    # 音频文件管理
│   └── config_manager.py   # 配置管理
├── data/
│   └── radios/             # 生成的音频文件
└── templates/
    └── prompts/            # LLM提示词模板
```

## 故障排除

### 模型未下载

**错误**: "模型未找到" 或 "模型下载失败"

**解决方案**:
```bash
# 方法1: 从HuggingFace下载
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 方法2: 从ModelScope下载（国内用户推荐）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"

# 验证
python tests/verify_all.py
```

### 音频生成失败

**错误**: "音频生成失败"

**可能原因**:
1. 模型未正确加载
2. 内存/显存不足
3. 文本过长

**解决方案**:
```bash
# 检查模型状态
python tests/verify_all.py

# 使用CPU模式（如果显存不足）
# 在代码中设置 use_gpu=False

# 检查系统资源
htop
```

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/your-repo/lobster-radio-skill.git
cd lobster-radio-skill

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行测试

```bash
pytest tests/
```

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 支持

如有问题，请访问：
- GitHub Issues: https://github.com/your-repo/lobster-radio-skill/issues
- OpenClaw文档: https://docs.openclaw.ai
- Qwen3-TTS文档: https://qwen.ai/blog?id=qwen3tts-0115

## 致谢

- OpenClaw - 强大的AI助手平台
- Qwen3-TTS - 阿里开源的高质量TTS模型

---

**注意**: 本项目仅用于教育和研究目的。请遵守当地法律法规，不要用于非法用途。
