---
name: 进击的知识库
slug: knowledge-base
description: |
  微信好用知识库，打通 Agent，多平台视频链接一键下载归档。
  微信/视频号/抖音/小红书/公众号的内容，丢过来自动识别、下载、上传腾讯文档，智能表格一键归档。
  抖音下载同步提取视频描述（创作者文案/#标签），保存为 .caption.txt。
  视频直传在线播放，文章自动转存。视频号用自研 sph-download，抖音/小红书用 yt-dlp，公众号用 web_fetch。
  支持 mp4/pdf/pptx/docx/jpg/png/文章。你负责发现好内容，我负责秒速入库。
  触发词：知识库、保存链接、存到知识库、帮我存这个、下载这个视频/文章、丢链接、进击的知识库
version: 2.4.1
token_budget: 8000
owner_type: user
tags:
  - knowledge
  - video
  - tencent-docs
  - video-download
  - caption-extraction
  - wechat-agent
---

# 🚀 进击的知识库

> **微信好用知识库，打通 Agent，多平台视频链接一键下载归档。**

## ⚠️ 安装前必读

> **此 Skill 需要以下前置条件，缺一不可：**

| # | 前置条件 | 说明 |
|---|---------|------|
| 1 | **腾讯文档 Skill 授权** | 在 WorkBuddy Skill 市场安装「腾讯文档」Skill，完成 TOKEN 授权 |
| 2 | **Python 3.8+** | 系统需安装 Python 3.8 或以上版本 |
| 3 | **yt-dlp** | `pip install yt-dlp`（抖音/小红书下载依赖） |

> 未完成以上三项，Skill 无法正常工作。详见下方「首次安装配置」。

## 核心能力

接收链接 → 自动识别来源 → 下载/解析 → 提取视频描述 → 上传腾讯文档 → 写 0 号索引。

**下载方案**：视频号用 `sph-download`（自研解析方案），抖音/小红书用 `yt-dlp`（含视频描述提取），公众号用 `web_fetch`。

| 来源 | 下载方式 | 文案提取 | 是否上传 |
|------|----------|---------|----------|
| 视频号 | parsers/sph.py（自研 sph-download 方案） | — | ✅ 上传腾讯文档 |
| 抖音 | yt-dlp（parsers/douyin.py） | ✅ 提取视频描述 | ✅ 上传腾讯文档 |
| 小红书 | yt-dlp（parsers/xiaohongshu.py） | — | ✅ 上传腾讯文档 |
| 公众号 | web_fetch 抓取 → markdown | ✅ 文章正文 | ✅ 上传腾讯文档 |

## ⚙️ 首次安装配置

> **此 Skill 面向新用户发布，每个用户需要自己完成以下配置。**

### 前置依赖

