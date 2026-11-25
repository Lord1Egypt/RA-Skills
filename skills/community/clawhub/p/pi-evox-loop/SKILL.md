---
name: pi-evox-loop
slug: pi-evox-loop
displayName: "Pi EvoX Loop"
description: "Give your coding agent an 'experience inheritance' runtime: recall validated fixes from an Evolver gene store at task start, register hits when a fix is actually used, and deposit newly-learned fixes after repairing a non-obvious failure. Optionally run controlled closed-loop experiments (R1 trap → distill → inject → R2) to measure inheritance gains. Every fix is traced to its model/host and checked across models. Use at the START of non-trivial tasks, after fixing a non-obvious failure, or when you want to measure agent self-evolution. Trigger words: 经验召回, 错题本, 经验继承, 自进化, evolver, 避坑, distill."
description_zh: "给编码智能体装上「经验继承」运行时：任务开始时从 Evolver 基因库召回已验证修法（编号列表），相关则采用并在结束时登记命中；任务中修复了非显而易见的失败后，将修法入库供未来召回；可选跑受控闭环实验量化继承收益。每条修法都记录来源模型与宿主，并做跨模型核验。非平凡任务开始时、修复有价值失败后、或想测量 agent 自进化效果时使用。触发词：经验召回、错题本、经验继承、自进化、evolver、避坑、distill"
description_en: "Experience-inheritance runtime for coding agents: recall validated fixes (numbered) at task start, register hits when used, deposit fixes after repairing failures; optional controlled closed-loop experiments to measure inheritance gains. Every fix is traced to its model/host and checked across models."
version: 0.44.0
platforms: [linux, macos, windows]
allowed-tools: Bash,Read,Write,Edit,Glob,Grep,env,network
homepage: https://github.com/stwhwing/pi-evox-lab
metadata:
  openclaw:
    requires:
      bins:
        - node
    envVars:
      - name: EVO_STORE_DIR
        required: false
        desc: 基因库目录（默认 ~/.evomap/assets）；仅 evolver 引擎模式读取
      - name: EVOX_HITS_DIR
        required: false
        desc: 命中登记目录（默认与基因库同级）
      - name: EVOX_TOPN
        required: false
        desc: 召回 top-N 数量（默认由 skill 内部策略决定）
      - name: EVOX_AUTO_APPROVE
        required: false
        desc: 沉淀是否自动批准（默认按 TTY/非 TTY 规则）
      - name: EVOX_SOURCE_MODEL
        required: false
        desc: 覆盖溯源记录的服务模型名（默认从宿主会话读取）
      - name: EVOX_SOURCE_HOST
        required: false
        desc: 覆盖溯源记录的宿主名
      - name: EVOX_HOME
        required: false
        desc: evomap 根目录（默认 ~/.evomap）
      - name: EVO_POOL_DIR
        required: false
        desc: 共享基因池目录（跨实例同步）
      - name: EVO_IDENTITY_DIR
        required: false
        desc: 签名链身份目录（Ed25519 密钥对）
      - name: EVOX_ALIGN_INJECT_MOD4
        required: false
        desc: 注入块估算 token 数补齐到 4 的倍数（相位对齐实验开关）
      - name: EVOX_KV_COMPRESSION
        required: false
        desc: 标记本机模型的 kv 压缩族（none/csa-s4/stride2/unknown）
      - name: EVOX_SAME_KV_WEIGHT
        required: false
        desc: 同 kv 压缩族基因的加权分（默认 +1.5，设 0 关闭）
      - name: EVOX_GENE_DECAY
        required: false
        desc: 基因有效性衰减总开关（默认开；设 0 关闭，行为与此前版本一致）
      - name: EVOX_GENE_DECAY_DAYS
        required: false
        desc: 衰减半衰期天数（默认 90：距上次反馈每过一个半衰期，该基因排序分减半）

---

# Pi × EvoX Loop — 智能体经验继承 Skill

> 让 Agent 的每个坑只踩一次：失败经验自动入库（守卫过滤），同类任务自动召回已验证修法。
>
> **术语约定**：正文以中文为主，技术字段在**首次出现时标注一次英文原名**（如「信号匹配 signals_match」），此后一律用中文，不再反复混排。完整中英对照见 `docs/faq.md` Q17。
>
> **文档地图**：
> - **新用户只需读三节**：30 秒上手 → 流程 A → 流程 B（约 60 行）；其余按需查。
> - **一分钟判断要不要用**：`docs/one-pager.md`
> - **最佳实践集中入口**：`examples/quickstart.md`（5 分钟闭环）+ `docs/overview.md`（项目概览）+ `docs/common-mistakes.md`（14 条反模式）——三份覆盖"上手/全景/避坑"。
> - **全部专题文档单一入口见 `docs/README.md`**（研究流程/运维细节的集中导航）；本文件其余部分 = 触发点/安全摘要/反模式速查/导航；`docs/advanced.md` = 回填寻址/harvest/并发/共享库/宿主接入/运维/安全门明细；`docs/common-mistakes.md` = 反模式清单；`docs/config-errors.md` = 配置错误；`docs/faq.md` = 完整 FAQ。
> - `docs/research.md` = 流程 C 受控实验 + 陷阱设计纪律——**研究专用，绝大多数用户无需打开**。

