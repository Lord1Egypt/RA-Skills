---
name: lobster-radio
description: "个性化资讯电台生成服务。使用场景：(1) 生成特定主题的电台，(2) 设置每日定时推送，(3) 配置TTS音色，(4) 收听历史电台。不适用：音乐播放、实时广播、视频内容。"
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["python3"]
  lobsterai:
    emoji: "🎙️"
    category: "productivity"
    requires:
      python: ">=3.10"
    permissions:
      - fileSystem
      - network
---

# 龙虾电台

个性化资讯电台生成服务，使用本地Qwen3-TTS模型，完全免费。

## 平台支持

- ✅ **OpenClaw** - 通过SKILL.md集成
- ✅ **LobsterAI(有道龙虾)** - 通过skill.json集成

## When to Use

✅ **USE this skill when:**
- "生成关于人工智能的电台"
- "每天早上8点推送科技新闻"
- "配置我的电台音色"
- "播放我的今日电台"
- "查看历史电台"

❌ **DON'T use this skill when:**
- 播放音乐 → 使用音乐播放器
- 实时广播 → 使用广播应用
- 视频内容 → 使用视频平台

## Prerequisites

### 安装Python依赖

```bash
pip install -r requirements.txt
```

### 下载Qwen3-TTS模型

**注意**: Qwen3-TTS模型**不在Ollama公共仓库中**，需要从HuggingFace或ModelScope下载。

#### 方法一：从HuggingFace下载（推荐）

```bash
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base
```

#### 方法二：从ModelScope下载（国内用户推荐）

```bash
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"
```

#### 方法三：首次运行时自动下载

Skill会在首次生成电台时自动检测并下载模型：

```bash
python scripts/generate_radio.py --topics "人工智能"
```

### 验证安装

```bash
python tests/verify_all.py
```

## Quick Start

### 生成电台

```bash
python scripts/generate_radio.py --topics "人工智能" --tags "科技"
```

### 配置TTS

```bash
python scripts/configure_tts.py --voice xiaoxiao
```

### 设置定时任务

**OpenClaw**:
```bash
# 每天早上8点推送科技电台
openclaw cron add \
  --name "每日科技电台" \
  --cron "0 8 * * *" \
  --session isolated \
  --message "生成科技新闻电台" \
  --announce \
  --channel feishu
```

**LobsterAI**:
在GUI中或通过对话创建定时任务：
```
"每天早上8点为我生成科技新闻电台"
```

## Configuration

### TTS配置

首次使用时，Skill会引导用户下载Qwen3-TTS模型。

**OpenClaw**: 配置存储在MEMORY.md中
**LobsterAI**: 配置存储在SQLite数据库中

### 用户偏好

用户偏好（订阅标签、常用音色等）：
- **OpenClaw**: 存储在MEMORY.md中
- **LobsterAI**: 存储在持久化记忆中

## Workflow

### 1. 生成电台

1. 解析用户输入的主题/标签
2. 调用平台LLM生成内容
3. 调用Qwen3-TTS模型转换为音频
4. 保存音频文件
5. 返回音频链接和文本摘要

## Cowork Mode（推荐）

在LobsterAI/OpenClaw的cowork mode下，可以利用平台主对话LLM生成内容，本Skill只负责TTS合成。

**支持任意LLM模型**：Claude、GPT-4、Qwen、Llama、Gemini等

**优势**:
- ✅ 无需额外LLM API密钥
- ✅ 利用平台LLM的强大能力（任意模型）
- ✅ 内容生成更智能、更自然
- ✅ 支持多模型切换对比

**重要：获取新闻内容**

生成电台前，需要先获取最新新闻内容。**建议多次调用 web-search skill** 获取不同主题的新闻：

> **建议**：生成的新闻文稿控制在 **200字以内**，确保音频时长在1分钟内，适合移动端收听。

> **注意**：根据 web-search skill 的文档，它可能不能直接通过 Python 导入使用。请按以下顺序尝试：
> 1. **首先尝试 Python 导入使用**：`from web_search import search`
> 2. **如果不行，尝试通过 bash 脚本调用**：`bash scripts/web_search.sh "搜索关键词"`

