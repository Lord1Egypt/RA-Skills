---
name: github-skill-teardown
description: |
  扫描 GitHub 上的热门 Agent Skill（SKILL.md 生态），按星标建立候选池、逐个拆解设计手法，
  并针对国内实际给出「可直接抄 / 必须换 / 不能抄」三档改造意见。
  Use when the user says 分析 github 热门 skill、拆解 skill、github 上有哪些好的 skill、
  skill 竞品调研、看看别人怎么写 skill、对标 skill、github skill teardown，
  或要做 skill 的竞品分析、给自己写的 skill 找定位、评估某个 skill 值不值得抄。
  也适用于：蒸馏新视角前先看看同类竞品怎么做。
  输出：候选池 JSON + 拆解报告（含每条样本的国内改造意见）。
agent_created: true
---

# GitHub 热门 Skill 拆解

## 这个 skill 解决什么

给定「帮我看看 GitHub 上热门的 skill」这类需求，产出一份**有实测数据支撑、逐条拆解、带国内落地方案**的报告。不是罗列清单，是回答三个问题：

1. 这个生态真实的形状是什么？（谁热、谁冷、哪块是空白）
2. 每个头部样本**具体做对了什么**？（引原文，不凭印象）
3. 搬到国内要改什么、不能抄什么？

---

## 核心原则（不可跳过）

### 1. 先扫描，再选样；不凭印象点名单

**禁止**直接凭记忆列"我知道的热门 skill"。必须先用 API 跑一遍候选池，拿到真实星标后再选。

### 2. 每条结论必须能指回原文

拆解时不能说"这个 skill 强调简洁"——要引用原文句子。所有引用取自实际拉取的文件，不是二手印象。

### 3. 选样按星标排序 + 以设计原型去重

纯按星标取前十会得到一堆同质样本。正确做法：按星标排序，然后**剔除同原型的**（比如已经有了"单文件极简派"，就不再来第二个）。

常见原型（保证每类最多一个）：
- 方法论框架（改的是流程）
- 个人工作流直出（卖的是"某人的日常"）
- 巨型技能库（数量策略）
- 单文件极简（一份文档）
- 官方规范参考（定义者自己发的）
- 单点小工具（一个痛点一个 skill）
- 基建类（记忆/上下文/路由）
- 国产模型适配
- 中文原生垂直领域

### 4. 必须区分「星标热度」与「真实启用率」

这个生态星标被严重污染——有 12 个仓库超 10 万星，但其中相当一部分是 awesome 清单或无关工具被关键词误伤。
**头部 30 个仓库的描述里，只有约 30% 出现 "skill" 这个词。** 要在报告里明确提示这一点，别让读者以为星标高就是好用。

### 5. 每个样本必须写「说实话的问题」

只写优点的拆解没有价值。至少要指出：门槛在哪、什么场景下不适用、有没有商业动机、维护可持续性如何。

---

## 执行流程

### 阶段 1 · 建立候选池

用 `scripts/scan_repos.py`，多组 topic + 关键词检索、合并去重。

关键 topic/关键词清单（已实测有效）：

```
topic:agent-skills          topic:claude-skills
topic:claude-code-skills    topic:claude-code+topic:skills
topic:skills+topic:agent    q=skills+claude+in:name
q=SKILL.md+in:readme        q="agent skills"+in:name,description
```

同时**必须**另跑一组"国内生态"关键词（这是国内改造建议的事实基础）：

```
wechat skill / 微信+skill / xiaohongshu / 小红书 / douyin
feishu OR lark skill / dingtalk / deepseek skill / qwen OR 通义 skill
openclaw / agent-skills+中文 / 技能+skill
```

产出：`gh_skill_pool.json`（全量）+ `cn_skill_pool.json`（国内生态）

### 阶段 2 · 结构探查

用 `scripts/scan_tree.py`，对候选逐个拉：
- 默认分支、文件总数、仓库体积
- **SKILL.md 数量**（关键指标，判断是"库"还是"单点"）
- .md / 脚本 数量、许可证、最近推送时间
- SKILL.md 路径清单（判断目录组织方式：根目录 / `skills/` / `plugins/*/skills/`）

产出：`gh_skill_tree.log` + `gh_skill_detail.json`

