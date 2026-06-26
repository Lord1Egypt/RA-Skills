---
name: photo-downloader
description: 批量下载豆瓣电影/电视剧/综艺的剧照和海报。输入片名自动搜索下载，完全自动化，不需要登录。支持缓存去重、反爬延迟。当用户提到"下载剧照"、"获取海报"、"批量下载图片"时使用。
license: MIT
compatibility: 需要Node.js环境
metadata:
  author: zj_john
  version: 1.1.0
  language: zh-CN
  category: media-download
  tags: "spider, crawler, image, download, photos, posters, douban"
  openclaw:
    requires:
      bins: ["node", "npm"]
    install:
      - id: playwright
        kind: node
        package: playwright
        bins: []
        label: "Install Playwright for Node.js"
security_warning: |
  本工具涉及网页爬取行为，可能受到豆瓣网的服务条款限制。使用前请确保：
  1. 遵守豆瓣网的用户协议和爬虫政策
  2. 仅用于个人学习、研究和私人用途
  3. 不用于大规模爬取、商业用途或公开分发
  4. 尊重网站的反爬虫机制和服务条款
  5. This tool does not connect to existing browser sessions for privacy
---

# 豆瓣剧照与海报批量下载工具

输入电影/电视剧/综艺的名称，自动搜索、提取、批量下载剧照或海报。完全自动化，不需要登录即可使用。

## 功能支持

✅ **核心功能**：输入名称 → 自动搜索 → 批量下载剧照/海报  
✅ 支持分类下载：剧照 (`S`) / 海报 (`R`)  
✅ 自动滚动加载更多图片  
✅ 缓存去重：已下载的文件自动跳过，支持分批下载  
✅ 随机延迟反爬（800-2000ms）  
✅ 正确处理 Referer 防盗链  
✅ 自动处理重定向  
✅ 保存到 `~/.openclaw/output/photo-download/{内容名}/{类型}/` 目录

## 支持场景

- ✅ 电影剧照和海报下载
- ✅ 电视剧剧照和海报下载  
- ✅ 综艺剧照和海报下载

## 不支持的场景

- ❌ 艺人/影人照片下载（豆瓣影人页面需要登录才能访问，公开API不支持）
- 需要登录才能访问的内容
- 大规模批量爬取整个网站（本工具仅适合少量下载）

## 文件说明

| 文件 | 作用 |
|------|------|
| **auto-download.js** | 推荐使用 - 全自动版本，Playwright无头浏览器自动完成搜索→提取→下载全流程 |
| **index.js** | 手动版本 - 纯HTTP请求，不用浏览器，兼容性较差 |
| **download.js** | 单页下载 - 只下载单个豆瓣照片页面里的图片，一般用不到 |

## 使用方法

### 基本用法（推荐）

```bash
# 下载默认：5张剧照
node auto-download.js "内容名称"

# 指定类型和数量：下载 10 张海报
node auto-download.js "内容名称" R 10

# 指定类型和数量：下载 3 张剧照
node auto-download.js "内容名称" S 3
```

参数说明：
- 第一个参数：**内容名称**（电影/电视剧/综艺名）
- 第二个参数：**类型**，`S` = 剧照（默认），`R` = 海报
- 第三个参数：**数量**，下载多少张，默认 5 张

## 使用示例

### 示例1：搜索《十二生肖》成龙电影，下载 2 张海报

```bash
node auto-download.js "十二生肖" R 2
```

### 示例2：搜索《人世间》电视剧，下载 2 张剧照

```bash
node auto-download.js "人世间" S 2
```

### 示例3：搜索《喜剧之王单口季》综艺，下载 2 张剧照

```bash
node auto-download.js "喜剧之王单口季" S 2
```

## 输出示例：

```text
========================================
🎬 剧照与海报批量下载 (自动无头浏览器版本)
🎬 内容: 人世间
📸 类型: 剧照
📊 批次数量: 2
========================================

🔍 Searching for "人世间"...
📍 Connecting to content platform...
✅ Found: "人世间 (2022)" (id: 35207856) rating: 8.4

🔍 Extracting photo ids from page...
🔌 Connecting to existing Chrome failed, starting new browser...
📖 Loading photos page: https://movie.douban.com/subject/35207856/photos?type=S
🖱️ Scrolling to load more photos...
Extracted photo IDs: 2864934437, 2864924871, ...
✅ Found 30 photos

💾 Download directory: /Users/xxx/.openclaw/output/photo-download/人世间 (2022)/剧照
📋 Found 0 already downloaded
⬇️ Downloading 2 photos...

  [1/2] 2864934437... ✅ 100KB
  [2/2] 2864924871... ✅ 138KB

🏁 Download complete! Success: 2, Failed: 0
📂 Saved to: /Users/xxx/.openclaw/output/photo-download/人世间 (2022)/剧照

💡 There are 28 more photos remaining.
   To download more, run: node auto-download.js 35207856 S 28
```

## 工作原理

豆瓣使用 Referer 防盗链机制来保护图片。本工具通过无头浏览器加载页面提取图片 ID，然后通过 Node.js 构造正确的请求头来下载图片，绕过防盗链保护。

**不需要登录**，公开剧照任何人都可以访问，所以不需要用户登录豆瓣。
