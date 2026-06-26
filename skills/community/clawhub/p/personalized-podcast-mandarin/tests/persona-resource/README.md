# Persona 跨时空对话测试指南

本目录包含端到端测试所需的资源和说明。

## 快速开始

### 1. 配置 API Key

API Key 存放在项目根目录的 `private/` 文件夹中：

```
ai-podcast-dual-host/
├── private/
│   ├── research Agent.txt    # Doubao API Key
│   ├── TTS.txt               # 火山引擎 TTS 配置
│   └── content Agent.txt
```

**方法一：直接设置环境变量**
```bash
# Doubao API (用于 LLM 生成)
set DOUBAO_API_KEY=bea84e03-aa7f-4d9c-9a24-60f70493da11

# 或设置 ARK_API_KEY（二选一）
set ARK_API_KEY=bea84e03-aa7f-4d9c-9a24-60f70493da11

# TTS API (用于语音合成)
set VOLCANO_TTS_APP_ID=2467721245
set VOLCANO_TTS_ACCESS_TOKEN=sO9sDDlzCsfz8rrSITooQ3JlThxiCwlX
```

**方法二：使用 private 目录文件**
Python 会自动读取 `private/` 目录下的配置（如果已实现）。

### 2. 运行端到端测试

```bash
python tests/persona-resource/extract_e2e.py
```

这将：
1. 从 `林黛玉.txt` 和 `林肯.txt` 提取 Persona
2. 生成跨时空对话脚本
3. 保存结果到 `output/` 目录

### 3. 生成音频

```bash
python tests/persona-resource/generate_audio_final.py
```

**注意**：需要使用正确的音色 ID。

## 音色配置说明

有效的音色 ID 格式（不是 BV001/BV005）：

| 角色 | 推荐音色 | voice_type |
|------|----------|------------|
| 磁性女声 | 魅力苏菲 2.0 | `zh_male_sophie_uranus_bigtts` ⚠️ |
| 年轻男性 | 少年梓辛 2.0 | `zh_male_shaonianzixin_uranus_bigtts` |
| 专业男性 | 刘飞 2.0 | `zh_male_liufei_uranus_bigtts` |
| 温柔女声 | 小何 2.0 | `zh_female_xiaohe_uranus_bigtts` |
| 知性女声 | 知性灿灿 2.0 | `zh_female_cancan_uranus_bigtts` |
| 甜美女声 | 甜美桃子 2.0 | `zh_female_tianmeitaozi_uranus_bigtts` |

### ⚠️ 常见误区

**"苏菲" 音色是男声！**
- `zh_male_sophie_uranus_bigtts` 官方命名为"魅力苏菲 2.0"
- ⚠️ **实际是磁性女声**，但 voice_type 含 `male` 是官方命名遗留
- 不要被 `male` 字样误导

**不要使用旧版标识**
- ❌ `BV001`, `BV005` - 已弃用
- ✅ `zh_male_sophie_uranus_bigtts` - 正确格式

完整列表见：
- `config/tts_voices.json` - 完整配置
- `api/TTS-voice-list.json` - 简洁列表

## 测试文件说明

| 文件 | 说明 |
|------|------|
| `林黛玉.txt` | 林黛玉人物资料（用于提取Persona） |
| `林肯.txt` | 林肯人物资料（用于提取Persona） |
| `extract_e2e.py` | 端到端测试脚本 |
| `generate_audio_final.py` | 音频生成脚本 |
| `output/` | 输出目录 |

## 输出文件

运行测试后生成：

```
output/
├── daiyu_e2e.json              # 林黛玉 Persona
├── lincoln_e2e.json            # 林肯 Persona
├── cross_time_script.txt       # 对话脚本（文本）
├── cross_time_script_e2e.json  # 对话脚本（JSON）
├── cross_time_podcast.mp3      # 完整音频
└── audio/                      # 分句音频
    ├── line_000_A.mp3
    ├── line_001_B.mp3
    └── ...
```

## 故障排查

### 问题：API Key 无效
```
ValueError: API key is required. Set DOUBAO_API_KEY environment variable.
```
**解决**：检查环境变量是否正确设置

### 问题：TTS resource ID 不匹配
```
RuntimeError: TTS合成失败... resource ID is mismatched...
```
**解决**：使用正确的 voice_type（不是 BV001/BV005）

### 问题：ScriptVersion 验证失败
```
pydantic.error_wrappers.ValidationError: ...
```
**解决**：使用 `ScriptVersion.create_for_test()` 创建测试实例

```python
from src.schema import ScriptVersion, DialogueLine

lines = [DialogueLine(speaker="A", text="...")]
script = ScriptVersion.create_for_test(lines)
```

### 问题：网络代理错误
```
urllib3.exceptions.ProxyError: Unable to connect to proxy
```
**解决**：代码已自动清理代理环境变量，如仍有问题手动检查：
```bash
set HTTP_PROXY=
set HTTPS_PROXY=
```

## 测试脚本示例

```python
import os
os.environ['DOUBAO_API_KEY'] = 'your_key'

from src.persona_extractor import extract_persona

# 测试提取（失败会抛出异常）
persona = extract_persona("像罗永浩那样", raise_on_error=True)

# 或安全模式（失败返回空结构）
persona = extract_persona("像罗永浩那样", raise_on_error=False)
```

## 注意事项

1. **API 调用费用**：端到端测试会消耗 Doubao API 和 TTS API 的配额
2. **音频生成时间**：生成 30 分钟音频约需 2-5 分钟
3. **文件编码**：所有文本文件使用 UTF-8 编码
4. **网络环境**：确保可以访问火山引擎 API（北京节点）