## 30 秒上手（Quick-Start）

> **EN**: Requires Node >= 22. Optional `@evomap/evolver` integration is GPL-3.0-or-later (only if you install and use `--engine evolver`); the default light backend is MIT, zero-dependency, zero-exfiltration. Three things only: **A recall** validated fixes at task start, **B deposit** after fixing a non-obvious failure, **C (optional, research) controlled experiments**. Daily use = A/B only.
> ⚠️ **前置要求：Node ≥ 22**（`node -v` 检查；旧版不支持，需先升级）。可选集成 `@evomap/evolver` 为 **GPL-3.0-or-later**——仅在你主动安装并使用 `--engine evolver` 时涉及，默认 light 后端为 MIT、零依赖零外发。
> **版本语义（0.40 单一数据源生成；0.43 O02 对齐实测轴并建 `docs/version-standards.md` 单一表）**：`package.json` 的 `optionalDependencies` 是**锁定依赖版本**（pi 0.74.2 / evolver 2.0.30，可选集成的兼容基线，A/B 流程零 npm 依赖即可运行）；下面的 1.5.2 / 2.0.51 是 **C42 上游实测版本**（仅用于兼容性评估，不是本项目安装的版本）。`@earendil-works/pi-coding-agent` 1.5.2 要求 Node ≥22.19.0；`@evomap/evolver` 2.0.51 要求 Node ^22.13.0 或 ≥23.4.0。默认 light 后端仍只需 Node ≥22。三轴完整口径见 `docs/version-standards.md`。
> **EN**: Optional integrations: pi-coding-agent 1.5.2 needs Node >=22.19.0; evolver 2.0.51 needs ^22.13.0 or >=23.4.0; the default zero-dependency light backend still needs only Node >=22. Full three-axis standards: `docs/version-standards.md`.
>
> 本 Skill 只做三件事：**A 任务开始召回**已验证修法、**B 修复失败后背沉淀**、**C（可选，研究用）受控实验量化收益**。日常只用 A/B，C 默认全关，请勿用于生产。

```bash
# A — 任务开始，对靶召回（替换成你的任务一句话）
node code/evolver-recall.mjs --query "处理 GBK 编码文件报错" --top 5

# B — 修复了非显而易见的失败后，贴原始报错生成草稿，再补 FIX 落库
node code/light-cli.mjs draft --error "<原始报错>" --tool <工具名> --context "<当时在做什么>"
node code/light-cli.mjs draft --error "<原始报错>" --strategy "AVOID: <什么不该做> FIX: <具体参数/命令/编码>" --commit
```

命令均在本仓库根目录执行；未安装依赖先见下方「安装」。

### 首次运行 · 3 步就绪（先跑自检，再沉淀）

1. **装 Node ≥22**（traps 生成器与 pi/evolver 均要求；见 FAQ·Q8）；
2. **自检环境**：`node code/light-cli.mjs doctor` —— 校验 Node 版本、经验库目录可写、命中登记目录可达（失败项给修正指引）；
3. **点亮经验库**：空库无修法可召回属正常，按下方流程 B 沉淀第一条修法即点亮。

### 新手必读（高频问答速览）
- **首次运行召回显示「无可召回修法」？** 正常——库从零开始，先跑一次 B 沉淀即可点亮（FAQ·Q1）。
- **Node 版本要求？** 需 **≥22**（traps 生成器还需 Python 3），过低 pi/evolver 会启动失败（FAQ·Q8）。
- **更多问题**见 `docs/faq.md`（完整 14 条）与下方反模式速查。

## 安装（一次性）

> **EN**: One-time setup. **A/B flows need ONLY Node >= 22 — zero npm dependencies.** Get the folder by any of three paths below; any location works (a "skill" is just a folder — put it wherever your host expects, e.g. `~/.claude/skills/pi-evox-lab`). Default backend = built-in light (pure Node, MIT). evolver is an optional integration (`--engine evolver`, needs `npm install`). Flow C additionally needs Pi CLI + an OpenAI-compatible LLM key.

