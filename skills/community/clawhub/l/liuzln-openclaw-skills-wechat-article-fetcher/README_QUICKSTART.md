# WeChat Article Fetcher - 快速使用指南

## 📦 Skill 结构

```
skills/wechat-article-fetcher/
├── SKILL.md                    # 完整文档
├── README_QUICKSTART.md         # 本文件
├── scripts/                     # 工具脚本
│   ├── fetch.py                # 单篇文章爬取（主工具）
│   ├── batch_fetch.py          # 批量爬取工具
│   └── run_in_venv.py         # 虚拟环境运行工具
└── examples/                    # 示例脚本
    └── fetch_wechat_article.py # 示例脚本
```

## 🚀 快速开始

### 1. 爬取单篇文章（最简单）

```bash
# 基本用法
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw

# 指定输出目录
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  -o ./my_articles
```

### 2. 在虚拟环境中运行（推荐）

```bash
# 使用虚拟环境运行
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --venv /path/to/playwright-env
```

### 3. 批量爬取

创建 `urls.txt`：
```
https://mp.weixin.qq.com/s/xxx
https://mp.weixin.qq.com/s/yyy
https://mp.weixin.qq.com/s/zzz
```

然后运行：
```bash
# 从文件批量爬取
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py \
  --urls-file urls.txt

# 或者在虚拟环境中批量爬取
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  --urls-file urls.txt --venv /path/to/playwright-env --batch
```

## 📝 命令详解

### fetch.py - 单篇文章爬取

```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py [OPTIONS] URL

必需参数:
  URL                   微信公众号文章 URL

选项:
  -o, --output PATH     输出目录（默认: ./wechat_articles）
  --no-images           不保存图片
  --no-screenshot       不保存截图
  --headless BOOLEAN    无头模式（默认: true）
  --timeout INTEGER     超时时间（毫秒，默认: 60000）
  -h, --help            显示帮助信息
```

### batch_fetch.py - 批量爬取

```bash
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py [OPTIONS]

必需参数（二选一）:
  --urls URL1 URL2...   直接指定多个 URL
  --urls-file FILE      从文件读取 URL 列表

选项:
  -o, --output PATH     输出目录（默认: ./wechat_articles）
  --no-images           不保存图片
  --no-screenshot       不保存截图
  --headless BOOLEAN    无头模式（默认: true）
  --timeout INTEGER     超时时间（毫秒，默认: 60000）
  --delay FLOAT         每次爬取之间的延迟（秒，默认: 2.0）
  -h, --help            显示帮助信息
```

### run_in_venv.py - 虚拟环境运行

```bash
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py [OPTIONS] [URL_OR_ARGS...]

必需参数:
  --venv, -v PATH       虚拟环境路径

选项:
  --batch               使用批量爬取模式
  --script, -s PATH     指定要运行的脚本路径
  --script-args ...     传递给脚本的其他参数
  -h, --help            显示帮助信息
```

## 📁 输出目录结构

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

## 💡 使用示例

### 示例 1: 快速爬取一篇文章

```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw
```

### 示例 2: 只保存文字，不保存图片

```bash
python3 skills/wechat-article-fetcher/scripts/fetch.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --no-images
```

### 示例 3: 使用虚拟环境运行

```bash
python3 skills/wechat-article-fetcher/scripts/run_in_venv.py \
  https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw \
  --venv /home/liuzln/playwright-env
```

### 示例 4: 批量爬取 10 篇文章

创建 `my_urls.txt`：
```
https://mp.weixin.qq.com/s/xxx1
https://mp.weixin.qq.com/s/xxx2
...
https://mp.weixin.qq.com/s/xxx10
```

然后运行：
```bash
python3 skills/wechat-article-fetcher/scripts/batch_fetch.py \
  --urls-file my_urls.txt \
  --delay 3
```

## 🔧 配置说明

所有脚本都是通用的，可以处理任意微信公众号文章 URL，不需要修改代码！

## 📚 更多文档

详细文档请查看：`skills/wechat-article-fetcher/SKILL.md`
