# 同类写作 SKILL 调研报告

**调研问题**：优秀的文档类 skill 怎么承载"不同文体该怎么写"。

调研执行日 2026-11-14。样本 6 个，其中 3 个只读到摘要层，结论按此打折。

## 一、摘要

1. **结论**：文体规范不写在 SKILL.md 里。每个文体一份独立说明文件，文件里是严格格式模板加一份样例。
2. **现在做什么**：先按这个模子重做一个文体，你看过再铺开，别一次改六份。
3. **最大风险**：样本不是随机抽的，三份只看过第三方转述，不能当成"全网普遍做法"。

## 二、方法与样本

选样方式：从两个官方仓库和三个索引站，按"与文档写作相关"挑，不是随机抽样。能读到全文的优先。

证据分三级，下文每条发现都标级别：

| 级别 | 含义 | 判断依据 |
|---|---|---|
| A | 读过文件全文 | 拿到 SKILL.md 或说明文件的完整内容 |
| B | 只看到目录与文件大小 | 通过仓库接口拿到文件清单 |
| C | 只有第三方转述 | 索引站的简介页或文章 |

| Skill | 级别 | 读到的材料 |
|---|---|---|
| internal-comms | A | SKILL.md **1,511 字节**，3p-updates.md **3,274 字节** |
| doc-coauthoring | A | SKILL.md 约 **1.6 万字符** |
| prd（awesome-copilot） | A | SKILL.md 全文 |
| design-docs-creator | C | 仓库 README 转述 |
| user-research | C | 索引站摘录的 SKILL.md 片段 |
| design_doc（社区） | C | 索引站摘录的 SKILL.md 片段 |

**不覆盖**：非写作类 skill、安装量与评分、真实使用效果。

## 三、发现

### 1. SKILL.md 只负责指路（A）

`internal-comms` 的 SKILL.md 正文只有三节：什么时候用、去读哪个文件、关键词。三个文体各指一个文件，第四个是兜底。全文没有一句"应该怎么写"。

`mcp-builder` 走同一路子：SKILL.md **11,129 字节**，另配 `reference/` 和 `scripts/` 两个目录（B 级，只看到清单）。

### 2. 规范落在"每个文体一份文件"，体量都在 2–3KB（A）

`internal-comms/examples/` 四份文件，大小分别是 **3,274 / 3,295 / 2,366 / 602 字节**。最大的一份也没有超过 3.3KB。

这个体量能一次读完，也改得动。超过这个量级，维护成本会吃掉收益。

### 3. 说明文件是四段式（A）

`3p-updates.md` 的四个小标题，顺序固定：

1. **Instructions**：这是什么、给谁看、多长、三个部分各写什么
2. **Tools Available**：素材从哪捞（Slack 高反应帖、Drive 高浏览文档、回复多的邮件、重要例会）
3. **Workflow**：四步，确认范围 → 捞素材 → 起草 → 检查够不够短
4. **Formatting**：严格格式，原文写"格式永远一样"，并禁止换成别的排版

### 4. 格式给到句数和阅读时长（A）

3P 的要求：每节 **1–3 句**，整篇 **30–60 秒**读完，要带数，语气平实，不要散文腔。

格式模板直接可填：

```
[一个 emoji] [团队名] (覆盖日期)
Progress: [1-3 句话]
Plans: [1-3 句话]
Problems: [1-3 句话]
```

这是全篇最值得抄的一处。它把"写多长""写几句"变成可执行的数，而不是形容词。

### 5. 章节多的时候分必写和选写（C）

`design-docs-creator` 把 21 节拆成 **8 必写 / 4 关键 / 9 建议**，再按项目类型变。支付与登录类项目，安全章节必写。生产系统，监控和回滚必写。

C 级证据，只看到 README 的转述，没读到它的 SKILL.md 原文。

### 6. 样例和正反例是标配（A）

`prd` 给了两组：

- 反例与正例对照：`搜索要快` 对比 `1 万条数据 200 毫秒内返回、Precision@10 ≥ 85%`
- 末尾一份完整范例，标题就叫"Example: Intelligent Search System"

`doc-coauthoring` 不给范例，改给流程：三阶段，每阶段有目标、步骤和退出条件。第三阶段让一个没有上下文的模型按预测问题去读稿，专门抓作者自己看不见的盲点。

### 7. 两条路线可以叠加（A）

结构型给骨架和样例，流程型给提问和验收。两者不冲突：先用流程问清楚，再套结构写。

## 四、和你现在这套的对照

| 维度 | 同类优秀做法 | writer-skill 现状 |
|---|---|---|
| SKILL.md 体量 | 1.5–11KB，只指路 | 约 **20KB**，规则与路由混在一起 |
| 文体规范 | 每文体一份 2–3KB 说明 | 七种原型各一行，写在 write-flow 的表格里 |
| 格式模板 | 可直接填的占位格式 | 无 |
| 长短与语气 | 给句数、阅读时长、语气词 | 只给句长上限（45/60 字） |
| 样例 | 一份完整范例 | examples 里有案例，文体规范里没有 |
| 提问 | 5 个元问题 + 5–10 个追问 | 通用五问 + 分文体补问，已有，可保留 |

你原来的强项不在这张表里：出处、模态、数字对账、修订可回退，同类 skill 基本没有。这层别动。

## 五、结论

1. 缺的不是"行业知识"，是**把知识压成可填格式**这一步。同类做得好的，都能让模型直接照格式写，而不是让模型自己发挥。
2. 一份说明文件控制在 3KB 以内、四段式、带一个样例，是这批样本的共同上限。
3. 先做一份，验证"模型拿到这份文件能不能写出合格文档"，再决定要不要铺到六种。

## 六、局限

- 6 个样本按可获得性挑的，不代表全网分布。
- 3 个只读到第三方转述，发现 5 的证据最弱。
- 同一仓库的星数在两个站点不一致：一处写 **41.1k**，一处写 **34.1k**，取证时点不同，未核实，不采用。
- awesome-copilot 的 skill 清单在接口响应处被截断，只看到前 **112 个**，实际更多。
- 没读 mcp-builder 的 `reference/` 内容，也没读 internal-comms 另外三份说明文件，无法判断它们的写法是否一致。

## 七、依据

访问日期均为 2026-11-14。只列仓库与页面，不逐条抄文件地址。

- anthropics/skills：internal-comms、doc-coauthoring 两组说明与示例，https://github.com/anthropics/skills
- github/awesome-copilot：prd 说明，https://github.com/github/awesome-copilot
- Michelangelo-Dev-Toolkit：design-docs-creator 说明，https://github.com/BrunoMartino/Michelangelo-Dev-Toolkit
- user-research 片段（第三方转述）：https://vibehackers.io/claude-code/skills/user-research-anthropics
- design_doc 片段（第三方转述）：https://claudepluginhub.com/skills/shouenlee-design-doc-plugins-design-doc/design_doc
