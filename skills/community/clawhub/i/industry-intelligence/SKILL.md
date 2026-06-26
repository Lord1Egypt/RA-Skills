---
name: industry-intelligence
description: 行业情报 — 构建并维护某一行业的竞争对手资源库，持续采集监管动态/政策动态、媒体关注、企业官方发布、业务动态、企业数智化动态、国际同行、江湖传闻七大类信息，评估可信度与影响力，生成简报或详报。凡是用户提到"行业情报"、"竞争对手动态"、"行业动态"、"监管动态"、"政策动态"、"竞争对手资源库"、"行业情报收集"、"江湖传闻"、"国际同行"、"企业数智化"，或者想了解某个行业的竞争格局、跟踪同业动向时，都应触发本 skill。
---

# 行业情报（Industry Intelligence）

帮助用户对特定行业建立竞争情报体系：先构建资源库，再持续采集信息，最后生成可读报告。

---

## 执行规范（硬约束）/ Execution Rules (Hard Constraints)

**部分宿主环境（如 OpenClaw 4.10+）启用了 `exec preflight` 安全预检，会拦截"复杂解释器调用"。本技能所有代码执行必须严格遵循以下规范，否则会触发 `complex interpreter invocation detected` 报错。**

Some host environments (e.g. OpenClaw 4.10+) enable an `exec preflight` safety check that blocks "complex interpreter invocations". All code execution in this skill MUST follow these rules, otherwise the host will raise `complex interpreter invocation detected`.

### ✅ 允许的调用形式 / Allowed

只允许对 `{SKILL_DIR}/scripts/` 目录下已存在的脚本文件进行**直接调用**。由于 cwd 通常位于工作区而非技能安装目录，调用时需使用 `{SKILL_DIR}` 前缀（请把 `{SKILL_DIR}` 替换为 `SKILL.md` 所在目录的实际路径）。

Only **direct invocations** of existing script files under `{SKILL_DIR}/scripts/` are allowed. Because cwd typically sits in the workspace (not the skill install directory), prefix calls with `{SKILL_DIR}` (replace it with the actual directory of `SKILL.md`).

**⚠️ 解释器路径规则 / Interpreter Path Rule**：部分宿主（如 OpenClaw 4.10+）的 `exec preflight` 会拦截 `python` / `python3` 等裸命令形式的脚本调用，但**放行绝对路径解释器调用**（如 `/usr/bin/python3`）。因此：

Some hosts (e.g. OpenClaw 4.10+) block bare `python` / `python3` script invocations but **allow absolute-path interpreters** (e.g. `/usr/bin/python3`). Therefore:

**在首次调用脚本前，先运行 `which python3`（或 `command -v python3`）获取 Python 解释器绝对路径，后续所有脚本调用统一使用该绝对路径。** 若首次尝试裸 `python3` 命令即被 `exec preflight` 拦截，立即用 `which python3` 取得绝对路径后重试。

Before the first script call, run `which python3` (or `command -v python3`) to obtain the Python interpreter's absolute path. Use that absolute path for ALL subsequent script calls. If a bare `python3` call is blocked by `exec preflight`, immediately run `which python3` and retry with the absolute path.

```bash
# 第一步：获取 Python 解释器绝对路径（仅需一次）
which python3
# 输出示例: /usr/bin/python3

# 第二步：使用绝对路径调用脚本（请将 /usr/bin/python3 替换为实际输出）
/usr/bin/python3 {SKILL_DIR}/scripts/web_fetchers.py dynamic <URL>
/usr/bin/python3 {SKILL_DIR}/scripts/web_fetchers.py encoding <URL>
/usr/bin/python3 {SKILL_DIR}/scripts/web_fetchers.py xueqiu
/usr/bin/python3 {SKILL_DIR}/scripts/web_fetchers.py zhihu <URL>
/usr/bin/python3 {SKILL_DIR}/scripts/md_to_pdf.py <MD文件路径>
/usr/bin/python3 {SKILL_DIR}/scripts/md_to_pdf.py --check-fonts
/usr/bin/python3 {SKILL_DIR}/scripts/download_fonts.py
```

**Windows 用户不受此限制**，可直接使用 `python` 裸命令。Windows users are not affected — bare `python` works fine.

### ❌ 严禁的调用形式 / Forbidden

以下所有形式**一律禁止**，即便是"临时处理一下数据"也不行：

All of the following are **strictly forbidden**, even for "just quickly processing some data":

