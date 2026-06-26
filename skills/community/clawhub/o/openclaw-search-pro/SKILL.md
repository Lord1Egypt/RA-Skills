---
name: openclaw-search-pro
displayName: OpenClaw Search Pro - 搜索增强工具
version: 1.0.2
description: |
  OpenClaw 搜索增强工具 - 多引擎聚合搜索，获取最新信息。
  支持免费搜索引擎（必应/搜狗/360）+ 可选 API（Tavily/百度/Google）。
  内容提取、结果去重、智能排序。安全内网访问检查。
  关键词：openclaw, search, web, research, productivity, multi-engine, tavily
license: MIT-0
acceptLicenseTerms: true
tags:
  - openclaw
  - search
  - web
  - research
  - productivity
  - multi-engine
  - tavily
  - content-extraction
  - bing
  - baidu
---

# Search Pro - 搜索增强工具

强大的多引擎搜索工具，让搜索更准确、更全面。

---

## ✨ 功能特性

- 🔍 **多引擎聚合** - 免费搜索引擎 + 可选 API
- 📄 **内容提取** - URL 内容提取
- 📊 **结果去重** - 智能去重 + 排序
- 💾 **搜索历史** - 历史记录 + 收藏
- 📈 **质量分析** - 搜索质量评估

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/search-pro
chmod +x search-pro/scripts/*.py
```

---

## 📖 使用

### 多引擎搜索

```bash
python3 search-pro/scripts/multi-search.py "OpenClaw 技能开发"
```

### 内容提取

```bash
python3 search-pro/scripts/extract.py --url https://example.com
```

---

## 🛠️ 脚本

| 脚本 | 功能 | 网络访问 | 文件写入 |
|------|------|---------|---------|
| `multi-search.py` | 多引擎搜索 | ✅ 是 | ❌ 否 |
| `free_search.py` | 免费搜索引擎 | ✅ 是 | ❌ 否 |
| `baidu_search.py` | 百度搜索 | ✅ 是 | ❌ 否 |
| `extract.py` | 内容提取 | ✅ 是 | ❌ 否 |

**注意：** 搜索历史功能需要手动实现，当前版本不自动保存历史

---

## 🔒 安全说明

### 网络访问 ⚠️
**本技能需要联网访问外部服务：**
- 免费搜索引擎（360、搜狗等）
- 百度搜索引擎
- 可选：Tavily API（需配置 API Key）

**网络权限：**
- 出站 HTTPS 请求（443 端口）
- 不监听任何端口
- 不运行服务器

### 文件访问
**路径说明：** 所有文件存储在 `~/.openclaw/workspace/skills/search-pro/`

- **读取：**
  - `config/search-config.json` - 搜索配置和 API 密钥（可选）
- **写入：**
  - 当前版本不自动写入文件
  - 搜索结果输出到命令行
- **extract.py 安全检查：**
  - ✅ 仅支持 http:// 和 https:// 协议
  - ✅ 检查 IP 地址（10/8, 172.16/12, 192.168/16, 127/8）
  - ✅ DNS 解析后检查（防止域名指向内网）
  - ✅ 检查内网域名模式（.local, .internal, .intranet, .lan）
  - ✅ 阻止常见内网主机名（localhost, internal 等）

### 数据安全
- **不上传：** 不上传用户配置文件或敏感数据
- **搜索查询：** 会发送到配置的搜索引擎（百度、必应等），这是搜索功能的必要条件
- **API 密钥：** 存储在本地配置文件，不发送到除 API 提供商外的第三方

### API 密钥（可选）
**免费搜索：** 无需 API Key，直接使用

**可选 API 配置：**
```bash
# 方法 1: 环境变量（推荐，更安全）
export TAVILY_API_KEY="your-key"

# 方法 2: 配置文件
# 编辑 config/search-config.json
{
  "tavily": {
    "api_key": "your-key"
  }
}
```

**注意：** API Key 存储在 `config/search-config.json`，没有单独的 api-keys.json 文件

**安全建议：**
- 配置文件权限：`chmod 600 config/search-config.json`
- 不要将 API Key 提交到 Git（添加到 .gitignore）
- 使用环境变量更安全（不写入文件）

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