| 依赖 | 安装方式 |
|------|---------|
| **腾讯文档 Skill** | WorkBuddy Skill 市场安装 → 完成 TOKEN 授权 |
| **Python 3.8+** | 系统自带或 [python.org](https://python.org) 下载 |
| **yt-dlp** | `pip install yt-dlp` 或 `winget install yt-dlp.yt-dlp` |

### 1. 创建你的知识库空间

打开 [docs.qq.com](https://docs.qq.com)，新建一个知识库空间，从 URL 中获取 `space_id`：

```
https://docs.qq.com/space/DS2RjWGhWZ1VyaWt
                         └────── space_id ──────┘
```

### 2. 创建 0 号索引智能表格

在空间中新建智能表格，命名为「0号索引」，按以下字段建表：

| 列名 | 类型 |
|------|------|
| 文件名字 | 文本 |
| 文档大小(KB) | 数字 |
| 入库时间 | 日期时间 |
| 格式 | 单选 |
| 来源类型 | 单选 |
| 来源 | 文本 |
| 是否外链 | 复选 |
| 腾讯文档链接 | URL |
| 等级 | 单选 |

### 3. 配置环境变量

从表格 URL 中获取 `file_id` 和 `sheet_id`，设置环境变量：

**Windows：**
```cmd
setx KB_INDEX_FILE_ID "你的file_id"
setx KB_INDEX_SHEET_ID "你的sheet_id"
setx KB_TENCENT_SPACE_ID "你的space_id"
```

**macOS / Linux：**
```bash
export KB_INDEX_FILE_ID="你的file_id"
export KB_INDEX_SHEET_ID="你的sheet_id"
export KB_TENCENT_SPACE_ID="你的space_id"
```

> 也可以直接编辑 `agent.py` 和 `add_to_sheet.py` 中的配置区域，修改等号右边的默认值。

### 4. 验证

```bash
python agent.py identify "https://mp.weixin.qq.com/s/test"
# 应输出: {"url": "...", "source_type": "微信公众号"}
```

⚠️ **如果未配置环境变量**，脚本会打印警告但不会报错——索引写入功能会跳过。上传到腾讯文档的功能依赖腾讯文档 Skill 的 TOKEN 授权。

## 0 号索引字段

| 列名 | 类型 | 字段 ID（固定） |
|------|------|----------------|
| 文件名字 | 文本 | fkfKit |
| 文档大小 | 数字(KB) | f2cnP7 |
| 入库时间 | 日期时间 | fHSMJO |
| 格式 | 单选 | fOVcRT |
| 来源类型 | 单选 | fPoljj |
| 来源 | 文本 | f6drfQ |
| 是否外链 | 复选 | fcP5do |
| 腾讯文档链接 | URL | fBW04a |
| 等级 | 单选 | fWqSI6 |

## 工作流程

### 步骤总览

```
链接/文件 → 识别来源 → 下载到本地 → upload_to_docs.py → 腾讯文档 + 0号索引
```

### 各来源处理

#### 视频号

```
1. 下载（自研 sph-download 方案，无需 yt-dlp）：
   python parsers/sph.py <视频号链接> --output-dir <临时目录>
   → 返回 JSON {title, author, video, size_bytes}

2. 上传+索引：
   python upload_to_docs.py <video_path> \
     --name "<title>" --format mp4 --source-type 视频号 \
     --source-url "<原始链接>" --author "<作者>" --level 一般
```

#### 抖音

```
1. 下载 + 视频描述提取：
   python parsers/douyin.py <链接> --output-dir <临时目录>
   → 返回 JSON {title, author, video, size_bytes, description}
   → 同时保存 <video>.caption.txt（视频描述文案文件）

2. 上传+索引：
   python upload_to_docs.py <video_path> \
     --name "<title>" --format mp4 --source-type 抖音 \
     --source-url "<原始链接>" --author "<author>" --level 一般
```

#### 小红书

```
1. 下载（yt-dlp 方案，与抖音完全一致）：
   python parsers/xiaohongshu.py <链接> --output-dir <临时目录>
   → 返回 JSON {title, author, file, size_bytes, type}

2. 上传+索引：
   python upload_to_docs.py <file_path> \
     --name "<title>" --format <type> --source-type 小红书 \
     --source-url "<原始链接>" --author "<author>" --level 一般
```

#### 微信公众号

```
1. web_fetch 抓取文章内容，转 markdown
2. 创建腾讯文档（smartcanvas 或 markdown）
3. 上传+索引：
   python upload_to_docs.py <markdown_file> \
     --name "<标题>" --format 文章 --source-type 微信公众号 \
     --source-url "<原始链接>" --author "<公众号名>" --level 一般
```

#### 本地文件（pdf/pptx/docx/jpg/png）

```
python upload_to_docs.py <文件路径> \
  --name "<文件名>" --format <格式> --source-type 本地上传 \
  --level 一般
```

### upload_to_docs.py 自动完成

该脚本自动执行：
1. `manage.pre_import` — 获取 COS 上传凭证
2. `curl PUT` — 上传到 COS
3. `manage.async_import` — 触发导入
4. `manage.import_progress` — 轮询直到完成
5. `add_to_sheet.py` — 写入 0 号索引

```bash
python upload_to_docs.py <文件路径> \
  --name "标题" \
  --format "mp4|pdf|pptx|docx|jpg|png|文章" \
  --source-type "视频号|抖音|小红书|微信公众号|本地上传" \
  --source-url "原始链接" \
  --author "作者名" \
  --level "机密|高|一般|普通"
```

`--level` 不传默认为 `一般`，`--is-external` 不传默认为 `False`。

## 文件结构

```
knowledge-base/
├── SKILL.md              # 本文件
├── agent.py               # CLI 辅助
├── add_to_sheet.py        # 智能表格记录添加
├── upload_to_docs.py      # 一键上传（pre_import→COS→import→索引）
├── README.md              # 使用说明
└── parsers/
    ├── sph.py             # 视频号下载（自研 sph-download 方案）
    ├── douyin.py         # 抖音下载（yt-dlp）
    ├── xiaohongshu.py    # 小红书下载（yt-dlp）
    └── wechat_article.py  # 公众号文章解析
```

## 注意事项

- 视频文件大小限制：腾讯文档单文件 < 100MB
- 小红书 yt-dlp 依赖：需要 yt-dlp + cookies（如需要登录态）
- 公众号文章过长时可能触发 CreateProcess 命令行限制，使用 `upload_to_docs.py` 可绕过
- 索引记录的"入库时间"字段暂不支持 API 设置，需在腾讯文档 UI 上配置自动填入

## 常见问题

**Q：视频上传腾讯文档后能播放吗？**
A：能。腾讯文档支持 mp4 在线播放。

**Q：小红书下载失败？**
A：确认 yt-dlp 已更新到最新版：`yt-dlp -U`。个别小红书链接可能需要浏览器 cookies。

**Q：怎么确认上传成功了？**
A：查看 0 号索引智能表格，新记录出现即表示成功。也可以直接打开腾讯文档链接确认。
