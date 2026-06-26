---
name: paper-kb
description: |
  Research paper knowledge base for storing and querying academic papers.
  Activate when:
  1. User shares an arxiv link or PDF file AND expresses intent to save/store it —
     keywords: "入库"、"存到知识库"、"加到知识库"、"帮我存"、"收藏"、"记录一下"、"保存起来"、"加进去"、"科研知识库"
  2. User says something like "帮我加到我的科研知识库" after receiving paper info
  3. User queries their personal knowledge base —
     keywords: "知识库里有没有"、"帮我查一下存过的"、"有没有我之前存的"、"查一下知识库"
  Do NOT activate when user only wants to summarize, discuss, or analyze a paper without any storage or query intent.
---

# 科研知识记忆库 (paper-kb)

---

## 第零步：每条消息必须先做的事

**获取用户身份**：从当前会话的 sender metadata 中提取 `open_id` 字段，作为本次所有工具调用的 `feishu_user_id`。这个值在整个对话中保持不变。

**检查用户是否注册**：调用 `query_papers`，`action=get_index`，传入 `feishu_user_id`。
- 返回 `success=true` → 用户已注册，继续正常流程
- 返回 `error` 包含"用户未注册" → 立即进入【流程A：新用户注册】，暂停处理原始请求

---

## 流程A：新用户注册

### A1. 发送注册引导消息（固定格式，不要修改）

> 你好！我是科研知识库助手 📚
>
> 检测到你是新用户，需要先完成一次初始化，只需两步：
>
> **第一步：注册 Gitea 账号**（已有账号跳过）
> 👉 http://43.156.243.152:3000/user/sign_up
> 用户名建议用英文，如 `mayidan`
>
> **第二步：回复以下内容**
>
> ```
> 用户名：你的 Gitea 用户名
> 姓名：你的姓名
> ```
>
> 示例：
> ```
> 用户名：mayidan
> 姓名：马一丹
> ```
>
> 回复后我会自动为你创建专属知识库和飞书表格 🚀

### A2. 解析用户回复

从用户回复中提取：
- `gitea_username`：`用户名：` 后面的内容，去掉空格
- `display_name`：`姓名：` 后面的内容，去掉空格

如果格式不对，礼貌提示用户按格式重新回复。

### A3. 调用 init_user 创建 Gitea 仓库

```
tool: init_user
参数:
  feishu_user_id: {open_id}
  gitea_username:  {用户填写的用户名}
  display_name:    {用户填写的姓名}
```

- 返回 `success=false`，`error` 包含"用户名不存在" → 告知用户先去 Gitea 注册，链接：http://43.156.243.152:3000/user/sign_up
- 返回 `success=true` → 继续 A4

### A4. 创建飞书多维表格

**A4-1. 创建表格应用**
```
tool: feishu_bitable_create_app
参数:
  name: "{display_name}的论文知识库"
```
记录返回值中的 `app_token`、`root_table_id`（即 table_id）、`url`。

**A4-2. 依次创建 9 个字段**（按顺序调用 9 次 feishu_bitable_create_field）

| 字段名 | field_type |
|--------|-----------|
| 标题 | 1 |
| 作者 | 1 |
| 年份 | 2 |
| 分类 | 3 |
| 关键词 | 4 |
| AI摘要 | 1 |
| 相关性 | 2 |
| Gitea链接 | 15 |
| 入库时间 | 5 |

每次调用格式：
```
tool: feishu_bitable_create_field
参数:
  app_token: {A4-1返回的app_token}
  table_id:  {A4-1返回的root_table_id}
  field_name: {字段名}
  field_type: {类型值}
```

### A5. 将表格信息存回 Gitea

```
tool: init_user
参数:
  feishu_user_id:   {open_id}
  action:           update_bitable_info
  feishu_app_token: {A4-1返回的app_token}
  feishu_table_id:  {A4-1返回的root_table_id}
  feishu_table_url: {A4-1返回的url}
```

### A6. 回复用户（固定格式）

> 初始化完成 ✓
>
> · Gitea 知识库：{init_user返回的repo_url}
> · 飞书知识表格：{A4-1返回的url}
>
> **请点击表格链接，向 AIFusionBot 申请编辑权限**，申请后管理员会为你开通。
>
> 开通后即可使用，发 arxiv 链接或 PDF 给我就能入库 📄

---

## 流程B：入库 arxiv 论文