### 阶段 3 · 抓正文

用 `scripts/fetch_bodies.py`，对入选样本拉 README + 主 SKILL.md 正文（截断 7000 字符，避免爆上下文）。

**抓取策略**（避免抓成几万个文件）：
```
skills = [f for f in files if f.endswith("SKILL.md")]
skills = [s for s in skills if s.count("/") <= 3]      # 只取浅层
root_first = sorted(skills, key=lambda s: (s.count("/"), len(s)))
for s in root_first[:4]: 拉取
```

产出：`gh_skills_raw/` 目录 + `gh_skills_raw.json`

### 阶段 4 · 统计与选样

用 `scripts/stats.py` 算：
- 星标分档分布
- 语言 / 许可证分布
- 活跃度（本月 / 近三月 / 更早）
- **编程类 vs 非编程类关键词命中数**（核心指标，用来证明"某块是空白"）

然后按「星标排序 + 原型去重」定十（或用户指定数量）个样本。

### 阶段 5 · 逐条拆解

每条固定四段，缺一不可：

```markdown
### N. owner/repo — 123,456★
**「一句话概括它是什么打法」**

**基本盘**：文件数 / 体积 / 主语言 / 许可证 / 分发通道 / 商业化入口

**它做对了什么**（3–5 点，每点必须引原文或给具体数字）

**说实话的问题**（2–4 点：门槛 / 不适用场景 / 商业动机 / 可持续性）

**国内拆改**
| 档 | 内容 |
|---|---|
| 可直接抄 | … |
| 必须换 | … |
| 不能抄 | … |
```

### 阶段 6 · 横向规律 + 国内总纲

见 `references/china-adaptation.md`（国内约束、可用通道、四条红线、空白位）。
横向规律部分要提炼**跨样本重复出现的模式**，而不是各说各话。

---

## 拆解时的几个高频洞察（已验证，可直接复用）

- **description 陷阱**：description 里概括工作流 → agent 会走捷径只读 description。实测案例见 superpowers。→ 只写「什么时候用」，不写「我做什么」。
- **「一次输出」检验**：能用一次输出交付可验证结果的 skill 才活得下来。改流程的（方法论）装了容易闲置。
- **可调参数 > 判断原则 > 方法论**：给配置卡（几个旋钮 + 信号→值映射表）比给方法论有效得多。
- **好骨架固定**：name+desc → When to Use → Principles → Checklist → 硬阈值 → 反模式表 → 失效条件 → 验证判据。**国内作者普遍缺最后三行。**
- **渐进式加载是硬要求**：metadata（~100 词常驻）→ SKILL.md 正文（触发时）→ references/scripts（按需）。800 行的 SKILL.md 会让用户觉得"装了变慢"。
- **meta-skill 决策树**：skill 超过 3 个就必须有路由图，否则没人用。

---

## 环境陷阱（Windows + WorkBuddy 沙箱，已实测）

- **Bash 工具下 coreutils 全缺**：`dirname` / `head` / `tail` / `grep` / `ls` / `awk` 一律 command not found。**不要在 Bash 里用管道和这些命令。**
- 但**直接调绝对路径的 python / node 是好用的**：
  `"$HOME/.workbuddy/binaries/python/envs/default/Scripts/python.exe"`
- 长任务（多仓库 × 多 API 调用）**必须后台跑 + 重定向到日志文件**，否则超时被 SIGTERM：
  ```
  python script.py > out/scan.log 2>&1
  ```
  然后 Read 日志文件（不要用 `tail`）。
- **PowerShell 工具不回传 stdout**，要 `Out-File` 到临时文件再 Read。
- GitHub API 用 `gh api`（已登录，5000/小时配额）。`gh.exe` 路径：
  `C:\Program Files\GitHub CLI\gh.exe`
- 每次 API 调用之间 `time.sleep(2)`，避免触发 secondary rate limit。

---

## 输出物

主报告：`outputs/GitHub热门Skill拆解与国内改造建议.md`

附：候选池 JSON、结构清单、原始正文目录、全部脚本（留档，下次改路径即可复用）。

---

*本 Skill 由一次真实调研沉淀而成（2026-09-21，319 个候选仓库，拆解 10 个头部样本 + 19 个观察名单）。*
