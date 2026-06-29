# Skill: ingest_paper — paper-kb 资料入库（全类型）

## 用途

把用户发来的任意科研资料——论文、行业调研、开源项目、技术文档、实验记录、会议纪要
——自动分析并存入其专属 Gitea 知识库：生成结构化摘要页、更新跨文档概念页与科研资源页、
同步飞书多维表格、回复用户。支持来源形态：arxiv 链接、GitHub 链接、普通网页、
PDF、Word、Excel、txt、md、以及用户直接打字的纯文本。

> 注意：Skill 名虽叫 ingest_paper，但已支持全部六类资料，不限于论文。

## 触发条件

**Activate when（满足任一）：**
- 消息含 arxiv / GitHub / 普通网页链接，且有存储意图（"存"/"入库"/"保存"/"记录"/"加到知识库"）。
- 用户上传了文件（PDF/Word/Excel/txt/md），且有存储意图。
- 用户直接打字发来一段内容（如会议纪要、实验记录、想法），且有存储意图。
- 只发了链接/文件、没说存不存 → 先问"需要我把它存入知识库吗？"，确认后再执行。
- 上一轮查重发现疑似重复后，用户回复"覆盖"/"是"/"继续存"。

**Do NOT activate when：**
- 用户在查找/提问知识库内容 → 交给 query_papers。
- 用户未注册（init_user check 返回 registered=false）→ 先走 init_user。
- 用户明确说不要存了 / 取消。

## 前置依赖

- **current_user_open_id**：从消息上下文 sender 获取，传给所有脚本的 --open_id。
- 本 Skill 根目录需有 .env（GITEA_URL / GITEA_ADMIN_TOKEN / GITEA_BOT_USERNAME）。
- 用户必须已注册。用户记录里的 research_direction 在分析评分时要用。

## 两个维度彻底解耦（核心原则）

资料的**来源形态**和**资料类型**是两件独立的事，绝不能用形态推类型：
- **来源形态**只决定"怎么拿到文字"（见 Step 1）。一份 PDF 可能是论文、也可能是会议纪要。
- **资料类型**只根据"文字内容本身"判断（见 Step 2）。先无脑提取出文字，再纯看内容定类型。

## 六种资料类型

| type_key | 中文 | 是否评分 | 文件名 | 子文件夹 |
|----------|------|---------|--------|---------|
| paper | 论文 | 是（与研究方向相关性） | 标题 | summaries/papers/ |
| survey | 行业调研 | 是 | 标题 | summaries/surveys/ |
| project | 开源项目 | 是 | 项目名 | summaries/projects/ |
| doc | 技术文档 | 是 | 标题 | summaries/docs_tech/ |
| experiment | 实验记录 | 否（自有资料） | 日期+标题 | summaries/experiments/ |
| meeting | 会议纪要 | 否（自有资料） | 日期+标题 | summaries/meetings/ |

## 临时文件路径约定

所有中间文件放 /tmp/paperkb/：
- arxiv PDF：/tmp/paperkb/arxiv_{arxiv_id}.pdf（/ 替换为 _）
- 上传文件：/tmp/paperkb/upload_{原文件名}
- 网页/纯文字内容：写成 /tmp/paperkb/text_{简短名}.txt
- 你生成的草稿：/tmp/paperkb/draft_summary.md、draft_concept_*.md 等

PDF 路径中途丢失时，arxiv 论文按上述规则用 arxiv_id 重建；不存在则重跑 fetch_arxiv.py。

---

## 完整执行流程

### Step 1：拿到文字（只管提取，不判类型）

按来源形态分流，目标是得到一个本地文字文件 text_path：

**A. arxiv 链接：**
```bash
python3 scripts/fetch_arxiv.py --url "<链接或ID>"
```
得到 arxiv_id / title / authors / published / primary_category / abstract / pdf_path。
再对 pdf_path 跑 Step 1-E 的 process_doc 提取全文。

**B. GitHub 链接：** 用 GitHub/web 工具抓取该仓库 README 全文 + 基本信息
（用途、主要语言、star 数、目录结构概要），写入 /tmp/paperkb/text_<repo名>.txt 作为 text_path。

**C. 普通网页链接：** 用 web 抓取工具（参考 web-tools-guide）取正文，
写入 /tmp/paperkb/text_<简短名>.txt 作为 text_path。

**D. 用户直接打字的纯文本：** 把消息正文写入 /tmp/paperkb/text_<简短名>.txt 作为 text_path。
（不需要提取，文本就是内容。）

**E. 上传文件（PDF/Word/Excel/txt/md）：**
```bash
python3 scripts/process_doc.py --path "<文件路径>"
```
按后缀自动提取，输出 text_path（全文 txt）、truncated、head。
失败（纯扫描件等）把 message 转告用户并终止。

### Step 2：判断资料类型（纯看内容）

