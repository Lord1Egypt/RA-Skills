---
name: invest_skill_copilot
description: |
  【仓库驱动的全场景投研分析技能】运行时读取 invest-skill 项目（Gitee 主源 warwickInv/invest-skill，
  GitHub 镜像 chenxyzcyxpp/invest-skill 可降级）的方法论与数据纪律，把仓库投研 Skill 的框架内化后，由一个统一入口直接完成用户要求的股票投研分析，
  覆盖个股诊断、股票对比、选股策略、行业速报、主题产业链、政策解读、舆情风险、底部信号、宏观配置、
  市场热点、每日收评、隔夜外围复盘等仓库全部应用场景；输出 Markdown + 自包含 HTML，全程遵守仓库防幻觉护栏。
  功能目录随仓库更新自动同步：检测远端 commit，有更新即重建 capability-catalog.md 功能目录。
  触发词：投研分析、帮我分析、个股诊断、这只票怎么样、对比分析、选股、策略选股、行业机会、
  产业链分析、政策影响、舆情风险、抄底、能不能加仓、宏观配置、市场热点、收评、盘前前瞻、隔夜外围、
  更新功能目录、同步 invest-skill、有什么新增能力、你能做什么。
version: 1.1.0
author: Warwick
source: 方法论源自 invest-skill（Gitee 主源 / GitHub 镜像），运行时动态读取
license: Apache-2.0
metadata:
  hermes:
    tags: [投研分析, 全场景, 个股诊断, 选股, 行业分析, 政策解读, 复盘, invest-skill]
    related_skills: [stock-5d-deep-analysis, industry-brief, market-daily-review, overnight-review]
  openclaw:
    requires:
      bins: [git, python3]
      env: []
---

# 仓库驱动的全场景投研分析（invest_skill_copilot）

> 基于开源项目 `invest-skill`（Gitee 主源 `warwickInv/invest-skill`，GitHub 镜像 `chenxyzcyxpp/invest-skill` 可降级）的投研方法论与数据纪律，做**一个入口、全场景**的股票投研分析。
> 所有数据可溯源、带时间戳；取数失败如实标注，严禁编造。不构成投资建议。

## 一、技能定位
本技能是一个**元技能**：先读取 invest-skill 仓库的方法论与数据纪律并内化，再由自己直接完成投研分析。
- 不把分析转交给仓库里的单一 skill；复用其**方法论框架、数据纪律、输出模板**，按用户需求组合。
- 规范是运行时动态读取的，仓库升级后自动跟随；**功能目录（capability-catalog.md）随仓库 commit 变化自动重建**，始终反映仓库最新能力。
- 适用：用户提出任意股票投研需求，且未指定必须用仓库某个具体 skill 时；或用户要求查看/更新功能目录。
- 不适用：纯交易执行、买卖/仓位/止损建议（越界，须拒绝并说明）。

### 功能目录同步（本技能的两份本地快照）
- `references/capability-catalog.md`＝**功能目录**：仓库全部 skill 的 id/分类/形态/触发词/方法论一句话，文件头记 `repo_commit` 与 `synced_at`。用于路由与回答"有哪些能力"。
- `references/repo-spec-digest.md`＝**规范摘要**：数据纪律、护栏、降级链、场景映射的浓缩。用于分析时快速内化。
- 二者由 `scripts/repo_sync.py` 生成/刷新，Agent 与用户都不手写。远端不可达时保留上一版并标注 commit 时间，不猜测、不清空。

## 二、硬红线（最高优先级，继承自仓库 GATEWAY_REFERENCE.md 第 5 节）
> 源于一次数据编造事故，不可妥协。与输出质量冲突时，宁可少写结论，不可编造数据。
1. **不编造**：取数失败、字段缺失、源无数据，一律标注「数据缺失 / N/A / 源不可用」，严禁模型生成数字、结论或引用。
2. **可溯源**：每个数值标注 `data_source` 与获取时间；读者能区分「实测数据」与「本报告观点/推演」。
3. **降级留痕**：记录数据源切换轨迹（从哪级、因何、切到哪级、最终命中）。
4. **明确报错**：全源失败返回 error，不回退过期缓存、不返回"看起来合理"的占位值。
5. **事实与结论分离**：推断须显式标注为观点，不得当已验证事实陈述。
6. **局部失败不阻断**：某维度取数失败，该维度显式标记，其余照常输出，不掩盖缺口。
7. **不越界**：不提供买卖/仓位/止损建议，重点个股统一称「重点公司验证」，全文附免责声明。

## 三、数据源与降级（继承自仓库四级链）
严格顺序命中即止：**Tushare（需 TOKEN）→ Akshare → Baostock → 东方财富/腾讯网页源**。
- 无 token 自动降级，不中断。
- 关键字段（收盘价、PE/PB、涨跌幅）至少取一个次级源交叉校验；偏差超阈值（价格>1%、比率>5%）标记 conflict 并显式提示，不自动选其一。
- 字段缺失不插值、不估算。
- 用户未配置任何数据源 token 且开源源也失败时，如实说明"无法获取实时数据"，可基于仓库样例做**方法论演示**但必须显著标注"演示数据，非实时行情"。

## 四、强制执行流程