- `python -c "..."` — 内联代码串
- `python <<EOF ... EOF` — heredoc 形式
- `bash -c "python ..."` — 嵌套 shell 调用
- `echo ... | python` / 任何管道拼接的解释器调用
- 现场用 `Write` 生成一个临时 `.py` 文件再 `python` 执行它
- `node -e "..."` 及其他语言的等价内联形式

### 🚨 遇到 preflight 报错时的正确应对 / Correct Response to Preflight Errors

若宿主返回 `complex interpreter invocation detected`，说明**上一条命令的解释器调用方式被 preflight 拦截**，正确应对是：

If the host returns `complex interpreter invocation detected`, the interpreter invocation was blocked. Correct response:

1. **首先尝试改用 Python 解释器绝对路径**：运行 `which python3` 获取绝对路径（如 `/usr/bin/python3`），然后用该绝对路径重新调用同一脚本。大多数情况下这能立即解决问题；
2. 若绝对路径仍失败，**改用 `WebSearch` / `WebFetch` / `Write` / `Read` 等原生工具**完成同等功能；
3. **绝对禁止**以此为借口退化为"手动编造情报数据"——这会违反本技能"不自行编制情报"的核心红线（见"注意事项"章节）。宁可减少覆盖面、降级输出格式，也不可伪造数据。

1. **First, retry with the absolute interpreter path**: run `which python3`, then re-invoke the same script using the absolute path (e.g. `/usr/bin/python3 scripts/xxx.py <args>`). This resolves most cases immediately.
2. If the absolute path still fails, **fall back to native tools** (`WebSearch` / `WebFetch` / `Write` / `Read`).
3. **Never** fabricate intelligence data as a workaround — prefer reducing scope or downgrading output format.

---

## 文件路径约定 / File Path Convention

**本技能严格区分"只读技能资产"与"可写工作区输出"两类路径，严禁把生成的资源库 / 报告 / 日志写入技能安装目录。**

This skill strictly separates **read-only skill assets** from **writable workspace outputs**. Generated resource libraries, reports, and logs MUST NOT be written into the skill install directory.

### 🔒 只读技能资产 / Read-Only Skill Assets（`{SKILL_DIR}`）

指 `SKILL.md` 所在的技能安装目录，通常由宿主挂载为只读或跨会话共享。以下资源**只读**，只能通过相对 `SKILL.md` 的路径访问：

Refers to the directory containing `SKILL.md` — typically mounted read-only or shared across sessions by the host. Access via paths relative to `SKILL.md`:

| 用途 / Purpose | 路径 / Path |
|---------------|------------|
| 模板文件 / Templates | `{SKILL_DIR}/templates/{resource,brief-report,detail-report,log}.md` |
| 辅助脚本 / Helper scripts | `{SKILL_DIR}/scripts/{web_fetchers,md_to_pdf,download_fonts}.py` |
| 中文字体 / CJK fonts | `{SKILL_DIR}/fonts/*.ttf` |

### ✍️ 可写工作区输出 / Writable Workspace Outputs（`{WORKSPACE_DIR}/industry-intelligence/`）

所有**生成的文件**（资源库、简报、详报、PDF、采集日志）必须写入**当前 agent 工作区**下的 `industry-intelligence/` 子目录，而不是技能安装目录。默认以**当前工作目录（cwd）**作为工作区根，所有输出路径写作 `./industry-intelligence/...`：

All **generated files** (resource libraries, briefs, detail reports, PDFs, collection logs) MUST be written into the **current agent workspace** under an `industry-intelligence/` subdirectory — never into the skill install directory. The current working directory (cwd) is treated as the workspace root by default, so output paths are written as `./industry-intelligence/...`:

| 输出类型 / Output | 路径 / Path |
|------------------|------------|
| 资源库 / Resource library | `./industry-intelligence/resource/{行业名称}-resources.md` |
| 详报 MD / Detail report MD | `./industry-intelligence/reports/{行业名称}行业情报-{YYYY-MM-DD}.md` |
| 详报 PDF / Detail report PDF | `./industry-intelligence/reports/{行业名称}行业情报-{YYYY-MM-DD}.pdf` |
| 简报 / Brief | `./industry-intelligence/reports/{行业名称}简报-{YYYY-MM-DD}.md` |
| 采集日志 / Collection log | `./industry-intelligence/log/{报告名称}-{YYYYMMDDThhmmss}.md` |

**首次写入前**：若 `./industry-intelligence/` 或其子目录不存在，使用 `Write` 工具创建文件时直接使用完整路径即可（Write 会自动建立缺失的父目录）；若必须显式建目录，使用 `mkdir -p ./industry-intelligence/{resource,reports,log}`，不得使用内联 Python。

