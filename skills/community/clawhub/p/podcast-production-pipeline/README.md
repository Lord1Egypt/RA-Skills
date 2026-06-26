# 🎙️ Podcast Production Pipeline

**端到端播客制作流水线 - 从选题到发布的完整自动化**

[![ClawHub](https://img.shields.io/badge/ClawHub-podcast--production--pipeline-blue)](https://clawhub.com/skills/podcast-production-pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 痛点

独立播客主播和小团队在制作上花的时间远多于录制本身：
- 嘉宾调研动辄 **数小时**
- 节目笔记 **总是被拖延**
- 社交媒体宣发 **第一个被砍掉**

真正有创造力的部分——**对话本身**——可能只占总工作量的 **30%**。

这个技能帮你处理剩下的 **70%**。

---

## ✨ 功能

### 📋 前期制作

| 功能 | 说明 |
|------|------|
| 嘉宾研究 | 背景、成就、公开观点、争议话题 |
| 话题研究 | 趋势、新闻、常见误解、受众知识 |
| 节目大纲 | 冷开场、开场白、采访问题、备用问题、结束语 |
| 采访策略 | 从建立融洽感到深度探讨的渐进式问题 |

### 🎬 后期制作

| 功能 | 说明 |
|------|------|
| 节目笔记 | 时间戳、关键点、资源链接 |
| SEO 描述 | Spotify、Apple Podcasts、YouTube 优化 |
| 社交素材 | X/LinkedIn/Instagram 或 小红书/微博/微信 |
| 精华片段 | 最有趣的 3 个时刻，带时间戳 |

---

## 🚀 快速开始

### 安装

```bash
clawhub install podcast-production-pipeline
```

### 前期制作

```bash
cd ~/.openclaw/workspace/skills/podcast-production-pipeline/scripts
node pre-production.cjs 1 "AI Agent发展趋势" "Sam Altman"
```

### 后期制作

```bash
node post-production.cjs 1 ~/podcast/episodes/ep1/transcript.txt
```

---

## 🌍 平台支持

### 国际平台
- Spotify for Podcasters
- Apple Podcasts
- YouTube
- X/Twitter, LinkedIn, Instagram

### 国内平台
- 小宇宙
- 喜马拉雅
- B站 / 网易云音乐
- 小红书 / 微信公众号 / 微博 / 抖音

---

## 📁 输出结构

```
podcast/episodes/ep<N>/
├── prep/                    # 前期制作
│   ├── outline.md           # 节目大纲
│   ├── guest-research.md    # 嘉宾研究
│   └── topic-research.md    # 话题研究
├── transcript.txt           # 转录稿
└── publish/                 # 发布素材
    ├── show-notes.md        # 节目笔记
    ├── description.md       # SEO 描述
    ├── social/              # 社交媒体
    │   ├── xiaohongshu.md
    │   ├── weibo.md
    │   └── weixin.md
    └── highlights.md        # 精华片段
```

---

## ⚙️ 配置

编辑 `config/settings.json`:

```json
{
  "podcast_name": "你的播客名称",
  "host_name": "主播名字",
  "discord_channel": "DISCORD_THREAD_ID",
  "storage_path": "~/podcast",
  "platforms": {
    "china": ["xiaoyuzhou", "ximalaya", "bilibili"]
  },
  "social_media": {
    "china": ["xiaohongshu", "weixin", "weibo"]
  },
  "apis": {
    "tavily": "YOUR_TAVILY_KEY",
    "gemini": "YOUR_GEMINI_KEY"
  }
}
```

---

## 🇨🇳 国内创作者统计

| 指标 | 数据 |
|------|------|
| 平均每期净工作时长 | **12.9 小时** |
| 剪辑平均耗时 | **4.5 小时** |
| 兼职创作者占比 | **80%** |

用智能体自动化流水线工作，把有限的时间集中在内容本身。

---

## 📝 更新日志

### v1.1.0 (2026-03-14)
- ✅ 添加国内平台支持
- ✅ 添加社交媒体素材包
- ✅ 添加精华片段提取

### v1.0.0 (2026-03-12)
- ✅ 初始版本

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [用例来源](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/usecases/podcast-production-pipeline.md)
- [小宇宙主播入驻](https://podcaster.xiaoyuzhoufm.com/)
- [喜马拉雅创作中心](https://zhubo.ximalaya.com/)
- [Whisper (本地转录)](https://github.com/openai/whisper)