**三种获取路径（任选其一）**：
```bash
# 路径 1：git clone（推荐）  路径 2：受限网络 → Release zip 直下（附 sha256，国内镜像见 FAQ Q7）
git clone https://github.com/stwhwing/pi-evox-lab.git && cd pi-evox-lab
# 路径 3：市场一键安装 —— skillhub.cn / ClawHub 搜 pi-evox-loop（WorkBuddy/OpenClaw 用户）

node -v                # 前置要求：Node >= 22（唯一硬依赖）
node code/light-cli.mjs doctor   # 30 秒自检——通过即可用，无需任何安装步骤
```
- **A/B 日常流程零 npm 依赖**；以下 `npm install` 仅为可选集成/实验模式 C 准备（国内网络先 `npm config set registry https://registry.npmmirror.com`，版本检查等价写法见 FAQ Q7 与 `docs/version-standards.md`）：

## Provider 配置（仅流程 C 需要）

> **EN**: Flow C only - any OpenAI-compatible endpoint; `$ENV` interpolation needs pi >= 0.85.1. Examples + domestic endpoints (DeepSeek/Bailian/SiliconFlow/Zhipu): [`docs/providers.md`](docs/providers.md).

## 流程 A：任务开始 — 召回经验（任何非平凡任务）

> **EN**: Flow A - recall at task start. `--query` with the task text does targeted recall (unrelated experience is never injected - injection is gated by signals_match x query-token overlap, below threshold = no injection). On error (T3), the raw error text IS the query. Multiple matches: geneConflicts drops anti_patterns-mutual low scorers; no targeted hit = no injection. Register the hit at task end with `--register-hit --gene <id>` (id-addressed, concurrency-safe).
```bash
# 国内高频场景（中文 Windows 日志 / CSV 默认 GBK，按 utf-8 读必炸）——空库跑 starter 后先试这条最易见效
node code/evolver-recall.mjs --query "读取中文日志报 UnicodeDecodeError" --top 5

# 推荐：带上任务文本做「对靶」召回（与任务无关的经验不会注入）
node code/evolver-recall.mjs --query "<当前任务的一句话/关键信号>" --top 5

# 遇到报错时（T3）：报错原文即查询——错误本身就是提醒
node code/evolver-recall.mjs --error "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4"
```

- 只输出「已审核 **且** 通过修法守卫 **且** 与查询对靶」的编号修法列表（空库有明确提示，属正常）；
- **参数默认值**：`--top` 默认 5 条（软提示注入有上下文成本，宁少勿多）；经验库无硬性容量上限，但建议单库 <500 条（超过后对靶精度下降，可用共享池分流）；
- **对靶规则**：按基因 `signals_match` 命中与查询词的交集打分，**低于阈值即整条不注入**（避免不对靶注入反而增加成本）；
- **多基因冲突时**：`geneConflicts` 守卫已自动剔除 `anti_patterns` 互斥的低分项；仍有多条时取分高者；**无对靶项时宁可不注入**，不用无关基因凑数；
- 与本任务相关时优先采用；结束时实际采用了某条，登记命中（`--gene <id>` 按 id 寻址，并发安全）；无关的经验不要硬套，未采用的条目不必登记：

```bash
node code/evolver-recall.mjs --register-hit --gene <asset_id或gene_id> --note "<任务一句话>"
```

## 流程 B：失败修复后 — 沉淀经验

> **EN**: Flow B - deposit after fixing a non-obvious failure. Deposit bar (any one): docs/2+ tries needed, environment-specific, counter-intuitive error, or second occurrence. Guided path: `draft --error` auto-extracts signals + pre-fills AVOID + writes anti_patterns; fill in FIX then `--commit`. Manual path: `distill` with explicit signals. strategy MUST be an executable fix (params/commands/encodings) - success summaries are filtered by the repair-signal guard. `--shareable` only for genes meant for the shared pool.
**判定标准（满足任一条即值得沉淀）**：
- 排查过程需要查文档 / 试错 ≥2 次才解决；
- 依赖本机或环境特性（编码、路径规范、shell 差异、网络环境）；
- 报错信息反直觉，或与文档描述不符；
- 同一坑在历史任务中出现过第二次。
（不满足任一条的普通失败不必沉淀——避免经验库噪声。）

**推荐路径：引导式（贴原始报错，信号与「负经验」自动抽取）**

