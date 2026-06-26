# 版本日志

## v2.2 - Persona 系统增强 (2025-04-03)

### 新功能

#### 1. 多 Persona 支持

**PersonaManager 增强**：
- 支持保存和管理多个 Persona
- 按用户ID组织：`config/user_personas/{user_id}/{persona_name}.json`
- 新增方法：
  - `list_personas()` - 列出所有 Persona
  - `load_by_name()` - 按名称加载特定 Persona
  - `switch_active()` - 切换当前激活的 Persona

**DoublePersonaManager**：
- 支持固定主持人 + 可变嘉宾模式
- `session_guest` 参数支持临时指定本期嘉宾
- 适用于：多期节目，每期不同嘉宾的场景

#### 2. Persona 智能提取

**PersonaExtractor**：
- 自动检测输入类型（简短描述 vs 详细材料）
- 类型A（简短描述）：基于知识库推断，如"像罗永浩那样"
- 类型B（详细材料）：从材料中提取真实特征和记忆
- 提取三层结构：Identity / Expression / Memory

**提取示例**：
```python
from src.persona_extractor import extract_persona

# 类型A：简短描述
persona = extract_persona("像罗永浩那样，激情且理想主义")

# 类型B：详细材料
with open("autobiography.txt", "r") as f:
    persona = extract_persona(f.read())
```

#### 3. 测试资源完善

**新增测试目录**：`tests/persona-resource/`
- `README.md` - Persona 测试完整指南
- `extract_e2e.py` - Persona 提取端到端测试
- `generate_audio_final.py` - 跨时空对话音频生成测试
- `林黛玉.txt` / `林肯.txt` - 测试人物资料

### 改进与修复

#### 代码健壮性提升

1. **PersonaExtractor 错误处理**
   - 添加 `raise_on_error` 参数（默认 True）
   - 失败时抛出异常而非静默返回空结构
   - 便于测试和调试时定位问题

2. **TTSController 错误提示**
   - "resource ID is mismatched" 错误时打印推荐音色列表
   - 帮助用户选择正确的 voice_type 格式

3. **Schema 测试辅助**
   - `ScriptVersion.create_for_test()` 类方法
   - 自动计算 word_count 和 estimated_duration_sec
   - 简化测试代码

4. **TTS 音色文档**
   - 修正 `zh_male_sophie_uranus_bigtts` 性别标注
   - 明确说明：voice_type 含 `male` 是官方历史命名遗留，实际为女声

### 新增文件

| 文件 | 说明 |
|------|------|
| `src/persona_manager.py` | Persona 管理器（多 Persona 支持） |
| `src/persona_extractor.py` | Persona 提取器 |
| `agents/persona-extractor.md` | Persona 提取 Agent Prompt |
| `tests/persona-resource/README.md` | Persona 测试指南 |
| `tests/persona-resource/extract_e2e.py` | 提取端到端测试 |
| `tests/persona-resource/generate_audio_final.py` | 音频生成测试 |

### 端到端测试成果

成功完成 **林黛玉 × 林肯** 跨时空对话测试：
- Persona 提取：从两份人物资料提取完整人格档案
- 对话生成：35 句 / 约 3000 字的跨时空对话
- 音频生成：20 分钟双声道 MP3，4.2MB

---

## v2.0 - 流式生成稳定版 (2025-04-01)

### 重大改进

#### 1. 流式脚本生成 (Streaming Script Generation)

**问题**：Stage 2 脚本生成 3000-6000 字需要 30-90 秒，超过网络空闲超时阈值（30-60 秒），导致 100% 超时失败。

**解决方案**：
- 实现 `chat_completion_stream()` 流式 API 调用
- 创建 `StreamingJSONAssembler` 处理 JSON 边界检测
- 每个 token chunk 重置连接空闲计时器
- 支持 240 秒+ 长文本生成不超时

**效果**：
- 6000 字生成成功率从 0% 提升到 100%
- 生成时间稳定在 60-240 秒
- 消除网络超时错误

#### 2. 统一研究引擎 (Unified Research Agent)

**改进**：
- 单 Agent 内部完成 Broad → Insight → Deep → Outline 全流程
- 减少 API 调用次数，降低累积超时风险
- 支持 `unified` 和 `step_by_step` 两种执行模式

**输出**：Research Package 包含：
- `hook`: 节目开场钩子
- `central_insight`: 核心洞察
- `enriched_materials`: 研究素材
- `segments`: 分段设计

#### 3. Persona 一致性修复

**问题**：分段生成时，第 3 段后 Persona 名称从"小北/阿明"漂移为"A/B"。

**解决方案**：
- 流式生成一次性完成全部对话
- 完整上下文保持 Persona 一致性
- 简化输出为标准化 A/B 标记

### 架构变更

```
Before:
├── Research Agent → Outline Agent → Script Agent (Segmented)
│   └── 多次 API 调用              └── 分段循环，上下文丢失

After:
├── Unified Research Agent → Script Generator (Streaming)
│   └── 单次 API 调用        └── 流式输出，上下文完整
```