Before first write: if `./industry-intelligence/` or its subdirectories don't exist, simply use the full path with the `Write` tool (it auto-creates missing parents). If explicit creation is needed, use `mkdir -p ./industry-intelligence/{resource,reports,log}` — never inline Python.

### 📌 模式判断时如何定位资源库 / How to Locate the Resource Library During Mode Detection

进入技能时，按以下顺序查找现有资源库，命中任一即进入**采集模式**：

On skill entry, search for an existing library in this order; hit any → enter **Collection Mode**:

1. `./industry-intelligence/resource/{行业名称}-resources.md`（**首选**，当前工作区）
2. `./resource/{行业名称}-resources.md`（兼容旧版布局，当 cwd 已经位于工作区 `industry-intelligence/` 内部时）

均未命中 → 进入**建库模式**，最终写入位置为 `./industry-intelligence/resource/{行业名称}-resources.md`。

Neither hit → enter **Library-Building Mode**, writing the final library to `./industry-intelligence/resource/{行业名称}-resources.md`.

### 🚨 严禁的路径用法 / Forbidden Path Usage

- ❌ 向 `{SKILL_DIR}/resource/`、`{SKILL_DIR}/reports/`、`{SKILL_DIR}/log/` 写入任何新生成的文件
- ❌ 使用绝对路径引用技能安装目录（如 `/Users/.../industry-intelligence/resource/...`）来写入输出
- ❌ 假设技能安装目录可写——在 OpenClaw 等宿主中它通常是只读或会被下次部署覆盖

技能仓库内保留的 `resource/` `reports/` `log/` 目录仅作为**示例存档**与**模板参考**，不参与运行时输出。

The `resource/`, `reports/`, `log/` directories within the skill repository serve only as **example archives** and **template references** — they are not runtime output destinations.

---

## 工作模式判断

**每次被调用时，先判断当前处于哪个模式：**

1. **建库模式** — 用户首次对某行业开展情报工作，或尚无该行业的资源库文件。  
   → 执行"构建资源库"流程。

2. **采集模式** — 该行业的资源库文件已存在。  
   → 执行"情报采集与报告"流程。

资源库文件命名规则：`{行业名称}-resources.md`，保存在**当前工作区**的 `./industry-intelligence/resource/` 目录下（详见上方"文件路径约定"）。严禁写入技能安装目录。

---

## 模式一：构建资源库

### 目标
生成一份结构化的竞争对手资源清单，让后续信息采集有迹可循。

### 零代码路径 / Zero-Code Path

**建库阶段完全不需要执行任何 Python 脚本**。全流程仅使用以下原生工具：

The library-building phase **does not require executing any Python script**. The entire flow uses only native tools:

- `WebSearch` — 查询行业排名、主体数量、监管机构、官网 URL 等
- `WebFetch` — 按需验证单个页面（如公司官网是否可达）
- `Read` — 读取 `{SKILL_DIR}/templates/resource.md` 模板（只读技能资产）
- `Write` — 将填充好的资源库内容写入 `./industry-intelligence/resource/{行业名称}-resources.md`（当前工作区）

**若你发现自己正准备写 `python -c "..."` 或生成临时脚本来"结构化处理"搜索结果，说明路径走错了**——请立即停止，改回"WebSearch 获取 → 直接在对话上下文中整理 → Write 一次性写入"的纯文本流程。搜索结果的归纳整理应在模型推理中完成，而不是通过代码执行。

If you find yourself about to write `python -c "..."` or generate a temporary script to "structurally process" search results, **you are on the wrong path** — stop immediately and return to the plain-text flow: WebSearch → organize in-context → Write. Aggregation of search results should happen in model reasoning, not via code execution.

### 资源文件检查规则

**在生成资源文件前，必须执行以下检查：**

1. **检查已存在资源文件**：查看当前工作区 `./industry-intelligence/resource/` 目录下是否已存在相同行业的资源文件，包括：
   - 同名文件（如"证券行业-resources.md"）
   - 相似名称文件（如"证券业-resources.md"、"券商-resources.md"）

2. **存在时的处理规则**：
   - 若存在相同行业的资源文件，则在原资源文件基础上**补充**新信息
   - **不要删除或改变原资源文件内容**，因为用户可能已手工修改过
   - 除非用户明确表示要覆盖，否则只能增量添加

3. **质量问题处理**：
   - 若判断原资源文件质量很差，难以获取有效信息
   - 可向用户提出重新生成资源文件的申请
   - 在用户明确同意后，方可重新生成该行业的资源文件

### 竞争对手范围规则