```bash
# 1) 生成草稿：自动抽 signals_match + 预填 AVOID 模板 + 写入 anti_patterns（负经验 token）
node code/light-cli.mjs draft --error "<原始报错文本>" --tool <出错工具名> --context "<你当时在做什么>"

# 2) 照草稿补全 FIX 后落库（--strategy 覆盖预填占位符）
node code/light-cli.mjs draft --error "<原始报错文本>" \
    --strategy "AVOID: <什么不该做> FIX: <具体参数/命令/编码>" --commit

# 3) 审核（四语义状态机见下方「审核状态机」单节；approve 自动先跑取证）
node code/light-cli.mjs approve <gene_id>
```

**AVOID/FIX 模板适用边界**（写清才不被守卫拒）：
| 段 | 写什么 | 边界 |
|---|---|---|
| `AVOID:` | 什么不该做（负经验，可含危险词——那是**警告**） | 一句到两句；不要写成功总结 |
| `FIX:` | 具体到**参数/命令/编码**的可执行修法 | **必须真填**——占位符/重试日志/旁白会被 depositionGate 拒绝（fail-closed） |
| `anti_patterns:` | 单 token 字面量（如 `assume-default-utf8`） | 冲突判定按整串匹配，勿写 kebab 长句 |
| `signals_match:` | 召回对靶信号词 | 与查询词有交集才召得回；勿堆无关词 |

**备选路径：手写式（已明确 signals 时）**

```bash
node code/light-cli.mjs distill --category repair --signals bash,exception \
    --strategy "<一句话修法；多步用分号分隔；要具体到参数/命令/编码>" \
    --summary "<坑的一句话描述>" [--shareable]
```

- **沉淀门槛的真实数据（诚实边界）**：生产真实会话中可自动抽取的"干净修法对"密度很低（实测 `distillablePairs=0`）——本库基因主要来自人工/引导式沉淀。

## 沉淀质检 depositionGate（fail-closed）

> **EN**: Quality gate at DEPOSITION time (fail-closed): rejects unfilled placeholder / retry-log repetition / narration openings / missing repair-signal words / AVOID-without-FIX. Non-interactive deposits default to quarantined. Full review semantics: the「审核状态机」section below.
`distill` / `draft --commit` 时逐条检查，不合法**直接拒绝**（不落盘）：

| 拒绝条件 | 理由 | 下一步 |
|---|---|---|
| FIX 是未填占位符 `<在此填写可执行修法>` | 注入后毫无价值 | 在 draft 里补上真实修法再提交 |
| `retry with corrected args`（重试日志复述） | "重试然后好了"不是修法 | 写 AVOID(为何错)+FIX(怎么做) |
| 旁白开场（Now I understand…）或缺修法信号词 | 推理流水不可执行 / 不像在描述坑与修法 | 同上 |
| 有 AVOID 无 FIX（半成品） | 只有坑没有修法，注入后毫无价值（历史复审实证：3 条截断 deposit 全是此形态） | 补上可执行修法（参数/命令/编码） |

## 审核状态机（单一事实源）

> 基因从入库到可注入的**全部审核语义只在这一节维护**，其余文档一律指到这里（防多处表述漂移——0.35 评测点名）。
> **EN**: The single source of truth for all review semantics; other docs only point here.

| 场景 | 默认行为 | 覆盖方式 |
|---|---|---|
| 本地**交互式**沉淀（`draft --commit` / `distill`，有 TTY） | **自动通过** | `config --auto-approve off` 改人工；仅作用于本地沉淀 |
| 本地**非交互**沉淀（脚本/cron/管道，无 TTY） | **默认隔离**（quarantined） | 显式 `--auto-approve` 才通过 |
| `approve <gene_id>` | **自动先跑取证**——本地四台账（工具错误/召回/注入/回填）三级输出（强证据/弱上下文/无证据），核对一致才批 | `--skip-evidence` 为已知无证据场景的显式逃生门（不鼓励）；结论被后续事件推翻的保持隔离并留痕 |
| 池导入 `gene import` / `gene pull` | **official tier 直通**（签名验证）；**community 默认隔离** | `--tier` 决定 |

- 状态台账 `review.jsonl` 为 **LWW 追加式**，approve/quarantine 双向可逆；`info` 的「待审」= 最后状态既非 approved 也非 quarantined。
- 与两层质量门的关系：depositionGate 在**入库前**拒收（上节），四道守卫在**召回侧**过滤（下节）——任何一层拒绝都不注入。
- 无本地证据的基因（共享池/其他机器/起步包来源）按内容与来源审核，批准时注明。

> **EN**: Review-with-evidence: before `approve`, run `evidence <gene_id>` to check the four local ledgers for events matching the gene's claimed failure/fix. Approve only when consistent; genes whose conclusions were overturned by later events stay quarantined with an audit note. Genes without local evidence (pool imports / other machines / starter pack) are reviewed on content and source, noted at approval.

