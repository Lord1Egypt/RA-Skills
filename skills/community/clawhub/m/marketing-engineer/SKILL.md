---
name: marketing-engineer
description: Marketing Engineer 营销工程体系（源自 Shann Holmberg 方法论）+ 单文件营销驾驶舱。当用户要搭建/运营产品营销工作区、要「随时看到整体情况/文件状态/排期」的可视看板、做内容营销策划、GEO/SEO 优化、AI 引擎可见度诊断、关键词调研、多渠道分发、竞品情报、上线推广 campaign 时使用。覆盖：一键工作区脚手架、治理规则（证据留源/人审/口径一致）、内容生产管线（工单制）、GEO 打法、驾驶舱引擎（工作区全景：左目录树/右文件列表、状态判定、实时扫描、明亮暗夜双主题）、外部增强 skill 编排（缺失时自动降级）。
agent_created: true
---

# Marketing Engineer（营销工程体系）

把营销当工程项目做：**知识层 → 垂直域 → 工作流/工单 → 审核闭环 → 数据回流**，再加一层随时可查的**驾驶舱**。不靠灵感堆内容，靠可复用的结构让每一篇产出都建立在已核实的事实与固定口径之上。

## 交互原则（先记住这一条）

**脚本是实现细节，不是给用户的接口。** 用户给的是意图（「建个工作区」「看下整体情况」），agent 负责把它翻译成具体的脚本动作。
除非用户明确要手动执行 / 挂定时任务 / 排查问题，**不要在回复里让用户去复制命令行**。

## 快速开始（用户说什么 → agent 做什么）

| 用户说 | agent 执行 |
|---|---|
| 「给 XX 建个营销工作区，带驾驶舱」 | `python3 <skill>/scripts/init_workspace.py <目录> --product "<产品名>" --with-dashboard` |
| 「看下整体情况 / 打开驾驶舱」 | `python3 scripts/serve_dashboard.py <工作区> 8799` → 打开 `http://127.0.0.1:8799/dashboard.html`，实时扫描后汇报 |
| 「内容变了，刷新驾驶舱」 | `python3 scripts/build_dashboard.py <工作区>`（已存在时加 `--force`） |
| 「这篇发在 XX 了，链接是…」 | 回填 `results/channel-posts.md` → 重建驾驶舱 |

骨架建好后，引导用户填 `shared-knowledge/` 五件套；之后用户只需说「今天写什么 / 发什么 / 调研谁」。完整说明见 **`references/usage-manual.md`（使用手册）**。

## 何时使用

- 用户要求搭建营销/增长工作区，或「参考某方法论做营销体系」
- **用户要看整体：工作区有哪些目录、每个文件什么状态、什么时候发的**
- 策划内容（公众号/知乎/小红书/X/Medium 等）、上线推广 campaign
- 做 SEO/GEO（生成式引擎优化）、AI 引擎可见度诊断、关键词调研
- 管理自有渠道矩阵、多平台分发、竞品情报

## 核心工作流（总控）

0. **没有工作区 → 先建**：`scripts/init_workspace.py <目录> --with-dashboard`（或 `build_dashboard.py` 给已有目录接上驾驶舱），再按 `references/workspace-structure.md` 逐层填充（shared-knowledge 优先于一切产出）。
1. **任何产出前 → 先读后写**：查 shared-knowledge 的事实、口径、渠道表；工作区没有的事实，先调研入库（带来源+日期）再动笔。
2. **内容 → 走工单制管线**：见 `references/workflow-content-production.md`（brief → ticket → 草稿 → 人审 → 排版/封面 → 发布 → 台账回填 → 数据回流）。
3. **GEO/SEO 需求 → 走 GEO 剧本**：见 `references/geo-playbook.md`（关键词调研五步法、AI 引擎信源图谱、月度探针、可见度基线与 KPI）。
4. **渠道决策 → 查渠道矩阵规则**：见 `references/workspace-structure.md` 的渠道分组与分发原则。
5. **口径/术语/定位一经变更 → 立刻做品牌口径巡检**：见 `references/brand-consistency-audit.md`（六项固定扫描 + 内部视图层也要扫 + 留档）。**内部看板/驾驶舱必须纳入同步清单**——否则旧口径会从内部文件回流进素材。
6. **用户要"随时看整体情况 / 排期 / 任务"的直观视图 → 建驾驶舱**：见 `references/dashboard-playbook.md`（单文件 dashboard.html：工作区全景 + 月历 + 倒计时 + 工单/台账/决策区块；近期日程同步苹果日历，AppleScript 被权限拦截时降级 .ics + open）。
7. **驾驶舱要有「工作区全景」**：左目录树 / 右文件列表，状态四级判定、实时扫描、明亮暗夜双主题——见 `references/dashboard-playbook.md` 第五节「驾驶舱引擎」。
8. **每个环节都可挂外部增强 skill**：见下方「工具箱」——有则用、无则按降级路径走，不改变流程与闸门。

## 铁律（任何环节不可违反）

