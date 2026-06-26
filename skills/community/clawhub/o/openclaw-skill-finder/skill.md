---
name: skill-finder
description: Search, browse, and discover OpenClaw skills from ClawHub platform with advanced filtering | 搜索、浏览、发现 ClawHub 平台上的 OpenClaw 技能
tags: [openclaw, clawhub, skill-search, skill-discovery, cli-tool, package-manager, skill-management]
repository: https://github.com/ZhenRobotics/openclaw-skill-finder
homepage: https://github.com/ZhenRobotics/openclaw-skill-finder#readme
requires:
  tools:
    - node>=18
    - npm
  packages:
    - name: openclaw-skill-finder
      source: npm
      version: ">=1.0.0"
      verified_repo: https://github.com/ZhenRobotics/openclaw-skill-finder
      verified_commit: main
install:
  commands:
    - npm install -g openclaw-skill-finder
  verify:
    - skill-finder --version
  notes: |
    No API keys required. Command-line tool for discovering OpenClaw skills.
---

# 🔍 Skill Finder | 技能查找器

**English** | [中文](#中文版本)

---

## English Version

Command-line tool to search, browse, and discover OpenClaw skills from the ClawHub platform. Find the right skill for your needs with powerful filtering and recommendations.

### 🔒 Security & Trust

This tool is **safe and verified**:
- ✅ All code runs **locally** on your machine
- ✅ **No API keys required** - connects to public ClawHub API
- ✅ Source code is **open source** and auditable
- ✅ Uses official **npm package** (openclaw-skill-finder)
- ✅ **Verified repository**: github.com/ZhenRobotics/openclaw-skill-finder
- ✅ **Read-only access** - only searches and displays information

### ✨ Features

**🔎 Smart Search**
- Full-text search across skill names, descriptions, and tags
- Fuzzy matching for typo-tolerant results
- Category-based filtering

**📊 Advanced Filtering**
- Filter by tags (video, automation, ai, data, etc.)
- Sort by popularity, date, or relevance
- Show only verified skills

**💡 Recommendations**
- Discover trending skills
- Get personalized recommendations based on your installed skills
- Related skills suggestions

**📋 Detailed Information**
- View complete skill metadata
- Check dependencies and requirements
- Read installation instructions
- See verified commit information

### 📦 Installation

```bash
# Install globally via npm
npm install -g openclaw-skill-finder

# Verify installation
skill-finder --version
```

Or via ClawHub:
```bash
clawhub install skill-finder
```

### 🚀 Quick Start

#### Basic Search

```bash
# Search for skills
skill-finder search video

# Search with multiple keywords
skill-finder search "video generation automation"

# Search by tag
skill-finder search --tag video
```

#### Browse Skills

```bash
# List all available skills
skill-finder list

# Show trending skills
skill-finder trending

# Show recently updated
skill-finder recent
```

#### View Details

```bash
# Get detailed information about a skill
skill-finder info video-generator

# Show installation instructions
skill-finder install-info video-generator
```

### 📋 Commands

#### Search Commands

```bash
# Search for skills
skill-finder search <query> [options]

Options:
  --tag <tag>          Filter by tag
  --verified           Show only verified skills
  --sort <field>       Sort by: relevance, popularity, date (default: relevance)
  --limit <number>     Limit results (default: 20)
```

#### Browse Commands

```bash
# List all skills
skill-finder list [options]

# Show trending skills
skill-finder trending [--limit <number>]

# Show recent updates
skill-finder recent [--limit <number>]

# Browse by category
skill-finder category <name>
```

#### Information Commands

```bash
# Show skill details
skill-finder info <skill-name>

# Show installation guide
skill-finder install-info <skill-name>

# Show related skills
skill-finder related <skill-name>
```

### 🎯 Usage Examples

#### Example 1: Find Video Skills

```bash
# Search for video-related skills
$ skill-finder search video --tag video

Found 5 skills:

1. video-generator
   📝 Automated text-to-video generation
   🏷️  video, automation, ai, tts
   ⭐ 234 users

2. video-editor
   📝 CLI video editing tool
   🏷️  video, editing, cli
   ⭐ 156 users

Use 'skill-finder info <name>' for details
```

#### Example 2: Discover Trending

```bash
# Show trending skills
$ skill-finder trending --limit 5

🔥 Trending Skills:

1. video-generator     ⭐ 234 users  ⬆️  +45 this week
2. data-analyzer       ⭐ 189 users  ⬆️  +32 this week
3. code-reviewer       ⭐ 167 users  ⬆️  +28 this week
```

#### Example 3: Get Skill Details

```bash
# View detailed information
$ skill-finder info video-generator

📦 video-generator (v1.6.0)

Description:
  Automated text-to-video generation system with multi-provider
  TTS/ASR support and premium visual styles

Tags: video, automation, ai, tts, remotion
Repository: github.com/ZhenRobotics/openclaw-video-generator
Verified: ✅ Yes (commit: 6f93635)

Requirements:
  - Node.js >= 18
  - npm
  - ffmpeg

Installation:
  clawhub install video-generator
  npm install -g openclaw-video-generator

More info: skill-finder install-info video-generator
```

### 🔧 Configuration

Create `~/.skill-finder/config.json` for custom settings:

```json
{
  "defaultSort": "popularity",
  "defaultLimit": 20,
  "showVerifiedOnly": false,
  "apiEndpoint": "https://api.clawhub.ai"
}
```

### 📊 Output Formats

```bash
# Default (pretty table)
skill-finder list

# JSON output
skill-finder list --json

# Compact list
skill-finder list --compact
```

### 🐛 Troubleshooting

#### Cannot Connect to ClawHub
- Check your internet connection
- Verify firewall settings
- Try: `skill-finder --debug`

#### No Results Found
- Try broader search terms
- Remove filters
- Check spelling

### 🔗 Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-skill-finder
- **npm**: https://www.npmjs.com/package/openclaw-skill-finder
- **ClawHub**: https://clawhub.ai
- **Issues**: https://github.com/ZhenRobotics/openclaw-skill-finder/issues

### 📄 License

MIT License - See LICENSE file for details

---

## 中文版本

**[English](#english-version)** | 中文

---

命令行工具，用于从 ClawHub 平台搜索、浏览、发现 OpenClaw 技能。通过强大的过滤和推荐功能找到适合您需求的技能。

### 🔒 安全与信任

此工具**安全且经过验证**：
- ✅ 所有代码在您的**本地机器**上运行
- ✅ **无需 API 密钥** - 连接到公共 ClawHub API
- ✅ 源代码**开源**且可审计
- ✅ 使用官方 **npm 包**（openclaw-skill-finder）
- ✅ **已验证的仓库**: github.com/ZhenRobotics/openclaw-skill-finder
- ✅ **只读访问** - 仅搜索和显示信息

### ✨ 功能特性

**🔎 智能搜索**
- 全文搜索技能名称、描述和标签
- 模糊匹配，容错搜索
- 基于分类的过滤

**📊 高级过滤**
- 按标签过滤（video、automation、ai、data 等）
- 按热度、日期或相关性排序
- 仅显示已验证技能

**💡 推荐系统**
- 发现热门技能
- 基于已安装技能的个性化推荐
- 相关技能建议

**📋 详细信息**
- 查看完整技能元数据
- 检查依赖和要求
- 阅读安装说明
- 查看验证提交信息

### 📦 安装

```bash
# 通过 npm 全局安装
npm install -g openclaw-skill-finder

# 验证安装
skill-finder --version
```

或通过 ClawHub：
```bash
clawhub install skill-finder
```

### 🚀 快速开始

#### 基础搜索

```bash
# 搜索技能
skill-finder search video

# 多关键词搜索
skill-finder search "视频生成 自动化"

# 按标签搜索
skill-finder search --tag video
```

#### 浏览技能

```bash
# 列出所有可用技能
skill-finder list

# 显示热门技能
skill-finder trending

# 显示最近更新
skill-finder recent
```

#### 查看详情

```bash
# 获取技能详细信息
skill-finder info video-generator

# 显示安装说明
skill-finder install-info video-generator
```

### 📋 命令

#### 搜索命令

```bash
# 搜索技能
skill-finder search <查询> [选项]

选项:
  --tag <标签>         按标签过滤
  --verified           仅显示已验证技能
  --sort <字段>        排序方式: relevance, popularity, date (默认: relevance)
  --limit <数量>       限制结果数量 (默认: 20)
```

#### 浏览命令

```bash
# 列出所有技能
skill-finder list [选项]

# 显示热门技能
skill-finder trending [--limit <数量>]

# 显示最近更新
skill-finder recent [--limit <数量>]

# 按分类浏览
skill-finder category <名称>
```

#### 信息命令

```bash
# 显示技能详情
skill-finder info <技能名称>

# 显示安装指南
skill-finder install-info <技能名称>

# 显示相关技能
skill-finder related <技能名称>
```

### 🎯 使用示例

#### 示例 1: 查找视频技能

```bash
# 搜索视频相关技能
$ skill-finder search video --tag video

找到 5 个技能:

1. video-generator
   📝 自动化文本转视频生成
   🏷️  video, automation, ai, tts
   ⭐ 234 用户

2. video-editor
   📝 CLI 视频编辑工具
   🏷️  video, editing, cli
   ⭐ 156 用户

使用 'skill-finder info <名称>' 查看详情
```

#### 示例 2: 发现热门

```bash
# 显示热门技能
$ skill-finder trending --limit 5

🔥 热门技能:

1. video-generator     ⭐ 234 用户  ⬆️  本周 +45
2. data-analyzer       ⭐ 189 用户  ⬆️  本周 +32
3. code-reviewer       ⭐ 167 用户  ⬆️  本周 +28
```

#### 示例 3: 获取技能详情

```bash
# 查看详细信息
$ skill-finder info video-generator

📦 video-generator (v1.6.0)

描述:
  多厂商 TTS/ASR 支持的自动化文本转视频系统
  和高端视觉风格

标签: video, automation, ai, tts, remotion
仓库: github.com/ZhenRobotics/openclaw-video-generator
已验证: ✅ 是 (提交: 6f93635)

要求:
  - Node.js >= 18
  - npm
  - ffmpeg

安装:
  clawhub install video-generator
  npm install -g openclaw-video-generator

更多信息: skill-finder install-info video-generator
```

### 🔧 配置

在 `~/.skill-finder/config.json` 中创建自定义设置：

```json
{
  "defaultSort": "popularity",
  "defaultLimit": 20,
  "showVerifiedOnly": false,
  "apiEndpoint": "https://api.clawhub.ai"
}
```

### 📊 输出格式

```bash
# 默认（美化表格）
skill-finder list

# JSON 输出
skill-finder list --json

# 紧凑列表
skill-finder list --compact
```

### 🐛 故障排除

#### 无法连接到 ClawHub
- 检查您的互联网连接
- 验证防火墙设置
- 尝试: `skill-finder --debug`

#### 未找到结果
- 尝试更广泛的搜索词
- 移除过滤器
- 检查拼写

### 🔗 链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-skill-finder
- **npm**: https://www.npmjs.com/package/openclaw-skill-finder
- **ClawHub**: https://clawhub.ai
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-skill-finder/issues

### 📄 许可证

MIT License - 详见 LICENSE 文件

---

**Version | 版本**: v1.0.0
**Last Updated | 最后更新**: 2026-03-23
**Maintainer | 维护者**: ZhenStaff
