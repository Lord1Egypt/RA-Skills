# 龙虾电台 Skill - 快速开始指南

## 🎯 项目概述

龙虾电台是一个OpenClaw Skill，使用本地Qwen3-TTS模型生成个性化资讯音频。

## 📦 项目结构

```
lobster-radio-skill/
├── SKILL.md                 # Skill主定义文件
├── README.md               # 使用说明
├── requirements.txt        # Python依赖
├── LICENSE                 # MIT许可证
├── .gitignore             # Git忽略文件
├── __init__.py            # 包初始化
├── cowork_mode.py          # Cowork Mode主入口
├── providers/             # TTS提供商
│   ├── __init__.py
│   ├── tts_base.py        # TTS基类
│   ├── tts_factory.py     # TTS工厂
│   └── qwen3_tts.py       # Qwen3-TTS本地模型实现
├── scripts/               # 脚本
│   ├── configure_tts.py   # 配置TTS
│   └── list_radios.py     # 列出历史电台
├── utils/                 # 工具模块
│   ├── __init__.py
│   ├── content_generator.py # 内容生成器
│   ├── audio_manager.py    # 音频管理器
│   └── config_manager.py   # 配置管理器
├── templates/             # 模板文件
│   └── prompts/
│       └── radio_content.txt
├── data/                  # 数据目录
│   └── radios/            # 音频文件存储
└── tests/                 # 测试文件
    └── verify_all.py
```

> **注意**: 本Skill仅支持Cowork Mode，内容由平台主对话LLM生成，Skill只负责TTS语音合成。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd lobster-radio-skill
pip install -r requirements.txt
```

### 2. 下载Qwen3-TTS模型

**重要**: Qwen3-TTS模型**不在Ollama公共仓库中**，需要从HuggingFace或ModelScope下载。

**方式A：从HuggingFace下载（推荐）**

```bash
# 安装huggingface_hub
pip install huggingface_hub

# 下载模型（0.6B版本，推荐）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base
```

**方式B：从ModelScope下载（国内用户推荐）**

```bash
# 安装modelscope
pip install modelscope

# 下载模型
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"
```

**方式C：首次运行时自动下载**

Skill会在首次生成电台时自动检测并下载模型。

### 3. 验证安装

```bash
python tests/verify_all.py
```

### 4. 配置TTS

```bash
python scripts/configure_tts.py --voice xiaoxiao --emotion neutral --speed 1.0
```

### 5. 生成电台（Cowork Mode）

在 LobsterAI/OpenClaw 对话中，直接调用 Skill：
```python
from cowork_mode import cowork_generate

audio_url = cowork_generate(
    title="科技新闻",
    content="【平台LLM生成的新闻内容】",
    voice="yunjian"
)
```

### 6. 查看历史电台

```bash
python scripts/list_radios.py
```

## 🎨 可用音色

### 中文音色
- **xiaoxiao** (晓晓): 女声，温柔，适合新闻播报
- **yunjian** (云健): 男声，沉稳，适合财经资讯
- **xiaochen** (晓辰): 女声，活泼，适合娱乐新闻
- **xiaoyu** (晓宇): 男声，年轻，适合科技资讯
- **xiaoya** (晓雅): 女声，知性，适合教育内容

### 情感表达
- **neutral**: 中性，适合新闻播报
- **happy**: 开心，适合娱乐内容
- **sad**: 悲伤，适合严肃话题
- **excited**: 兴奋，适合科技突破

## 📝 使用示例

### 示例1: 生成科技电台（Cowork Mode）

```python
from cowork_mode import cowork_generate

content = """
欢迎收听今天的科技新闻。

首先，关于人工智能领域...

其次，在芯片行业...

最后，在互联网行业...
"""

audio_url = cowork_generate(
    title="科技新闻",
    content=content,
    voice="yunjian",
    emotion="neutral"
)
```

### 示例2: 配置音色

```bash
python scripts/configure_tts.py \
  --voice yunjian \
  --emotion neutral \
  --speed 1.0 \
  --pitch 1.0
```

### 示例3: 测试TTS

```bash
python scripts/configure_tts.py --test
```

### 示例4: 清理过期电台

```bash
python scripts/list_radios.py --cleanup 30
```

## 🔧 高级配置

### 自定义模型

本Skill仅支持CustomVoice版本的模型：
- Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice（推荐）
- Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice

```bash
python scripts/configure_tts.py --model Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice
```

### 调整语速和音调

```bash
python scripts/configure_tts.py --speed 1.2 --pitch 0.9
```

## 🧪 运行测试

```bash
python tests/verify_all.py
```

## 📊 性能指标

- **CPU推理速度**: 1-2秒/100字
- **GPU推理速度**: 0.5-1秒/100字
- **内存占用**: 约500MB
- **模型大小**: 约5GB

## 💰 成本优势

- ✅ **完全免费**: 无API调用费用
- ✅ **无使用限制**: 可无限次使用
- ✅ **数据隐私**: 所有处理在本地完成
- ✅ **可离线使用**: 无网络依赖

## 🐛 故障排除

### 模型未下载

**错误**: "模型未找到" 或 "模型下载失败"

**重要**: 本Skill仅支持CustomVoice版本的模型！

**解决方案**:
```bash
# 方法1: 从HuggingFace下载
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-CustomVoice

# 方法2: 从ModelScope下载（国内用户推荐）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice', cache_dir='./models')"

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

## 📚 相关文档

- [OpenClaw文档](https://docs.openclaw.ai)
- [Qwen3-TTS文档](https://qwen.ai/blog?id=qwen3tts-0115)
- [Qwen3-TTS HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**注意**: 本项目仅用于教育和研究目的。请遵守当地法律法规，不要用于非法用途。
