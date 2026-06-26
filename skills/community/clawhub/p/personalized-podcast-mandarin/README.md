# AI 双主持人播客生成器

> *"让每一篇文章、每一个主题，都能被两个真正有个性的人聊出来。"*

**将任意 URL / PDF / 主题转化为带有真实 Persona 的双主持人播客 + 双声道 TTS 音频。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [运行原理](#运行原理) · [核心特性](#核心特性)

---

## 安装

### Claude Code / OpenClaw

> **注意**：Agent 从 git 仓库根目录的 skills 文件夹查找 skill。

```bash
# Claude Code（当前项目）
mkdir -p .claude/skills
git clone https://github.com/liaozicen666-tech/ai-podcast-dual-host .claude/skills/ai-podcast-dual-host

# Claude Code（全局）
git clone https://github.com/liaozicen666-tech/ai-podcast-dual-host ~/.claude/skills/ai-podcast-dual-host

# OpenClaw（当前项目）
mkdir -p .openclaw/skills
git clone https://github.com/liaozicen666-tech/ai-podcast-dual-host .openclaw/skills/ai-podcast-dual-host
```

### 依赖

```bash
pip install -r requirements.txt
```

---

## 环境要求

- **Python**：3.9+
- **Doubao API Key**：用于 Research 和 Script 生成
- **TTS（可选）**：火山引擎 `VOLCANO_TTS_APP_ID` + `VOLCANO_TTS_ACCESS_TOKEN`，不配置时只生成文本
- **FFmpeg（可选）**：推荐安装，用于生成双声道立体声音频
- **不需要 GPU**，不需要本地模型，不需要 Docker

---

## 使用

### 方式一：一句话启动（本地完整模式）

```bash
# 设置 API Key
export DOUBAO_API_KEY="your-api-key"

# 生成播客
python -m src.podcast_pipeline "远程办公三年，到底是效率革命还是管理灾难" --style 深度对谈
```

### 方式二：Claude Code / Sub-Agent 注入模式

如果你使用 Claude Code 等具备 WebSearch 能力的 Agent，可让主 Agent 完成真实网络检索，再将结果注入本地 Pipeline：

```python
from src.podcast_pipeline import PodcastPipeline

pipeline = PodcastPipeline(skip_client_init=True)
result = pipeline.generate(
    source="人工智能的发展趋势",
    source_type="topic",
    research_package=research_pkg,  # 由外部 Sub-Agent 提供
    output_dir="./my_podcasts"
)
```

更多 API 用法与 `ResearchPackage` 格式见下文 [Python API](#python-api)。

---

## 效果示例

> 输入：`"远程办公三年，到底是效率革命还是管理灾难"`，风格：`深度对谈`

```
============================================================
🎙️ 播客生成完成
============================================================

📌 主题: 远程办公三年，到底是效率革命还是管理灾难
🏷️ 风格: 深度对谈
⏱️ 预估时长: 约25分钟

🔍 内容亮点
----------------------------------------
💡 开场钩子: 远程办公三年，到底是效率革命，还是管理灾难？
🎯 核心洞察: 远程办公不是简单的地点转移，而是一场组织协作范式的重构

📝 内容结构
----------------------------------------
第1段 (6分钟)
   从疫情期间的大规模远程办公实验切入
   对话: A说12句, B说15句

第2段 (10分钟)
   抛出核心冲突：效率提升 vs 协作困难
   对话: A说18句, B说22句

第3段 (9分钟)
   给出可落地的混合办公框架建议
   对话: A说10句, B说14句

📁 输出文件
----------------------------------------
🎧 音频: ./output/podcast_xxx.mp3
📄 数据: ./output/podcast_xxx.json
📝 文稿: ./output/podcast_xxx.md
```

---

## 运行原理

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  URL / PDF  │────→│   Research  │────→│   Script    │────→│    TTS      │
│    / 主题    │     │   研究引擎   │     │  脚本生成器  │     │  双声道音频  │
└─────────────┘     └──────┬──────┘     └──────┬──────┘     └─────────────┘
                           │                    │
                           ↓                    ↓
                    ┌─────────────┐      ┌─────────────┐
                    │  网络检索   │      │  A/B 对话   │
                    │  大纲构建   │      │  指定Persona │
                    └─────────────┘      └─────────────┘
```

**Persona 如何影响脚本**：
Script Generator 在生成每一句话时，会同时参考两位主持人的 **身份（archetype）+ 说话风格（expression）+ 记忆种子（memory_seed）**，确保 A 和 B 的不是"两个 generic AI"，而是有真实性格差异的对话者。

---

## 核心特性

- **双主持人架构**：A（理性/数据驱动）与 B（感性/善于举例）的角色扮演
- **风格对标预设**：8 种知名播客风格一键应用（十三邀、鲁豫有约、圆桌派、罗永浩、李诞等）
- **三层 Persona 配置**：风格预设 / 一句话生成 / 文档提取人格
- **多种输入源**：支持主题、URL、PDF 三种输入
- **5 种对话风格**：高效传达、发散漫谈、深度对谈、观点交锋、喜剧风格
- **流式脚本生成**：SSE 流式输出，长文本不超时
- **TTS 2.0 优化**：火山引擎 TTS，WebSocket 连接复用、引用上文、双声道立体声
- **生成摘要展示**：自动展示内容亮点、段落结构和输出文件

---

## 前置条件

| 项目 | 要求 | 说明 |
|------|------|------|
| **Doubao API Key** | 必需 | 用于 Research 和 Script 生成 |
| **火山引擎 TTS** | 可选 | 不配置时只生成文本脚本，不产音频 |
| **FFmpeg** | 可选 | 推荐安装，用于生成双声道立体声 MP3 |

---

## Python API

### 基础用法

```python
from src.podcast_pipeline import PodcastPipeline

pipeline = PodcastPipeline()

# 主题输入
result = pipeline.generate(
    source="人工智能对程序员工作的影响",
    source_type="topic",
    style="深度对谈",
    verbose=True
)

# URL 输入
result = pipeline.generate(
    source="https://example.com/article",
    source_type="url",
    style="深度对谈",
    verbose=True
)

# PDF 输入
result = pipeline.generate(
    source="./documents/paper.pdf",
    source_type="pdf",
    style="深度对谈",
    verbose=True
)

# 访问结果
print(f"音频文件: {result['audio_path']}")
for segment in result['script']:
    print(f"\n{segment['segment_id']}:")
    for line in segment['lines']:
        print(f"{line['speaker']}: {line['text']}")
```

### Sub-Agent Research 注入模式

完整 `ResearchPackage` 示例见 [`examples/research_package_example.py`](examples/research_package_example.py)。

### Persona 管理

```python
from src.persona_resolver import PersonaResolver

# 用户说"用罗永浩风格讲量子力学"
resolver = PersonaResolver()
result = resolver.resolve(explicit_description="罗永浩风格")

pipeline = PodcastPipeline()
pipeline.generate(
    source="量子力学",
    source_type="topic",
    persona_config=result.persona_config,
    style="喜剧风格"
)
```

### 命令行

```bash
# 基本用法（主题）
python -m src.podcast_pipeline "主题"

# 指定风格和输出目录
python -m src.podcast_pipeline "主题" --style 观点交锋 --output ./my_podcasts

# 使用 URL 作为输入
python -m src.podcast_pipeline "https://example.com/article" --type url

# 使用 PDF 作为输入
python -m src.podcast_pipeline "./paper.pdf" --type pdf
```

---

## 项目结构

```
ai-podcast-dual-host/
├── SKILL.md                        # skill 入口（含 frontmatter）
├── README.md                       # 本文档
├── DEVELOPMENT.md                  # 开发文档与架构说明
├── VERSION_LOG.md                  # 版本历史
├── agents/                         # Agent Prompts
│   ├── unified-research-agent.md   # 统一研究引擎（本地 Doubao）
│   ├── external-research-agent.md  # 外部 Sub-Agent 研究引擎
│   ├── script-generator.md         # 脚本生成器
│   ├── persona-extractor.md        # Persona 提取 Agent
│   └── external-persona-extractor.md
├── config/                         # 配置文件
│   ├── default-persona.json        # 默认主持人配置
│   ├── tts_voices.json             # TTS 音色配置
│   ├── presets/                    # 8 种风格预设
│   ├── styles/                     # 5 种对话风格模板
│   └── user_personas/              # 用户 Persona 存储
├── examples/                       # 示例代码
│   └── research_package_example.py
├── src/                            # 核心源代码
│   ├── podcast_pipeline.py         # 主 Pipeline
│   ├── volcano_client_requests.py  # API 客户端（流式支持）
│   ├── streaming_json_assembler.py # JSON 流式组装器
│   ├── tts_controller.py           # TTS 控制器
│   ├── persona_manager.py          # Persona 管理器
│   ├── persona_extractor.py        # Persona 提取器
│   ├── persona_resolver.py         # Persona 匹配/解析
│   ├── script_generator.py         # 脚本生成器
│   ├── setup_wizard.py             # 首次配置向导
│   ├── web_scraper.py              # 网页抓取
│   └── pdf_parser.py               # PDF 解析
└── tests/                          # 测试目录
    ├── test_e2e_complete.py
    ├── test_tts_*.py
    ├── test_pdf_parser.py
    └── persona-resource/
```

---

## 配置说明

### TTS 配置

设置环境变量启用音频生成功能：

```bash
# Windows
set VOLCANO_TTS_APP_ID=your_app_id
set VOLCANO_TTS_ACCESS_TOKEN=your_access_token
set VOLCANO_TTS_SECRET_KEY=your_secret_key

# Linux/Mac
export VOLCANO_TTS_APP_ID=your_app_id
export VOLCANO_TTS_ACCESS_TOKEN=your_access_token
export VOLCANO_TTS_SECRET_KEY=your_secret_key
```

### Persona 配置

Persona 采用三层结构：`identity`（身份原型）+ `expression`（说话风格）+ `memory_seed`（记忆种子）。支持三种创建方式：
- **风格预设**：一键应用 8 种知名播客风格
- **一句话描述**：如"像鲁豫那样温暖的女主持，搭配沉稳理性的男嘉宾"，自动生成
- **文档提取**：上传人物访谈/自传，提取真实人格

---

## 风格对标预设

| 预设名称 | 风格特点 | 适用场景 |
|---------|---------|---------|
| **十三邀-许知远** | 知识分子式追问，书籍引用，时代焦虑 | 深度人物访谈、思想探讨 |
| **鲁豫有约-鲁豫** | 温情倾听，故事挖掘 | 人物专访、情感故事 |
| **定义-易立竞** | 犀利直接，直击要害 | 争议话题、真相探究 |
| **圆桌派-窦文涛** | 朋友闲聊，发散联想，互相调侃 | 文化话题、轻松讨论 |
| **罗永浩的十字路口** | 理想主义，激情表达 | 创业故事、产品发布 |
| **梁文道・八分** | 冷静克制，知识分享 | 文化解读、深度思考 |
| **姜思达** | 独特视角，自我表达 | 个人叙事、新锐话题 |
| **李诞** | 幽默解构，降维打击 | 轻松话题、生活吐槽 |

---

## 测试

```bash
# 端到端完整测试（推荐）
python tests/test_e2e_complete.py

# TTS 专项测试
python tests/test_tts_comprehensive.py      # 综合测试
python tests/test_tts_connection_reuse.py   # 连接复用
python tests/test_tts_context.py            # 引用上文
python tests/test_tts_dual_speaker.py       # 双发音人
python tests/test_tts_long_text.py          # 长文本压力

# Persona 测试
python tests/persona-resource/extract_e2e.py
python tests/persona-resource/generate_audio_final.py
```

---

## 相关文档

- [SKILL.md](SKILL.md) — Claude Code skill 定义文档
- [DEVELOPMENT.md](DEVELOPMENT.md) — 架构设计与 Sub-Agent 集成
- [VERSION_LOG.md](VERSION_LOG.md) — 版本更新历史

---

MIT License © [liaozicen666-tech](https://github.com/liaozicen666-tech)