## 基因签名与 provenance

> **EN**: Every deposit is signed with this machine's Ed25519 identity (private key 0600, never leaves the machine); pool imports verify signatures - tampered content is REJECTED. Version-by-version details (v2 canonicalization, source attribution, source_kv, decay): `docs/advanced.md` §Provenance.

- 沉淀自动签、入池随行、导入验签：**内容被篡改 → 拒绝导入**；无签名的老基因原样接受（legacy）；私钥不出本机，公钥随基因出入池供他机验签——信任模型是「按 keyid 溯源」，不是中心化 CA；
- 溯源字段随 deposit/回填自动记录（`source_model` / `source_host` / `source_kv` 压缩方案族）；基因有效性按反馈衰减（时间半衰期 90 天 + 否定压力，地板 0.25，无反馈不衰减）——**逐版明细见 [`docs/advanced.md`](docs/advanced.md) §Provenance**。

## 部署与分发

> **EN**: Download paths, host integration, pool collaboration, concurrency semantics and scoring; version-by-version detail in `docs/advanced.md` §Deployment.

- **下载**：GitHub Release zip / npm（国内镜像见 FAQ Q7，附 sha256 校验）；
- **宿主接入**：`light-cli.mjs install <claude-code|cursor|codex|agents-md>`（`--yes` 落盘）；OpenClaw/Hermes 用 `install-hooks`；触发规程可 `install-snippet` 写进任意指令文件；
- **基因池协作**：`gene pull --pool <URL|命名> --tier official [--scene <场景>]`（签名验证）；`gene submit --bundle <file>` 回传维护者；命名池见 `~/.evomap/pools.json`；贡献条款见 CONTRIBUTING.md（CC-BY-4.0）；
- **并发语义**（三层，完整行为表见 [`docs/boundary-and-triggers.md`](docs/boundary-and-triggers.md) §5）：单机多会话=withLock 文件锁；跨机=基因池 Git 化（LWW 台账裁定）；多宿主按 gene_id 寻址；
- **召回打分与阈值（公开数值）**：signals 命中 +3/个 + 正文 token 交集 +1/个 + 负载均衡偏置 ±2；**低于阈值 2 分不注入**（不对靶注入比不注入更差，实测 +36pp）；分词=ASCII token（≥3 字符）+ 中文 2 字二元词——**多字中文短语写进 signals 无效**（`fix-signals` 可体检）；
- **会话围栏**：`session open "<任务>"` 一步完成 T1 召回+记账，`session close "<结论>"` 收尾——未配对的 open/close 会被构建门禁拒绝（审计绑定）；
- **效果量化与回填**：`report` 周报（L1 活性/L2 回填率/L3 复发，`--json` 机读）；`recall --record "<结论>"` 回填验证结论；`license verify <token>` 验证 Ed25519 签名许可；
- **IO 韧性与错误码**：瞬态错误自动重试（3 次/3s）→ 连续 5 次失败熔断 10s（IO 恢复即闭合）；全部失败附具名错误码 `[E_USAGE]`/`[E_ARGS]`/`[E_GUARD]`/`[E_NOTFOUND]`/`[E_INTERNAL]`（保留 0/1/2 退出码）——参数与完整表见 `docs/advanced.md`。

## 安全：四道门

> **EN**: Four gates: repair-signal guard, narration guard, injection guard (malice; AVOID=warning allowed vs FIX=instruction blocked), redaction gate (privacy, fail-closed off-machine). Per-gate details: `docs/security-and-license.md` §Gates.

| # | 门 | 管什么 | 在哪生效 |
|---|---|---|---|
| 1 | **修法守卫** | 有没有**真修法**（无可执行内容 → 不注入；宁缺毋滥） | 召回 |
| 2 | **叙述守卫** | 是不是**旁白流水**（旁白对智能体是零信息，实测等效噪声 +36pp） | 召回 |
| 3 | **注入守卫** | 是不是**恶意指令**（提示词注入 → 不注入；对抗"基因反向操纵宿主"的主防线） | 召回（CLI / Pi 扩展桥精简版 / 编排器）+ 导入 + 导出 |
| 4 | **脱敏闸门** | 会不会**泄私有内容**（IP/路径/密钥 → 拦截不出网） | 导出 + 导入 |

- **降级语义**：导出/导入 **fail-closed**（守卫模块缺失即拒绝执行）；召回侧只跳过注入门、其余三门照常（宿主 bootstrap 路径不因守卫失败而阻断使用者——只读不阻断、写入必须 closed）。
- 每道门**具体扫什么、命中后的行为**、0.31 修复的两个漏检与回归用例：统一见 [`docs/security-and-license.md`](docs/security-and-license.md) §Gates——本文不复述注入触发特征，避免文档自身被扫描器当成样本（本仓有为此发版的先例）。