- 用户已明确说了类型（"这是会议纪要"/"存为实验记录"）→ 直接采用。
- 否则读 text_path 内容判断属于六类中的哪一类，依据是**内容写的是什么**，不是从什么文件来：
  - 论文：摘要/方法/实验/参考文献结构，学术写作
  - 行业调研：技术趋势、市场、多玩家横向分析、报告/综述口吻
  - 开源项目：README、安装使用、代码仓库说明
  - 技术文档：某工具/框架的用法、配置、教程
  - 实验记录：第一人称的实验目的/参数/结果/踩坑
  - 会议纪要：时间、参与者、讨论、决定、待办
- 实在判断不出 → 归为技术文档（doc）兜底。

记下 type_key（paper/survey/project/doc/experiment/meeting）。

### Step 3：AI 分析（你自己完成，按类型选模板）

先取用户的 research_direction。读 text_path 全文，按 type_key 选模板输出结构化 JSON。
所有类型共用统一 frontmatter 字段，差异只在正文 body_sections。

统一 JSON 外层：
```json
{
  "type_key": "<六选一>",
  "title": "中文标题（英文标题翻译；纯文本/会议则提炼标题）",
  "title_original": "原文标题（无则留空）",
  "brief": "一句话简介（50字内）",
  "keywords": ["关键词1", "...5-8个"],
  "relevance": {"score": 8, "reason": "结合研究方向说明"},
  "concepts": ["抽象概念，如 力控制"],
  "resources": [{"name": "具体资源名", "type": "数据集|开源项目|工具|硬件", "note": "如何使用/评价"}],
  "body_sections": [ {"h": "小标题", "md": "该节 Markdown 内容"} ]
}
```

**评分规则**：paper/survey/project/doc 需要 relevance（与 research_direction 相关性 1-10）；
experiment/meeting 是自有资料，不评分，relevance 留空。

各类型 body_sections 模板（小标题）：
- **论文 paper**：研究问题 / 核心方法 / 主要结论（带数据） / 章节要点 / 中文综述
- **行业调研 survey**：核心趋势 / 关键发现 / 主要观点 / 对我研究的启发 / 中文综述
- **开源项目 project**：项目用途 / 技术栈 / 核心功能 / 能否复用与上手难度 / 简介
- **技术文档 doc**：主题 / 关键知识点 / 操作要点 / 适用场景 / 简介
- **实验记录 experiment**：实验目的 / 配置与参数 / 结果数据 / 遇到的问题 / 结论与下一步
- **会议纪要 meeting**：时间与参与者 / 讨论要点 / 达成的决定 / 待办事项 / 关键结论

全部中文。concepts 只列抽象概念；resources 只列内容里实际使用/评测过的具体资源。

### Step 4：查重
```bash
python3 scripts/check_duplicate.py --open_id <open_id> \
    --title "<title>" --arxiv_id "<arxiv_id，无则省略>" --text_path "<text_path>"
```
- duplicate:true → 告知已存在（给 existing 标题与时间），问是否覆盖；确认后从 Step 5 继续，
  save 时加 --force；否则终止。
- possible_duplicate:true → 告知疑似与《existing.title》重复（similarity），同样问。
- 否则直接继续。

### Step 5：概念与资源规划（你自己完成）
```bash
python3 scripts/kb_read.py --open_id <open_id> --list all
```
据 Step 3 的 concepts/resources 与已有目录，决定每项 create/update/skip。规则：
- 知识库文档 ≤ 3 篇时，每篇最多新建 2-3 个概念页，宁缺毋滥。
- 同名或含义重叠的一律 update 已有页，不要 create。
- 不为"文档主题本身"建概念页。资源页同理：已有 update，新的才 create。

### Step 6：生成并保存概念页 / 资源页
create 项写草稿到 /tmp/paperkb/draft_concept_<名>.md 后：
```bash
python3 scripts/save_page.py --open_id <open_id> --kind concept \
    --name "<概念名>" --file "<草稿路径>" --brief "<一句话定义>"
```
update 项先 kb_read.py --read "concepts/<名>" 读旧内容，把新信息**融合改写进全文**（非追加），
再用 save_page.py 同名保存。资源页用 --kind resource --resource_type。

**【wikilink 格式铁律，所有页面通用】**
所有 [[...]] 双链**只写文件名本身，绝不带任何目录前缀**：
- 对 → `[[潜在扩散模型]]`、`[[视觉分词器]]`、`[[某论文标题]]`
- 错 → `[[concepts/潜在扩散模型]]`、`[[summaries/papers/某论文]]`（带前缀会导致 Gitea 拼出
  `concepts/concepts/...` 这种重复路径而 404；Obsidian 也只需文件名即可跳转）
- 文件名唯一即可被正确解析，无需写路径。链接目标必须是确实存在的页面。
- **标题尽量唯一**：因为只靠文件名跳转，若两个文件同名（即使在不同子文件夹）Obsidian
  会无法区分。生成标题时避免过于通用的名字（如单独的"实验记录""笔记"），可加上主题词。

