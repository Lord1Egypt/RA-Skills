# Skill Finder | 技能查找器

**English** | [中文](#中文版本)

---

## English Version

Command-line tool to search, browse, and discover OpenClaw skills from the ClawHub platform.

### Version

**Current Version**: v1.0.0
**Release Date**: 2026-03-23

### Features

- **🔎 Smart Search** - Full-text search with fuzzy matching
- **📊 Advanced Filtering** - Filter by tags, verified status, popularity
- **💡 Recommendations** - Discover trending and related skills
- **📋 Detailed Info** - View complete skill metadata and requirements

### Quick Start

#### Installation

```bash
# Install via npm (recommended)
npm install -g openclaw-skill-finder

# Or via ClawHub
clawhub install skill-finder
```

#### Basic Usage

```bash
# Search for skills
skill-finder search video

# List all available skills
skill-finder list

# Show trending skills
skill-finder trending

# Get detailed information
skill-finder info video-generator
```

### Commands

#### Search Commands

```bash
skill-finder search <query> [options]
  --tag <tag>          Filter by tag
  --verified           Show only verified skills
  --sort <field>       Sort by: relevance, popularity, date
  --limit <number>     Limit results (default: 20)
```

#### Browse Commands

```bash
skill-finder list [options]      # List all skills
skill-finder trending [--limit]  # Show trending skills
skill-finder recent [--limit]    # Show recent updates
skill-finder category <name>     # Browse by category
```

#### Information Commands

```bash
skill-finder info <skill-name>          # Show skill details
skill-finder install-info <skill-name>  # Show installation guide
skill-finder related <skill-name>       # Show related skills
```

### Examples

**Find Video Skills**
```bash
$ skill-finder search video --tag video

Found 5 skills:
1. video-generator - Automated text-to-video generation
2. video-editor - CLI video editing tool
```

**Discover Trending**
```bash
$ skill-finder trending --limit 5

🔥 Trending Skills:
1. video-generator  ⭐ 234 users  ⬆️ +45 this week
2. data-analyzer    ⭐ 189 users  ⬆️ +32 this week
```

**Get Details**
```bash
$ skill-finder info video-generator

📦 video-generator (v1.6.0)
Description: Automated text-to-video generation system
Tags: video, automation, ai, tts
Verified: ✅ Yes
```

### Configuration

Create `~/.skill-finder/config.json`:

```json
{
  "defaultSort": "popularity",
  "defaultLimit": 20,
  "showVerifiedOnly": false,
  "apiEndpoint": "https://api.clawhub.ai"
}
```

### Output Formats

```bash
skill-finder list              # Pretty table
skill-finder list --json       # JSON output
skill-finder list --compact    # Compact list
```

### Troubleshooting

**Cannot Connect to ClawHub**
- Check internet connection
- Verify firewall settings
- Try: `skill-finder --debug`

**No Results Found**
- Use broader search terms
- Remove filters
- Check spelling

### Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-skill-finder
- **npm**: https://www.npmjs.com/package/openclaw-skill-finder
- **ClawHub**: https://clawhub.ai
- **Issues**: https://github.com/ZhenRobotics/openclaw-skill-finder/issues

### License

MIT License - See LICENSE file for details

---

## 中文版本

**[English](#english-version)** | 中文

命令行工具，用于从 ClawHub 平台搜索、浏览、发现 OpenClaw 技能。

### 版本

**当前版本**: v1.0.0
**发布日期**: 2026-03-23

### 功能特性

- **🔎 智能搜索** - 全文搜索，模糊匹配
- **📊 高级过滤** - 按标签、验证状态、热度过滤
- **💡 推荐系统** - 发现热门和相关技能
- **📋 详细信息** - 查看完整技能元数据和要求

### 快速开始

#### 安装

```bash
# 通过 npm 安装（推荐）
npm install -g openclaw-skill-finder

# 或通过 ClawHub
clawhub install skill-finder
```

#### 基础使用

```bash
# 搜索技能
skill-finder search video

# 列出所有可用技能
skill-finder list

# 显示热门技能
skill-finder trending

# 获取详细信息
skill-finder info video-generator
```

### 命令

#### 搜索命令

```bash
skill-finder search <查询> [选项]
  --tag <标签>         按标签过滤
  --verified           仅显示已验证技能
  --sort <字段>        排序: relevance, popularity, date
  --limit <数量>       限制结果 (默认: 20)
```

#### 浏览命令

```bash
skill-finder list [选项]         # 列出所有技能
skill-finder trending [--limit]  # 显示热门技能
skill-finder recent [--limit]    # 显示最近更新
skill-finder category <名称>     # 按分类浏览
```

#### 信息命令

```bash
skill-finder info <技能名称>          # 显示技能详情
skill-finder install-info <技能名称>  # 显示安装指南
skill-finder related <技能名称>       # 显示相关技能
```

### 示例

**查找视频技能**
```bash
$ skill-finder search video --tag video

找到 5 个技能:
1. video-generator - 自动化文本转视频生成
2. video-editor - CLI 视频编辑工具
```

**发现热门**
```bash
$ skill-finder trending --limit 5

🔥 热门技能:
1. video-generator  ⭐ 234 用户  ⬆️ 本周 +45
2. data-analyzer    ⭐ 189 用户  ⬆️ 本周 +32
```

**获取详情**
```bash
$ skill-finder info video-generator

📦 video-generator (v1.6.0)
描述: 自动化文本转视频生成系统
标签: video, automation, ai, tts
已验证: ✅ 是
```

### 配置

创建 `~/.skill-finder/config.json`:

```json
{
  "defaultSort": "popularity",
  "defaultLimit": 20,
  "showVerifiedOnly": false,
  "apiEndpoint": "https://api.clawhub.ai"
}
```

### 输出格式

```bash
skill-finder list              # 美化表格
skill-finder list --json       # JSON 输出
skill-finder list --compact    # 紧凑列表
```

### 故障排除

**无法连接到 ClawHub**
- 检查互联网连接
- 验证防火墙设置
- 尝试: `skill-finder --debug`

**未找到结果**
- 使用更广泛的搜索词
- 移除过滤器
- 检查拼写

### 链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-skill-finder
- **npm**: https://www.npmjs.com/package/openclaw-skill-finder
- **ClawHub**: https://clawhub.ai
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-skill-finder/issues

### 许可证

MIT License - 详见 LICENSE 文件

---

**Version | 版本**: v1.0.0
**Last Updated | 最后更新**: 2026-03-23
**Maintainer | 维护者**: ZhenStaff
