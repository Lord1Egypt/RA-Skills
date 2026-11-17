# Advanced — 回填寻址 / 时间线 / 并发 / 共享库 / 宿主接入 / 运维

> 本文档是 SKILL.md（日常用法）的进阶分册：接生产环境、排查「没生效」、跨实例共享时看这里。

## 回填寻址与时间线（0.18）

> 方法论致谢：timeline/harvest 的「取证重建」思路来自 **Perplexity 开源的 numbat**（agent 行为审计器，github.com/perplexityai/numbat，Apache-2.0）——「把账本变成监控录像」；实现为本机账本自有格式。

### register-hit/negate 改按 id 寻址（并发安全）
多会话并行写同一库时，位置编号会漂移（选择快照 `.evox-last-selection.json` 是共享单文件，会被其他会话的 recall 覆盖——实测错记 63→65）。0.18 起：

```bash
node code/evolver-recall.mjs --register-hit --gene gene_manual_xxx --note "<任务一句话>"
node code/evolver-recall.mjs --negate --gene <asset_id> --note "<为什么没起作用>"
```
位置写法 `--register-hit <N>` 仍兼容，但并发环境不可靠。

### `light-cli timeline`：四账本时间线
```bash
node code/light-cli.mjs timeline [--last 50]
```
把 召回/注入/回填/工具错误 四个账本按时间合并成 Markdown 表——一眼看出"先踩哪个坑→召回了哪条→是否回填"。失效修法的典型信号：**注入之后 N 步仍出现同类报错**。

### `light-cli harvest`：错误候选 → 沉淀建议
```bash
node code/light-cli.mjs harvest [--last 10]                    # 盘点未处理候选（附可复制的 draft 命令）
node code/light-cli.mjs harvest --done <N>                     # 已沉淀：移入 error_candidates.done.jsonl（留痕）
node code/light-cli.mjs harvest --dismiss <N>                  # 无价值驳回：同样留痕，不产基因
```
候选只是线索：**FIX 必须由你补全成可执行修法**（占位符会被 depositionGate 拒绝）。处理过的候选移入 `.done.jsonl`——未处理列表只减不增。

### 并发写锁（0.19）
多会话/多进程并行写同一基因库时，`append` 之间的「读-改-写」窗口会被并发回滚（实测 shareable 标记毫秒级丢失、approve 假 ✓）。0.19 起所有台账写入（genes/review/hits/pending）与池 staging 均持 **O_EXCL 文件锁**（`.evox.lock`）：15s stale 自动破除（持锁进程崩溃不死锁）、5s 超时 **fail-open**（锁是优化不是门，绝不让写入因锁失败）。Python 侧 hook 用同一协议。

