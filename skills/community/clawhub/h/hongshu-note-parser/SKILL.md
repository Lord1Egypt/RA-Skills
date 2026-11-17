---
name: hongshu-note-parser
slug: hongshu-note-parser
displayName: 小红书笔记解析
version: 1.0.1
summary: 丢一条小红书笔记链接，自动抓取标题/正文/图片/标签/互动数据，AI 分析后输出品牌可复用的结构化胶囊卡片 HTML 报告。
description: 丢一条小红书笔记链接，自动抓取笔记内容（标题/正文/图片/标签/互动数据），AI 分析后输出交互式胶囊卡片 HTML 报告。需要联网访问小红书页面下载笔记内容和图片。分析由调用方 AI 完成，不需要外部 API Key。
license: MIT
author: zhouq2039-lang
---

# hongshu-note-parser — 小红书笔记解析

**支持平台**：小红书 (xiaohongshu.com / xhslink.com)

## 一句话说明

用户丢一条小红书笔记链接 → 脚本抓取笔记内容+下载图片 → **你**（AI）分析内容 → 脚本生成 HTML 报告 → 交付给用户。

## 安全与权限

### Required Capabilities

| 权限 | 用途 | 触发条件 | 最小化说明 |
|------|------|----------|-----------|
| 网络访问（HTTP GET） | 访问小红书笔记页面、下载笔记图片 | 用户提供笔记链接时 | 仅访问用户提供的链接对应的小红书页面和图片 CDN |
| 本地文件写入 | 保存笔记数据 JSON、下载的图片、HTML 报告 | 采集和生成报告时 | 仅写入 output/ 目录 |
| 本地文件读取 | 读取 AI 生成的分析 JSON 生成 HTML | --generate-html 模式 | 仅读取指定的 JSON 文件 |

### 不执行的操作

- 不读取本地任意文件（仅读取用户指定的分析 JSON）
- 不访问任意 URL（仅访问用户提供的小红书链接和该链接中的图片资源）
- 不发送数据到第三方服务（不调用任何外部 API）
- 不执行子进程命令（不使用 subprocess / os.system）
- 不修改或删除已有文件

### 网络行为说明

- 脚本从 `xiaohongshu.com` 下载笔记页面 HTML
- 脚本从小红书图片 CDN（如 `xhscdn.com`）下载笔记配图
- 短链 `xhslink.com` 会被跟随重定向到完整链接
- 所有网络请求使用 urllib（Python 标准库），不依赖外部命令

### 数据隐私

- 笔记内容可能包含个人信息，请勿处理含敏感内容的笔记
- 分析由调用方 AI 完成，笔记内容不发送到任何外部 LLM API
- 请仅处理用户明确提供的链接

## 架构

```
parse.py（采集层）              AI（分析层）              parse.py --generate-html（交付层）
──────────────                 ──────────               ──────────────────────────────────
抓取笔记 → 下载图片 → stdout JSON → 读内容+看图 → 分析 JSON → 胶囊卡片交互 HTML
```

脚本只负责抓取内容和 HTML 渲染，**不做任何分析**。分析由调用方 AI 完成——不需要外部 API Key。

## HTML 报告样式

最终 HTML 是一个干净的卡片式交互页面：

- **Hero**：平台徽章 + 笔记标题 + 作者/类型/日期 + 互动数据栏（赞/收藏/评论/分享）
- **笔记图片**：缩略图画廊（如有多图）
- **一句话总结卡片**：左侧彩色竖线，核心观点 `<em>` 高亮
- **视觉策略分析**：独立区块，2 列卡片网格，品牌策划核心维度（封面策略/图片节奏/图文配合/视觉风格/品牌植入）
- **4 张胶囊卡片**：点击展开详情面板（内容拆解/金句摘录/数据标签/品牌可复用）
- **Footer**

## 依赖

```bash
# 无需额外安装！仅使用 Python 标准库（urllib / json / re / html）
```

## 工作流（四步）

### 调用约束

- **仅处理用户明确提供的链接** — 不主动扫描或推测 URL
- **处理前确认** — 抓取到笔记信息后，向用户展示标题/作者/互动数据，等待确认后再继续
- **单次一条链接** — 每次调用处理一条笔记

### 步骤 1：采集

```bash
python scripts/parse.py "小红书笔记链接"
```

stdout 输出单行 JSON：

```json
{
  "status": "parsed",
  "note_id": "abc123",
  "platform": "小红书",
  "title": "笔记标题",
  "desc": "笔记正文全文...",
  "note_type": "图文笔记",
  "publish_date": "2024.08.15",
  "author": {"nickname": "作者昵称", "user_id": "xxx", "avatar_url": "..."},
  "interactions": {"liked_count": "1234", "collected_count": "567", "comment_count": "89", "share_count": "12"},
  "tags": ["标签1", "标签2"],
  "images": [
    {"url": "https://...", "local_path": "output/0815-小红书-标题-img/img_0.jpg", "width": 1080, "height": 1440}
  ],
  "video_url": null,
  "data_path": "output/0815-小红书-标题-笔记数据.json",
  "output_dir": "output/"
}
```

> **必须从 stdout 解析**。stderr 是进度日志，忽略。

> 如果 `images` 中有 `local_path`，用 Read 工具读取图片文件来做视觉分析。

### 步骤 2：分析

读取 `desc` 字段（笔记正文）和 `images` 中的本地图片路径，深度理解笔记内容后，按以下 schema 输出分析 JSON：

