---
name: ai-podcast-dual-host
description: >
  使用此 skill 当用户想要将 URL、PDF 或任意主题生成带有双声道 TTS 音频的
  双人对话播客。适用于双人讨论节目、指定主持人 persona（如鲁豫、罗永浩、
  李诞风格）、或将文章与资料转化为可收听音频内容的场景。
---

# AI 双主持人播客生成器 v2.2

将任意 URL / PDF / 主题 转化为结构化双主持人对谈内容 + 双声道 TTS 音频。

## 核心特性

- **生成摘要展示**：生成完成后自动展示内容亮点、段落结构和输出文件
- **流式脚本生成**：解决长文本动态字数超时问题，成功率100%
- **可选外部研究引擎**：支持由 OpenClaw / Claude Code 等主 Agent 调用 Sub-Agent 完成真实网络检索
- **统一研究引擎（本地Fallback）**：单 Agent 完成从泛化检索到大纲构建的全流程
- **三层Persona配置**：风格对标预设 / 一句话生成 / 文档提取，支持固定主持人+可变嘉宾模式
- **TTS 2.0 优化**：WebSocket连接复用、引用上文、智能重试、动态超时
- **多种输入源**：主题、URL、PDF三种输入方式
- **5种风格模板**：高效传达、发散漫谈、深度对谈、观点交锋、喜剧风格
- **双声道立体声**：A左声道、B右声道，收听体验更佳
- **动态字数控制**：默认约8-12分钟（2500字），支持由大纲或用户参数扩展

## 触发条件

当用户有以下需求时，使用此 skill：

| 场景 | 示例 |
|------|------|
| 生成播客 | "生成一期关于AI的播客" |
| 文章转对话 | "把这篇文章转成两人对话形式" |
| 音频内容 | "将这篇论文转为可听的音频" |
| 双人对话 | "做一个关于科技趋势的对谈节目" |
| TTS音频 | "生成带配音的播客脚本" |
| 带Persona的播客 | "用郭德纲风格讲量子力学" / "像我上次配的鲁豫风格那样讲这篇文章" |

**不应使用此 skill 的场景**：
- 简单文本摘要（不需要播客格式）
- 单人独白（非双人对话）
- 纯文本输出（不需要音频）

## 使用方法

### 命令行

```bash
# 从主题生成（默认）
python -m src.podcast_pipeline "人工智能的发展趋势" --style 深度对谈

# 从 URL 生成
python -m src.podcast_pipeline "https://example.com/article" --type url --style 观点交锋

# 从 PDF 生成
python -m src.podcast_pipeline "./paper.pdf" --type pdf --style 高效传达

# 跳过音频、指定目标字数
python -m src.podcast_pipeline "主题" --skip-audio --target-length 3000
```

### Python API — 本地完整模式

```python
from src.podcast_pipeline import PodcastPipeline

pipeline = PodcastPipeline()
result = pipeline.generate(
    source="人工智能的发展趋势",
    source_type="topic",
    style="深度对谈",
    output_dir="./my_podcasts",
    verbose=True
)

print(f"Session ID: {result['session_id']}")
print(f"音频文件: {result['audio_path']}")
print(f"脚本行数: {sum(len(seg['lines']) for seg in result['script'])}")
```

### Python API — Sub-Agent Research 注入模式

```python
from src.podcast_pipeline import PodcastPipeline

# 外部 Sub-Agent 已完成真实网络检索
research_pkg = { ... }  # 参见 examples/research_package_example.py

pipeline = PodcastPipeline(skip_client_init=True)
result = pipeline.generate(
    source="人工智能的发展趋势",
    source_type="topic",
    research_package=research_pkg,
    output_dir="./my_podcasts",
    verbose=True
)
```

完整 Sub-Agent 注入示例见 [`examples/research_package_example.py`](examples/research_package_example.py)。

## 自然语言 Persona 处理

当用户的输入涉及 Persona 需求时，由你（外层 Agent）**直接调用底层工具函数**，无需等待内部路由。核心工具是 `PersonaResolver`，它封装了匹配/创建/保存/更新的完整逻辑。

### Persona 使用决策树

#### 1. 首次使用检测
调用 `PersonaResolver(user_id).resolve()` 或 `check_first_time(user_id)`。若 `is_first_time=True`，**必须先询问用户**希望主持人是什么风格，不要默默使用默认。

> 建议话术："这是你第一次使用播客生成skill。你希望播客主持人是什么风格？例如：十三邀的风格、郭德纲与林志玲聊天的感觉、或者给我一篇文章，我来提取真实人物人格。"

#### 2. 非首次使用
- **用户未提及 Persona**（无描述、无文档、无 preset）  
  → 直接使用上次保存的 `default.json`（无需额外参数）。

- **用户给出自然语言描述**（如"用郭德纲风格"、"像鲁豫那样"）  
  → 调用 `PersonaResolver.find_matching_persona(description)`。它会先精确匹配 preset / saved persona 名称，再使用轻量级 LLM 语义匹配。  
  - 若命中：直接使用该 persona，并同步为 default。  
  - 若未命中：自动生成新的双人 persona，保存为 default。

