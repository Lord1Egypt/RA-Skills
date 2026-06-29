# 🚀 进击的知识库

> **v2.3.0** | 发个链接就完事。视频号/抖音/小红书/公众号 → 自动采集 → 腾讯文档归档 → 智能索引

自动把微信 / clawbot 传来的链接或文件，解析下载后结构化保存到腾讯文档知识库。

## 支持来源

| 来源 | 状态 | 处理方式 |
|------|------|---------|
| 视频号 | ✅ | parsers/sph.py（自研 sph-download）→ upload_to_docs.py 上传 |
| 抖音 | ✅ | yt-dlp（parsers/douyin.py）→ upload_to_docs.py 上传 |
| 小红书 | ✅ | yt-dlp（parsers/xiaohongshu.py）→ upload_to_docs.py 上传 |
| 微信公众号 | ✅ | web_fetch 抓取 → 转 markdown → upload_to_docs.py 上传 |
| 图片/PDF/PPT/Word | ✅ | upload_to_docs.py 直接上传 |

## 支持的格式

| 格式 | 上传方式 | 在线预览 |
|------|---------|---------|
| mp4 | COS 直传 | ✅ 腾讯文档内置播放器 |
| pdf | COS 直传 | ✅ |
| pptx | COS 直传 | ✅ |
| docx | COS 直传 | ✅ |
| jpg/png | COS 直传 | ✅ |
| 文章 | 创建 markdown/smartcanvas 文档 | ✅ |

## 依赖

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.8+ | 脚本运行环境 |
| yt-dlp | latest | 抖音/小红书视频下载 |
| mcporter | latest | 腾讯文档 MCP 调用 |
| curl | Windows 10+ 自带 | COS 文件 PUT 上传 |
| 腾讯文档 Skill | — | MCP 服务端（mcporter 依赖） |

安装 yt-dlp：
```bash
pip install yt-dlp
# 或
winget install yt-dlp.yt-dlp
```

## 快速开始

### 1. 初始化知识库（仅首次）

⚠️ **每个用户需要配置自己的腾讯文档空间**，详见 SKILL.md 中的「首次安装配置」章节。

通过环境变量配置（推荐）：
```bash
# Windows: setx KB_INDEX_FILE_ID "你的file_id"
# macOS/Linux: export KB_INDEX_FILE_ID="你的file_id"

export KB_TENCENT_SPACE_ID="你的空间ID"
export KB_INDEX_FILE_ID="你的智能表格file_id"
export KB_INDEX_SHEET_ID="你的sheet_id"
```

也可直接编辑 `agent.py` 和 `add_to_sheet.py` 修改默认值。

### 2. 处理单个链接

视频号：
```bash
python parsers/sph.py "https://weixin.qq.com/sph/xxx" --output-dir ./temp
# 返回 {title, author, video, size_bytes}
python upload_to_docs.py ./temp/video.mp4 \
  --name "视频标题" --format mp4 --source-type 视频号 \
  --source-url "原始链接" --author "作者名"
```

抖音：
```bash
python parsers/douyin.py "https://v.douyin.com/xxx/" --output-dir ./temp
# 返回 {title, author, video, size_bytes}
python upload_to_docs.py ./temp/video.mp4 \
  --name "视频标题" --format mp4 --source-type 抖音 \
  --source-url "原始链接" --author "作者名"
```

小红书：
```bash
python parsers/xiaohongshu.py "https://www.xiaohongshu.com/xxx" --output-dir ./temp
# 返回 {title, author, file, size_bytes, type}
python upload_to_docs.py ./temp/file.mp4 \
  --name "笔记标题" --format mp4 --source-type 小红书 \
  --source-url "原始链接" --author "作者名"
```

公众号：
```bash
# 1. web_fetch 获取文章 HTML
# 2. 转 markdown 保存为 .md 文件
python upload_to_docs.py ./article.md \
  --name "文章标题" --format 文章 --source-type 微信公众号 \
  --source-url "原始链接" --author "公众号名"
```

本地文件：
```bash
python upload_to_docs.py "C:\path\to\file.pdf" \
  --name "文件标题" --format pdf --source-type 本地上传
```

## upload_to_docs.py 完整参数

```bash
python upload_to_docs.py <文件路径> [选项]

选项:
  --name <标题>                        文件名
  --format <mp4|pdf|pptx|docx|jpg|png|文章>  格式
  --source-type <视频号|抖音|小红书|微信公众号|本地上传>
  --source-url <原始链接>              来源 URL
  --is-external <True|False>           是否外链（默认 False）
  --level <机密|高|一般|普通>          等级（默认 一般）
  --author <作者名>                    作者/发布者
```

自动完成 5 步：
1. `manage.pre_import` → 获取 COS 上传凭证
2. `curl PUT` → 上传到 COS
3. `manage.async_import` → 触发腾讯文档导入
4. `manage.import_progress` → 轮询直到完成
5. `add_to_sheet.py` → 写入 0 号索引

## 文件结构

```
knowledge-base/
├── SKILL.md              # Skill 定义（WorkBuddy 入口）
├── README.md             # 本文件
├── DESIGN.md             # 架构设计文档
├── CHANGELOG.md          # 版本变更记录
├── agent.py              # CLI 自动化脚本
├── upload_to_docs.py     # 一键上传脚本（5 步链路）
├── add_to_sheet.py       # 智能表格记录追加
└── parsers/
    ├── sph.py             # 视频号下载（自研 sph-download 方案）
    ├── douyin.py         # 抖音下载（yt-dlp）
    ├── xiaohongshu.py    # 小红书下载（yt-dlp）
    └── wechat_article.py  # 公众号文章解析
```

## 0号索引字段

| 列名 | 字段 ID | 类型 |
|------|--------|------|
| 文件名字 | fkfKit | 文本 |
| 文档大小(KB) | f2cnP7 | 数字 |
| 入库时间 | fHSMJO | 日期时间 |
| 格式 | fOVcRT | 单选 |
| 来源类型 | fPoljj | 单选 |
| 来源 | f6drfQ | 文本 |
| 是否外链 | fcP5do | 复选 |
| 腾讯文档链接 | fBW04a | URL |
| 等级 | fWqSI6 | 单选 |

## 工作原理

```
clawbot/微信 → WorkBuddy → 知识库管理 Skill
                              ↓
                        识别来源类型
                              ↓
                  ┌──────────┼──────────┐
                  │          │          │
              sph.py    yt-dlp    web_fetch
              (视频号)  (抖音/小红书)  (公众号)
                  │          │          │
                  └──────────┼──────────┘
                             ↓
                    上传到腾讯文档
                             ↓
                    0号索引 追加记录
```

## 常见问题

**Q：视频上传腾讯文档后能播放吗？**
A：能。腾讯文档支持 mp4 在线播放。

**Q：小红书/抖音下载失败？**
A：确认 yt-dlp 已更新到最新版：`yt-dlp -U`。极少数链接可能需要浏览器 cookies。

**Q：公众号文章太长怎么办？**
A：使用 `upload_to_docs.py` 可绕过命令行长度限制，文章内容通过文件传入。

**Q：怎么确认上传成功了？**
A：查看 0 号索引智能表格，新记录即表示成功。也可直接打开腾讯文档链接确认。

**Q：小红书 yt-dlp 方案和之前的 web_fetch 方案有什么区别？**
A：旧方案只提取文本，无法下载视频。新方案使用 yt-dlp，一行命令完整下载视频/图片，与抖音方案完全统一。
