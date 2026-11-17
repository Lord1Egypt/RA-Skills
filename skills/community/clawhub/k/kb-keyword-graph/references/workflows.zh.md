# 执行文档 · 四类任务的具体步骤

先读 SKILL.md 的路由表与公共约束。本文件是每类任务的执行细节。
所有命令从 skill 目录运行：`python3 scripts/kw_graph.py <子命令> [--base-id N] ...`。
引擎统一输出单个 JSON 到 stdout；`ok:false` 时 `error` 字段说明原因。

共同前置：确认 base_id（用户给的 / 配置默认），确认凭证已配（见 SKILL.md 首次使用）。
每类任务先向用户复述「我要对库 <id> 做 <任务>」，再执行。

---

<a id="structure"></a>
## 1. 知识结构 structure

**何时用**：用户问「这个库里有什么 / 知识结构 / 有哪些方面 / 结构长什么样」。

**跑**：
```bash
python3 scripts/kw_graph.py structure --base-id 700
```

**读输出**：`levels`（l1/l2/l3 各层节点数）+ `outline`（每个一级主题 → 其二级子话题 → 三级叶子）。`share_pct` 是该一级主题在全部一级里的 count 占比。

**怎么讲给用户**（模板）：
> 库 <id>（<file_count> 篇资料）分 <l1> 个一级主题、<l2> 个二级、<l3> 个三级。
> 一级主题有：<主题1>、<主题2>…（可带占比）。
> 其中「<最大主题>」下面细分为 <子话题…>。想深入哪一块？

**纪律**：一级主题按 outline 顺序或按 count 排序都可，但节点名和数字必须来自输出。不要把三层全部平铺念完（太长），先给一级 + 最重主题的展开，其余按需。

---

<a id="graph"></a>
## 2. 关键词图谱 graph

**何时用**：用户说「关键词图谱 / 知识图谱 / 词云 / 画个图」。

**跑**（必须给 `--html` 绝对路径，否则默认写到 state 目录）：
```bash
python3 scripts/kw_graph.py graph --base-id 700 --html /tmp/kw-700.html
```

**读输出**：`levels` + `metric: sibling_count_percentage` + `html`（生成的文件路径）。

**怎么讲给用户**：
> 图谱已生成（<l1>/<l2>/<l3> 三层），在 `<html路径>`。
> 交互：点一级主题 → 二级在同一张图内圈出现；点二级 → 三级继续出现。
> 图上百分比 = 节点在其**直接兄弟**中的占比（每组同级合计 100%），不是全库绝对占比，也不显示原始 count。

**纪律**：图是自包含单 HTML，可直接浏览器打开、可离线。不要声称它与 2brain 网页版逐节点完全一致——它渲染的是同一份 API 返回的树，呈现方式是我们定的（同级百分比 + 渐进环形）。

---

<a id="topics"></a>
## 3. 主题分布 topics

**何时用**：用户问「主要讲哪些主题 / 主题分布 / 哪块最多 / 重点是什么」。

**跑**：
```bash
python3 scripts/kw_graph.py topics --base-id 700
```

**读输出**：`topics` 是一级主题按 count 降序，每项含 `count` / `share_pct`（全库一级占比）/ `platform_weight`（2brain 给的同级重要度 0-100）/ `subtopic_count`。

**怎么讲给用户**：
> 库 <id> 的主题分布（按资料量）：
> 1. <主题> — 占 <share_pct>%（平台权重 <platform_weight>）
> 2. …
> 头部主题是 <top1>、<top2>，说明这个库主要沉淀了这些方向的资料。

**纪律**：`share_pct`（count 占比）和 `platform_weight`（平台权重）是两个不同视角，用户问"占比/最多"用 share_pct，问"平台认为的重点"用 platform_weight；两个都报更完整。不要把二者混为一谈。

---

<a id="relate"></a>
## 4. 解释资料关系 relate

**何时用**：用户问「X 和 Y 有什么关系 / 这两块怎么联系」。

**跑**：
```bash
python3 scripts/kw_graph.py relate --a Visa --b Sponsorship --base-id 700
```

**读输出**：`relation` ∈ {ancestor-descendant（上下位）, shared-parent（同一主题下直接同级）, cousin（同一上位主题、不同分支的远亲）, unrelated-in-graph（分属不同一级主题）}，加 `explanation` 与 `lowest_common_topic`。若某个关键词不在图中，`related:null` + `message` 提示。

**怎么讲给用户**：直接转述 `explanation`，并补一句 `caveat`（关系仅表示层级同现，不代表因果/语义等价/文档级来源）。

**纪律**：关键词大小写不敏感匹配。若同一关键词在树里出现多处（如既是一级又是某处叶子），引擎取首个匹配路径——必要时提醒用户该词有多重位置，或改用更具体的词。词不在图中就如实说「图谱里没有这个关键词」，不要硬编关系。

---

<a id="troubleshooting"></a>
## 5. 排错 troubleshooting

| 现象（引擎 error / 行为） | 原因 | 处理 |
|---|---|---|
| `缺少 2brain 图谱 Key` | 没配 TWOBRAIN_GRAPH_KEY / config.json | 按 SKILL.md 首次使用配置；提示用户去平台生成图谱 Key |
| `缺少有效的整数 base_id` | 没给 base_id | 向用户要目标库的整数 base_id，别猜 |
| `图谱 Key 无效或过期(HTTP 401/403)` | Key 错/过期 | 提示重新生成图谱 Key，别反复重试 |
| `无法连接 2brain` | 本机网络到不了 API_BASE | 检查网络/TWOBRAIN_API_BASE；课程环境应指 test.2brain.ai |
| `响应里没有非空的 keywords_tree` | 该库资料太少 / 刚入库未解析 | 如实告知资料不足以成图；刚入库的等解析完再用 `--fresh` 重拉 |
| 数字和网页版对不上 | 缓存旧 / 不同时刻响应 | 用 `--fresh` 重拉；说明图谱随入库内容变化 |