## 能力边界速查（什么时候别指望它）

> 不适用场景 6 类（多机同写一库 / 100% 避坑保证 / 实时同步库 / 一次性任务 / 当权威知识库 / 跨架构直接复用）与量化边界（注入默认 5 条、库规模上限**合成集已实测、真实宿主未验证**（EN: measured on synthetic sets; real host unverified）、跨机无分布式锁、Node ≥22）**统一见 [`docs/boundary-and-triggers.md`](docs/boundary-and-triggers.md) §1–§2**。
> **EN**: Capability limits ("when NOT to use") and quantitative bounds: `docs/boundary-and-triggers.md` §1–§2.

## 什么时候提醒：五个触发点

> **EN**: Recall bound to concrete action nodes: T1 task start, T2 before first side-effecting action, T3 on error, T4 after fixing, T5 task end. Full spec: `docs/boundary-and-triggers.md`.
> 「装了技能但没人调用」是本项目最根本的失效模式——**连作者都会忘**。所以不能指望"用户记得"，必须把召回**绑死在具体动作节点上**。

| # | 触发点 | 时机 | 命令 | 没接会怎样 |
|---|---|---|---|---|
| **T1** | 任务开始 | 拿到非平凡任务、**规划之前** | `recall --query "<任务>"` | 预防失效：该避的坑照踩 |
| **T2** | 行动前 | **即将执行第一次不可逆动作之前**（写文件/提交代码/部署/调外部接口/删改数据）；同一任务内同类动作**只触发一次**，后续沿用本次结论 | 同上（query=**将要做的具体动作**） | 贴身预防（可选） |
| **T3** | **遇到报错** | 工具返回错误、**准备重试之前**——报错原文直接当查询（唯一「不用你记得」的触发点） | `recall --error "<报错原文>"` | **最可惜**：明明库里就有修法，却盲目重试 |
| **T4** | 修好坑后 | 修复了一个不显而易见的坑 | `draft --error ...`（沉淀） | 经验流失，下台机器再踩 |
| **T5** | 任务结束 | 收尾 | `--register-hit --gene <id>` / `--negate --gene <id>` | 无法度量，失效修法发现不了 |

> **完整触发规格统一见 [`docs/boundary-and-triggers.md`](docs/boundary-and-triggers.md)**——含 T2 判定口径与 3 个例子、多宿主并发矩阵、触发词↔命令映射、三类宿主接入方式、国内镜像、「装了没生效」自检。
> 触发词只是**调用提示**，不是召回匹配机制（命中靠 `signals_match × query-token` 对靶）；任务开始只要判定为"非平凡"就走 T1，不需措辞命中任何一组。

## 常见错误用法（反模式速查）

> 完整 14 条（每条讲机制 + 🔧现行/✅已修复 状态标注）见 [`docs/common-mistakes.md`](docs/common-mistakes.md)；跨机与命名池工作流见 [`docs/cross-machine.md`](docs/cross-machine.md)。最高频三条：

| 错误做法 | 为什么会错（机制） | 正确做法 |
|----------|--------------------|----------|
| 注入「成功总结」型 strategy | 软提示里「结论」对智能体零信息；只有**可执行动作**改变下一轮行为（等效噪声 +36pp） | 写成可执行修法（含参数/命令/编码） |
| 冷启动就期待避坑效果 | 召回是「对靶注入」，空库时物理上无可注入修法 | 先按流程 B 沉淀，价值复利增长 |
| 生产环境开 `--auto-approve --llm-refine` | 人工审核门是唯一质量闸，跳过即让未复核内容直达注入 | 保留人工审核门 |

> 完整目录与各文档职责表见 `docs/README.md`（skillhub 包无 README 时的等价入口）；高频入口：`docs/advanced.md`（生产运维/安全门明细/回填寻址）、`docs/glossary.md`（术语一页纸）、`docs/faq.md`（完整 17 问）、`docs/version-standards.md`（三轴版本口径）。

## 安全与数据外发声明（精简版）

