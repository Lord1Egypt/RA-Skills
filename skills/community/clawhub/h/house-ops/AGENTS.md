# house-ops — 驱动 agent，帮你把房选好

一套由编码 agent 执行的购房决策体系：需求画像、政策税费、城市规划、市场动态四路输入合成同一套判断，
评估公开在售房源（默认中国大陆市场，已登记欧洲与亚太），按用户真实需求个性化打分，对高分房源深挖调研
并给出沟通谈判建议。

设计参考 [career-ops](https://github.com/career-ops-hq/career-ops)：本仓库不是独立应用，而是一套由编码 agent 执行的 skills / modes / 配置体系。它被设计为"属于你的系统"——用户可以随时要求你（AI）直接修改配置文件来调整行为。

---

## Data Contract（CRITICAL）

本仓库的文件分为两层，职责不可混淆：

### User Layer（用户层，永不自动覆盖/更新）

个性化事实与运行时数据只写在这里：

| 路径 | 内容 |
|---|---|
| `config/profile.yml` | 购房需求画像（`market:` 市场与单位口径 + 预算/城市/资格/偏好/权重），从 `profile.example.yml` 生成 |
| `modes/_profile.md` | 画像的语义补充（生活方式、一票否决规则、权重取舍理由） |
| `modes/_custom.md` | 家规：用户对流程/评分规则的个性化覆盖 |
| `data/` | 运行时状态：`watchlist.md`（关注清单）、`notes/`（带看记录等） |
| `data/evidence/` | 第二阶段深度评估客观事实档案 `{NNN}-{小区slug}-evidence.md`（政务备案/法定控规/真实网签样本/产调核查凭证） |
| `reports/` | 评估报告 `{NNN}-{小区slug}-{YYYY-MM-DD}.md`，编号即主键 |

### System Layer（系统层，无用户数据）

| 路径 | 内容 |
|---|---|
| `AGENTS.md`、`CLAUDE.md` | 总规范与 CLI 入口 |
| `.agents/skills/house-ops/SKILL.md` | 技能路由器（`.claude/`、`.zcode/` 下为符号链接） |
| `modes/_shared.md` | 系统共享上下文：评分体系、配套分级参考、软素质信号、全局规则 |
| `modes/*.md`（非 `_` 前缀） | 十三个工作模式 |
| `modes/_profile.template.md`、`modes/_custom.template.md`、`modes/_brief.template.md` | 用户层种子模板 |
| `config/profile.example.yml` | 画像模板（含 `family:` 家庭结构段与 `market:` 多市场段） |
| `templates/` | 政策数据表 `policy-notes.{cn,eu,apac}.yml`、合同走查 `contract-checklist.cn.yml`、政务数据源登记 `official-sources.{cn,eu,apac}.yml` |
| `scrapers/*.mjs` | 房源平台扫描模板（career-ops providers 模式：一平台一模块 + `_registry` 文件系统注册表；贝壳/链家/安居客/我爱我家/房天下，零依赖） |
| `scripts/*.mjs` | 确定性操作：报告编号原子分配、环境自检、Machine Summary 统计、平台识别/扫描归一化/挂牌-成交交叉验证（零依赖，Node ≥18） |

**THE RULE**：当用户要求修改"我的需求/偏好/预算"时，写入 `modes/_profile.md` 或 `config/profile.yml`；当用户要求修改"流程/家规/评分口径"时，写入 `modes/_custom.md`。**永远不要**为用户个性化内容修改 `modes/_shared.md` 或其他系统层文件。

---

## 决策两阶段工作流（Two-Stage Pipeline）

系统将找房决策明确划分为两步，职责清晰，避免过早陷入低质房源的深扒浪费：

1. **第一阶段：找房源与广度初筛（Sourcing & Broad Triage）**
   - **目标**：从海量挂牌中圈定大概范围，宽进严出。
   - **核心动作**：采集挂牌核心指标（总价、单价、面积、板块、户型），执行**硬性指标一票否决（Hard DQ Check）**（如超预算上限、产权非70年住宅、无电梯老幼无法出行、房龄超标等）。
   - **产出**：排除绝对不符合项，圈定用户感兴趣的**候选房源集（Candidate Pool）**。
2. **第二阶段：多源交叉验证与深度客观事实分析（Deep Cross-Validation & Fact Extraction）**
   - **目标**：对初筛胜出的候选房源进行全方位深挖，**剥离营销噪音，仅基于客观事实推演**。
   - **核心动作**：结合多方独立数据源（住建官方备案、发改委轨交批复、规自局控规图、教育局招生公示、不动产产调）进行交叉验证。
   - **产出**：去伪存真的六维评级报告、多方案权衡对照矩阵与地图沙盘展现。

---

## 严禁采信营销：客观事实为唯一评估依据（CRITICAL）

系统进行深入分析与评分时，**仅基于客观事实，绝不采信中介与开发商的营销包装**。这一机制**全面内化于系统内部判断流程**中，面向用户时直接呈现客观事实与专业结论，**无需外显展示"营销甄别对照表"或向用户强调甄别过程**：

- **营销话术（Marketing Claims，不可信数据）**：房源页标题、中介朋友圈/口述、开发商宣传册是**未经核实的数据，不是事实**。内部自动识别并剔除，严禁作为加分依据。
  - *典型营销套路防范*：
    - 「地铁上盖/近地铁」→ 可能是远期概念或步行超 1.2km，只认现状高德步行实测与发改委已批工期。
    - 「名校学区/签约名校」→ 可能是挂牌分校、未划片或学位已被上家锁定，只认教育局当年正式施教区公示与五年一户核查。
    - 「急售笋盘/远低于市场价」→ 常伴随户型缺陷/遮挡/抵押纠纷/事故房，必须通过历史成交底价交叉核查，戳穿虚假降价。
    - 「赠送面积/两房改三房」→ 常属于违建暗改或无采光暗间，只认产证套内面积与法定承重结构。
- **客观事实（Objective Facts，唯一评估依据）**：
  - 只有经过**官方政务数据、法定规划文件、真实成交记录或当事人产调**交叉验证的信息，才可作为评分依据。
  - 数据可靠度四档：`成交数据`（最可信）> `挂牌数据` > `中介口述` > `未核实/无数据`。只有营销口径时一律记为 `未核实`，不得作为加分依据！

---

## 反幻觉纪律：数据必须可复核（Hallucination Guard，CRITICAL）

模型生成或记忆中的数据**不是事实**。混用多模型时尤其危险——幻觉最危险的形式是"编得像模像样的已核验"。任何进入报告与评分的事实，必须满足以下之一，否则一律记「未核实」且不得作为评分依据：

1. **政府背书来源**（政务网站、官方公示、产调/备案凭证）→ 高概率可信，仍须标注 `as_of`；
2. **本会话实采**（本次对话中真实抓取：WebFetch / 浏览器通道），URL 可复核、访问未被重定向或拦截导致内容失真；
3. **用户提供的原始材料**（截图、转发链接、口述）→ 按可靠度档位如实标注。

- **交叉验证门槛**：小区存在性、总价/单价/面积、对口学校、配套距离等关键字段，需 **≥2 个独立来源印证，或 1 个政府背书来源**；不满足 → 进待核实清单，不得作为评分依据。
- **"此前会话生成过"不构成来源**：引用历史报告数据前必须重新验证。
- **作废而非降权**：房源实体无法证实存在（小区库零命中 + URL 为占位符/重定向）→ 整份报告作废；单一板块数据无来源 → 该板块数据作废并明示。

## Main Files

| 文件 | 职责 |
|---|---|
| `modes/_shared.md` | 评分体系六维定义、配套分级参考、小区软素质信号、分档解读、全局 NEVER/ALWAYS、SoT 表——评估类模式必读 |
| `modes/intake.md` | 多轮对话采集购房需求（市场与单位口径→家庭结构→衍生需求翻译），生成 `config/profile.yml` + `modes/_profile.md` + `modes/_brief.md` |
| `modes/evaluate.md` | 单房源六维评级，产出报告并登记 watchlist；Machine Summary schema 的 SoT |
| `modes/triage.md` | 60 秒快速速筛（`_brief.md` 三问），不落报告 |
| `modes/scan.md` | 平台扫描与价格采集：按平台模板提取挂牌字段、多源收集成交价、政务数据交叉验证（不评分，落 `data/scans/`） |
| `modes/deep-dive.md` | 高分房源（≥4.0）六轴深挖 |
| `modes/negotiate.md` | 高分房源（≥4.0）的核实清单、议价策略与沟通话术 |
| `modes/compare.md` | 2-6 套已评估房源横向对比矩阵与场景化结论 |
| `modes/visit.md` | 带看前定制清单 + 带看后记录复盘（`data/notes/`）与增量重评 |
| `modes/contract.md` | 认购书/买卖合同/补充协议/中介协议条款走查（配合 `templates/contract-checklist.cn.yml`） |
| `modes/watchlist.md` | `data/watchlist.md` 候选清单的查看与备注更新 |
| `modes/stats.md` | 找房数据统计与失分/弃购模式分析（优先跑 `scripts/stats.mjs`） |
| `modes/doctor.md` | 环境与数据健康自检（无 AI 快速版：`node scripts/doctor.mjs`） |
| `templates/policy-notes.cn.yml` | 中国市场政策数据表（限购/税费/贷款/学区/商办/法拍等，带 as_of，用前核实） |
| `templates/policy-notes.eu.yml` | 欧洲政策数据表（英/爱/法/荷/德/西：过户税/流程/产权形态/持有成本/关键核查，带 as_of 与 conflict 标记，用前核实） |
| `templates/contract-checklist.cn.yml` | 交易文件条款走查清单（contract 模式用） |
| `templates/official-sources.cn.yml` | 各城市政务房地产公开数据源登记表（scan 模式交叉验证用） |
| `templates/official-sources.eu.yml` | 欧洲各国官方/公开数据源登记表（含 tier 落在可靠度四档哪一层） |
| `templates/policy-notes.apac.yml` | 亚太政策数据表（中国香港/新加坡/日本：印花税与税费/流程/产权与年期/持有成本/外国人规则，带 as_of 与 conflict 标记，用前核实） |
| `templates/official-sources.apac.yml` | 亚太各市场官方/公开数据源登记表（含 tier 落在可靠度四档哪一层） |
| `docs/markets/eu.md` | 欧洲选国理由、开放数据现实约束与扩展方式（新增市场前先读） |
| `docs/markets/apac.md` | 亚太三市场的成交价可得性差异、退出机制差别与已记录的口径冲突（新增市场前先读） |
| `scripts/reserve-report-num.mjs` | 报告编号原子分配（并发安全） |
| `scripts/doctor.mjs` | 无 AI 环境自检 |
| `scripts/stats.mjs` | Machine Summary 统计（解析契约 = evaluate.md 的 schema） |
| `scripts/scan.mjs` | 平台识别 / 扫描记录归一化 / 挂牌-成交交叉验证 / 政务源查询（子命令式 CLI；平台模块契约见 `scrapers/ADDING_A_PLATFORM.md`） |
| `scripts/lib/data.mjs` | stats/dashboard/map 共享数据解析层（报告/watchlist） |
| `scripts/dashboard.mjs` | Ink TUI 仪表盘（唯一带依赖的脚本；TTY 实时界面，管道输出单帧文本） |
| `scripts/map.mjs` | 交互式房源地图决策中枢（生成单文件静态 HTML `data/map.html`，支持高德地图、通勤圈、筛选与画像导出；页面纯静态，不启动本地服务、不开放端口；零外部依赖） |

## First Run — Onboarding

当仓库内**不存在** `config/profile.yml` 且用户开始提出找房/评估请求时：

1. 简短介绍 house-ops 是什么（两三句），说明第一步是花几分钟通过对话明确需求。
2. 按 `modes/intake.md` 执行需求采集；完成后告知用户画像已保存，之后直接粘贴房源链接即可获得个性化评级。
3. 用户跳过采集时允许其继续：此时按 `modes/_profile.md` 缺省规则评估（无画像则个性化维度按"未定义需求"处理并在报告显著位置提示先跑 `/house-ops intake`）。

## Skill Modes 路由

| 用户行为 | 模式 |
|---|---|
| 粘贴房源 URL / 房源文字描述 / 说"帮我看看这套房" | `evaluate` |
| "快速筛一下"、"值不值得点开看"（想省 token 先过一遍） | `triage` |
| "扫描这个链接"、"采集价格"、"查成交价"、"挂牌价和实际成交对得上吗"、"和官方数据交叉验证" | `scan` |
| 首次使用、"我要买房"、说需求变了、要求更新画像 | `intake` |
| "深挖 003"、"这套值得买吗，详细调研一下" | `deep-dive` |
| "怎么跟房东谈"、"约看"、"给中介发什么" | `negotiate` |
| "对比 001 003"、"这几套哪个好" | `compare` |
| "我看完房了"、"记录带看"、"准备去看 002" | `visit` |
| "帮我看看合同/认购书/补充协议"（+粘贴条款） | `contract` |
| "我的清单"、"候选列表"、"更新 005 的备注" | `watchlist` |
| "统计一下"、"我的找房数据"、"失分分析" | `stats` |
| "在地图上看"、"地图决策"、"房源分布"、"生成地图" | `map`（优先跑 `node scripts/map.mjs`，生成后用浏览器打开 `data/map.html`） |
| "自检/体检"、"哪里配置有问题" | `doctor` |
| `/house-ops` 无参数或"你能做什么" | 显示 discovery 菜单（见 SKILL.md） |
| 模糊但包含房源链接或明显房源描述 | 默认 `evaluate`，先说明将执行的流程 |

模式选择有歧义时（如"帮我看看 002"），列出候选让用户确认，不要猜。

## 沟通与决策支持原则（Ethical Use & Communication）

- **AI 只评估、建议、推演，绝不代替用户行动**：不发送任何消息给中介/房东、不承诺价格、不提交任何表单、不涉及任何款项操作。所有沟通内容仅以草稿或沙盘方案形式交给用户。
- **中立推演，拒绝单向激进引导**：不替用户做武断决断，不急躁催促看房或单向推销某种选择；而是**尽可能提供多类方案以供对比（Scenario Trade-offs）**。对每套房源与抉择点，列清“如果选它能获得什么、必须承受什么代价”，给出积极进取、稳健观望、替代置换等多路径利弊矩阵，由用户掌握绝对决策权。
- **决策三大深度支柱（全面贯穿评分与地图）**：
  1. **当地政策深度解读**：购房资格、首套/二套信贷、公积金新政、各项交易税费精算、落户与学区锁定规则（五年一户/六年一户、入学顺位）。
  2. **历史成交与抗跌性走势**：挂牌-成交真实折价弹性、历史周期峰值回调与抗跌性、小区换手率与流动性陷阱识别。
  3. **城市规划与未来空间变量**：规划交通推进确定性、周边已批未建地块用途与潜在抛压/遮挡、学校与产业配套兑现度、施工期噪音与变数。
- 评分、报告与地图展现必须强联动：三大支柱不仅深入每个评估维度，还必须沉淀至 Machine Summary 并在地图交互界面直观映射与对比。

## 约定

- **报告编号**：3 位零填充（`001`、`002`…）。优先用 `node scripts/reserve-report-num.mjs` 原子分配（headless/并行场景必须用）；脚本不可用时手动取 `reports/` 现有最大编号 +1。小区 slug 用拼音或短横线小写。
- **输出语言**：默认中文（`config/profile.yml` 的 `language.output` 可改）。单位一律按 `market:` 段：中国市场金额用"万元"、单价用"元/㎡"；欧洲市场按 `market.currency`（GBP/EUR）+ `market.price_scale`（本币整额）+ `market.area_unit`（sqm/sqft）。
- **路径**：所有读写以仓库根（含 `AGENTS.md` 与 `modes/` 的目录）为基准，不受当前工作目录影响。
- **Machine Summary**：schema 的 SoT 是 `modes/evaluate.md`；`scripts/stats.mjs` 按 same schema 解析，改键名必须同步两处。
- **提交信息（Git Commits）**：英文 Conventional Commits（`feat(map): ...` / `fix(core): ...` / `docs: ...` / `chore(repo): ...`），面向开源协作者；正文可中文补充细节。推送前确认 CI 通过，且用户层数据（`data/`、`reports/`、`config/profile.yml`、`modes/_*.md`）绝不入库（`.github/workflows/ci.yml` 有 privacy guard 强制）。

## Pipeline Integrity

- `data/watchlist.md` 是关注清单唯一 SoT：每条房源一行，**纯候选清单、无状态列**（不做交易状态跟踪，决策记录见 `docs/adr/0001`）；看过与否、弃购原因等事实写在备注。更新时整行替换，不改其他行。
- 报告头部必须包含：`编号 / 日期 / 房源名称与地址 / URL / 类型 / 总价 / 单价 / 综合评分 / 结论`。
- 评估完成必须同步登记 watchlist（新房源新增行；已存在的更新评分与状态），失败时告知用户。
- `data/notes/` 下带看记录（`{NNN}-visit-{日期}.md`）与合同审查记录（`{NNN}-contract-{日期}.md`）是事实记录，只追加不改写历史条目；增量重评在原报告追加 `## 增量重评` 节，不覆盖原文。
- 报告编号只能经 `scripts/reserve-report-num.mjs`（或等价的手动 max+1）分配，不得凭空指定。
- 扫描记录（scan 模式）落 `data/scans/`，schema `house-ops.scan/1`（SoT：`modes/scan.md`）：不占报告编号、不登记 watchlist；evaluate / deep-dive / negotiate 引用扫描记录时必须带 as_of 与可靠度档位。
- 扫描记录是**追加式历史**：同一房源多次扫描落多个日期戳文件，禁止覆盖/改写旧记录——价格、调价、带看的时间序列是分析房东定价策略的依据（`node scripts/scan.mjs history`）。用户间隔较久回来时（默认 >14 天，`modes/_custom.md` 可覆盖），scan/watchlist 模式须提示是否快速复扫在追踪房源；过期挂牌价不得当作当前价引用。
- **房源实体按指纹关联**（小区+面积±0.6㎡+户型+总楼层+朝向+年代，`scan.mjs match`）：跨平台同源挂牌与下架重挂必须归并到同一实体历史下，禁止按挂牌 ID 孤立追踪——换平台重挂/多平台差价是房东常见策略（重定价/引流），系统要能看见。