用户可以用以下关键词指定覆盖范围，默认按行业收入排名确定：

| 用户指定 | 默认覆盖范围 |
|---------|------------|
| **头部企业**（或"龙头"、"Top 10"） | 行业收入排名前 10 名 |
| **中坚力量**（或"中型"、"第二梯队"） | 行业收入排名第 11～30 名 |
| **全市场**（或"全行业"） | 行业全部主体（受下述规则限制） |
| 用户直接指定公司名称 | 以用户指定为准，不受排名限制 |
| 用户指定具体数量（如"前20名"） | 以用户指定数量为准 |
| 用户指定区域范围（如"华东"、"广东省"） | 在指定区域内按排名确定 |

**若用户未说明范围，按以下规则确定：**

1. 行业主体数量 > 100 家：取前 30 名
2. 行业主体数量 ≤ 100 家：取前 20 名
3. 用户可通过设置区域范围（如"华东地区"、"广东省"）来限制行业主体数量
4. 若无法判断行业主体数量：取影响力最大的前 20 名

使用 WebSearch 确认当前行业排名和主体数量，优先使用最新年度收入数据。

### 步骤

**第一步：确认行业范围**  
向用户确认行业名称、关注焦点（如"商业银行"、"公募基金"、"消费金融"）、竞争对手范围以及区域范围（如有）。若未指定范围，按上述规则自动确定。

**第二步：调研并填充资源库**  
通过搜索工具（WebSearch）或用户提供的信息，收集以下内容：

**权威信息源（每家公司必须覆盖）：**
- 公司官网（官方公告、新闻发布）
- 主要监管机构（包含行业协会）
- 权威财经媒体

**推荐关注源（可选覆盖）：**
- 微信公众号、视频号等官方账号（建议人工查阅或使用第三方聚合源）
- 抖音号、小红书等自媒体账号

**监管与行业权威信息源：**
- 主要监管机构（如银保监会、证监会、央行等，按行业确定）及其官网/公众号
- 行业协会官网/公众号
- 权威财经媒体（如财新、21世纪经济报道、证券时报等）

**第三步：生成资源库文件**  
读取 `{SKILL_DIR}/templates/resource.md` 模板，按格式填充后用 `Write` 工具写入当前工作区的 `./industry-intelligence/resource/{行业名称}-resources.md`（**严禁写入技能安装目录**，Write 会自动创建缺失的父目录）。

输出文件后，告知用户文件的**实际绝对路径**，并提示："资源库已建立，可随时开始情报采集。"

---

## 模式二：情报采集与报告

### 前置确认
采集开始前，向用户确认：
- **时间范围**：由用户指定，不设默认值
- **报告类型**：简报 or 详报（用户未明确则默认详报）
- **重点关注**：是否有特别关注的公司或类别

**报告类型判断规则：**
- 用户明确说"简报"：生成简报
- 用户只说"情报"、"月报"、"周报"、"动态"、"报告"等字眼，未明确是"简报"：默认生成**详报**

**情报条数规则（全局限制）：**
为了保证报告精华度，防止内容臃肿导致输出限流或中断，最终写入报告的情报总数有着明确的上限。
1. **统一数量标准**：为保证报告信息的充实度与精华度的平衡，根据设定时间段，对最终报告入选条数设定如下标准范围：
   - 统计周期为 **31日以上**（如月报等）：入选条数原则上控制在 **40～50条**。
   - 统计周期为 **31日及以下，且大于1天**（如周报等）：入选条数原则上控制在 **30～35条**。
   - 统计周期为 **1天及以内**（如日报）：入选条数原则上控制在 **20～25条**。
   - **执行要求**：在执行情报采集检索时，应**充分收集并尽可能达到目标区间的下限**（例如周报必须尽力产出至少20条高价值情报），当可用情报总数超过上限后，再依系统评定截断。
2. **全局筛选**：生成报告前，从采集池中以**可信度**和**影响力**综合评分进行全局排序。严格截取对应限额内的最核心条目写入简报或详报。

### 信息采集规则

**采集阶段无数量限制：**
- 竞争对手、国际同行、行业主流供应商在采集阶段不限数量，符合时间范围和发布日期要求的情报均应采集
- 其他信息源同样无采集数量限制

**报告生成时的筛选规则：**
- 竞争对手、国际同行、行业主流供应商采集的情报**总体按影响力从高到低排序**
- 若单个数据源（单家公司）采集的信息超过 2 条，在生成报告时**最多选取 2 条**写入报告
- 选取原则：优先选取影响力最高的 2 条信息