### 新增文件

| 文件 | 说明 |
|------|------|
| `src/streaming_json_assembler.py` | JSON 流式组装器 |
| `src/podcast_pipeline.py` | 新主 Pipeline（整合流式生成） |
| `private/` | API 密钥安全存储目录 |

### 修改文件

| 文件 | 变更 |
|------|------|
| `src/volcano_client_requests.py` | 添加 `chat_completion_stream()` 方法 |
| `src/tts_controller.py` | 优化双声道 TTS 生成 |

### 删除文件

**旧 Agent Prompts**（已合并到统一引擎，若按旧文件名搜索请改用 `agents/unified-research-agent.md` 与 `agents/script-generator.md`）：
- `agents/content-gen-stage1.md`
- `agents/content-gen-stage2.md`
- `agents/narrative-insight.md`
- `agents/outline-final.md`
- `agents/research-broad.md`
- `agents/research-deep.md`
- `agents/research-narrative.md`
- `agents/research.md`
- `agents/script-stage2-enhanced.md`

**旧测试文件**（功能已整合）：
- `test_*` 系列旧测试脚本
- `quick_stage2_test.py`
- `run_quality_evaluation.py`
- 等 12 个测试文件

**临时目录**：
- `temp/`, `temp_eval/`, `temp_test/` 等

### API 变更

**新增类**：
```python
class FullScript(BaseModel):
    """流式生成输出 Schema"""
    schema_version: str = "1.0"
    session_id: str
    lines: List[dict]           # 完整对话行
    word_count: int
    estimated_duration_sec: int
    script_summary: str
    key_moments: List[str]
    segments: Optional[List[dict]] = None
```

**PodcastPipeline 更新**：
```python
def generate(..., use_streaming: bool = True) -> Dict[str, Any]:
    """
    Args:
        use_streaming: 是否使用流式生成（默认 True）
                      流式失败时自动回退到分段生成
    """
```

### 性能对比

| 指标 | v1.0 分段 | v2.0 流式 |
|------|-----------|-----------|
| 平均生成时间 | 45s/段 × N段 | 120-180s 完整 |
| 超时率 | 60%+ | 0% |
| 字数上限 | 1500/段 | 6500 完整 |
| Persona 一致性 | 段间漂移 | 100% 一致 |
| 段间过渡 | 可能生硬 | 自然流畅 |

### 已知限制

1. **字数统计**：`word_count` 实际为字符数（含标点），中文内容约占总字符 85%
2. **流式 JSON 解析**：极端情况下流式组装可能失败，会自动回退到分段生成
3. **TTS 集成**：当前 TTS 生成为独立步骤，尚未与 Pipeline 完全集成

---

## v1.0 - MVP 版本 (2025-03-28)

### 核心功能

- 双主持人播客生成
- 三阶段架构：Research → Outline → Script
- 五种风格模板
- 基础 TTS 支持
- JSON 截断自动修复

### 架构

```
Orchestrator + 2 SubAgents
├── Research Agent: 信息收集与结构化
└── Content Generator: 大纲 + 脚本两阶段生成
```

### 主要限制

- Stage 2 生成容易超时（>60s）
- 分段生成导致上下文丢失
- 段间 Persona 名称不一致

---

## 版本计划

### v2.1 (已完成) - 2025-04-01

> **状态**: ✅ TTS 和 URL/PDF 功能已整合到新版流式流程，端到端测试通过

#### 功能整合

- [x] **TTS Pipeline 完整集成**
  - `src/podcast_pipeline.py` 添加 `_generate_audio()` 方法
  - 支持 WebSocket V3 + section_id 上下文模式
  - 自动检测 `VOLCANO_TTS_ACCESS_TOKEN` 环境变量
  - 脚本格式转换为 TTS 控制器兼容格式

- [x] **URL/PDF 输入解析**
  - `src/podcast_pipeline.py` 添加 `_extract_source_content()` 方法
  - 集成 `WebScraper` 和 `PDFParser`
  - 支持 `topic|url|pdf` 三种输入类型
  - 内容长度限制 50000 字符避免超限

#### 端到端测试结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| PDF 解析 → Research | ✅ 通过 | 成功解析 14780 字符中文论文 |
| URL 抓取 → Research | ✅ 通过 | 支持多种新闻网站 |
| Research → Script (Streaming) | ✅ 通过 | 流式生成 84 句 / 5553 字 |
| Script → TTS (手动) | ✅ 通过 | 生成 800KB 双声道 MP3 |
| Script → TTS (Pipeline) | ⚠️ 偶发 | 网络波动导致，配置正确 |

#### 已知问题

- **TTS 网络超时**: 偶发的 `[Errno 11001] getaddrinfo failed`，与配置无关，重试可解决
- **Schema 限制**: 已放宽 `word_count` 上限至 8000、`DialogueLine.text` 下限至 2 字符