1. **先读后写**：产出前必须读 shared-knowledge；不得虚构渠道、数据、功能。
2. **证据留痕**：所有事实带来源+日期；未核实的一律标 `[未验证]`，不流入成品。
3. **发布必须人工审批**：草稿送审，用户确认后才排版/发布；台账以线上实际发布版本为准。
4. **口径一致性**：术语、域名、免费表述、邀请码等口径全渠道唯一且一致——AI 引擎跨源验证，漂移即降权。口径冲突先归一再发内容。
5. **密钥只进 .env**，不得写进任何素材或文档。
6. **产出归位**：草稿/成品/台账按工作区约定目录存放，便于跨会话续作。
7. **敏感边界**：不点名竞品贬损（讲机制、讲数据主权）；定价未定稿不出现具体价格。
8. **看板是视图不是源**：驾驶舱从台账/工单/渠道表/周报派生，不得反过来把看板当真相源；数据变化后重跑 `build_dashboard.py`（或起实时服务）。

## 工具箱（可选增强 skill，缺失时优雅降级）

本体系可与下列外部 skill 组合；环境中没有它们时，按「降级路径」执行，不阻塞流程。检测方式：调用 Skill 工具时若报找不到该名称，即视为未安装。

| 环节 | 推荐 skill | 用途 | 未安装时的降级路径 |
|------|-----------|------|------------------|
| 选题 / 竞品情报 / 趋势验证 | `last30days` | 抓取任意话题近 30 天的跨平台真实讨论与互动数据（Reddit / X / HN / GitHub / Polymarket 等），按点赞与热度排序 | 多路 WebSearch 采样，结论按定性判断标 `[未验证]` |
| ↑ 同上（中文主对标） | 用 **WebSearch/WebFetch**，不用 last30days | 中文产品的真实讨论在中文社媒，`last30days` 免 key 源不索引中文（实测全空） | — |
| 选题与方案压力测试 | `grilling`（入口 `grill-me`） | 拷问式质询，逼出计划中未考虑的边界与假设 | 自查四问：目标 / 受众 / 依据 / 风险 |
| brief → 规格冻结 | `to-spec` | 把已有讨论综合成规格文档（不追问） | 按 `workspace-structure.md` 的 brief 骨架手写 |
| 计划 → 工单 | `to-tickets` | 拆成带阻塞边的 tracer-bullet 工单 | 按 `workflow-content-production.md` 的 ticket 模板手写 |
| 外部一手资料调研与落档 | `research` | 后台 agent 调研，产出 markdown 到工作区 | 自行 WebSearch / WebFetch 后按证据留痕规范落档 |

**两条纪律**（与铁律同级）：

1. **工具不改变闸门**：任何 skill 的产出仍只是草稿，必须走人审；台账一律以线上实际发布版本为准。
2. **隐私优先**：涉及浏览器 cookie、本地凭据读取类能力（例如 last30days 的 `--allow-browser-cookies`）默认关闭，须用户显式授权才可启用；API key 只进 `.env`。

装了什么、来源与许可登记在工作区 `shared-knowledge/toolchain.md`（如该文件存在）。

## 目录

- **`references/usage-manual.md` —— 使用手册（先读这个）**：三种入口、五步启动法、日常指令卡、驾驶舱用法、铁律速查、recipes、排错表
- `references/workspace-structure.md` —— 工作区目录模板、各文件骨架、目录语义册、文件状态口径、渠道矩阵与分发原则
- `references/workflow-content-production.md` —— 工单制内容生产管线（选题→发布→回流全流程）
- `references/geo-playbook.md` —— GEO/SEO 完整打法（关键词调研、AI 引擎诊断、探针机制、KPI）
- `references/dashboard-playbook.md` —— 营销驾驶舱：看板设计 + 月历 + 苹果日历同步 + **驾驶舱引擎（工作区全景五、状态判定、更新机制、主题、踩坑清单）**
- `references/brand-consistency-audit.md` —— 品牌口径巡检（六项固定扫描清单、内部视图层必扫、结果留档模板、防复发四条固定动作）

## 脚本

| 脚本 | 作用 |
|---|---|
| `scripts/init_workspace.py` | 新工作区脚手架（目录树 + README 骨架）；`--with-dashboard` 一并部署驾驶舱三件套并生成 dashboard.html |
| `scripts/scan_workspace.py` | 扫描工作区 → `.cache/workspace_map.json`（目录含义 + 文件日期/状态/说明） |
| `scripts/build_dashboard.py` | 扫描 + 注入骨架 → 生成单文件 `dashboard.html`（含离线文本快照，幂等、自动备份） |
| `scripts/serve_dashboard.py` | 本地服务：`/api/tree` 实时扫描 + `/api/file` 读全文 |
| `scripts/md-faq-to-schema.py` | FAQ 定稿（Markdown）→ schema.org FAQPage JSON-LD，供页面嵌入；同源生成保证 JSON-LD 与可见文字一致 |
| `assets/dashboard-skeleton.html` | 驾驶舱页面骨架（主题、两栏视图、Markdown 渲染、图片预览、代码复制；`build_dashboard.py` 用它生成正式页） |

---

由 2Ryun 团队打磨 · 2ryun.wiki