```python
# 1. 首先，多次调用 web-search skill 获取不同主题的新闻
#    （可能需要3-5次搜索以覆盖不同主题）
#    按上述说明尝试 Python 导入或 bash 脚本调用

# 搜索结果示例：
# - 第一次搜索: "今日国际要闻"
# - 第二次搜索: "最新科技动态"  
# - 第三次搜索: "今日财经要闻"
# - 第四次搜索: "体育热点新闻"
# - 第五次搜索: "娱乐热点事件"

# 2. 平台主对话LLM整合搜索结果，生成连贯的电台内容
content = """
欢迎收听今日新闻摘要。

首先是国际要闻...（根据web-search结果生成）

接下来是科技动态...（根据web-search结果生成）

财经方面...（根据web-search结果生成）

体育要闻...（根据web-search结果生成）

娱乐热点...（根据web-search结果生成）

以上就是今天的新闻摘要，感谢收听。
"""

# 3. 调用Skill合成语音
audio_url = cowork_generate(
    title="今日新闻摘要",
    content=content,
    voice="xiaoxiao",  # 新闻适合女声
    emotion="neutral"
)

print(f"音频已生成: {audio_url}")
```

**本Skill仅支持Cowork Mode**：

| 模式 | 内容生成 | TTS合成 | 需要API密钥 | 支持模型 |
|------|---------|---------|------------|---------|
| **Cowork Mode** | **平台LLM生成** | **Skill合成** | **无需额外API** | **任意模型** |

> **注意**：本Skill仅支持Cowork Mode，内容由平台主对话LLM生成，Skill只负责TTS语音合成。

### 2. 设置定时任务

**OpenClaw**:
1. 解析用户的定时需求
2. 调用OpenClaw的cron系统创建任务
3. OpenClaw按时执行任务并推送

**LobsterAI**:
1. 解析用户的定时需求
2. 调用LobsterAI的scheduled-task skill创建任务
3. LobsterAI按时执行任务并推送

### 3. 配置TTS

1. 检查模型是否已下载
2. 展示可用音色供选择
3. 保存配置到平台存储

## Available Voices

### 中文音色
- **xiaoxiao** (晓晓): 女声，温柔，适合新闻播报
- **yunjian** (云健): 男声，沉稳，适合财经资讯
- **xiaochen** (晓辰): 女声，活泼，适合娱乐新闻

### 情感表达
- **neutral**: 中性，适合新闻播报
- **happy**: 开心，适合娱乐内容
- **sad**: 悲伤，适合严肃话题
- **excited**: 兴奋，适合科技突破

## Examples

### Example 1: 生成科技电台

**User**: "生成关于人工智能的电台"

**Bot**: 
```
🎙️ 正在为您生成人工智能主题电台...

📝 内容摘要：
今天的人工智能领域发展迅速，OpenAI发布了最新的GPT-5模型...

🎧 [播放音频]
📥 [下载链接]

⏱️ 时长：3分45秒
```

### Example 2: 设置定时推送

**User**: "每天早上8点推送科技新闻"

**Bot**:
```
✅ 定时任务创建成功！

⏰ 推送时间：每天早上8:00
📌 订阅标签：科技
📢 推送渠道：当前对话

明天早上8点将自动为您生成并推送电台！
```

## Platform-Specific Notes

### OpenClaw

- LLM配置复用OpenClaw的配置
- 定时任务使用OpenClaw的cron系统
- 用户配置存储在OpenClaw的MEMORY.md中

### LobsterAI

- LLM配置复用LobsterAI的配置（Claude Agent SDK）
- 定时任务使用LobsterAI的scheduled-task skill
- 用户配置存储在LobsterAI的持久化记忆中
- 支持通过IM（飞书、钉钉、Telegram）远程触发

## Troubleshooting

### 模型未下载

**错误**: "模型未找到" 或 "模型下载失败"

**解决方案**:
```bash
# 方法1: 使用HuggingFace
pip install huggingface_hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base

# 方法2: 使用ModelScope（国内用户推荐）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')"
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
# 在配置中设置 use_gpu=False

# 检查系统资源
htop
```

## Performance

- **CPU推理**: 1-2秒/100字
- **GPU推理**: 0.5-1秒/100字
- **内存占用**: 约500MB
- **模型大小**: 约5GB

## Cost

- ✅ **完全免费**
- ✅ **无API调用费用**
- ✅ **无使用限制**
- ✅ **可离线使用**

## Support

如有问题，请访问：
- GitHub Issues: https://github.com/your-repo/lobster-radio-skill
- OpenClaw文档: https://docs.openclaw.ai
- LobsterAI文档: https://github.com/netease-youdao/LobsterAI
- Qwen3-TTS文档: https://qwen.ai/blog?id=qwen3tts-0115
