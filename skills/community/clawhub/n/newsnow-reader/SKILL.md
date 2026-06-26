---
name: newsnow-reader
description: 优雅地阅读实时热门新闻。支持微博、知乎、百度、抖音、华尔街见闻、今日头条、澎湃新闻等8个主流平台。
---

# NewsNow 新闻阅读器

获取并展示实时热门新闻，基于 newsnow 项目实现原理，直接调用各平台 API。

## 系统依赖

本 skill 仅使用 Python 标准库，无需任何外部依赖：
- `urllib`：Python 标准库，用于发送 HTTP 请求
- `json`、`re`、`time`：Python 标准库

无需安装任何额外依赖或二进制文件。

## 支持的新闻源

| 来源 | 标识 | 说明 |
|------|------|------|
| 微博热搜 | `weibo` | 微博实时热搜榜 |
| 知乎热榜 | `zhihu` | 知乎热门话题 |
| 百度热搜 | `baidu` | 百度搜索热点 |
| 抖音热榜 | `douyin` | 抖音热门话题 |
| 华尔街见闻 | `wallstreetcn` | 华尔街见闻热门文章 |
| 今日头条 | `toutiao` | 今日头条热榜 |
| 澎湃新闻 | `thepaper` | 澎湃新闻热搜 |

## 使用方法

### 1. 获取并展示新闻

```bash
# 获取微博热搜（默认）
python newsnow-reader/scripts/fetch_news.py

# 获取知乎热榜
python newsnow-reader/scripts/fetch_news.py zhihu

# 获取抖音热搜，限制10条
python newsnow-reader/scripts/fetch_news.py douyin 10

# 获取华尔街见闻
python newsnow-reader/scripts/fetch_news.py wallstreetcn 10

# 获取今日头条
python newsnow-reader/scripts/fetch_news.py toutiao 10

# 获取澎湃新闻
python newsnow-reader/scripts/fetch_news.py thepaper 10
```

### 2. 格式化输出

```bash
# 优雅格式（带边框、emoji）
python newsnow-reader/scripts/format_news.py news.json elegant

# 紧凑格式
python newsnow-reader/scripts/format_news.py news.json compact

# Markdown格式
python newsnow-reader/scripts/format_news.py news.json markdown

# 摘要格式（前5条）
python newsnow-reader/scripts/format_news.py news.json summary
```

### 3. 完整流程示例

```bash
# 获取微博热搜并优雅展示
python newsnow-reader/scripts/fetch_news.py weibo 15 > /tmp/news.json && \
python newsnow-reader/scripts/format_news.py /tmp/news.json elegant
```

## 输出格式

### JSON 格式

```json
[
  {
    "id": "唯一标识",
    "title": "新闻标题",
    "url": "完整URL",
    "mobileUrl": "移动端URL（可选）",
    "extra": {
      "info": "附加信息（如热度）",
      "hover": "悬停描述"
    }
  }
]
```

### Elegant 样式示例

```
╔══════════════════════════════════════════════════════════╗
║               📰 实时热门新闻                            ║
╠════════════════════════════════════════════════════════╣
║  更新时间: 2024-01-15 14:30:25                                                     ║
╚════════════════════════════════════════════════════════╝

1️⃣ 新闻标题内容 🔥1234567
   📍 微博热搜
   🔗 https://...

2️⃣ 另一条新闻标题 🔥987654
   📍 微博热搜
```

## 快速命令

| 需求 | 命令 |
|------|------|
| 微博热搜 | `python newsnow-reader/scripts/fetch_news.py weibo \| python -m json.tool` |
| 知乎热榜 | `python newsnow-reader/scripts/fetch_news.py zhihu` |
| 百度热点 | `python newsnow-reader/scripts/fetch_news.py baidu` |
| 抖音热搜 | `python newsnow-reader/scripts/fetch_news.py douyin` |
| 华尔街见闻 | `python newsnow-reader/scripts/fetch_news.py wallstreetcn` |
| 今日头条 | `python newsnow-reader/scripts/fetch_news.py toutiao` |
| 澎湃新闻 | `python newsnow-reader/scripts/fetch_news.py thepaper` |