**时间范围严格控制：**
- 采集的情报**必须**在用户设定的统计时间段内，以情报的**发布日期**为准。
- **柔性时间校验**：若网页缺乏明确的发布日期，允许模型根据网页收录时间、前后文进行合理推断论证。仅经过推断仍完全无法确定时间范围的情报，才视作无效并丢弃。
- 若情报内容提及的日期与发布日期不一致（如预告类信息），以发布日期判定是否在统计区间内。

**数据源访问策略：**

信息采集遵循“全网汇聚 -> 头部深挖”的两步走策略，不再强制暴力穷举所有官网。

1. **第一层面：全网汇聚（优先）**
   优先使用WebSearch进行全网层面的新闻和行业动态搜索。在限定时间范围内，重点检索 “[行业名称] 行业动态” 及重点公司的直接相关新闻。这能快速覆盖大部分具备影响力的情报（包含监管动态、媒体关注、国际媒体报道等）。
   
2. **第二层面：头部深挖（补充验证）**
   在全网汇聚后，为补充第一层级未能采集到的详细官方披露，仅对行业内**排名前 10 名的头部企业**的核心资产（通常即为各家主官网）进行深入排查。对中小企业与其他次级官网不再强制要求逐一访问。

**注意事项：**通过以上策略，在保障情报覆盖面的前提下有效降低单次大模型调用开销。被明确跳过查询的渠道数据源请在最终日志中一笔记录。对于自媒体与社区的情报收尾工作，严禁模型尝试模拟需要强制登录授权（扫码等）的媒体。

**访问方式优先级：**
1. **优先使用WebFetch**：快速获取静态页面
2. **WebFetch返回动态内容时**：
   - 若返回内容包含"需要启用JavaScript"、"SPA框架"、"动态渲染"等提示
   - 或返回内容为Vue/React模板语法（如 `{{item.title}}`）
   - 或返回内容为空HTML框架但无实际数据
   - **必须调用Playwright进行提取**，不得直接放弃该数据源
3. **WebFetch完全失败时**：记录错误原因，尝试其他采集方式

**首页无信息时的处理：**
- 如果在首页获取不到有效信息
- 尝试进入"公司新闻"、"公司动态"以及有行业相关关键字的栏目中进行查询

**翻页处理：**
- 如果发现消息列表下有"Next"、"更多"、"下一页"、可翻页的页码等信息
- 且当前页消息的日期仍在统计区间内
- 则自行进行"更多"或翻页点击操作

### 信息类别
采集时将信息归入以下七类：

| 类别 | 包含内容 |
|-----|---------|
| 🏛️ 监管动态/政策动态 | **管制类行业**（证券、银行、保险等）：政策导向与行业监管机构动向。**非管制类行业**：中央政府和地方政府对该行业的政策、法规、扶持措施等动态。栏目名称根据行业类型自动调整。 |
| 📌 媒体关注 | 公众媒体报道的并购重组、战略调整公告、年报/季报发布、高管变动等重大事件 |
| 🏢 企业官方发布 | 同业公司官网、官方微信公众号、视频号、抖音等官方渠道发布的公告、新闻、产品上线等 |
| 💼 业务动态 | 同业在业务领域的创新突破或重大成就。**信息来源**：权威媒体报道与各公司官方渠道发布的信息。**重点关注**：新产品、新服务发布，某一业务领域厚积薄发的成果，影响力评分权重提高 |
| 🔬 企业数智化动态 | 同业在企业数智化领域的重大投入或成就。**重点关注**：新系统上线、新技术应用、AI等技术落地成果，影响力评分权重提高 |
| 🌍 国际同行 | 国际主流财经/行业媒体报道、海外同业机构官网、官方Twitter/X、YouTube、LinkedIn等渠道发布的信息 |
| 🌫️ 江湖传闻 | 可信度 ≤ 3.5 的信息，来源为自媒体、微博、知乎、雪球等非权威渠道 |

### 采集记录格式
每条信息记录以下字段：

**⚠️ 时间校验要求**：发布时间字段为必填项，无法确定发布时间的情报不予收录。发布日期必须在用户设定的统计时间段内。

```
- 标题：{简短描述}
- 来源：{信息源名称}（类型：权威/非权威）
- 发布时间：{YYYY-MM-DD HH:MM} — ⚠️ 必填，无发布时间视为无效情报
- 关联公司：{公司名称，或"行业通用"}
- 类别：{监管动态/政策动态 / 媒体关注 / 企业官方发布 / 业务动态 / 企业数智化动态 / 国际同行 / 江湖传闻}
- 摘要：{100字以内的内容摘要}
- 原文链接：{URL，如有}
- 可信度：{1.0-5.0} — 评分依据见下方，精确到小数点后1位
- 舆情方向：{正面 / 中性 / 负面}
- 影响力：{1.0-5.0} — 评分依据见下方，精确到小数点后1位
```