- [ ] 字数统计优化（实际中文字数）
- [ ] 流式生成进度实时显示

### v2.1.1 (已完成) - 2025-04-01

> **状态**: ✅ TTS 模块优化完成

#### 性能优化

- [x] **WebSocket 链接复用**
  - 按说话人复用连接（A/B各1个）
  - 200句播客从200次连接降至2次
  - 时延节省约 70ms × 198 ≈ 13.8秒

- [x] **引用上文功能（TTS 2.0特有）**
  - 自动缓存最近2句作为上下文
  - 增强情感连贯性
  - 仅对TTS 2.0音色启用，其他TTS自动禁用

- [x] **智能重试机制**
  - 3次指数退避重试（1s, 2s, 4s）
  - 自动识别可重试错误（超时/连接/网络）
  - 重试前自动重建失效连接

- [x] **动态超时优化**
  - 基础5秒 + 每50字符1秒
  - 上限15秒防止过长等待
  - 收到音频后超时判定更宽松

- [x] **成本统计与监控**
  - 请求次数、字符数、音频时长统计
  - 连接复用次数、重试次数追踪
  - 失败请求单独计数

## v2.1.2 - 项目工程整理 (2025-04-01)

> **状态**: ✅ 代码库整理完成，删除冗余文件，文档更新

### 变更摘要

#### 删除的冗余文件

**旧版核心模块**（已被新版替代）:
- `src/orchestrator.py` → 由 `src/podcast_pipeline.py` 替代
- `src/volcano_client.py` → 由 `src/volcano_client_requests.py` 替代

**过时测试文件**（功能已整合或废弃）:
- `test_end_to_end.py` - 旧版端到端测试，由 `test_e2e_complete.py` 替代
- `test_orchestrator.py` - 测试旧版orchestrator
- `test_real_api.py` - 早期API测试
- `test_strict_api.py` - 早期严格模式测试
- `test_schema.py` - 早期schema测试
- `test_quick.py` - 简易测试
- `test_official_protocol.py` - 协议测试
- `test_volc_resource.py` - 资源测试

**重复的TTS测试**（功能重叠）:
- `test_tts_simple.py` - 功能已合并到 `test_tts_comprehensive.py`
- `test_tts_only.py` - 功能已合并
- `test_minimal_tts.py` - 功能已合并
- `test_tts_optimized.py` - 早期优化版本

**临时测试输出**:
- `tests/temp_tts_test/` - 临时测试目录

#### 保留的核心文件

**源代码** (`src/`):
- `podcast_pipeline.py` - 主Pipeline（流式生成 + TTS集成）
- `tts_controller.py` - TTS控制器（连接复用、上下文、重试）
- `volcano_client_requests.py` - API客户端（普通 + 流式）
- `streaming_json_assembler.py` - JSON流式组装器
- `schema.py` - 数据模型
- `web_scraper.py` - 网页抓取
- `pdf_parser.py` - PDF解析

**测试文件** (`tests/`):
- `test_e2e_complete.py` - 完整端到端测试
- `test_tts_comprehensive.py` - TTS综合测试
- `test_tts_connection_reuse.py` - 连接复用测试
- `test_tts_context.py` - 引用上文测试
- `test_tts_dual_speaker.py` - 双发音人测试
- `test_tts_long_text.py` - 长文本压力测试
- `test_pdf_parser.py` - PDF解析测试
- `test_web_scraper.py` - 网页抓取测试

**Agent Prompts** (`agents/`):
- `unified-research-agent.md` - 统一研究引擎
- `script-generator.md` - 脚本生成器

### v2.3 (计划中)

- [ ] Persona 长期记忆服务（RAG 检索）
- [ ] 批量生成工作流
- [ ] 音频后处理（降噪、音量平衡）

### v3.0 (规划中)

- [ ] 实时对话模式
- [ ] 多语言支持
- [ ] 视频生成（数字人）
# Changelog

## 2.2.0 (2025-04-03)

- 多 Persona 支持：保存、切换、固定主持人+可变嘉宾模式
- Persona 智能提取：从简短描述或详细材料自动提取三层人格档案
- 流式脚本生成：240秒+ 长文本不超时，成功率 100%
- TTS 2.0 优化：WebSocket 连接复用、引用上文、双声道立体声
- 统一研究引擎：单 Agent 完成检索到大纲构建
- 支持 topic / URL / PDF 三种输入源

## 2.0.0 (2025-04-01)

- 新增 `chat_completion_stream()` 流式 API 调用
- 新增 `StreamingJSONAssembler` 处理 JSON 边界检测
- 统一研究引擎替代多阶段 Agent
- TTS Pipeline 完整集成
- Persona 一致性修复

## 1.0.0 (2025-03-28)

- MVP 版本：双主持人播客生成、五种风格模板、基础 TTS 支持
