---
name: wechat-article-fetcher
description: Fetch and save WeChat Official Account articles with full content and images. Supports any WeChat article URL, automatic image download, JSON export, and full-page screenshots. Use when you need to archive, save, or analyze WeChat Official Account articles.
---

# WeChat Article Fetcher Skill

微信公众号文章爬取 Skill，支持任意微信公众号文章 URL，自动下载图片，导出 JSON，保存完整截图。

## 功能特性

- ✅ 支持任意微信公众号文章 URL
- ✅ 自动提取标题、作者、发布时间
- ✅ 提取完整文章内容
- ✅ 自动下载并保存文章图片
- ✅ 保存完整页面截图
- ✅ 导出 JSON 格式结果
- ✅ 支持虚拟环境（如 playwright-env）
- ✅ 无头模式（无 UI 服务器部署）
- ✅ 命令行工具支持

## 快速开始

### 1. 使用命令行工具

```bash
# 爬取单篇文章
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw

# 指定输出目录
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --output ./my_articles

# 不保存图片
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --no-images
```

### 2. 使用虚拟环境运行

```bash
# 方式 1: 激活虚拟环境后运行
source playwright-env/bin/activate
python3 skills/wechat-article-fetcher/scripts/fetch.py <url>

# 方式 2: 使用提供的包装脚本
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  <url> --venv /path/to/playwright-env
```

### 3. 在代码中使用

```python
from wechat_article_fetcher import fetch_article

# 爬取文章
result = fetch_article("https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw")

print(f"标题: {result['title']}")
print(f"作者: {result['author']}")
print(f"内容长度: {result['length']}")
print(f"图片数量: {result['images_count']}")
```

## 命令行工具

### fetch.py - 主要爬取工具

```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py [OPTIONS] URL

参数:
  URL                   微信公众号文章 URL（必需）

选项:
  -o, --output PATH     输出目录（默认: ./wechat_articles）
  --no-images           不保存图片
  --no-screenshot       不保存截图
  --headless BOOLEAN    无头模式（默认: true）
  --timeout INTEGER     超时时间（毫秒，默认: 60000）
  -h, --help            显示帮助信息
```

### batch_fetch.py - 批量爬取工具

```bash
# 从文件中读取 URL 列表
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py \
  --urls-file urls.txt

# 或者直接在命令行指定多个 URL
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py \
  --urls "url1" "url2" "url3"
```

### run_in_venv.py - 虚拟环境运行工具

```bash
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  <url> --venv /path/to/playwright-env
```

## 输出说明

每次爬取会创建一个以时间戳命名的目录：

```
wechat_articles/
└── 20260302_125500/
    ├── article.json          # JSON 格式结果
    ├── article.png           # 完整页面截图
    └── images/               # 文章图片目录
        ├── 001_image1.jpg
        ├── 002_image2.png
        └── ...
```

### article.json 结构

```json
{
  "title": "文章标题",
  "author": "作者名称",
  "publish_date": "2026-03-02",
  "url": "https://mp.weixin.qq.com/s/...",
  "content": "完整文章内容...",
  "images": [
    {
      "index": 1,
      "url": "https://mmbiz.qpic.cn/...",
      "alt": "图片描述",
      "filename": "001_image.jpg",
      "success": true
    }
  ],
  "images_count": 5,
  "images_dir": "wechat_articles/20260302_125500/images",
  "fetch_time": "2026-03-02T12:55:00.000000",
  "length": 15000
}
```

## 配置文件

可以创建 `config.json` 来自定义默认配置：

```json
{
  "headless": true,
  "timeout": 60000,
  "output_dir": "./wechat_articles",
  "save_images": true,
  "save_screenshot": true,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
}
```

## 使用示例

### 示例 1: 爬取单篇文章

```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw
```

### 示例 2: 批量爬取

创建 `urls.txt`：
```
https://mp.weixin.qq.com/s/xxx
https://mp.weixin.qq.com/s/yyy
https://mp.weixin.qq.com/s/zzz
```

然后运行：
```bash
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py \
  --urls-file urls.txt
```

### 示例 3: 在虚拟环境中使用

```bash
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --venv /home/user/playwright-env
```

## 最佳实践

1. **使用虚拟环境**: 隔离依赖，避免冲突
2. **合理设置超时**: 根据网络情况调整
3. **批量爬取时添加延迟**: 避免给服务器造成压力
4. **定期检查输出**: 确保图片和内容完整
5. **遵守 robots.txt**: 尊重网站的爬取规则

## 故障排除

### 问题: 找不到模块

**解决方案**: 确保在正确的虚拟环境中运行，或安装依赖：
```bash
pip install playwright
playwright install chromium
```

### 问题: 浏览器无法启动

**解决方案**: 安装系统依赖：
```bash
sudo apt install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
  libxfixes3 libxrandr2 libgbm1 libasound2
```

### 问题: 图片下载失败

**解决方案**: 检查网络连接，或使用 `--no-images` 跳过图片下载。

### 问题: 页面加载超时

**解决方案**: 增加超时时间：
```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  <url> --timeout 90000
```

## 相关资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [微信公众号开放平台](https://open.weixin.qq.com/)

## 更新日志

### v1.0.0
- 初始版本
- 支持单篇文章爬取
- 支持图片下载
- 支持 JSON 导出
- 支持完整页面截图
- 支持虚拟环境
- 提供命令行工具
- 提供批量爬取工具
