# DESIGN.md — 知识库管理 Skill 架构设计

> v2.3.0 | 2026-06-14

## 设计目标

将微信/clawbot 传来的链接或文件，自动识别来源、下载/解析、上传到腾讯文档知识库，并写入 0 号索引智能表格。一条龙自动化。

## 架构总览

```
┌──────────────────────────────────────────────────────────┐
│                      输入层（链接/文件）                     │
│  视频号 │ 抖音 │ 小红书 │ 微信公众号 │ PDF/PPT/Word/图片     │
└─────────┬─────────┬─────────┬──────────┬──────────────────┘
          │         │         │          │
     ┌────▼────┐ ┌─▼──┐ ┌───▼────┐ ┌───▼──────┐
     │parsers/ │ │yt- │ │yt-dlp  │ │web_fetch │
     │sph.py   │ │dlp │ │        │ │          │
     └────┬────┘ └─┬──┘ └───┬────┘ └────┬─────┘
          │        │        │           │
          └────────┼────────┼───────────┘
                   │        │
              ┌────▼────────▼────┐
              │ upload_to_docs   │
              │  pre_import      │
              │  → COS PUT      │
              │  → async_import │
              │  → poll         │
              │  → add_to_sheet │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  腾讯文档知识库   │
              │  + 0号索引表格   │
              └─────────────────┘
```

## 核心设计决策

### 1. 统一下载方案：yt-dlp

**决策**：视频类（抖音、小红书）全部使用 yt-dlp。

**原因**：
- 抖音和小红书均为 yt-dlp 原生支持的 extractor
- 一行命令搞定，无需维护独立爬虫
- 自动处理格式选择、合并、重试
- 统一输出格式（JSON），调用方无需区分来源

**对比旧方案**（v1.0 小红书）：
- 旧：web_fetch → 解析 `__INITIAL_STATE__` → 只提取文本
- 新：yt-dlp 直接下载视频/图片 → 与抖音完全一致

### 2. 上传流水线：upload_to_docs.py

**决策**：将 pre_import → COS PUT → async_import → poll → add_to_sheet 封装为单一脚本。

**原因**：
- 避免 AI 在 WorkBuddy 上下文中逐步执行 5 个步骤
- 减少 token 消耗，提高可靠性
- 轮询逻辑内置，一次调用等到底

### 3. 索引写入：add_to_sheet.py

**决策**：独立脚本，统一管理 0 号索引的字段映射。

**固定字段 ID**（腾讯文档智能表格列 ID）：
- `fkfKit` — 文件名字
- `f2cnP7` — 文档大小(KB)
- `fHSMJO` — 入库时间
- `fOVcRT` — 格式
- `fPoljj` — 来源类型
- `f6drfQ` — 来源
- `fcP5do` — 是否外链
- `fBW04a` — 腾讯文档链接
- `fWqSI6` — 等级

## 组件设计

### parsers/

| 文件 | 功能 | 工具 | 输出 |
|------|------|------|------|
| `douyin.py` | 抖音视频下载 | yt-dlp | `{title, author, video, size_bytes}` |
| `xiaohongshu.py` | 小红书笔记下载 | yt-dlp | `{title, author, file, size_bytes, type}` |
| `wechat_article.py` | 公众号文章解析 | re (正则) | `{title, author, content, pub_time, url}` |

### 核心脚本

| 文件 | 功能 | 调用方式 |
|------|------|---------|
| `agent.py` | CLI 统一入口 | `python agent.py <cmd>` |
| `upload_to_docs.py` | 一键上传 | `python upload_to_docs.py <file> [options]` |
| `add_to_sheet.py` | 索引追加 | 被 upload_to_docs.py 调用，也可独立使用 |

## 数据流

```
链接输入
  │
  ├─ 视频号 → sph-download skill → title + video_path
  ├─ 抖音   → parsers/douyin.py   → title + video_path
  ├─ 小红书 → parsers/xiaohongshu.py → title + file_path
  ├─ 公众号 → web_fetch + parsers/wechat_article.py → title + content
  └─ 本地文件 → 直接取文件名
      │
      ▼
  upload_to_docs.py
    ├── [1/5] pre_import → upload_url, file_key, task_id
    ├── [2/5] curl PUT → COS
    ├── [3/5] async_import → 触发导入
    ├── [4/5] import_progress poll → file_url
    └── [5/5] add_to_sheet → 索引记录
      │
      ▼
  腾讯文档 + 0号索引
```

## 安全分析

### subprocess 调用清单

| 文件 | 调用 | 风险 | 结论 |
|------|------|------|------|
| `agent.py` | yt-dlp, mcporter, certutil, curl | 低 | 均为受控 CLI 工具，参数由内部构造 |
| `upload_to_docs.py` | mcporter, curl.exe | 低 | 参数由内部构造，不直接拼接用户输入 |
| `add_to_sheet.py` | mcporter | 低 | JSON 参数通过 json.dumps 序列化 |
| `parsers/douyin.py` | yt-dlp | 低 | URL 经过 extract 函数清洗 |
| `parsers/xiaohongshu.py` | yt-dlp | 低 | URL 经过 extract 函数清洗 |

**结论**：所有 subprocess 调用均为合理的 CLI 工具链调用，参数经过内部构造或清洗，无命令注入风险。✅

### 敏感信息

- `TENCENT_SPACE_ID`、`INDEX_FILE_ID`、`INDEX_SHEET_ID` 不再硬编码，改用环境变量 `KB_*` 或手动编辑配置
- 腾讯文档 API 鉴权由 mcporter + 环境变量 `TENCENT_DOCS_TOKEN` 统一管理
- ✅ 无硬编码 API Key
- ✅ v2.3.0 完成去个人化改造：所有用户特定 ID 均从环境变量读取

## 外部依赖

| 依赖 | 用途 | 安装方式 | 用户需自行配置 |
|------|------|---------|---------------|
| Python 3.8+ | 运行环境 | 系统安装 | — |
| yt-dlp | 抖音/小红书视频下载 | `pip install yt-dlp` 或 `winget install yt-dlp` | — |
| mcporter | 腾讯文档 MCP 调用 | npm/npx（腾讯文档 Skill 自带） | ✅ 需安装腾讯文档 Skill + TOKEN 授权 |
| curl | COS 文件上传 | Windows 10+ 自带 | — |
| 腾讯文档 Skill | MCP 服务端 | WorkBuddy Skill 市场安装 | ✅ 每个用户独立授权 |

## 版本演进

| 版本 | 日期 | 关键变更 |
|------|------|---------|
| v1.0 | 2026-06 | 初始版：基础 agent.py + 视频号支持 |
| v2.0 | 2026-06 | 小红书重写 yt-dlp 方案、新增 upload_to_docs.py |
| v2.1 | 2026-06 | 全量文档修复、新增 DESIGN.md/CHANGELOG.md、SkillHub 发布 |
| v2.2 | 2026-06 | 品牌升级「进击的知识库」、新增 parsers/sph.py 自研方案 |
| v2.3 | 2026-06 | **去个人化改造**：所有 ID 改为环境变量读取，新增首次安装配置引导 |
