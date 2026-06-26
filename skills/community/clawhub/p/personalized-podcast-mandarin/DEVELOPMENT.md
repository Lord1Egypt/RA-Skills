# 开发文档

> 本文档面向项目开发者和维护者，说明架构设计、开发规范和调试方法。

## 目录

- [架构概述](#架构概述)
- [核心模块](#核心模块)
- [开发规范](#开发规范)
- [调试指南](#调试指南)
- [常见问题](#常见问题)
- [扩展开发](#扩展开发)

---

## 架构概述

### 系统架构 (v2.1+)

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Podcast System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌──────────────────────────────────────┐   │
│  │   Input     │───→│        PodcastPipeline               │   │
│  │ - Topic     │    │  ┌──────────┐      ┌──────────────┐  │   │
│  │ - URL       │    │  │  Stage 1 │─────→│   Stage 2    │  │   │
│  │ - PDF       │    │  │ Research │      │Script(Stream)│  │   │
│  └─────────────┘    │  └──────────┘      └──────────────┘  │   │
│                     └──────────────────────────────────────┘   │
│                              │                                   │
│                              ↓                                   │
│                     ┌──────────────────┐                        │
│                     │  TTS + Output    │                        │
│                     │  (MP3/JSON/MD)   │                        │
│                     └──────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 核心组件关系

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Input Sources  │────→│ PodcastPipeline │────→│  Output Files   │
│  - Topic        │     │                 │     │  - MP3 Audio    │
│  - URL          │     │ ┌─────────────┐ │     │  - JSON Data    │
│  - PDF          │────→│ │   Stage 1   │ │     │  - Markdown     │
└─────────────────┘     │ │   Research  │ │     └─────────────────┘
                        │ └─────────────┘ │
                        │ ┌─────────────┐ │
                        │ │   Stage 2   │ │
                        │ │ Script Gen  │ │
                        │ │ (Streaming) │ │
                        │ └─────────────┘ │
                        │ ┌─────────────┐ │
                        │ │    TTS      │ │
                        │ │(WebSocket)  │ │
                        │ └─────────────┘ │
                        └─────────────────┘
```

### 数据流

```
Input
  │
  ▼
┌───────────────────────────────────────────────────────────────┐
│ Stage 1: Research                                             │
│  - Unified Research Agent 生成 Research Package               │
│  - 包含: hook, central_insight, materials, segments          │
│  - 输出: ~500-1000 tokens, ~10-15秒                          │
└───────────────────────────────────────────────────────────────┘
  │
  ▼
┌───────────────────────────────────────────────────────────────┐
│ Stage 2: Script Generation (Streaming)                        │
│  - Script Generator 使用流式 API 生成完整对话                  │
│  - 输入: Research Package + Persona + Style                  │
│  - 输出: 2000-8000+ 字符（由大纲动态计算）, ~40-200 句, 60-300秒 │
└───────────────────────────────────────────────────────────────┘
  │
  ▼
Output (JSON + Markdown)
```

---

## 核心模块

### 1. PodcastPipeline

**文件**: `src/podcast_pipeline.py`

**职责**: 主流程编排，协调 Research、Script Generation 和 TTS 三个阶段。

**核心方法**:

```python
def generate(
    self,
    source: str,
    source_type: str = "topic",
    style: str = "深度对谈",
    persona_config: Optional[dict] = None,
    output_dir: str = "test_outputs/latest",
    verbose: bool = True
) -> Dict[str, Any]
```

**内部流程**:
1. `_run_research()` - 调用 Unified Research Agent
2. `_generate_script()` - 调用 Script Generator（流式）
3. `_generate_audio()` - 调用 TTS Controller 生成音频
4. `_save_markdown()` - 保存为 Markdown 格式

**流式生成逻辑**:
```python
def _generate_script(..., use_streaming: bool = True):
    if use_streaming:
        try:
            return self._generate_script_streaming(...)
        except Exception as e:
            # 流式失败时回退到分段生成
            return self._generate_script_segmented(...)
```

**TTS 集成**:
```python
def _generate_audio(...):
    # 检查 TTS 配置
    if not os.getenv("VOLCANO_TTS_ACCESS_TOKEN"):
        return None  # 跳过音频生成

    controller = VolcanoTTSController()
    # 转换脚本格式并生成双声道音频
    return controller.generate_dual_audio(script, output_path)
```

### 2. VolcanoArkClientRequests

**文件**: `src/volcano_client_requests.py`

**职责**: 火山引擎 Ark API 客户端，支持普通和流式两种调用方式。

**核心方法**:

| 方法 | 用途 | 超时 |
|------|------|------|
| `chat_completion()` | 普通非流式调用 | 180s |
| `chat_completion_stream()` | 流式调用 | 300s |

**流式实现要点**:

```python
def chat_completion_stream(self, ...):
    # 使用官方 Ark SDK 的流式接口
    stream = client.chat.completions.create(..., stream=True)

    assembler = StreamingJSONAssembler()
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ''
        result = assembler.feed(delta)
        if result:
            return result  # 获得完整 JSON
```

**注意**: 流式调用使用官方 `volcenginesdkarkruntime` SDK，而非 requests。

### 3. StreamingJSONAssembler

**文件**: `src/streaming_json_assembler.py`

**职责**: 处理流式输出中的 JSON 分割和组装。

**核心算法 - JSON 边界检测**:

```python
def feed(self, chunk: str) -> Optional[Dict[str, Any]]:
    self.buffer += chunk

    # 从 buffer 中查找完整 JSON 对象
    for i, char in enumerate(self.buffer):
        # 处理字符串中的转义
        if self.escape:
            self.escape = False
            continue
        if char == '\\':
            self.escape = True
            continue

        # 处理字符串引号
        if char == '"' and not self.escape:
            self.in_string = not self.in_string
            continue

        # 只在非字符串状态下处理括号
        if not self.in_string:
            if char == '{':
                if self.depth == 0:
                    self.json_start = i
                self.depth += 1
            elif char == '}':
                self.depth -= 1
                if self.depth == 0:
                    # 找到完整 JSON
                    json_str = self.buffer[self.json_start:i+1]
                    return json.loads(json_str)

    return None  # 尚未完整
```

**边界情况处理**:
- JSON 对象被分割在多个 chunk 中
- 字符串中包含 `{` 或 `}` 字符
- 转义字符 `\"` 正确处理
- 多个 JSON 对象连续输出

### 4. PersonaManager & DoublePersonaManager

**文件**: `src/persona_manager.py`

**职责**: Persona 的保存、加载、列表、切换管理，支持多 Persona 和固定主持人+可变嘉宾模式。

**PersonaManager 核心方法**:

```python
class PersonaManager:
    def save(self, persona: Dict[str, Any]) -> bool
    def load(self) -> Optional[Dict[str, Any]]
    def update(self, persona: Dict[str, Any]) -> bool
    def delete(self) -> bool

    @classmethod
    def list_personas(cls, user_id: str) -> List[Dict[str, Any]]
    # 返回: [{"name": str, "display_name": str, "archetype": str, "has_memory": bool}]

    @classmethod
    def load_by_name(cls, user_id: str, persona_name: str) -> Optional[Dict[str, Any]]

    @classmethod
    def switch_active(cls, user_id: str, persona_name: str) -> bool
    # 将指定 persona 复制为 default.json

    @staticmethod
    def format_for_display(persona: Dict[str, Any]) -> str
    @staticmethod
    def quick_adjust(persona: Dict[str, Any], adjustments: Dict[str, Any]) -> Dict[str, Any]
```

**DoublePersonaManager 核心方法**:

```python
class DoublePersonaManager:
    """双主持人配置 - 支持固定主持人 + 可变嘉宾模式"""

    def __init__(self, user_id: str, session_guest: Optional[str] = None):
        """
        Args:
            user_id: 用户ID
            session_guest: 本期嘉宾persona名称（可选，临时指定）
        """

    def save(self, host_a: Dict[str, Any], host_b: Dict[str, Any],
             host_a_name: str = "me", host_b_name: str = "partner") -> bool

    def load(self) -> Optional[tuple]:
        """返回: (host_a_persona, host_b_persona)"""

    def get_host_a_name(self) -> Optional[str]
```

**使用场景**:
- 用户想做多期节目，每期不同嘉宾：固定主持人 Persona + 临时嘉宾 Persona
- 用户想尝试不同风格：保存多个 Persona，按需切换

### 5. PersonaExtractor

**文件**: `src/persona_extractor.py`

**职责**: 从用户输入自动提取三层 Persona 档案。

**输入类型自动检测**:

| 类型 | 特征 | 处理方式 |
|------|------|----------|
| **类型A** | 简短描述（<100字）| 基于知识库推断，memory_seed为空 |
| **类型B** | 详细材料（自传、访谈）| 从材料提取真实特征和记忆 |

**核心方法**:

```python
def extract_persona(text: str, user_hint: str = "", raise_on_error: bool = True) -> Dict[str, Any]:
    """
    从文本提取三层 Persona 档案

    Args:
        text: 输入文本（简短描述或详细材料）
        user_hint: 用户额外提示
        raise_on_error: 失败时是否抛出异常（默认True）

    Returns:
        {
            "identity": {"name": ..., "archetype": ..., "core_drive": ..., "chemistry": ...},
            "expression": {"pace": ..., "sentence_length": ..., "signature_phrases": [...], "attitude": ...},
            "memory_seed": [...]  # 类型B有内容，类型A为空
        }
    """
```

**错误处理**:
- `raise_on_error=True`（默认）: API失败时抛出异常，便于定位问题
- `raise_on_error=False`: API失败时返回空结构，用于容错场景

### 6. TTSController

**文件**: `src/tts_controller.py`

**职责**: 火山引擎 TTS 2.0 WebSocket V3 接口封装，支持双声道输出。

**核心功能**:
- WebSocket链接复用（降低约70ms/次连接开销）
- 引用上文支持（TTS 2.0特有，增强情感连贯性）
- 智能重试机制（指数退避，自动重建失效连接）
- 成本统计与监控
- 长文本动态超时（根据文本长度自动调整）

**链接复用机制**:
```python
# 按说话人复用连接，减少WebSocket建连次数
# 200句播客 → 仅2次连接（A和B各1次）
# 时延节省: 约 (198 * 70ms) ≈ 13.8秒

controller = VolcanoTTSController()
# 同一人连续多句自动复用连接
# 说话人切换时才重建连接
```

**引用上文（TTS 2.0特有）**:
```python
# 自动缓存最近2句作为上下文
# 增强情感连贯性，无需手动管理
controller = VolcanoTTSController(enable_context=True)

# 内部实现：additions.context 字段
additions = {
    "section_id": previous_session_id,
    "context": "前一句文本内容"  # TTS 2.0特有
}
```

**成本统计**:
```python
cost_tracker = {}
controller = VolcanoTTSController(cost_tracker=cost_tracker)
# 生成完成后查看统计
print(f"请求次数: {cost_tracker['total_requests']}")
print(f"字符总数: {cost_tracker['total_chars']}")
print(f"连接复用: {cost_tracker['connection_reuses']}次")
print(f"重试次数: {cost_tracker['retry_count']}次")
```

**超时优化**:
- 动态超时：根据文本长度自动计算（基础5秒 + 每50字符1秒，上限15秒）
- 容错增强：最多3次连续超时后才判定失败
- 智能检测：收到音频后超时判定更宽松，避免过早终止

**关键实现细节**:
```python
# 空JSON结束信号检测（关键修复）
if audio_chunks and sid and event_type is None and audio_data is None:
    break  # 会话正常结束

# 动态超时计算
text_len = len(text)
base_timeout = 5
dynamic_timeout = min(base_timeout + text_len // 50, 15)
```

---

## 开发规范

### 代码风格

1. **类型注解**: 所有函数参数和返回值必须加类型注解
2. **文档字符串**: 类和方法必须有 docstring 说明
3. **错误处理**: 使用 try-except 捕获具体异常，不捕获裸异常
4. **日志输出**: 使用 `verbose` 参数控制详细程度，支持中文输出

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `PodcastPipeline`, `StreamingJSONAssembler` |
| 方法/函数 | snake_case | `generate_script`, `chat_completion_stream` |
| 常量 | UPPER_CASE | `DEFAULT_MODEL`, `API_BASE` |
| 私有方法 | _snake_case | `_run_research`, `_fix_truncated_json` |

### 文件组织

```
ai-podcast-dual-host/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── podcast_pipeline.py    # 主流程（新）
│   ├── volcano_client_requests.py  # API 客户端
│   ├── streaming_json_assembler.py # 流式 JSON 处理
│   ├── tts_controller.py      # TTS 控制器
│   ├── schema.py              # 数据模型
│   └── protocols/             # 协议定义
├── agents/                 # Agent Prompts
│   ├── unified-research-agent.md
│   └── script-generator.md
├── config/                 # 配置
│   ├── default-persona.json
│   └── styles/               # 风格模板
├── tests/                  # 测试
├── test_outputs/           # 测试输出（不提交 git）
├── private/                # API 密钥（不提交 git）
├── README.md               # 用户文档
├── DEVELOPMENT.md          # 本文档
└── VERSION_LOG.md          # 版本日志
```

### Git 规范

**不提交的文件**:
- `test_outputs/` - 测试输出文件
- `private/` - API 密钥
- `*.pyc`, `__pycache__/` - Python 缓存
- `.env` - 环境变量

**提交信息规范**:
```
feat: 添加流式生成功能
fix: 修复 JSON 解析错误
docs: 更新 README
refactor: 重构 Pipeline 架构
```

---

## 调试指南

### 启用详细日志

```python
pipeline = PodcastPipeline()
result = pipeline.generate(
    source="测试主题",
    verbose=True  # 启用详细输出
)
```

### 测试流式生成

```python
# 测试短文本
python -m src.podcast_pipeline "简短测试" --style 高效传达

# 测试长文本（6000字）
python -m src.podcast_pipeline "人工智能发展史详细梳理" --style 深度对谈
```

### 调试 JSON 组装

```python
from src.streaming_json_assembler import StreamingJSONAssembler

assembler = StreamingJSONAssembler()
chunks = ['{"a":', '1}', '{"b":', '2}']

for chunk in chunks:
    result = assembler.feed(chunk)
    if result:
        print(f"提取到: {result}")
```

### 检查 API 响应

在 `volcano_client_requests.py` 中添加调试输出:

```python
def chat_completion_stream(self, ...):
    ...
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ''
        print(f"[DEBUG] Chunk: {delta[:50]}...")  # 添加此行
        ...
```

### 常见问题排查

#### 问题 1: SSL 连接错误

**症状**: `EOF occurred in violation of protocol`

**原因**: 网络超时或代理问题

**解决**:
1. 检查网络连接
2. 确保使用流式生成（默认开启）
3. 尝试更换网络环境

#### 问题 2: JSON 解析失败

**症状**: `Failed to parse JSON response`

**原因**: 模型输出格式不正确或被截断

**解决**:
1. 检查 `_clean_json_content()` 是否移除 Markdown 代码块
2. 检查 `_fix_truncated_json()` 是否补全括号
3. 查看原始输出内容进行手动分析

#### 问题 3: 流式生成超时

**症状**: `Stream ended without complete JSON`

**原因**: 生成长度超过 `max_tokens` 限制

**解决**:
1. 增加 `max_tokens` 参数（默认 12000）
2. 减少生成字数要求
3. 系统自动回退到分段生成

#### 问题 4: Persona 名称不一致

**症状**: 对话中出现 "A/B" 而非配置的 "小北/阿明"

**原因**: 流式生成使用标准化输出

**解决**: 当前版本使用 A/B 标准化标记，TTS 阶段映射到具体音色

---

## 扩展开发

### 添加新风格模板

1. 在 `config/styles/` 创建新的 JSON 文件:

```json
{
  "name": "新风格",
  "description": "风格描述",
  "content_characteristics": {
    "data_density": "高",
    "storytelling_ratio": "中",
    "debate_intensity": "低"
  },
  "persona_interaction": {
    "interaction_frequency": "高",
    "interruption_style": "温和",
    "emotional_arc": "平稳"
  },
  "special_instructions": "特殊指令..."
}
```

2. 在 `podcast_pipeline.py` 的 `predefined_styles` 列表中添加新风格名

### 添加新 Agent

1. 在 `agents/` 创建新的 prompt 文件
2. 在 `PodcastPipeline._load_prompts()` 中加载
3. 实现对应的调用方法

### 修改流式生成逻辑

**关键文件**: `src/podcast_pipeline.py`

```python
def _generate_script_streaming(self, ...):
    # 1. 构建流式生成专用 prompt
    streaming_prompt = self.script_prompt + "\n## 流式生成要求\n..."

    # 2. 调用流式 API
    result, tokens = self.client.chat_completion_stream(...)

    # 3. 将完整脚本转换为分段格式
    full_script = []
    for i, seg in enumerate(segments):
        # 分配 lines 到各 segment
        ...

    return full_script
```

### 集成新的 TTS 引擎

1. 创建新的 TTS 客户端类
2. 实现 `synthesize(text, voice_id) -> audio_bytes` 方法
3. 在 `TTSController` 中添加新引擎支持

---

## API 参考

### Persona 结构

```python
{
    "identity": {
        "name": str,                    # 显示名称
        "archetype": str,               # 原型: 追问者/讲故事的人/观察者/吐槽者/理想主义者
        "core_drive": str,              # 核心驱动力
        "chemistry": str                # 与搭档互动方式
    },
    "expression": {
        "pace": "fast|normal|slow",
        "sentence_length": "short|mixed|long",
        "signature_phrases": List[str],  # 最多3个口头禅
        "attitude": "curious|skeptical|playful|mournful|authoritative"
    },
    "memory_seed": [                   # 类型B有内容，类型A为空
        {
            "title": str,
            "content": str,             # 100字以内
            "tags": List[str]
        }
    ]
}
```

### PersonaManager 类接口

```python
class PersonaManager:
    def __init__(self, user_id: str, persona_name: str = "default")
    def save(self, persona: Dict[str, Any]) -> bool
    def load(self) -> Optional[Dict[str, Any]]
    def update(self, persona: Dict[str, Any]) -> bool
    def delete(self) -> bool

    @classmethod
    def list_personas(cls, user_id: str) -> List[Dict[str, Any]]
    @classmethod
    def load_by_name(cls, user_id: str, persona_name: str) -> Optional[Dict[str, Any]]
    @classmethod
    def switch_active(cls, user_id: str, persona_name: str) -> bool
    @staticmethod
    def format_for_display(persona: Dict[str, Any]) -> str
    @staticmethod
    def quick_adjust(persona: Dict[str, Any], adjustments: Dict[str, Any]) -> Dict[str, Any]
```

### DoublePersonaManager 类接口

```python
class DoublePersonaManager:
    def __init__(self, user_id: str, session_guest: Optional[str] = None)
    def save(self, host_a: Dict, host_b: Dict, host_a_name: str = "me", host_b_name: str = "partner") -> bool
    def load(self) -> Optional[tuple]  # (host_a_persona, host_b_persona)
    def exists(self) -> bool
    def get_host_a_name(self) -> Optional[str]
```

### Research Package 结构

完整 Sub-Agent 注入示例见 `examples/research_package_example.py`。

```python
{
    "hook": str,                    # 开场钩子
    "central_insight": str,         # 核心洞察
    "style_selected": str,          # 选中的风格
    "enriched_materials": [         # 研究素材
        {
            "material_id": str,
            "source_type": str,
            "content": str,
            "key_insights": [str],
            "confidence_score": float
        }
    ],
    "segments": [                   # 分段设计
        {
            "segment_id": str,
            "narrative_function": str,
            "dramatic_goal": str,
            "content_focus": str,
            "estimated_length": int,
            "materials_to_use": [str]
        }
    ]
}
```

### Script 输出结构

```python
[
    {
        "segment_id": str,
        "lines": [
            {"speaker": "A", "text": str},
            {"speaker": "B", "text": str}
        ],
        "summary": str,
        "key_moments": [str],
        "word_count": int
    }
]
```

### PodcastPipeline.generate() 接口

**参数**:
```python
def generate(
    self,
    source: str,                    # 主题/URL/PDF路径
    source_type: str = "topic",      # topic|url|pdf
    style: str = "深度对谈",
    persona_config: Optional[dict] = None,
    output_dir: str = "test_outputs/latest",
    verbose: bool = True
) -> Dict[str, Any]:
```

**返回值**:
```python
{
    "session_id": str,
    "source": str,
    "source_type": str,              # topic|url|pdf
    "style": str,
    "research": dict,                # Research Package
    "script": List[dict],            # 分段脚本
    "audio_path": Optional[str],     # 音频文件路径（TTS配置后）
    "timestamp": str
}
```

### TTS 配置

**环境变量**:
```bash
VOLCANO_TTS_APP_ID=your_app_id
VOLCANO_TTS_ACCESS_TOKEN=your_access_token
VOLCANO_TTS_SECRET_KEY=your_secret_key
```

**注意**: 未配置 TTS 时播客脚本正常生成，但不会产生音频文件。

---

## 性能优化

### 当前性能指标

| 阶段 | 数值 | 说明 |
|------|------|------|
| Research 阶段 | ~10-15 秒 | 单次 API 调用 |
| Script 阶段 (流式) | ~60-240 秒 | 2000-8000+ 字符（动态） |
| TTS 阶段 | ~60-300 秒 | 40-200 句，连接复用后 |
| **总生成时间** | **~4-10 分钟** | 完整流程（Research + Script + TTS） |
| 对话行数 | 40-200 句 | 由目标字数动态计算 |
| 预估音频时长 | 8-35 分钟 | 由目标字数动态计算 |

### TTS 性能优化效果

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 每句合成时间 | 50-90 秒 | ~1 秒 | **90x** |
| 连接次数 (200句) | 200 次 | 2 次 | **100x** |
| 连接建立耗时 | ~70ms/次 | 接近0 | 节省 ~14秒 |
| 失败重试 | 无 | 3次指数退避 | 稳定性↑ |

### 优化建议

1. **并发优化**: Research 和 Script 阶段无法并行，但可考虑预加载
2. **缓存优化**: Research 结果可缓存，相同主题直接复用
3. **流式优化**: 当前已实现最优方案，无需进一步优化

---

## 安全注意事项

1. **API 密钥**: 存储在 `private/` 目录，永不提交到 git
2. **日志脱敏**: 生产环境日志中隐藏 API 密钥
3. **输入验证**: 所有用户输入经过 Pydantic Schema 验证
4. **超时保护**: API 调用设置合理的超时时间，防止资源泄漏