**栏目名称判断规则：**
- **管制类行业**（证券、银行、保险、基金、期货、信托、支付等金融行业；医疗、医药、教育、能源等受强监管行业）：第一个栏目使用"🏛️ 监管动态"
- **非管制类行业**（互联网、消费、零售、制造业、服务业等）：第一个栏目使用"🏛️ 政策动态"，聚焦政府政策动态

**注意**："江湖传闻"类别仅收录可信度 ≤ 3.5 的信息，且需在来源中明确标注信息源平台（如"雪球用户XXX"、"知乎答主YYY"）。

**重要原则**：
- **不要自行编制任何情报或新闻**，严格以各个数据源获取的消息为准
- 在没有做专项的调动或查阅手段之前，**尽可能获取自媒体及社区情报**以充裕"江湖传闻"栏目

### 评估标准

**可信度评分（1.0-5.0）：**
| 分值 | 标准 |
|-----|------|
| 5.0 | 权威来源（监管机构官方、公司官方公告、主流财经媒体） |
| 4.0 | 可信来源（行业协会、知名财经媒体二次报道） |
| 3.0 | 一般可信（大型自媒体、知名分析师，有一定背书） |
| 2.0 | 待核实（小型自媒体、匿名消息源，内容有逻辑但未证实） |
| 1.0 | 存疑（流言、无来源消息、与其他信息明显矛盾） |

**影响力评分（1.0-5.0）：**
| 分值 | 标准 |
|-----|------|
| 5.0 | 影响行业格局或引发系统性变化（如重大监管法规、行业并购） |
| 4.0 | 影响多家公司或某类业务方向的重要动态 |
| 3.0 | 对特定公司或特定业务线有明显影响 |
| 2.0 | 影响有限，属常规经营动态 |
| 1.0 | 边缘信息，参考价值低 |

**业务动态与科技动态影响力加权规则：**
- 新产品/新服务发布、新系统上线、新技术应用落地：影响力评分 **+0.5**（最高不超过5.0）
- 某一业务领域厚积薄发的成果（如突破性产品、创新业务模式）：影响力评分 **+0.5**
- 这类信息在报告中优先展示，栏目内排序靠前

**舆情方向：**
- **正面**：对行业或相关公司有利的信息（如获批新牌照、重大合同中标）
- **中性**：事实陈述，无明显正负倾向（如人事调整、常规报告发布）
- **负面**：对行业或相关公司不利的信息（如处罚、业绩下滑、负面舆论）

---

## 报告生成

采集完成后，生成报告。

### 报告类型

**所有报告输出均写入当前工作区的 `./industry-intelligence/reports/` 目录**，严禁写入技能安装目录。

**详报（默认）：**
- 文件路径：`./industry-intelligence/reports/{行业名称}行业情报-{YYYY-MM-DD}.md`（同目录下再生成同名 `.pdf`）
- 标题格式：`{行业名称} 行业情报`
- 同时生成MD文件和PDF文件

**简报：**
- 文件路径：`./industry-intelligence/reports/{行业名称}简报-{YYYY-MM-DD}.md`
- 标题格式：`{行业名称} 简报 {日期}`
- 只生成MD文件

### 简报格式

读取 `{SKILL_DIR}/templates/brief-report.md` 模板（只读），填充后写入当前工作区的简报路径。

### 详报格式

读取 `{SKILL_DIR}/templates/detail-report.md` 模板（只读），填充后写入当前工作区的详报路径。

### PDF生成

**详报必须生成PDF文件：**
1. 先生成MD文件（写入 `./industry-intelligence/reports/`）
2. **使用** `{SKILL_DIR}/scripts/md_to_pdf.py` 脚本将 MD 转换为 PDF
3. PDF 文件与 MD 文件位于同一目录（即同在工作区 `./industry-intelligence/reports/`）

**调用方式：**
```bash
python {SKILL_DIR}/scripts/md_to_pdf.py ./industry-intelligence/reports/{行业名称}行业情报-{YYYY-MM-DD}.md
```

脚本不会修改 MD 源文件，默认输出 PDF 到与 MD 文件同路径的 `.pdf`。

**首次在新环境生成 PDF 前的字体自检（推荐）**：