**触发条件**：用户发送了 arxiv 链接，且表达了存储意图。

### B1. 查重

```
tool: ingest_paper
action: check_duplicate
feishu_user_id: {open_id}
arxiv_id: {从链接中提取，如 2401.12345}
```

- `is_duplicate=true` → 回复"这篇论文已在知识库中：{existing_md_url}"，流程结束
- `is_duplicate=false` → 继续 B2

### B2. 下载论文

```
tool: ingest_paper
action: fetch_arxiv
arxiv_url: {完整的arxiv链接}
```

返回：`title`、`authors`、`year`、`original_abstract`、`official_category`、`source_url`、`full_text`、`pdf_saved_path`、`pdf_downloaded`

### B3. 分析论文（你来完成，不调工具）

基于 `full_text`，生成以下内容：

| 字段 | 要求 |
|------|------|
| `keywords` | 5-8个英文关键词，列表格式 |
| `category` | 参考【分类指南】，确认或修正官方分类 |
| `abstract_summary` | 50字以内中文一句话概括 |
| `ai_overview` | 200-300字中文，说明做了什么、怎么做的、主要结果 |
| `relevance_score` | 1-10，评估与机器人/灵巧手/科研的相关性 |
| `relevance_reason` | 一句话说明评分依据 |
| `table_of_contents` | 保留原文章节编号和标题，换行分隔的字符串 |
| `chapter_summaries` | dict，key=章节标题，value=3-5句中文要点 |
| `core_methods` | list，每条一个核心技术点 |
| `main_conclusions` | list，每条一个主要结论或实验结果 |

### B4. 存入 Gitea

```
tool: ingest_paper
action: save
feishu_user_id: {open_id}
paper_data: {
  arxiv_id:          {B2返回}
  source_url:        {B2返回}
  title:             {B2返回}
  authors:           {B2返回}
  year:              {B2返回}
  original_abstract: {B2返回}
  category:          {B3生成}
  keywords:          {B3生成}
  abstract_summary:  {B3生成}
  ai_overview:       {B3生成}
  relevance_score:   {B3生成}
  relevance_reason:  {B3生成}
  table_of_contents: {B3生成}
  chapter_summaries: {B3生成}
  core_methods:      {B3生成}
  main_conclusions:  {B3生成}
  pdf_local_path:    {必须传入B2返回的pdf_saved_path原始值，即使经过多步分析也不要遗漏这个字段；若B2的pdf_downloaded=false则传null}
}
```

⚠️ **重要**：`pdf_local_path` 是必须从 B2 结果中原样传入的字段，不要省略，否则 PDF 文件将不会保存到 Gitea。

返回：`md_url`、`md_path`、`category`、`has_pdf`

### B5. 写入飞书表格

从 `query_papers get_index` 返回的 `user_info` 中读取 `feishu_app_token` 和 `feishu_table_id`。

```
tool: feishu_bitable_create_record
参数:
  app_token: {user_info.feishu_app_token}
  table_id:  {user_info.feishu_table_id}
  fields: {
    "标题":      {title},
    "作者":      {authors 用", "拼接成字符串},
    "年份":      {year，数字},
    "分类":      {category},
    "关键词":    {keywords 列表},
    "AI摘要":    {abstract_summary},
    "相关性":    {relevance_score，数字},
    "Gitea链接": {"text": "查看论文详情", "link": {md_url}},
    "入库时间":  {当前时间的毫秒时间戳}
  }
```

### B6. 回复用户

> 已入库 ✓
> 《{title}》
> 分类：{category} | 相关性：{relevance_score}/10
>
> {ai_overview 前120字}...
>
> Gitea：{md_url}

---

## 流程C：入库用户上传的 PDF

**触发条件**：用户发送了 PDF 文件，且表达了存储意图。

### C1. 提取全文

```
tool: ingest_paper
action: process_pdf
pdf_path: {OpenClaw提供的本地文件路径}
```

返回：`full_text`、`page_count`

若返回 `is_scanned=true`，回复用户："这个 PDF 是扫描版，无法提取文字，请提供可以复制文字的版本。"，流程结束。

### C2. 识别基本信息（你来完成）

从 `full_text` 中识别：
- `title`：通常在第一页最显眼位置
- `authors`：通常紧跟标题
- `year`：从参考文献、页眉页脚或版权信息推断
- `arxiv_id`：查找形如 `arXiv:2401.12345` 的标记，没有则设为 `null`
- `original_abstract`：找到 Abstract 部分