### Step 0 · 检测更新 → 同步功能目录 → 内化规范（本技能独有，不可跳过）
1. **检测仓库更新（双源降级）**：调用 `scripts/repo_sync.py --check`——按优先级探测 Gitee 主源（`https://gitee.com/warwickInv/invest-skill.git`），不可达自动切 GitHub 镜像（`https://github.com/chenxyzcyxpp/invest-skill.git`）；以命中源的 commit 与 `capability-catalog.md` 文件头的 `repo_source` + `repo_commit` 比对（两源 commit 可能不同，换源会被正确识别为变更）。
2. **有更新则同步**：源或 commit 不一致（或快照缺失 / `synced_at` 超 7 天）→ 运行 `scripts/repo_sync.py --sync --diff`，重建 `capability-catalog.md`（功能目录）与 `repo-spec-digest.md`（规范摘要），并向用户简述本次新增/移除/升版了哪些 skill。无更新则跳过，直接用本地快照。
3. **读功能目录**：读 `capability-catalog.md`，掌握仓库当前全部能力，作为 Step 1 场景路由的清单。
4. **读规范摘要 + 按需深读**：读 `repo-spec-digest.md` 内化「防幻觉护栏、四级降级链、场景映射」；命中具体场景后再追加读该 skill 的 `SKILL.md` + `references/`。
5. 读取方式：按快照 `repo_source` 选 raw 前缀——Gitee 用 `https://gitee.com/warwickInv/invest-skill/raw/main/<path>`，GitHub 镜像用 `https://raw.githubusercontent.com/chenxyzcyxpp/invest-skill/main/<path>`；两源都不可达时只读本地两份快照并标注"功能目录停留在 [源] commit XXX，未能检测更新"。
6. **禁止只读单个 SKILL.md 就分析**——必须连同其 `references/` 一起读（仓库 README 明确警告缺 references 会残缺）。
7. **用户显式要求时**（"更新功能目录/同步 invest-skill/有什么新增能力/你能做什么"）：强制执行 `--sync --diff` 并只输出功能目录与变更摘要，不进入投研分析。

### Step 1 · 意图识别与场景路由
- 按 `references/methodology-map.md` 的场景—方法论映射表识别一个或多个场景，确定主/辅线。
- 按需追加读取目标场景 Skill 的 `SKILL.md` + `references/`，提取其方法论框架与输出模板。
- 场景不明确时，用一句话向用户确认，不擅自假设。

### Step 2 · 取数（继承 §二/§三 全部纪律）
- 按目标方法论的字段清单取数，逐字段标注来源与时间。
- 执行交叉校验与降级留痕；任何缺口显式标注。

### Step 3 · 分析（内化方法论，自己执行）
- 严格套用目标方法论的框架与口径（如五维分析就按五维、产业链就按上中下游×核心弹性补涨）。
- 事实与观点分层；结论给出可证伪条件与失效信号。

### Step 4 · 输出
- 按目标场景的输出模板生成，结构完整、带溯源角标与免责声明。
- 同时产出 Markdown 与**自包含 HTML**（图表内嵌 data URI，无本地路径依赖，可离线打开）。
- 落盘至 `files/report/`，命名 `{主题}_{YYYYMMDD}_投研分析.md/.html`。
- 字数：单场景 2500–5000 字；多场景按主次分配，不机械堆砌。

## 五、输出格式（通用骨架，具体以场景模板为准）
1. 核心结论（前置，明确标注事实/观点）
2. 分析主体（按方法论框架分节）
3. 数据附录（来源与时间、降级轨迹、缺失项）
4. 风险提示与失效条件
5. 完整免责声明（不可简化）

## 六、能力边界
- 能：方法论级投研分析、报告生成、跨场景组合、随仓库规范进化、功能目录自动同步。
- 不能：实时交易、买卖建议、收益承诺、替代用户独立判断；不提供仓库尚未实现的能力（如统一网关运行时、基金类占位 skill）。

## 七、Common Pitfalls（踩坑清单）
- ✗ 只读 SKILL.md 不读 references → 输出残缺（仓库 README 重点警告）。
- ✗ 每次都声称"已同步功能目录"却没真去比对 commit → 必须实测远端 commit 再断言。
- ✗ 远端不可达时清空旧功能目录或编造新增 skill → 保留上一版并标注停留 commit。
- ✗ 把样例报告里的历史数值当实时行情 → 必须标注"历史样例/演示数据"。
- ✗ 数据缺失时"合理估算"→ 触发防幻觉红线，必须如实标注。
- ✗ 一次分析重复铺陈同一段行情 → 一条数据只取一次、一个结论只写一次。
- ✗ 把"报告观点"写成既成事实 → 观点须显式标注。
- ✗ 多个来源冲突时静默选一个 → 标记 conflict 并提示歧义。

## 八、Verification Checklist
- [ ] Step 0 已比对远端 commit；有更新已重建功能目录，无更新已复用有效快照
- [ ] 场景路由依据 capability-catalog.md，未只读单个 SKILL.md；目标方法论的 references 已读取
- [ ] 每个数值有来源与时间，事实/观点分层
- [ ] 降级轨迹与交叉校验已执行并留痕
- [ ] 缺失项显式标注，无编造、无插值
- [ ] 无买卖/仓位建议，免责声明完整
- [ ] MD + 自包含 HTML 均已落盘，HTML 可离线打开

## 九、免责声明
本服务内容来源于公开及第三方数据源，仅自动化加工展示，不构成投资建议或承诺，不能替代独立判断。受数据源、传输、解析等因素影响，内容可能存在偏差，不保证内容真实准确完整。服务方及作者不对据此决策产生的后果负责。**市场有风险，投资需谨慎。**

## 十、更新日志
- **1.1.0**：新增 GitHub 镜像（`chenxyzcyxpp/invest-skill`）作为双源降级；`repo_sync.py` 支持 `--source auto/gitee/github`，快照记录 `repo_source`+`repo_commit`，换源可正确识别变更。
- 1.0.0：首版——仓库驱动全场景投研分析 + 功能目录随 commit 自动同步。
