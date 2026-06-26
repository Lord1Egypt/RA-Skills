# 龙虾电台 - 个性化AI资讯播报系统

> 让AI为你播报专属资讯，解放双眼，随时随地获取信息

---

## 📢 产品简介

**龙虾电台**是一款基于AI技术的个性化资讯播报系统，能够根据用户的兴趣和需求，自动生成并播报定制化的新闻内容。无论是科技前沿、财经动态，还是娱乐八卦，龙虾电台都能为你量身打造专属的"声音资讯"。

### 核心特点

- 🎙️ **AI语音合成**：使用阿里Qwen3-TTS模型，9种预设音色，播报自然流畅
- 📰 **智能内容生成**：基于真实新闻搜索，8-20字标题+100字精悍内容
- ⏰ **定时推送**：支持设置每日定时播报，早报、晚报随心定制
- 🆓 **完全免费**：本地运行，无API调用费用，一次配置永久使用
- 🔒 **隐私安全**：数据本地处理，不上传云端，保护用户隐私

---

## 👥 面向不同人群

### 产品经理视角

**为什么需要龙虾电台？**

在信息爆炸的时代，用户面临严重的信息过载问题。传统的文字阅读方式需要占用视觉注意力，而音频播报可以让用户在通勤、运动、做家务时同步获取资讯。

**产品亮点**：
- **场景化设计**：针对通勤、晨跑、睡前等碎片化场景优化
- **个性化推荐**：基于用户标签和主题，精准推送感兴趣的内容
- **多平台支持**：同时支持OpenClaw和LobsterAI两大Agent平台

**典型使用场景**：
- 早晨8点自动推送"科技早报"
- 下班路上收听"财经晚报"
- 睡前聆听"今日热点回顾"

### 技术人员视角

**技术架构**

```
┌─────────────────────────────────────────────────────────────┐
│                     龙虾电台技术架构                          │
├─────────────────────────────────────────────────────────────┤
│  内容层                                                       │
│  ├── 新闻搜索（平台web-search技能）                           │
│  ├── 内容生成（8-20字标题 + 100字文稿）                       │
│  └── 内容过滤（去除结构标记，自然流畅）                       │
├─────────────────────────────────────────────────────────────┤
│  语音层                                                       │
│  ├── Qwen3-TTS模型（本地运行）                                │
│  ├── 9种预设音色（中英日韩等多语言）                          │
│  └── 情感控制（开心、悲伤、兴奋等）                           │
├─────────────────────────────────────────────────────────────┤
│  平台层                                                       │
│  ├── OpenClaw支持（SKILL.md配置）                             │
│  ├── LobsterAI支持（skill.json配置）                          │
│  └── 双平台适配器（自动检测平台）                             │
└─────────────────────────────────────────────────────────────┘
```

**核心技术栈**：
- **Python 3.10+**：主要开发语言
- **Qwen3-TTS**：阿里开源TTS模型，支持9种音色
- **Transformers**：HuggingFace模型库
- **Asyncio**：异步编程，提升性能

**创新点**：
1. **V2内容生成方案**：新闻搜索 + LLM加工，时效性强
2. **平台web-search技能复用**：无需额外申请新闻API
3. **内容标记过滤**：自动去除【开场】【结尾】等标记，播报更自然

### 行政/运营人员视角

**如何为团队配置龙虾电台？**

**Step 1：安装部署**
```bash
# 克隆代码
git clone <repository-url>
cd lobster-radio-skill

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**Step 2：下载模型**
```bash
# 下载Qwen3-TTS模型（约5GB）
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice \
  --local-dir ./models/Qwen3-TTS-12Hz-0.6B-CustomVoice
```

**Step 3：配置音色**
```bash
# 配置为yunjian男声（适合财经）
python scripts/configure_tts.py --voice yunjian

# 或配置为xiaoxiao女声（适合新闻）
python scripts/configure_tts.py --voice xiaoxiao
```

**Step 4：生成测试**
```bash
# 生成科技新闻电台
python scripts/generate_radio.py --topics "人工智能" --tags "科技"
```

**Step 5：设置定时任务**
```bash
# OpenClaw平台
openclaw cron add \
  --name "每日科技早报" \
  --cron "0 8 * * *" \
  --message "生成科技新闻电台" \
  --announce

# LobsterAI平台
# 在GUI中或通过对话："每天早上8点推送科技新闻"
```

---

## 🚀 快速开始

### 环境要求

- **操作系统**：macOS / Linux / Windows
- **Python版本**：3.10 或更高
- **磁盘空间**：至少10GB（模型文件约5GB）
- **内存**：建议8GB以上

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-repo/lobster-radio-skill.git
cd lobster-radio-skill

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice \
  --local-dir ./models/Qwen3-TTS-12Hz-0.6B-CustomVoice

# 5. 运行测试
python tests/test_skill.py
```