当你是首次在当前宿主环境（例如新装的 OpenClaw 实例）调用本技能、或上一次生成 PDF 时出现"中文方块字"时，请先运行字体自检：

```bash
python {SKILL_DIR}/scripts/md_to_pdf.py --check-fonts
```

该命令会打印本地 `{SKILL_DIR}/fonts/` 目录内容、三级降级策略（本地字体 → 显式系统路径 → 目录扫描）的命中结果，以及最终选定的正文/标题字体。若输出 `✅ 中文字体可用` 即可直接开始生成 PDF；若输出 `❌ 未命中任何中文字体`，按提示选择：

1. 运行 `python {SKILL_DIR}/scripts/download_fonts.py` 下载开源思源字体（需外网）；
2. 或手动把任意中文 TTF/OTF 文件放入 `{SKILL_DIR}/fonts/` 目录；
3. 或在系统层面安装 Noto CJK / 微软雅黑 / 苹方 等任一 CJK 字体。

**`md_to_pdf.py` 内置的字体容错能力**（无需你手动处理，了解即可）：

- **三级降级链**：本地 `fonts/` → 显式系统路径（已覆盖 macOS PingFang/STHeiti/Hiragino/Songti、Windows msyh/simsun/simhei、Linux Noto CJK/文泉驿/AR PL UMing）→ 兜底扫描标准字体目录匹配 CJK 关键字文件名；
- **正文↔标题双向兜底**：只要找到任一字重即可支撑另一字重，不会因缺 bold 整体崩退到 Helvetica；
- **TTC 集合字体支持**：自动以 `subfontIndex=0` 注册 macOS/Windows 的 `.ttc` 字体；
- **失败隔离**：单个字体注册异常只降级字体，不会中断整个 PDF 生成流程。
**安全降级策略**：如果执行 `md_to_pdf.py` 失败（例如缺少依赖库抛出错误，或被宿主 `exec preflight` 拦截），**严禁中止整个技能任务**。您只需在执行日志和最终回复里说明"由于系统环境依赖缺失或宿主安全策略限制，PDF生成未成功，当前已为您提供完整的 Markdown 格式报告"，技能即视为妥善完成。

**降级红线 / Downgrade Red Line**：脚本被拦截或失败时，允许的降级动作仅限于"跳过该数据源并在日志中记录"、"仅输出 Markdown 不输出 PDF"、"减少覆盖的竞争对手数量"等**缩小范围**类操作；**严禁**以"脚本无法执行"为由伪造情报标题、摘要、链接、评分或发布时间。宁可交付一份条目较少的真实报告，也不可交付一份条目充足但内容编造的报告。

When scripts are blocked or fail, permitted downgrades are limited to **scope reduction** actions: skipping the data source (and logging it), emitting Markdown only without PDF, covering fewer competitors, etc. **Never** fabricate titles, summaries, links, scores, or publish dates under the excuse of "scripts cannot execute". A shorter but truthful report is always preferable to a full-length fabricated one.

---

## 采集日志

### 日志目录

日志写入当前工作区的 `./industry-intelligence/log/` 子目录（Write 会自动创建），严禁写入技能安装目录。

### 日志文件格式

**文件路径**：`./industry-intelligence/log/{报告名称}-{YYYYMMDDThhmmss}.md`
- 时间格式为 ISO 8601 基本格式（年月日T时分秒）
- 示例：`./industry-intelligence/log/证券行业行业情报-20260408T103000.md`

**日志内容格式**：读取 `{SKILL_DIR}/templates/log.md` 模板（只读），按格式填充后写入上述路径。

### 日志清理规则

**保留期限**：7天

**清理机制**：
- 在生成新的日志文件前，检查工作区的 `./industry-intelligence/log/` 目录
- 删除创建日期超过 7 天的日志文件（按文件名中的日期时间判断）
- 使用 `Bash` 直接删除匹配的文件（如 `rm <path>`），不要使用内联 Python

---

## 采集工具增强

为解决 WebFetch 经常遇到的网页动态渲染、反爬机制与编码乱码问题，本技能已在 `{SKILL_DIR}/scripts/` 目录下提供了辅助脚本 `web_fetchers.py`。**请直接使用命令行调用该工具的各项子功能，无需您自行编写或执行复杂的多行 Python 请求代码**。

以下示例统一使用 `{SKILL_DIR}/scripts/...` 路径；若你的宿主会将 cwd 设为技能目录则可省略前缀，但带前缀的写法在工作区 cwd 场景下始终可用。

### 浏览器自动化工具（机制应对 SPA / JS 依赖）