> **EN**: All CLI calls are direct argv (no shell). Egress two axes: process & storage all local; model requests only in two opt-in paths - flow-C orchestrator (explicit provider/model/api-key) and `--llm-refine` (disabled by default). `--fresh` is destructive (auto-backed-up). Injected blocks are transparently marked; global output is redacted. Full text: `docs/security-and-license.md`.
全文见 [`docs/security-and-license.md`](docs/security-and-license.md)。要点：全部 CLI 调用为 **argv 直调**（无 shell、无拼接）；外发两轴——进程与存储全本地（A/B 流程零模型调用），模型请求仅两类显式 opt-in（流程 C 编排器发给用户配置的 provider / `--llm-refine` 默认禁用）；`--fresh` 有破坏性（自动备份）；注入块透明标注、全局输出脱敏（密钥不出现在任何 stdout）。
- **`traps/` 是本地测试夹具，不参与运行时**：该目录的 6 个陷阱生成器只用于在流程 C 受控实验里制造「环境必然失败」的场景（GBK 解码、非法 JSON 等）以量化继承收益；它们**不在召回 / 沉淀 / 注入的任何运行时路径上**，也不会被默认安装的钩子调用。保留是为了实验可复现——0.33 已实证：删除或隐藏不会改变静态扫描结论，反而损失可信度。
> **EN**: `traps/` holds LOCAL TEST FIXTURES ONLY - six generators used solely by flow-C controlled experiments to produce "environment-certain-failure" scenarios (GBK decode, invalid JSON) for measuring inheritance gains. They are NOT on any runtime path (recall / deposit / injection) and are never invoked by the installed hooks. Kept for reproducibility: removing or hiding them does not change static-scanner verdicts (verified in 0.33) and would only cost credibility.

## 权限与能力声明

> **EN**: Permission and capability disclosure — runtime behaviour is unchanged; this section only makes existing capabilities explicit for security reviewers.

- **`network` 能力**：仅用于可选集成（`evolver` 引擎模式）与用户显式 opt-in 的 `gene submit` 推送；默认 light 后端零外发、零 npm 依赖。不启用这些路径时不会发起任何网络请求。
- **auto-approve 策略**：`EVOX_AUTO_APPROVE` 默认关闭；仅当操作者显式设置时，本地沉淀的基因才可能不经人工审核进入后续召回。平台扫描器对「自动生成修法可被复用」的 concern 属策略说明，不改变审核门与 fail-closed 语义。
- **可选集成风险披露（O03）**：`package.json` 的 `optionalDependencies` 锁定 `@earendil-works/pi-coding-agent@0.74.2` 与 `@evomap/evolver@2.0.30`，是**可选集成的兼容基线，不是默认安装项**。**上游安全公告实测（2026-11-13 GitHub Security Advisory API）**：`earendil-works/pi` 公开 **4 条 GHSA**（GHSA-7v5m-pr3q-6453 / GHSA-r95r-rj6r-c39x / GHSA-jfgx-wxx8-mp94 / GHSA-mqxh-6gq7-558m，severity low/low/high/medium，公开于 2026-06-08）；`EvoMap/evolver` 公开 **6 条 GHSA**（含 1 条 critical，公开于 2026-04-20 / 04-27）。**GitHub API 未公开这些 advisory 的 CVE 编号与脆弱版本区间**，故**无法断言锁定版本是否受影响、亦无法据公告名推断修复版本**；按保守口径：pi 0.74.2 发布于 2026-05-21，**早于**其 4 条公告的公开时间，不能排除受影响 ⇒ 建议使用可选集成前升级并复验契约。本项目的 A/B 主流程与全部内置命令**不加载该包**；若需使用可选集成，请先升级到已修复版本并复验扩展钩子契约（见 `_upstream_check_0410.md`）。上游实测版本 pi 1.5.2 / evolver 2.0.51 仅为兼容性评估依据，绝不作为本项目安装版本。
- **`inspectionStatus=partial` 说明**：ClawHub 平台层 `moderation.verdict=clean` 与报告内 `clawscan.verdict=suspicious(medium)` 两层结论并存；后者 25 条 HIGH 中 17 条为 `analysis-evasion` 噪声、2 条经源码核验为误报（`cleanup` 已 guard、`network` 已在 `allowed-tools` 声明），其余由本版 O01/O03 修复或披露。本项目不宣称扫描器零发现。
- **注入内容不可信**：召回内容只作为提示文本，不改变权限、不触发工具、不提升信任档位；`REPAIR_SIGNAL_RE` / `NARRATION_RE` 双守卫保持 fail-closed。

## 致谢与上游

**平台主文档口径**：skillhub 分发包按平台约定**不含根 README.md**，本文件 `SKILL.md` 即该平台的主文档与权威入口；GitHub / ClawHub 包仍带根 README.md。三平台差异由发布清单唯一真源生成，不属缺失文件。
> **EN**: On skillhub the package intentionally ships no root README.md; SKILL.md is the primary document and authoritative entry there. GitHub/ClawHub builds still include README.md. This difference is generated from the single manifest source, not a missing file.