```json
{
  "meta": {
    "platform": "小红书",
    "title": "笔记标题",
    "author": "作者昵称",
    "note_type": "图文笔记",
    "date": "2024.08.15",
    "stats": {"likes": "1234", "collects": "567", "comments": "89", "shares": "12"},
    "images": ["https://笔记图片URL1", "https://笔记图片URL2"]
  },
  "summary": "一句话总结。<em>核心策略</em> 用 em 标签包裹，页面高亮显示。",
  "visual_strategy": [
    {"label": "封面策略", "body": "封面图的视觉设计手法：对比/数字/情绪钩子/品牌露出方式...分析封面如何吸引点击"},
    {"label": "图片节奏", "body": "图片数量、页面递进逻辑（问题→科普→产品→数据→信任→护理）、浏览体验流..."},
    {"label": "图文配合", "body": "图片与正文的互补关系：图片承载什么信息、文字承载什么、是否有信息增量..."},
    {"label": "视觉风格", "body": "整体视觉调性：配色策略/排版风格/字体层级/信息密度/品牌一致性..."},
    {"label": "品牌植入", "body": "品牌/产品如何视觉化呈现：产品露出方式/卖点视觉化手法/信任背书呈现..."}
  ],
  "capsules": [
    {
      "id": "content",
      "icon": "📝",
      "title": "内容拆解",
      "subtitle": "标题/开头/正文/结尾",
      "detail_title": "内容结构拆解",
      "type": "structure",
      "content": [
        {"label": "标题策略", "body": "标题用了什么手法（数字/情绪/悬念/对比）..."},
        {"label": "开头钩子", "body": "前3行如何吸引读者继续看..."},
        {"label": "正文结构", "body": "信息组织方式（列表/故事/对比/教程）..."},
        {"label": "结尾引导", "body": "如何引导互动（提问/号召/预告）..."}
      ]
    },
    {
      "id": "quotes",
      "icon": "💬",
      "title": "金句摘录",
      "subtitle": "笔记中的关键句",
      "detail_title": "金句摘录",
      "type": "quotes",
      "content": [
        {"text": "笔记中的关键金句——必须从正文逐字摘录，不可编造"}
      ]
    },
    {
      "id": "data",
      "icon": "📊",
      "title": "数据与标签",
      "subtitle": "互动/标签/选题",
      "detail_title": "数据与标签分析",
      "type": "judgment",
      "content": [
        {"label": "互动数据", "title": "数据表现判断", "body": "赞藏比/评论率分析，内容质量 vs 流量表现..."},
        {"label": "标签策略", "title": "标签选择分析", "body": "用了哪些标签、覆盖什么搜索池、标签竞争度..."},
        {"label": "选题判断", "title": "选题方向分析", "body": "选题属于什么类型（种草/教程/测评/观点）..."}
      ]
    },
    {
      "id": "brand",
      "icon": "💡",
      "title": "品牌可复用",
      "subtitle": "模板/差异化/注意",
      "detail_title": "品牌可复用洞察",
      "type": "highlights",
      "content": [
        {"title": "可复用模板", "body": "从这篇笔记可以提炼出什么内容模板..."},
        {"title": "差异化建议", "body": "品牌方做同类内容时如何差异化..."},
        {"title": "注意事项", "body": "直接照搬的坑、平台规则限制..."}
      ]
    }
  ]
}
```

**分析规范**：

- **visual_strategy 固定 5 条**：封面策略/图片节奏/图文配合/视觉风格/品牌植入——这是品牌策划案的核心参考维度，每条都要具体到可直接参考的细节
- **金句必须从笔记正文逐字摘录**，编造的会被看出来
- **summary 里的 `<em>` 标签**：2-5 处，包裹核心判断词/概念
- **胶囊固定 4 张**：content + quotes + data + brand
- **capsule type**：`structure`（标签+内容）、`quotes`（引用列表）、`judgment`（三栏卡片）、`highlights`（编号要点）
- **content 条数**：structure 4 条，quotes 2-5 条，judgment 固定 3 条，highlights 2-4 条
- **meta.images**：把采集 JSON 中的图片 URL 数组放入，HTML 会自动渲染图片画廊
- **meta.stats**：把采集 JSON 中的 interactions 数据转换成 stats 对象

将分析 JSON 写入 `output/_analysis.json`。

### 步骤 3：生成 HTML

```bash
python scripts/parse.py --generate-html output/_analysis.json
```

stdout 输出：

```json
{"status": "generated", "html_path": "output/0815-小红书-标题-报告.html"}
```

### 步骤 4：交付

HTML 报告已生成在 `html_path`，将其展示给用户。无需额外处理。

---

## 参数说明

| 参数 | 说明 |
|------|------|
| `笔记链接`（采集模式） | 小红书笔记链接（长链/短链/分享文本均可） |
| `--generate-html <file>` | 从分析 JSON 生成 HTML 报告 |
| `--out-dir` | 输出目录（默认 `output/`） |
| `--no-images` | 跳过图片下载（仅提取文字和URL） |

## 已知限制

- **链接须含 `xsec_token`**：通过「分享→复制链接」获取的完整链接包含此参数；直接从浏览器地址栏复制的可能没有
- **部分笔记需要登录**：私密笔记或被限流的笔记可能无法抓取
- **页面结构可能变化**：小红书前端更新可能导致 `__INITIAL_STATE__` 解析失败，脚本会降级到 meta 标签提取
- **图片下载可能被限制**：CDN 可能对频繁请求限流，建议间隔处理多条笔记

## 示例文件

`examples/` 目录包含两个真实案例。示例 HTML 为**轻量版**（图片以占位符代替 base64 数据以控制文件体积），实际运行生成的报告会完整内嵌所有图片。每个案例同时包含分析 JSON（AI 产出模板）和 HTML 报告（布局参考）。
