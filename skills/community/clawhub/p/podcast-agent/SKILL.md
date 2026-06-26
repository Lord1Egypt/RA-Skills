---
name: podcast-agent
description: Search articles on any topic, generate a two-host dialogue script, and synthesize podcast audio via TTS. Turn long reads into listenable content.
tags:
  - podcast
  - tts
  - content
  - audio
  - agent
requires:
  bins:
    - python
  env:
    - edge-tts
---

# 播客生成器 / Podcast Agent

搜索文章 → 提取核心观点 → 写对话脚本 → 合成播客音频。

Turn articles into podcasts. Search, summarize, script, synthesize.

## 工作流程

```
你说：帮我做一期关于"AI Agent 最新进展"的播客
  ↓
我搜索相关文章 (web_search)
  ↓
我读文章，提取 3-5 个核心观点
  ↓
我写对话体脚本（主持人 A 问，专家 B 答）
  ↓
TTS 合成音频（女声主持 + 男声专家）
  ↓
发给你 MP3 文件
```

## 前置安装

```bash
pip install edge-tts
```

## Agent 工作流

### 第一步：搜索文章

Agent 用 `web_search` 搜索相关文章，或者用工具直接抓取：

```bash
python podcast_gen.py fetch --url "https://example.com/article"
```

### 第二步：生成脚本

Agent 阅读文章后，生成对话体脚本。脚本格式：

```json
{
  "title": "AI Agent 最新进展",
  "duration_estimate": "5 min",
  "segments": [
    {"speaker": "A", "text": "大家好，欢迎收听今天的科技播客。今天我们来聊聊 AI Agent 的最新进展。"},
    {"speaker": "B", "text": "最近这个领域确实发展很快。最大的变化是..."},
    {"speaker": "A", "text": "听起来很有意思。那具体有哪些应用场景呢？"},
    {"speaker": "B", "text": "主要有三个方面..."}
  ]
}
```

**脚本写作指南：**
- A 是主持人，负责提问、过渡、总结
- B 是专家，负责回答、分析、举例
- 每段对话控制在 2-4 句话
- 有开头问候、中间讨论、结尾总结
- 语气自然，像真的在聊天

### 第三步：合成音频

```bash
python podcast_gen.py tts --script script.json --output podcast.mp3
```

## 语音配置

```bash
python podcast_gen.py voices
```

| 角色 | 语音 ID | 特点 |
|------|---------|------|
| A (主持人) | zh-CN-XiaoxiaoNeural | 女声，温暖 |
| B (专家) | zh-CN-YunyangNeural | 男声，专业 |

## 完整示例

### Agent 的完整操作流程

```python
# 1. 搜索
results = web_search("AI agent 最新进展", count=3)

# 2. 抓取每篇文章
for url in result_urls:
    content = fetch(url)

# 3. 写脚本（由 Agent 完成，基于对文章的理解）
script = {
    "title": "AI Agent 周报",
    "segments": [
        {"speaker": "A", "text": "..."},
        {"speaker": "B", "text": "..."},
        ...
    ]
}
save(script, "script.json")

# 4. 合成
podcast_gen.py tts --script script.json --output ai_agent_podcast.mp3
```

### 用户交互

用户说：
> "帮我做一期关于最新手机的播客"

Agent 自动：
1. 搜索 "最新手机发布 2026"
2. 读 2-3 篇文章
3. 写脚本（5 分钟，10-15 个对话轮次）
4. 合成音频
5. 发送 MP3

## 脚本模板

```json
{
  "title": "主题名称",
  "duration_estimate": "5 min",
  "segments": [
    {"speaker": "A", "text": "开场白 + 引入话题"},
    {"speaker": "B", "text": "回应 + 第一个观点"},
    {"speaker": "A", "text": "追问细节"},
    {"speaker": "B", "text": "展开说明 + 举例"},
    {"speaker": "A", "text": "过渡到下一个话题"},
    {"speaker": "B", "text": "第二个观点"},
    {"speaker": "A", "text": "总结 + 听众建议"},
    {"speaker": "B", "text": "补充 + 展望"},
    {"speaker": "A", "text": "结尾 + 下期预告"}
  ]
}
```

## 输出

音频文件保存在 `<skill_dir>/output/` 目录，格式 MP3。

## 注意事项

- **edge-tts 需要联网**（微软 TTS 服务）
- 音频质量取决于脚本质量——写得越自然，听起来越好
- 单个片段建议不超过 30 秒（约 100 字）
- 一期 5 分钟播客约需 10-15 个对话轮次
- 合并音频最好有 ffmpeg（没有也能用，质量稍降）

## 目录结构

```
podcast-agent/
├── SKILL.md              # 本文件
├── scripts/
│   └── podcast_gen.py    # CLI 工具
└── output/               # 生成的音频文件
```