### 基本使用

```bash
# 生成单条电台
python scripts/generate_radio.py --topics "人工智能" --tags "科技"

# 配置音色
python scripts/configure_tts.py --voice yunjian --emotion neutral

# 查看配置
python scripts/configure_tts.py --show
```

---

## 🛠️ 开发指南

### 项目结构

```
lobster-radio-skill/
├── providers/              # TTS提供商
│   ├── qwen3_tts.py       # Qwen3-TTS实现
│   ├── tts_base.py        # TTS基类
│   └── tts_factory.py     # TTS工厂
├── utils/                  # 工具模块
│   ├── content_generator.py      # V1内容生成
│   ├── content_generator_v2.py   # V2内容生成（推荐）
│   ├── content_filter.py         # 内容过滤
│   ├── platform_adapter.py       # 平台适配器
│   ├── platform_news_searcher_v2.py  # 新闻搜索
│   ├── audio_manager.py          # 音频管理
│   └── config_manager.py         # 配置管理
├── scripts/                # 脚本
│   ├── generate_radio.py   # 生成电台
│   ├── configure_tts.py    # 配置TTS
│   └── install.sh          # 安装脚本
├── templates/              # 模板
│   └── prompts/            # 提示词模板
├── tests/                  # 测试
│   ├── test_skill.py       # 功能测试
│   └── verify_all.py       # 验证脚本
├── SKILL.md               # OpenClaw配置
├── skill.json             # LobsterAI配置
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

### 核心模块说明

#### 1. 内容生成器（V2方案）

```python
from utils.content_generator_v2 import ContentGeneratorV2

generator = ContentGeneratorV2()
content = await generator.generate(
    topics=['人工智能'],
    tags=['科技'],
    max_segments=5  # 生成5条新闻
)

# 输出结构化内容
print(content.main_title)  # 主标题
for seg in content.segments:
    print(seg.title)      # 8-20字标题
    print(seg.content)    # 100字以内文稿
```

#### 2. TTS提供商

```python
from providers.qwen3_tts import Qwen3TTSProvider

provider = Qwen3TTSProvider()

# 合成语音
audio = await provider.synthesize(
    text="欢迎使用龙虾电台",
    voice_id="xiaoxiao",  # 9种音色可选
    emotion="neutral"   # 情感控制
)
```

#### 3. 平台适配器

```python
from utils.platform_adapter import get_platform_adapter

adapter = get_platform_adapter()

# 保存用户偏好
adapter.save_memory('subscribed_tags', ['科技', '财经'])

# 获取记忆
tags = adapter.get_memory('subscribed_tags')
```

### 扩展开发

#### 添加新的TTS提供商

1. 在`providers/`目录创建新文件
2. 继承`TTSProvider`基类
3. 实现必要方法
4. 使用`@register_provider`装饰器注册

```python
from .tts_base import TTSProvider, register_provider

@register_provider
class MyTTSProvider(TTSProvider):
    @property
    def name(self) -> str:
        return "MyTTS"
    
    async def synthesize(self, text, **kwargs):
        # 实现合成逻辑
        pass
```

#### 自定义内容生成策略

修改`utils/content_generator_v2.py`中的模板：

```python
self.templates['title'] = """你的自定义标题生成提示词..."""
self.templates['script'] = """你的自定义文稿生成提示词..."""
```

---

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **模型大小** | 5GB | 0.6B参数版本 |
| **推理速度** | 实时 | CPU即可流畅运行 |
| **内容生成** | <3秒 | 5条新闻生成时间 |
| **语音合成** | 1-2秒/100字 | 取决于硬件 |
| **内存占用** | 2-4GB | 运行时 |

---

## 🎯 适用场景

### 个人用户
- 📱 通勤路上听新闻
- 🏃 跑步时获取资讯
- 🍳 做饭时学习知识
- 🛏️ 睡前回顾一天热点

### 企业应用
- 📢 企业内训音频生成
- 📊 行业报告语音播报
- 📰 内部新闻自动播报
- 🎓 培训课程音频制作

### 内容创作者
- 🎙️ 播客内容快速生成
- 📹 视频配音辅助
- 📝 文章转音频
- 🎵 有声书制作

---

## 🤝 贡献指南

欢迎提交Issue和PR！

### 开发流程

1. Fork仓库
2. 创建特性分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/my-feature`
5. 提交Pull Request

### 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 添加必要的注释和文档字符串
- 编写单元测试

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) - 阿里开源TTS模型
- [OpenClaw](https://openclaw.ai) - Agent平台
- [LobsterAI](https://github.com/netease-youdao/LobsterAI) - 有道龙虾Agent

---

> **龙虾电台** - 让资讯触手可及，让信息更有温度 🦞