**上游引擎与宿主**：基于 [pi-coding-agent](https://github.com/earendil-works/pi) 与 [@evomap/evolver](https://github.com/EvoMap/evolver)。实测发现的 4+1 项上游缺口已提交官方 issue（evolver#624-#627、pi#9258），详见 README。

**方法论致谢（0.41 新增 5 项，完整列表见 README）**：0.41 核验并记录 HarnessMM（arXiv:2610.32813, v2）、其微信公众号解读、`jlon/pi-harnessmm`、`YuhuaJiang2002/HarnessMM` 与 `deepseek-ai/deepseek-harness`；**仅借鉴方法论 / Methodology only，未复制源码、未采纳其未验证外推**（见 `docs/research.md` §22）。

**方法论致谢（完整列表见 README）**：
- **[numbat](https://github.com/perplexityai/numbat)**（Perplexity AI，Apache-2.0）—— agent 行为审计器。`timeline` 与 `harvest` 的方法论直接受其启发；PoC 手册见 `docs/forensics-numbat.md`。
- **[FlyLoRA](https://arxiv.org/abs/2510.08396)**（NeurIPS 2025，清华大学）—— 负载均衡偏置与免训练合并不干扰两条原理的显式迁移来源（0.14.4）。
- **[The Universal Weight Subspace Hypothesis](https://arxiv.org/abs/2512.05117)**（Kaushik, Chaudhari, Vaidya, Chellappa, Yuille；arXiv:2512.05117）—— 「异构验证（跨源复现）」问题意识的来源（0.30）：同架构不同模型共享低维参数子空间，其开放问题「继承共同偏差与失败模式是否构成瓶颈」正是本项目跨源复现的出发点；「同构风险」须按「模型 × 版本 × 宿主」联合计算，不能按架构算。**论文自身结论本机未复现**（既未证实也未证伪）；坊间「16 维」「投影 98–99% 误差保功能」等转述在原文不可核实，本项目不引用（见 `docs/research.md` §19）。
- **[Periodic Weak Spots: Phase Sensitivity from Chunked KV-Cache Compression](https://arxiv.org/abs/2609.36322)**（ByteDance Seed）—— **相位轴**与**等长对照臂**这两项的来源（0.32）：分块 KV-cache 压缩引入「相位」这一新位置坐标，长上下文检索精度随其周期性起伏。本项目据此补上 R2-pad 等长中性对照臂，把继承增益从相位运气里分离出来（实测 n=10/臂、长度 Δ=0：语义 +100pp、相位 0pp）；并因论文把 CSA 核移植到 Qwen3-0.6B 骨架仍复现，把基因族字段定在**压缩方案**（`source_kv`）而非模型血统上。**论文自身结论本机未复现**（既未证实也未证伪），已在 `docs/research.md` §21.3 诚实标注；转述中越界的条目（`CSA2`、`Kimi`、`MLA` 等，原文 0 出现）本项目不引用。

> **EN**: **[Periodic Weak Spots](https://arxiv.org/abs/2609.36322)** (ByteDance Seed) - source of the *phase* axis and of the length-matched control arm (0.32): chunked KV-cache compression introduces a new positional coordinate, phase, and long-context retrieval accuracy rises and falls with it. It is why we added the R2-pad control arm that separates the inheritance gain from phase luck (measured n=10/arm, length Δ=0: semantic +100pp, phase 0pp), and why the gene-family field is the **compression scheme** (`source_kv`) rather than vendor lineage - the paper reproduces the effect by porting the CSA kernel onto a Qwen3-0.6B backbone.

**0.38 工程方法论致谢（完整列表见 README）**：
- 微信公众号文章《惭愧，我才真正看懂这个 AI 产品。》（阿颖，2026-11-05）—— 任务优先、验收清单、Router/Worker 分工的产品视角。
- [LobeHub](https://github.com/lobehub/lobehub)（Community License，canary）—— 确定性编排状态机、显式停止原因、`requiredEvidence` 验收制品、可插拔异构驱动；仅借鉴方法论、未复制源码。
- DeepSeek Harness《Super-agent 设计探索》（2026-10-31）与 [dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype)（MIT，research prototype）—— 不可变授权与「外部文本不可信」，启发本版注入内容不变量。
> **EN**: 0.38 also credits the WeChat article by 阿颖, LobeHub's orchestration sources, and DeepSeek Harness's Super-agent note/prototype; methodology only, no source copied, full list in README.

> 以上均为**研读与对照**：本项目与它们均无隶属关系，也不代表其观点；本仓库实现均为原创，默认后端是 MIT 的内置引擎。完整方法论清单（Palantir Ontology 等）见 README 致谢节。