当WebFetch发现目标页面返回内容包含要求启用JS、为空、为 Vue/React 模板结构，或触发防爬墙时，应当调用 Playwright 的 headless 工具等待渲染。

**调用方式：**
```bash
python {SKILL_DIR}/scripts/web_fetchers.py dynamic <URL>
```
此命令内部设定了对页面渲染的 `networkidle` 空闲等待机制，并可确保稳定提取真实文本元素。

### 编码处理工具（应对乱套编码）

当遇到如国内传统券商或金融门户（东方财富等）返回 GB2312/GBK 等乱码并导致解码异常时，调用以下命令进行智能转码，自适应获取 UTF-8 明文内容。

**调用方式：**
```bash
python {SKILL_DIR}/scripts/web_fetchers.py encoding <URL>
```

### 自媒体/社区采集处理（“江湖传闻”获取口径）

作为“江湖传闻”栏目的供给项，自媒体与社区类数据源有着极高潜藏价值，但同样伴随着极高抓取难点。因此在作业时需严格遵循以下要求：

1. **红线（禁用模拟操作）**：**严禁尝试使用代码或浏览器强行模拟微信、抖音、小红书的登录或自动化提取流程**。此类带强烈风控的闭源生态数据对于大模型抓取极不现实，遇此必须建议采用手工翻阅或外部RSS解决。
2. **雪球热帖**：若欲获取散户传闻关注，直接调用工具内封装的雪球公共热帖 JSON API：
   ```bash
   python {SKILL_DIR}/scripts/web_fetchers.py xueqiu
   ```
3. **知乎爬取**：可调用内置脚本解析知乎指定问题的答案列表：
   ```bash
   python {SKILL_DIR}/scripts/web_fetchers.py zhihu <URL>
   ```
   
**建议**：江湖传闻并不局限在社区闭源APP，绝大部分具备参考水准的传言也常会借由全网媒体二创外流。模型最有效的补充方案是在前面第一步（全网网络汇聚）检索新闻时留心此类附带的传闻观点，而不是执着于在封闭APP内翻爬。

---

## 注意事项

- **信息时效**：时间范围由用户指定，不设默认值。**情报发布日期必须严格在统计时间段内，超出范围的信息不予收录。无法确定发布日期的情报视为无效，不予收录。**
- **报告筛选规则**：竞争对手、国际同行、行业主流供应商采集时不限数量，但生成报告时单个数据源最多写入 2 条，按影响力排序选取最高的 2 条。
- **信息去重**：同一事件被多个来源报道时，合并为一条，注明所有来源，可信度取最高值。
- **栏目名称调整**：管制类行业（证券、银行、保险、基金、期货、信托、支付、医疗、医药、教育、能源等）使用"监管动态"；非管制类行业使用"政策动态"。
- **业务动态与数智化动态优先展示**：新产品、新服务、新系统、新技术应用相关信息优先展示，影响力评分加权。
- **业务动态信息来源**：权威媒体报道与各公司官方渠道发布的信息，两者均需关注。
- **国际同行信息源**：包括国际主流财经媒体（如Bloomberg、Reuters、FT、WSJ等）、海外同业官网、官方Twitter/X、YouTube、LinkedIn等渠道。信息需标注境外来源。
- **行业主流供应商信息源**：资源库中新增行业主流供应商（不超过10家）的官网、官方公众号、视频号等渠道，用于采集"企业数智化动态"栏目信息。已生成资源文件的行业需补充该类渠道信息。
- **不确定信息**：可信度 ≤ 3.5 的信息归入"江湖传闻"栏目，需加注"⚠️ 仅供参考，需自行核实"警告标记。
- **企业官方发布来源**：优先采集公司官网公告、官方微信公众号、官方视频号等渠道发布的消息，可信度通常为 5.0。
- **用户校正**：如用户对资源库中的信息源有增删，直接更新 `{行业名称}-resources.md` 文件即可，下次采集自动使用最新资源库。
- **评分精度**：可信度和影响力评分精确到小数点后1位（如 4.5、3.2），不使用星级展示。
- **尾注格式**：报告末尾统一使用三行格式：第一行声明AI辅助生成及免责声明；第二行列举数据来源；第三行标注"industry-intelligence skill by sunhang(citywanderr)"。
- **不自行编制情报**：严格以各个数据源获取的消息为准，不要自行编制任何情报或新闻。
- **分层访问数据源**：P0（监管机构、权威媒体、竞争对手官网）必须全部访问；P1（国际同行、国际媒体、行业供应商）优先访问；P2（自媒体、社区）尽力访问。被跳过的数据源须在日志中记录原因。