### Step 7：生成最终版 summary 并保存
白名单 = 本次 create/update 的页面 + kb_read 列出的已有页面。按 type_key 模板生成 summary，
[[wikilink]] 只允许指向白名单内页面，且遵守上面的「wikilink 格式铁律」（只写文件名、不带目录）。

summary 页结构（frontmatter 统一 + 正文按类型）：

**YAML frontmatter 格式铁律（避免 Obsidian 解析失败）：**
- 所有字符串值**用双引号包起来**（标题、原文标题里常有冒号/逗号，不引会破坏 YAML）
- 关键词用标准 YAML 数组，**每个元素单独加引号**，逗号空格分隔，
  不要用中文方括号、不要让连字符/空格裸露
- 示例正确写法见下，OpenClaw 必须照这个格式生成
```markdown
---
标题: "<title>"
原文标题: "<title_original，无则省略此行>"
类型: "<中文类型名>"
来源: "<arxiv / GitHub / 网页 / 上传文件 / 用户输入>"
arxiv_id: "<有则填，无则省略此行>"
关键词: ["关键词1", "关键词2", "关键词3"]
相关性评分: "<评分类型填 1-10；自有资料填 自有>"
存入时间: "<今天日期 yyyy-MM-dd>"
---

# <title>

## 一句话总结
<brief>

<按 type_key 依次写 body_sections 各小标题与内容>

## 关键概念
[[概念名]] [[另一个概念]]（只写文件名不带 concepts/ 前缀；仅白名单内；无则省略本节）

## 科研资源
[[资源名]]（只写文件名不带 resources/ 前缀；仅白名单内；无则省略本节）
```

写入 /tmp/paperkb/draft_summary.md，然后：
```bash
python3 scripts/save_paper.py --open_id <open_id> \
    --type_key <六选一> \
    --title "<title>" \
    --summary_file /tmp/paperkb/draft_summary.md \
    --keywords "<逗号分隔>" \
    --brief "<brief>" \
    --score <评分类型填数字；自有资料这行可省略> \
    --arxiv_id "<有则填>" \
    --pdf_path "<原始文件路径，有则填，会存档到 pdfs/>" \
    --text_path "<text_path>" \
    [--force]
```
脚本自动按 type_key 路由到正确子文件夹、按规则命名（会议/实验加日期前缀）、
自有资料评分自动记为"自有"。输出含 summary_url / pdf_url / repo_url。

### Step 8：同步飞书多维表格（可选，失败不阻塞）
用户记录里 feishu_app_token 和 feishu_table_id 非空时，调
feishu_bitable_app_table_record（action: create）。

**字段值格式必须严格遵守飞书 API 规则（之前踩过坑）：**
- 文本字段（标题/类型/关键词/arxiv_id）→ 传字符串
- 数字字段（相关性评分）→ 传**纯数字，不要加引号**。如 `8` 不是 `"8"`
- 日期字段（存入时间）→ 传**毫秒时间戳（纯数字）**，不是字符串。
  用今天日期算：`int(time.mktime(time.strptime("2026-06-13","%Y-%m-%d")))*1000`
- 超链接字段（Gitea链接）→ 传 **`"显示文本|URL"` 这种竖线分隔的字符串**，
  **不是** `{"text":...,"link":...}` 对象！例：`"重建与生成的权衡|http://43.134.182.170:3000/..."`

```
app_token / table_id: 取自用户记录
fields: {
  "标题": "<title>",
  "类型": "<中文类型名>",
  "关键词": "<逗号分隔字符串>",
  "相关性评分": <纯数字 1-10，不加引号；自有资料（实验/会议）这个字段整个不要写进 fields>,
  "存入时间": <今天的毫秒时间戳，纯数字>,
  "Gitea链接": "<title>|<summary_url>",
  "arxiv_id": "<有则填，无则空串>"
}
```
字段为空或调用失败 → 最多重试 1 次，仍失败则跳过，回复中注明"飞书表格同步失败，
不影响知识库"。绝不因此中断或丢弃已保存内容。

### Step 9：回复用户
```
✅ 已存入知识库！

📄 <title>
🏷 类型：<中文类型名>｜🔑 关键词：<前几个>
（评分类型加一行）⭐ 与你研究方向的相关性：<score>/10 — <reason 精简一句>
🧠 概念页：<新建X个/更新Y个，列名字；无则省略>
🛠 资源页：<同上；无则省略>
🔗 查看详情：<summary_url>
```
覆盖模式开头改"✅ 已覆盖更新！"。飞书跳过/失败时追加说明。

## 错误处理总则
- 脚本输出单行 JSON；success:false 时按 message 转告用户，不堆原始报错。
- stdout 非 JSON = 脚本异常，告知用户并建议联系管理员。
- 任何一步失败都明确告诉用户哪一步失败、能否重试，不静默吞掉。