### 独立取证（0.19 PoC：numbat）
在自有设备上用 [numbat](https://github.com/perplexityai/numbat)（Perplexity，Apache-2.0，**方法论致谢**）对 agent 会话做取证重建——原生解析 OpenClaw/Claude/Codex 日志。PoC 运行手册与实测结论见 `docs/forensics-numbat.md`：目标是用**时间线对靶核对**「注入的基因是否真的体现在 agent 后续命令里」，补强 register-hit 的自报单源。


## 安全：四道门（明细，自 SKILL.md 下沉）

> **EN**: Four gates detail (moved from SKILL.md for progressive disclosure). The injection guard distinguishes `AVOID:` (warning - allowed) from `FIX:` (instruction - blocked) contexts; regression suite (0.31): **16/16 malicious samples caught, 7/7 legitimate zero false-kill**, including the two newly fixed漏检 (text before `FIX:` was silently dropped; Chinese override regex too narrow). Fail-closed if the guard module is missing: export/import refuse to run; `evolver-recall.mjs` skips the injection gate but the other three still apply (read-only must not block, writes must be closed); the Pi bridge ships a reduced built-in guard and `pi_evolve.mjs` uses the full scanner without降级.

| # | 门 | 管什么 | 在哪生效 |
|---|---|---|---|
| 1 | **修法守卫** | 有没有**真修法**（无可执行内容 → 不注入） | 召回 |
| 2 | **叙述守卫** | 是不是**旁白流水**（开场白式 → 不注入） | 召回 |
| 3 | **注入守卫** | 是不是**恶意指令**（提示词注入 → 不注入） | 召回（CLI / Pi 扩展桥 / 编排器三条通道）+ 导入 + 导出 |
| 4 | **脱敏闸门** | 会不会**泄私有内容**（IP/路径/密钥 → 拦截不出网） | 导出 + 导入 |

**关键设计：区分 `AVOID` 与 `FIX` 语境**——`AVOID:` 段出现危险词 = 在警告别这么做（合法，放行）；`FIX:` 段出现危险词 = 在指示这么做（可疑，拦截）。

## 共享基因库（跨实例 / 跨用户，0.14.9 新增）

> **EN**: Shared pool (opt-in): mark genes `--shareable` at deposit time, `gene submit --pool <dir>` exports shareable AND approved genes only (pool = approved-only curated collection), `gene import` on other instances (idempotent by asset_id). Tier is decided by the operator-specified pool, never by the gene's self-claimed tier (anti-spoofing). Redaction gate is fail-closed before anything leaves the machine.

> 让「一个坑只踩一次」跨实例生效：把**已验证的修法**沉淀的基因放进**自建共享池**，其他实例拉取复用。**本地库始终是权威源**，共享是增量；离线完全可用。

```bash
# 1) 沉淀时标记「可共享」（默认不共享 = 不外发；命中脱敏闸门的私有内容永不外流）
node code/light-cli.mjs distill --signals gbk,encoding --strategy "FIX: 用 encoding='gbk' 读老文件" --shareable
# 2) 过闸写入自建共享池（幂等；只导出 shareable 且已审核通过的基因——池=已审核集合）
node code/light-cli.mjs gene submit --pool <自有共享池目录>
# 3) 其他实例拉取（按 asset_id 幂等合并；审核态由你指定的池信任级别决定）
node code/light-cli.mjs gene import <池文件>                      # 默认 community → 待审
node code/light-cli.mjs gene import <自建池文件> --tier official   # 自建策展池 → 自动通过
```

**设计要点（务必知悉）**：
- **池语义（0.18.1 拍板）**：submit 只导出 **shareable 且 LWW 审核态=approved** 的基因；待审/未决定留在本地库，submit 会报告「待审未推池 N 条」。**池永远是审核完毕的可共享集合**。
- **脱敏闸门 fail-closed**：基因离开本机/入池前必扫全部文本字段，命中私有 IP、绝对本地路径、密钥、内网服务/代号即**拦截**，不出网。
- **opt-in 共享**：`shareable` 默认 **false**；只有显式 `--shareable` 的基因才可导出。
- **审核门控不被绕过**：导入基因默认 **待审（quarantined）**；仅当显式信任某个自建池（`--tier official`）才自动通过。tier 由**操作者指定的池**决定，**不读取基因自称的 tier**（防恶意池伪装）。
- **幂等合并**：拉取按 `asset_id`(sha256) 去重，重复拉取不产生重复。
- 池目录默认 `~/.evomap/pool`（`EVO_POOL_DIR` 覆盖）。池可放自有 Git 仓（版本化 + 天然审计 + 权限即鉴权）。

## 非交互沉淀默认隔离（0.17.0）

> **EN**: Interactive deposits auto-approve (convenience since 0.16.0); non-interactive ones (scripts/cron/host pipes, no TTY) default to QUARANTINED unless `--auto-approve` is explicit. Auto pipelines are the origin of the 15 noise genes seen on a private node; the gate keeps them out of the injectable pool.

| 沉淀方式 | 默认行为 |
|---|---|
| **交互式**（人在终端敲命令） | 见 SKILL.md「审核状态机」 |
> **EN**: Interactive deposits follow the SKILL.md review-state-machine section (single source of truth).
| **非交互**（脚本/cron/宿主自动管道，无 TTY） | **默认隔离**——显式 `--auto-approve` 才通过 |
| `--no-auto-approve` / `config --auto-approve off` | 始终人工审 |

> 设计：自动管道（如宿主把每次重试都记录成基因）是私有节点那 15 条噪音的起源；非交互默认隔离 + 沉淀质检，让「自动沉淀的垃圾」进不了可注入池。

### install-snippet：自动沉淀的绑定点

> **EN**: The root cause of 'the agent never deposits' is that T4 never entered its context. `install-snippet --file <project>/AGENTS.md --yes` writes the five-trigger-point protocol into the project instruction file (idempotent, re-runnable to update).
「agent 不提醒就不沉淀」的根因是 T4（修好坑后）没有出现在它的上下文里。把规程写进**项目指令文件**即可：
```bash
node code/light-cli.mjs install-snippet --file <项目>/AGENTS.md        # 演练
node code/light-cli.mjs install-snippet --file <项目>/AGENTS.md --yes  # 写入（幂等，可重复执行更新）
```
写入后该项目的 agent **每个会话**都会看到 T1–T5（含 T4 修坑即沉淀）。AGENTS.md / CLAUDE.md 均可。

## 让经验真正生效：四个静默失败与对策（0.16.0）

> **EN**: The most common failure is SILENT: genes deposited but never recalled, or deposited but never approved (never injected). Counters: info shows loop health, own deposits are auto-approved by default, install-hooks auto-wires hosts, starter loads 20 curated genes so the first query hits.

| 静默失败 | 症状 | 对策 |
|---|---|---|
| **① 从未召回** | 沉淀了很多，却从没被用过 | `info` 显示「召回次数 0」并给命令；`install-hooks` 帮你接上宿主 |
| **② 沉淀未审核** | 基因入库却被隔离，**永不注入** | 审核语义统一见 SKILL.md「审核状态机」（`info` 列出待审并给 approve 命令） |
| **③ 宿主没接** | 装了但 agent 从不会自动召回 | `install-hooks`（演练 → 确认后才写入） |
| **④ 冷启动没手感** | 库里没几条，召回也不命中 | `starter` 一键装载 20 条通用教训 |

### 三条命令解决 90% 的「没生效」
```bash
node code/light-cli.mjs info            # ① 看闭环健康度：召回次数 / 命中 / 待审
node code/light-cli.mjs starter         # ② 装起步包，立刻有东西可召回
node code/light-cli.mjs install-hooks   # ③ 演练接线（看清会做什么；加 --yes 才写入）
```

**`install-hooks` 的两个常见疑问，答案直接给你（0.32 C-3：原在 FAQ Q10/Q12，内联于此，新手不必跳转）**：

1. **它会改坏我的宿主配置吗？** 不会。默认是**演练模式**——只打印"将要做什么"，**不落盘**；
   加 `--yes` 才真正写入，且写入前会备份。OpenClaw 改 handler 后需重启网关才生效；Hermes 只改脚本、
   若启用 allowlist 需刷新，且脚本 mtime 必须是 ISO-8601 字符串。`install-hooks --auto` 会先自动探测
   本机有哪些宿主，再给出**唯一一条**推荐命令，不用你自己选。
2. **我的 Agent 既不是 OpenClaw 也不是 Hermes，怎么自动用？** 用规程粘贴：
   `node code/light-cli.mjs snippet` 输出「五个触发点」操作规程，粘进你的 AGENTS.md / CLAUDE.md /
   系统提示即可——这是没有钩子机制的宿主最可靠的接入方式。

### 自动审核开关（默认开）
本地沉淀的审核默认行为、非交互隔离、approve 取证绑死与池 tier 语义：**统一见 SKILL.md「审核状态机」**（单一事实源，0.36 收敛），此处不再复述；共享池 `gene import` 按 `--tier` 判定。

## 宿主接入契约（0.15.0 融入实际应用的关键）

> **EN**: Experience inheritance is NOT 'install and forget' - it depends on the host feeding in task intent (T1: --query with the user message body) and reporting outcomes (T5: --register-hit / --negate).

> **EN**: Experience inheritance is NOT "install and forget" - it depends on the host feeding in task intent (T1: --query with the user message body) and reporting outcomes (T5: --register-hit / --negate).

经验继承**不是"装上就生效"**——它依赖宿主把「任务意图」喂进来、把「效果」回填回去。私有节点实测：机制在跑（153 次 recall），但**真正有效（对靶且有注入）仅 10%**。三个断点都在宿主侧。

### 逐步接入（三步，缺一不可）

**第 1 步：任务开始时，把用户的真实诉求传进来**
```bash
node code/evolver-recall.mjs --query "帮我抓取这个公众号文章" --agent openclaw
```
要传的是**用户真正想做的事**，不是信封包着的那条消息。recall 会自动剥离子企业IM/心跳等前缀；剥完若没有实质内容就**不注入**（宁缺毋滥）。

**第 2 步：任务结束时，回填这条修法到底有没有用**
```bash
node code/evolver-recall.mjs --register-hit --gene <id> --note "按 gbk 编码读取，抓取成功"
node code/evolver-recall.mjs --negate --gene <id> --note "仍超时，networkidle2 不够"
```
每次注入都会自动记一笔 `pending_injections.jsonl`；回填后「注入→有效」的转化率才算得出来。

**第 3 步：检查闭环是否真的跑起来了**
```bash
tail -5 experiments/recall_calls.jsonl   # noise=true 表示宿主传的是噪声、没拿到正文
wc -l experiments/hits.jsonl             # >1 条说明闭环闭合
```

### 可直接复制的钩子模板
| 文件 | 宿主 | 事件 |
|---|---|---|
| `examples/hooks/openclaw-bootstrap-recall.js` | OpenClaw | `agent:bootstrap` |
| `examples/hooks/hermes-pre-llm-recall.py` | Hermes | `pre_llm_call` |
| `examples/hooks/README.md` | — | 三步接入 + 常见接入问题排查表 |

改模板顶部三个路径常量即可用（也支持 `EVOX_RECALL_SCRIPT` / `EVOX_HITS_DIR` 环境变量）。

### 常见宿主对照
| 宿主 | 任务开始接入 | 传任务意图 | 结束回填 |
|---|---|---|---|
| **OpenClaw** | 原生钩子（`agent:bootstrap`） | 钩子里取用户正文 | 钩子里回调 |
| **Hermes** | 原生钩子（`pre_llm_call`） | 同 | 同 |
| **通用 Agent** | 提示词里加一句「先跑召回」 | 手工传 `--query` | 人工执行回填命令 |

> ⚠️ 只做第 1 步不做第 2 步：能召回但**不知道有没有用**；两者缺一，经验继承都不成立。宿主若长期「有效召回率」偏低，先确认**运行时部署的是不是最新版**。

## 运维与度量（ops）

| 脚本 | 作用 | 默认触发 |
|------|------|----------|
| `metrics_collect.mjs` | 采集基因库指标（总数/已审核/隔离/命中/recall 调用数），追加到 `exp/metrics/metrics.log` | 周常 |
| `distill_sessions.mjs` | 生产会话蒸馏适配器：直读宿主真实会话存储（SQLite），按「失败调用 vs 重试调用的参数差异」抽取修法 | 周常 |
| `evox-weekly.sh` | 周常包装：`metrics_collect.mjs` + `distill_sessions.mjs --days 7 --commit --auto-approve-lowrisk` | cron `17 3 * * 1` |

**抽取口径（宁缺毋滥）**：先判定「失败」——**结构化标志优先于文本标记**（`isError` / 非零 `exit_code` / `error` 字段），且**文本错误标记只对命令执行类工具生效**；再在同一会话内找**紧接着（≤6 个事件）、同名工具、结果不再失败**的下一次调用，取两者**参数差异**作为修法。差异过大一律拒绝；落库前再过**修法信号 + 叙述守卫**双闸。

**两级门（B+C）**：`--commit` 落库时，仅**纯参数微调型**自动批准；其余进 quarantine 并写入候选报告 `exp/metrics/distill-candidates-<日期>.md`。

**对靶注入**：`evolver-recall.mjs --query "<任务文本>"` 按 `signals_match` 命中 + 与 strategy 的 token 交集打分，**低于阈值即不注入**。

环境变量：`EVOX_ROOT`（默认 `$HOME/pi-evox-lab`）、`EVOX_STORE_DIR`（默认 `$HOME/.evomap/assets`）、`EVOX_NODE`（默认 `node`）、`EVOX_HITS_DIR`（默认 `$cwd/experiments`，**生产环境建议固定为 `$EVOX_ROOT/experiments`**——否则埋点散落在各项目目录，timeline/info 读不到）、`EVOX_OC_DB` / `EVOX_HERMES_DB`（宿主会话存储路径）等。

**生产接入（让继承真正发生）**：两条路——① 提示词接入：把「任务开始 recall / 修复后 deposit」写入智能体系统提示词；② 原生钩子接入（推荐：机制保证，而非依赖智能体自觉）。两类原生钩子均为**薄适配层**，只调用 `evolver-recall.mjs`；空库零注入、异常不影响宿主调度。

**支持的智能体宿主（已验证 / 设计支持）**
| 宿主 | 推荐接入 | 钩子 / 机制 |
|---|---|---|
| OpenClaw | 原生钩子 | `agent:bootstrap` 注入虚拟 bootstrap 文件（或 `pre_llm_call` shell hook） |
| Hermes | 原生钩子 | `pre_llm_call` shell hook，`is_first_turn` 做「每会话仅首轮」闸 |
| WorkBuddy / 通用 Agent | 提示词接入 | 写入系统提示（`AGENTS.md` / `SOUL.md`） |
| 任意支持 system prompt 或钩子的宿主 | 薄适配层 | 只需调用 `evolver-recall.mjs` |

> **诚实边界**：各宿主会话存储格式不一——结构化标志最可靠；只靠文本标记时召回率随宿主而异。bootstrap 类钩子可能**早于**当轮用户消息落库，此时该轮退化为「无查询 → top-N 封顶」。

**注入位置是显式实验变量（0.32 B-4，源自 arXiv:2609.36322）**：同一条基因在不同通道落在上下文的**相反两端**，二者不等价——

| 通道 | 代码位置 | 落在上下文 |
|---|---|---|
| OpenClaw 钩子 | `examples/hooks/openclaw-bootstrap-recall.js`（`bootstrapFiles.push`） | **前部**（虚拟引导文件） |
| Hermes 钩子 | `hermes-pre-llm-recall.py`（`{"context": ...}`） | **追加到当轮 user message** |
| Pi 扩展桥 | `code/evolver-bridge.ts`（`event.systemPrompt + block`） | **尾部**（system prompt 末端） |

> **为什么要在意**：分块 KV 压缩（如 DeepSeek-V4 CSA 的 W=8,S=4）会引入「相位」这一位置坐标，
> 同一信息在不同位置上可检索性可差数十个百分点（论文跨相位 best−worst 达 40.23pp）。
> 又：**注入块的 token 数会平移其后所有内容的相位**，而召回是动态 top-N ⇒ 注入长度随会话变化
> ⇒ 相位偏移近似随机。**做 A/B 时必须把「注入位置」和「注入长度」当作受控变量记录下来**
> （`evolver-bridge.ts` 已在 sidecar 写入 `chars` / `estTokens`；`EVOX_ALIGN_INJECT_MOD4=1` 可把
> 估算 token 数对齐到 4 的倍数）。⚠️ token 数为估算值，精确对齐需分词器。


## 基因签名与 provenance（明细，0.21）

> **EN**: Provenance detail: Ed25519 keypair per machine (`~/.evomap/identity/`, private key mode 0600). Signing domain = asset_id + canonical JSON (signature fields excluded, **v2: recursively canonicalized so nested content is covered**). Deposit signs automatically; `gene submit` carries the signature; `gene import` verifies with the embedded pubkey: tampered -> BLOCKED, unsigned/legacy -> accepted with note, unverifiable -> accepted with warning. Trust model = keyid traceability, not a central CA.

```
light-cli identity            # 查看本机 keyid 与密钥路径
light-cli verify <gene_id>    # 验签本地库基因（exit 1 = 验签失败）
light-cli evidence <gene_id>  # 审核取证（ approve 前自动执行；也可单独跑）
light-cli resign [--yes]      # 0.31：把存量 v1 签名升级为 v2（v2 覆盖嵌套内容；默认演练，--yes 才落盘）
```

**签名规范化 v1 / v2（0.31）**：v1 用 `JSON.stringify(rest, Object.keys(rest).sort())`，replacer 数组作用于**每一层** ⇒ 嵌套字段被静默丢弃、不在签名域内（改嵌套内容仍验签 `verified`，实测确认）。v2 改为递归规范化，嵌套内容全部纳入。为不让存量已签名基因集体变 `tampered`，按 `sig_v` 分派：v1 基因继续按 v1 验（验签通过但会提示可升级），新签名一律 v2。

## IO 重试、熔断与截止（0.21 重试 / 0.34 熔断，stability）

**中文·重试（0.21）**：`retryIo`（store.mjs）只对**瞬态**错误（EBUSY/EPERM/EACCES/ETIMEDOUT——Windows 上文件被占用/实时扫描的典型表现）重试：最多 3 次、50/100ms 退避、硬截止 3s，到期即把错误交还调用方。非瞬态错误（ENOENT/EISDIR）从不重试。

**中文·熔断与降级（0.34）**：连续 `EVOX_IO_CB_THRESHOLD`（默认 5）次瞬态失败 ⇒ 打开熔断；其后 `EVOX_IO_CB_COOLDOWN_MS`（默认 10s）内**只尝试 1 次**（跳过重试与退避），失败立即交还调用方 ⇒ 长时间故障下不再持续无谓重试。冷却期内任一次成功即闭合（半开自动恢复）。非瞬态失败（如首次运行的空库 ENOENT）**不计入**熔断，避免误触发。打开时输出一次中文可执行指引（限频，不刷屏）。

> **EN**: `retryIo` (store.mjs): bounded retries on TRANSIENT errors only (EBUSY/EPERM/EACCES/ETIMEDOUT - Windows file-in-use / AV-scan typical), max 3 attempts with 50/100ms backoff, hard deadline 3s, then the error propagates. Non-transient errors (ENOENT/EISDIR) never retried. **0.34 circuit breaker**: after `EVOX_IO_CB_THRESHOLD` (default 5) consecutive transient failures the breaker opens, and for `EVOX_IO_CB_COOLDOWN_MS` (default 10s) each call gets a single attempt (no retry, no backoff) before falling through - so a prolonged outage no longer causes repeated useless retries. Any success inside the cooldown closes the breaker again (half-open auto-recovery). Non-transient failures (e.g. ENOENT on a first-run empty store) do not count toward the breaker. Opening it prints one rate-limited actionable hint. Retry is an optimization, not a gate - it must never block the caller indefinitely (consistent with the fail-open philosophy).

## 显式错误码（0.34，errorHandling）

**中文**：所有 `fail()` 失败路径在**保留退出码**（0=成功 / 1=运行期失败 / 2=用法错误）以兼容既有调用方的同时，附加**具名错误码** `[E_XXX]`——脚本与宿主可据此精确区分失败类型，无需解析人类可读文案。

| 错误码 | 退出码 | 含义 | 典型触发 |
|---|---|---|---|
| `E_USAGE` | 2 | 用法错误：缺参数 / 未知命令 | `light-cli.mjs zzz-unknown`、`approve`（缺 `<gene_id>`） |
| `E_ARGS` | 2 | 参数值不合法：取值不在允许集合内 | `config --auto-approve bogus` |
| `E_GUARD` | 1 | 质量守卫拒绝：沉淀质检未通过 | `distill` / `draft --commit` 提交占位符或日志复述 |
| `E_NOTFOUND` | 1 | 目标不存在：基因 / 文件 / 编号未找到 | `verify <不存在的 gene_id>`、起步包缺失 |
| `E_INTERNAL` | 1 | 未预期的内部错误（详见原始错误） | 未捕获异常 / 未处理的 Promise 拒绝 |

> **EN**: every `fail()` path keeps the exit codes (0 = ok, 1 = runtime failure, 2 = usage error) for backward compatibility and additionally prints a **named error code** `[E_XXX]`, so scripts and hosts can tell failure types apart without parsing human-readable text. See the table above.

## 已知边界

- 修法注入是**软提示**（system prompt），遵从度模型相关；守卫保证噪声不入库不出库，但不承诺 100% 避坑；
- `tool_result` 失败点教学（扩展桥内）只在「策略注入后仍踩坑」时提供增量，价值在长时运行场景；
- 并发锁覆盖 JSONL 台账与池 staging 写入；其他文件操作的原子性仍在 0.21 评估范围（stability 评测点名）。

## 模块调用关系图（0.27，0.34 更新：命令分域下沉）

```
   宿主钩子/手工 →  evolver-recall.mjs（召回+回填）
                          │ import
   用户 CLI     →  light-cli.mjs（唯一入口：解析 argv → 派发；0.34 起仅 65 行）
                          │ 按命令域动态 import
                          ▼
              ┌─────────────────────────────────┐
              │  engine/light/commands/*.mjs    │  ← 命令实现层（0.34 新增）
              │  deposit.mjs     distill / fix-signals / draft
              │  review.mjs      approve / quarantine / list / feedback
              │  provenance.mjs  shareable / identity / verify / resign / gene-pull-trust
              │  forensics.mjs   timeline / evidence / harvest / session / report / export-evidence / stats
              │  setup.mjs       doctor / info / snippet / license / install* / config / starter / gene / demo
              │  _shared.mjs     共享 helpers（fail / usage / doctor / 路径常量…）
              └───────────────┬─────────────────┘
                              │ 复用
                              ▼
              ┌───────────────────────────┐
              │      engine/light/*      │  ← 引擎层（零依赖）
              │  store.mjs   账本读写（withLock/重试/熔断/埋点落点）
              │  distill.mjs 基因构造 + 四道守卫
              │  guards.mjs  注入前 ABF 扫描
              │  identity.mjs Ed25519 签名/验签 + license token
              │  ledger.mjs  审核台账（LWW 裁定）
              └───────────┬───────────────┘
                          │ 被复用，不重复实现
      gene_share.mjs（池协作 export/import/pull/submit）──┘
      pi_evolve.mjs（流程 C 实验编排，研究专用）
```

**读图要点**：用户只经 `light-cli.mjs` / `evolver-recall.mjs` 进入；引擎层是唯一实现——**改引擎行为只需改一处，所有入口同时生效**；`code/engine/light/store.mjs` 是账本与埋点的唯一落点（0.27 起 timeline 默认落在技能根 `experiments/`）。

**0.34 重构（P0-2）**：主入口 1299 行 → **65 行**，30 个命令按域分到 `engine/light/commands/` 五个文件，共享 helpers 下沉到 `_shared.mjs`。命令块为机械搬运（块级作用域与派发语义不变），**行为等价性由 `_rel0330/_smoke_matrix.mjs` 的 57 项基线保证（57 passed / 0 failed）**。迁移期两个坑：`path.dirname` 拼接需按层数改写为 `__CODE_DIR`/`__SKILL_ROOT`；命令模块需自行 import 守卫（如 `depositionGate`），共享层不会自动 re-export。

## §Provenance 与部署明细（0.36 自 SKILL.md 收敛）

> **EN**: Version-by-version details moved here from SKILL.md in 0.36 (single-source-of-truth slimming); SKILL.md keeps the summary and points here.

## 基因签名与 provenance（0.21）

> **EN**: Provenance signing (0.21, one of the last 1.0 criteria): every deposit is signed with this machine's Ed25519 identity (`~/.evomap/identity/`, private key 0600, never leaves the machine); genes carry {sig, keyid, pubkey}. Pool imports verify signatures - tampered content is REJECTED, unsigned/legacy genes pass with a note. `light-cli identity` shows your keyid; `light-cli verify <gene_id>` verifies.

- 沉淀自动签、入池随行、导入验签：**内容被篡改 → 拒绝导入**；无签名的老基因原样接受（legacy）；
- 私钥不出本机；公钥随基因出入池供他机验签——信任模型是“按 keyid 溯源”，不是中心化 CA；
- **签名规范化 v2（0.31）**：v1 的签名域**不含嵌套字段**（ replacer 数组作用于每一层，嵌套内容被静默丢弃）；v2 递归规范化，把嵌套内容全部纳入。新签名一律 v2，存量 v1 仍有效（验签通过但会提示可升级）；升级用 `light-cli resign --yes`（默认只演练不落盘）。
- **精确归因（0.32 D-2）**：此前 `~/.evomap/source.json` 只是**静态 per-host 默认值**，而宿主有 fallback 链——某轮实际由 fallback 服务时会被误记成 primary。现两个生产钩子把**本轮实际服务的模型**透传（OpenClaw 读 `transcript_events` 里最近一条 assistant 事件的 `model`；Hermes 读 `pre_llm_call` payload 的 `extra.model`），落成 `~/.evomap/last_source.json`。`sourceInfo()` 优先级：**env > last_source.json（7 天窗）> source.json > 空**。⚠️ 语义是「最近一次观测到的服务模型」，不保证与本次 deposit 同轮次；存量基因不回填。
- **压缩方案族 `source_kv`（0.32 B-5/B-6）**：`generation_meta.source_kv` 记录基因出自哪种 **KV 压缩方案**（`none` / `csa-s4`（W=8,S=4）/ `stride2` / `unknown`；闭源或架构未公开一律 `unknown`，不猜）。召回打分对**已知同族**基因加分（`EVOX_SAME_KV_WEIGHT`，默认 1.5，设 0 关闭）；**本机族未知时完全不加权**，行为与此前一致。为什么按压缩方案而非模型血统：arXiv:2609.36322 把 DeepSeek 的 CSA 压缩核移植到 Qwen3-0.6B 骨架从头预训练仍复现「位置相关的检索失败」⇒ 决定因素是压缩核，不是厂商。
- **注入长度留痕（0.32 B-1）**：注入块是追加在 system prompt 尾部的，其 token 数会**平移其后所有内容的相位**；召回是动态 top-N ⇒ 注入长度随会话变化。`evolver-bridge.ts` 现把 `chars`/`estTokens` 写入 sidecar；`EVOX_ALIGN_INJECT_MOD4=1` 可把**估算** token 数对齐到 4 的倍数（估算值，非真实分词）。
- **基因有效性衰减（0.33 C-7）**：修法会过期——环境变了、依赖升级了，老基因的 FIX 可能已失效。召回打分现对**有反馈**（hit/negate 至少一条）的基因按两个信号乘性衰减：**时间半衰期**（距上次反馈每过 `EVOX_GENE_DECAY_DAYS` 天——默认 90——排序分减半）与**否定压力**（negate ≥ 2 且否定率 ≥ 50% ⇒ 再减半）。衰减后低于对靶阈值的自然落选；注入行对衰减中的基因带一眼标记（如 `⚠[衰减:49%·多次未奏效·2天前反馈]`）。**无反馈的基因不衰减**（unproven 由审核门控管，不双重惩罚）；**地板 0.25**——衰减永不单独杀死基因，硬过滤仍是审核门控 + 守卫；`EVOX_GENE_DECAY=0` 一键关闭（行为与此前版本完全一致）。

> **EN**: 0.32 provenance & phase line - `~/.evomap/source.json` used to be only a static per-host default, so a turn actually served by a fallback was mis-recorded as the primary. The two production hooks now pass the **actually served model** (OpenClaw reads the most recent assistant event's `model` from `transcript_events`; Hermes reads `extra.model` from the `pre_llm_call` payload) into `~/.evomap/last_source.json`. `sourceInfo()` priority is **env > last_source.json (7-day window) > source.json > empty** - it means "most recently observed serving model", not guaranteed to be this deposit's turn; existing genes are not back-filled. Genes also carry `generation_meta.source_kv`, the **KV compression scheme** they came from (`none` / `csa-s4` (W=8,S=4) / `stride2` / `unknown`; closed or undisclosed architectures are always `unknown`, never guessed), and recall scoring bonus-boosts **known same-family** genes (`EVOX_SAME_KV_WEIGHT`, default 1.5, 0 disables; when the local family is unknown there is no weighting at all). The axis is the compression scheme rather than vendor lineage because arXiv:2609.36322 reproduces position-dependent retrieval failure by porting DeepSeek's CSA kernel onto a Qwen3-0.6B backbone. Finally, because the injected block is appended to the system prompt its token count **shifts the phase of everything after it**, and recall is dynamic top-N, so injection length varies per session: `evolver-bridge.ts` now logs `chars`/`estTokens` and `EVOX_ALIGN_INJECT_MOD4=1` aligns the **estimated** token count to a multiple of four (an estimate, not real tokenization). 0.33 adds **gene validity decay (C-7)**: recall scoring applies a multiplicative decay to genes **with feedback**, from a time half-life (default 90 days, `EVOX_GENE_DECAY_DAYS`) plus negation pressure (≥2 negates and ≥50% negate rate halves again), floored at 0.25. Genes **without feedback are never decayed** (unproven is the review gate's job), decay alone never kills a gene, and `EVOX_GENE_DECAY=0` restores the old behaviour exactly; decayed injections carry a visible marker (e.g. `⚠[衰减:49%·多次未奏效·2天前反馈]`).

## 部署与分发（0.23）

> **EN**: Download paths (GitHub / npm / restricted-network mirror), host integration one-command, and concurrency semantics for shared deployments.

- **下载**：GitHub Release zip / npm（`npm config set registry https://registry.npmmirror.com`）；网络受限环境用国内镜像 zip（附 sha256 校验，见 FAQ Q7）；
- **宿主接入**：`light-cli.mjs install <claude-code|cursor|codex|agents-md>`（自动定位配置文件写入规程，`--yes` 落盘）；OpenClaw/Hermes 用 `install-hooks`；
- **基因池协作**：`gene pull --pool https://zyx.pink/pool/genes.jsonl --tier official` 从官方镜像拉取全池（签名验证，66+ 条策划基因）；`gene submit --bundle <file>` 产出提交包回传维护者（PR / issue 附件 / 文件交换）；导入默认隔离+验签；池仓库贡献条款见 CONTRIBUTING.md（CC-BY-4.0）；
- **场景拉取**（0.24）：`gene pull --pool <URL> --scene <场景>` 只拉该场景子集；受控场景词表：`ops-deploy`（部署/服务器）/ `coding-debug`（编码/解析）/ `release-publish`（发布/版本）/ `api-integration`（API/webhook）/ `git-workflow`（git/仓库）/ `agent-runtime`（宿主/钩子/管线）；`gene list --scene <名>` 本地同粒度过滤；
- **并发语义**（三层，**完整行为表见 [`docs/boundary-and-triggers.md`](docs/boundary-and-triggers.md) §5**）：单机多会话=withLock 文件锁；跨机=基因池 Git 化（提交→审核→合并，LWW 台账裁定冲突）；多宿主召回幂等（重复召回同一基因不重复计数）。多宿主并行时按 gene_id 寻址（0.18 起），不用位置序号。
- **召回打分与阈值（公开数值，0.28 补）**：每条候选基因的得分 = **signals 精确命中 +3/个** + **与基因正文 token 交集 +1/个** + 负载均衡偏置 **±2**（冷门基因上抬、热门下压；命中全 0 时不生效）；**低于阈值 2 分即不注入**（宁缺毋滥：只注入不对靶内容比不注入更差，实测 +36pp）。命中判定用与召回同一套分词：ASCII token（≥3 字符）+ 中文 **2 字二元词**（CJK bigram）——因此**多字中文短语写进 signals 是无效的**（见 `fix-signals`）。`--top` 默认注入条数见 `evolver-recall.mjs --help`。
- **命名池（0.25）**：`~/.evomap/pools.json` 定义命名池源（`{"pools":{"official":"<url>","team":"<git-url>"}}`），`gene pull official` 按名拉取；已拉池缓存在 `~/.evomap/pool-cache/`。
- **会话围栏（0.27）**：`light-cli.mjs session open "<任务名>"` 一步完成「T1 召回 + 记账」（落生产账本）；`session close "<本轮结论>"` 收尾记结论；`session` 查看围栏记录。**围栏让召回与沉淀可审计**：跳过召回或收尾沉淀，账本里没有配对的 open/close，外部构建门禁会拒绝构建。配套：`doctor` 检查埋点落点漂移。
- **召回别名与触发词（0.28）**：`code/engine/light/aliases.json` 是概念别名表（concept → 英文 canonical + 中文别名短语）；①`draft --trigger "<动手前的措辞>"` 把触发短语展开成 signals（英文 canonical + 中文二元词**双写**）——预防型经验因此能在**动手前**被召回；②召回时中文 query 也会映射到英文 canonical（两种措辞都能命中）；③`light-cli.mjs fix-signals` 体检并展开存量基因里的**无效中文 signal**（>2 字在二元分词下永远匹配不上）。**打分公式与阈值不变**——语义只扩召回面，注入仍由确定性门决定。
- **溯源与异构验证（0.29）**：deposit / `--register-hit` / `--negate` 都记录 `source_model` + `source_host`（环境变量 `EVOX_SOURCE_MODEL` 可显式指定模型）；`report` 新增 **L4 异源复现率**（同一基因被 ≥2 个不同「模型｜宿主」复现过才算 cross-source）与 **negate 根因分布**（`--because model-diff|env-diff|scene-mismatch|fix-wrong`）；`gene export` 给基因打 `trust` 标签（single-source / unknown-source）。**动机**：基因库是单点，防污染的三道门是同源代码——「单作危机」的直接指标就是跨源率，单源占比高说明该修法只被一个环境验证过。
> **EN**: Our "heterogeneous verification" question comes from arXiv:2512.05117 (models of the same architecture share a low-dimensional weight subspace, and may therefore **inherit shared biases and failure modes**; the paper leaves "is that lack of diversity a bottleneck" as an **open question** and notes cross-architecture comparison has no method yet). What we do is a **response-level measurement** (failure-signature agreement across models on one deterministic trap) - not a port of its weight-space results.
- **理论出处（0.30）**：本项目的「异构验证」问题意识来自 arXiv:2512.05117《The Universal Weight Subspace Hypothesis》（同架构模型共享低维参数子空间 → 可能**继承共同偏差与失败模式**；该文把"是否构成瓶颈"列为**开放问题**，跨架构比较尚无方法）。我们据此做的是**响应级实测**（不同模型在同一确定性陷阱上的失败签名一致率），**不是**权重空间结论的移植——详见 README 致谢区与 `docs/research.md`。
- **效果量化（0.25）**：`light-cli.mjs report` 周报（L1 活性/L2 回填率/L3 错误家族复发，`--json` 可机读）；`recall --record "<结论>"` 把验证结论回填生产账本；`draft/distill --commit` 自动写 deposit 事件。
- **许可验证（0.25）**：`light-cli.mjs license verify <token>` 验证 Ed25519 签名许可（发行方公钥随包 `assets/issuer-pub.txt（ClawHub/GitHub 0.25.0 首发的 .pem 版同样兼容）`）；许可机制本身开源，便于任何发行方接入。
- **IO 重试语义**：文件读写对瞬态错误（EBUSY/EPERM/EACCES/ETIMEDOUT）自动重试（默认 3 次/截止 3s，`EVOX_IO_RETRY`/`EVOX_IO_DEADLINE_MS` 可调）；非瞬态错误不重试；重试是优化不是门——绝不因重试机制阻塞调用方（fail-open）。
- **IO 熔断与降级（0.34）**：连续 5 次瞬态失败打开熔断，其后 10s 内只尝试 1 次（不重试、不退避）并输出一次可执行指引（`EVOX_IO_CB_THRESHOLD`/`EVOX_IO_CB_COOLDOWN_MS` 可调）；IO 一旦恢复即自动闭合；非瞬态失败（如空库的 ENOENT）不触发熔断。
- **显式错误码（0.34）**：所有失败输出在保留退出码（0/1/2）的同时附加具名错误码 `[E_USAGE]`/`[E_ARGS]`/`[E_GUARD]`/`[E_NOTFOUND]`/`[E_INTERNAL]`，便于脚本精确区分失败类型；完整错误码表见 `docs/advanced.md`。