- **用户提供了文档/文本**（如"用这篇访谈里的人物风格来讲"）  
  → 将文档内容作为 `document_text` 参数传入 `generate()`。Pipeline 内部会自动完成：提取 persona → 匹配是否已有 → 更新或创建 → 保存为 default。

### 推荐调用方式

```python
from src.podcast_pipeline import PodcastPipeline
from src.persona_resolver import PersonaResolver

# 场景 A：用户说"用郭德纲风格讲量子力学"
resolver = PersonaResolver()
result = resolver.resolve(explicit_description="郭德纲风格")
# result.source 可能为 "description_matched"（已有）或 "description_new"（新建）

pipeline = PodcastPipeline()
pipeline.generate(
    source="量子力学",
    source_type="topic",
    persona_config=result.persona_config,
    style="喜剧风格"
)

# 场景 B：用户上传了文档
pipeline = PodcastPipeline()
pipeline.generate(
    source="科技趋势",
    source_type="topic",
    document_text=open("interview.txt", "r", encoding="utf-8").read(),
    style="深度对谈"
)

# 场景 C：首次使用，必须主动确认
resolver = PersonaResolver()
first = resolver.resolve_first_time()
if first.is_first_time:
    # 向用户提问，获取描述后再调用 resolver.resolve(explicit_description=...)
    pass
```

## 输入参数

### 必需参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `source` | str | 输入内容：主题文本 / URL / PDF文件路径 |
| `source_type` | str | 输入类型：`topic` / `url` / `pdf` |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `style` | str | `auto` | **对话风格**：`auto` / 深度对谈 / 观点交锋 / 发散漫谈 / 高效传达 / 喜剧风格 |
| `persona_config` | dict | None | 自定义主持人配置（覆盖默认） |
| `research_package` | dict | None | 外部 Sub-Agent 提供的 Research Package（提供时跳过本地 Research） |
| `output_dir` | str | `./output` | 输出目录 |
| `verbose` | bool | True | 是否打印详细日志 |
| `skip_audio` | bool | False | 是否跳过音频生成 |
| `pause_before_audio` | bool | False | 是否在音频生成前暂停，等待用户确认 |
| `target_length` | int | None | 显式指定目标字数（优先级最高），默认由大纲动态计算 |

## 输出格式

### 返回数据

```python
{
    "session_id": str,
    "source": str,
    "source_type": str,
    "style": str,
    "research": dict,
    "script": List[dict],
    "audio_path": Optional[str],
    "timestamp": str
}
```

### 生成文件

在 `output_dir` 目录下生成：

| 文件 | 格式 | 说明 |
|------|------|------|
| `podcast_{session_id}.json` | JSON | 完整数据（research + script） |
| `podcast_{session_id}.md` | Markdown | 可读对话格式 |
| `podcast_{session_id}.mp3` | MP3 | 双声道音频（TTS配置后） |

## 前置条件

- **API Key**：配置 `DOUBAO_API_KEY`（用于 Research 和 Script 生成）
- **TTS（可选）**：配置 `VOLCANO_TTS_APP_ID` 和 `VOLCANO_TTS_ACCESS_TOKEN`（不配置时只生成文本）
- **音色推荐**：见 `config/tts_voices.json` 中的 `_meta.notes`

更多安装配置、Persona 管理、风格预设、文件结构详见 [README.md](README.md)。

## Sub-Agent 模式

如果你使用 **Claude Code**、**OpenClaw** 等具备 WebSearch 能力的 Agent：
1. 主 Agent 调用 `agents/external-research-agent.md` 定义的 Sub-Agent 完成真实检索
2. 主 Agent 将返回的 `ResearchPackage` 直接注入 `PodcastPipeline.generate(..., research_package=pkg)`
3. 本地 Pipeline 跳过 Research，直接执行 Script Generation + TTS

Sub-Agent 详情与数据结构说明见 [DEVELOPMENT.md](DEVELOPMENT.md)。

## 性能指标

| 阶段 | 时间 | 说明 |
|------|------|------|
| Research | ~10-15s | 单次API调用 |
| Script (流式) | ~60-300s | 2000-8000+字符（动态），无超时 |
| TTS (优化后) | ~60-300s | 40-200句，连接复用 |
| **总计** | **~4-10分钟** | 生成8-35分钟播客 |

## 测试

```bash
# 端到端测试
python tests/test_e2e_complete.py

# TTS 专项测试
python tests/test_tts_comprehensive.py
python tests/test_tts_connection_reuse.py
python tests/test_tts_context.py
python tests/test_tts_long_text.py

# 功能回归验证
python tests/test_fix_validation.py
```

## 相关文档

- [README.md](README.md) — 项目介绍、快速开始、使用示例、Persona 管理
- [DEVELOPMENT.md](DEVELOPMENT.md) — 架构设计、开发规范、Sub-Agent 集成
- [VERSION_LOG.md](VERSION_LOG.md) — 版本历史
- [agents/external-research-agent.md](agents/external-research-agent.md) — 外部 Sub-Agent Prompt