### C3. 查重（如果找到了 arxiv_id）

```
tool: ingest_paper
action: check_duplicate
feishu_user_id: {open_id}
arxiv_id: {C2识别到的arxiv_id，null则跳过此步}
```

### C4. 分析论文

与流程B的 B3 完全相同。

### C5. 存入 Gitea

与流程B的 B4 相同。

⚠️ **重要**：`pdf_local_path` 必须传入 C1 中 OpenClaw 提供的原始本地路径，不要省略。这是将用户上传的 PDF 保存到 Gitea 的唯一途径。

### C6. 写入飞书表格 & 回复用户

与流程B的 B5、B6 相同。

---

## 流程D：查询知识库

**触发条件**：用户询问知识库里有没有某类论文，或要查找之前存过的内容。

### D1. 读取索引

```
tool: query_papers
action: get_index
feishu_user_id: {open_id}
```

若 `total=0`，回复："知识库目前还没有论文，发 arxiv 链接或 PDF 给我就能开始入库 📄"，流程结束。

### D2. 分析相关性（你来完成）

对 `papers` 列表中的每篇论文，结合其 `title`、`keywords`、`abstract_summary`、`category`，判断与用户问题的相关度。选出最相关的论文（最多5篇）。

### D3. 读取论文详情

```
tool: query_papers
action: get_papers
feishu_user_id: {open_id}
paper_ids: [{相关论文的id列表}]
```

### D4. 回复用户

格式：
> 找到 {N} 篇相关论文：
>
> **1. 《{标题}》**（{年份}，{分类}）
> 相关性：{score}/10
> {ai_overview}
> Gitea：{md_url}
>
> **2. ...**

---

## 分类指南

| 代码 | 含义 | 典型内容 |
|------|------|---------|
| cs.RO | Robotics | 机器人操作、抓取、运动规划 |
| cs.LG | Machine Learning | 深度学习、强化学习、模型训练 |
| cs.CV | Computer Vision | 图像识别、目标检测、视觉感知 |
| cs.AI | Artificial Intelligence | AI方法、规划、推理 |
| cs.SY | Systems and Control | 控制系统、动力学 |
| cs.HC | Human-Computer Interaction | 人机交互、遥操作 |
| eess.SP | Signal Processing | 传感器信号处理 |
| eess.SY | Systems and Control (EE) | 电气控制系统 |
| math.OC | Optimization and Control | 优化算法、最优控制 |
| other | 其他 | 不属于上述分类 |

每篇论文只归入**一个**主分类文件夹。

---

## 错误处理

| 情况 | 处理方式 |
|------|---------|
| arxiv 下载失败 | 告知用户 PDF 下载失败，`pdf_local_path` 传 `null` 继续入库（只存 MD，不存 PDF） |
| PDF 是扫描版 | 告知用户提供可复制文字的版本，流程结束 |
| Gitea 提交失败 | 告知用户"存储失败，请稍后重试"，不写飞书表格 |
| 重复入库 | 告知用户已存在，给出已有链接，询问"是否需要更新这篇论文的分析？" |
| 用户未注册 | 进入流程A，完成后继续原始请求 |
| Gitea 用户名不存在 | 提示用户先注册，给出链接 |
| 无法识别 PDF 中的标题/作者 | 在 save 之前先问用户："请确认这篇论文的标题和第一作者是？" |

---

## 工具速查

| 工具 | action | 核心用途 |
|------|--------|---------|
| init_user | （无action，默认注册） | 创建 Gitea 仓库，写 users.json |
| init_user | update_bitable_info | 把飞书表格的 app_token/table_id/url 存入 users.json |
| ingest_paper | fetch_arxiv | 下载 arxiv 论文，提取全文 |
| ingest_paper | process_pdf | 从本地 PDF 提取全文 |
| ingest_paper | check_duplicate | 查重 |
| ingest_paper | save | 写 Gitea（MD + PDF + index.json） |
| query_papers | get_index | 读用户索引 + 用户bitable信息 |
| query_papers | get_papers | 读具体论文 MD 内容 |
| feishu_bitable_create_app | — | 创建新多维表格（OpenClaw内置） |
| feishu_bitable_create_field | — | 创建字段/列（OpenClaw内置） |
| feishu_bitable_create_record | — | 写入一行论文数据（OpenClaw内置） |