## 实现原理

本 skill 基于 [newsnow](https://github.com/ourongxing/newsnow) 项目实现，采用以下方式获取数据：

- **微博热搜**: 解析 HTML + 特定 Cookie
- **知乎热榜**: 直接调用官方 JSON API
- **百度热搜**: 从 HTML 注释中提取 JSON 数据
- **抖音热榜**: 获取 session cookie 后调用 API
- **华尔街见闻**: 直接调用热门文章 API
- **今日头条**: 直接调用热榜 API
- **澎湃新闻**: 直接调用右侧边栏 API

所有数据获取均通过 Python 标准库 `urllib` 直接调用各平台 API，无需 MCP Server 或外部依赖。

## 故障排查

1. **网络超时**：检查网络连接，或增加超时时间
2. **无数据返回**：尝试更换新闻源或稍后再试
3. **Cookie 失效**：抖音等平台需要定期更新 session cookie
4. **API 变更**：如果某个平台长期无法获取数据，可能是 API 发生变更

## 网络请求说明

本 skill 会向以下第三方域名发送 HTTP 请求：

| 平台 | 域名 | 说明 |
|------|------|------|
| 微博 | `s.weibo.com` | 使用随机生成的 Cookie 模拟请求 |
| 知乎 | `www.zhihu.com` | 公开 JSON API |
| 百度 | `top.baidu.com` | 公开页面 + HTML 解析 |
| 抖音 | `login.douyin.com` + `www.douyin.com` | 自动获取 session cookie |
| 华尔街见闻 | `api-one.wallstcn.com` | 公开 JSON API |
| 今日头条 | `www.toutiao.com` | 公开 JSON API |
| 澎湃新闻 | `cache.thepaper.cn` | 公开 JSON API |

**注意事项**：
- ⚠️ **网络访问**：本 skill 会主动向多个第三方平台发送网络请求
- ⚠️ **速率限制**：部分平台可能有速率限制或 IP 封锁
- ⚠️ **敏感环境**：如在具有敏感网络访问权限的服务器或代理上运行，请注意流量
- ⚠️ **行为审查**：建议在隔离环境中运行，审查代码行为

## 安全说明

- 本 skill 直接调用各平台公开 API
- 不使用 MCP Server 或动态脚本执行
- 不依赖其他 skill与其他外部二进制文件
- 所有凭证均为自动获取或生成，**无需用户配置**
- 使用 Python 标准库 `urllib` 发送 HTTP 请求
- 无遥测数据收集，无意外出站端点

## 凭证说明

本 skill 实现了无需用户配置凭证的自动机制，具体如下：

| 平台 | 凭证处理方式 | 实现说明 |
|------|--------------|----------|
| 微博 | ✅ 自动生成 | 每次请求动态生成随机 Cookie 格式，无需用户配置 |
| 知乎 | ❌ 无需 | 官方公开 JSON API，直接访问 |
| 百度 | ❌ 无需 | 公开页面 + HTML 解析，直接访问 |
| 抖音 | ✅ 自动获取 | 自动请求 login.douyin.com 获取 session cookie |
| 华尔街见闻 | ❌ 无需 | 官方公开 JSON API，直接访问 |
| 今日头条 | ❌ 无需 | 官方公开 JSON API，直接访问 |
| 澎湃新闻 | ❌ 无需 | 官方公开 JSON API，直接访问 |

**说明**：
- 所有凭证（cookie）均为 skill 自动获取或生成，**无需用户提供**
- 微博使用随机生成的 Cookie 格式来模拟真实用户，避免反爬虫限制
- 抖音会自动获取 session cookie，无需用户干预
- 其他平台使用公开 API，无需任何凭证
