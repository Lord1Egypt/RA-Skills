---
name: podcast-production-pipeline
slug: podcast-production-pipeline
version: 1.1.0
description: 端到端播客制作流水线 - 从选题到发布的完整自动化。支持录制前调研、大纲生成、节目笔记、社交媒体宣发。含国内平台适配（小宇宙/喜马拉雅/B站/小红书）。
author: sunnyhot
license: MIT
homepage: https://github.com/sunnyhot/podcast-production-pipeline
keywords:
  - podcast
  - production
  - automation
  - content-creation
  - show-notes
  - social-media
  - xiaoyuzhou
  - ximalaya
  - bilibili
metadata:
  clawdbot:
    emoji: 🎙️
    requires:
      bins: ["node"]
    optionalBins: ["whisper"]
    os: ["linux", "darwin", "win32"]
    configPaths:
      - config/settings.json
---

# 🎙️ Podcast Production Pipeline

**端到端播客制作流水线 - 从选题到发布的完整自动化**

---

## 🎯 核心功能

### 📋 前期制作 (Pre-Production)

**录制前自动完成**:
- ✅ **嘉宾研究** - 背景、成就、公开观点、争议话题
- ✅ **话题研究** - 趋势、新闻、常见误解、受众知识
- ✅ **节目大纲** - 开场白、采访问题、备用问题、结束语
- ✅ **采访策略** - 从建立融洽感到深度探讨的渐进式问题

### 🎬 后期制作 (Post-Production)

**录制后自动生成**:
- ✅ **节目笔记** - 时间戳、关键点、资源链接
- ✅ **SEO 描述** - Spotify、Apple Podcasts、YouTube 优化
- ✅ **社交媒体素材包** - X/LinkedIn/Instagram 或 小红书/微博/微信
- ✅ **精华片段** - 最有趣的 3 个时刻，带时间戳

---

## 🌍 平台支持

### 国际平台
| 类型 | 平台 |
|------|------|
| 播客托管 | Spotify for Podcasters, Apple Podcasts |
| 视频播客 | YouTube |
| 社交宣发 | X/Twitter, LinkedIn, Instagram |

### 国内平台
| 类型 | 平台 |
|------|------|
| 播客托管 | 小宇宙, 喜马拉雅, 网易云音乐 |
| 视频播客 | B站 |
| 社交宣发 | 小红书, 微信公众号, 微博, 抖音/视频号 |

---

## 📅 使用方法

### 1. 前期制作（录制前）

```bash
cd ~/.openclaw/workspace/skills/podcast-production-pipeline/scripts
node pre-production.cjs <episode_number> "<topic>" "<guest_name>"
```

**示例**:
```bash
node pre-production.cjs 1 "AI Agent发展趋势" "Sam Altman"
```

**生成内容**:
- 📋 嘉宾研究资料
- 📊 话题趋势分析
- 📝 节目大纲
  - 冷开场钩子 (1-2 句)
  - 开场白脚本 (30 秒)
  - 5-7 个采访问题（从简单到深入）
  - 2-3 个备用问题
  - 结束语和行动号召

### 2. 后期制作（录制后）

```bash
node post-production.cjs <episode_number> <transcript_file>
```

**示例**:
```bash
node post-production.cjs 1 ~/podcast/episodes/ep1/transcript.txt
```

**生成内容**:
- 📝 带时间戳的节目笔记
- 🔍 SEO 优化的节目描述
- 📱 社交媒体素材包
  - 国际版: X/LinkedIn/Instagram
  - 国内版: 小红书/微博/微信
- ⭐ 精华片段列表（带时间戳）

---

## 📋 工作流程

```
选题 + 嘉宾
    │
    ▼
┌─────────────────┐
│  前期制作        │
├─────────────────┤
│ • 嘉宾研究      │
│ • 话题研究      │
│ • 生成大纲      │
│ • 采访问题      │
└────────┬────────┘
         │
         ▼
      录制
         │
         ▼
┌─────────────────┐
│  后期制作        │
├─────────────────┤
│ • 节目笔记      │
│ • SEO 描述      │
│ • 社交素材      │
│ • 精华片段      │
└────────┬────────┘
         │
         ▼
      发布
```

---

## 📁 文件结构

```
podcast/episodes/ep<N>/
├── prep/                    # 前期制作
│   ├── outline.md           # 节目大纲
│   ├── guest-research.md    # 嘉宾研究
│   └── topic-research.md    # 话题研究
├── recording/               # 录制文件
│   └── audio.mp3
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
    "international": ["spotify", "apple", "youtube"],
    "china": ["xiaoyuzhou", "ximalaya", "bilibili", "netease"]
  },
  "social_media": {
    "international": ["twitter", "linkedin", "instagram"],
    "china": ["xiaohongshu", "weixin", "weibo", "douyin"]
  },
  "apis": {
    "tavily": "YOUR_TAVILY_KEY",
    "gemini": "YOUR_GEMINI_KEY"
  }
}
```

---

## 🇨🇳 国内创作者特别说明

### 中文播客制作周期
- 平均每期净工作时长达 **12.9 小时**
- 剪辑平均耗时 **4.5 小时**
- 近 **80%** 创作者为兼职状态

### 视频播客趋势
2026 年视频播客正从"补充形态"变为"主流形态"。建议在流水线中加入短视频切片（抖音/视频号）的自动化环节。

### 转录工具
- **Whisper** (本地) - 免费开源
- **讯飞听见** - 中文识别准确率更高
- **飞书妙记** - 团队协作友好

---

## 🔗 相关技能

| 技能 | 功能 |
|------|------|
| **content-factory** | 多智能体内容工厂 |
| **video-frames** | 视频片段提取 |
| **summarize** | 内容摘要 |

---

## 📝 更新日志

### v1.1.0 (2026-03-14)
- ✅ 添加国内平台支持（小宇宙/喜马拉雅/B站/小红书）
- ✅ 添加社交媒体素材包生成
- ✅ 添加精华片段提取
- ✅ 优化 Discord 推送

### v1.0.0 (2026-03-12)
- ✅ 初始版本
- ✅ 前期制作脚本
- ✅ 后期制作脚本

---

## 🚀 安装

```bash
clawhub install podcast-production-pipeline
```

---

## 📄 许可证

MIT License
