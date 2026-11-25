# 能力边界 & 触发方式速查表

> **本页定位**：「**什么时候不该用** / **能用到什么程度** / **什么时候该跑一次**」的**唯一权威入口**。
> 原先散落在 `docs/overview.md`、`docs/common-mistakes.md`、`docs/faq.md` 与 SKILL.md 各处的边界与触发信息，**全部收敛在本页**；其余文档只做指针，不再各自复述。
> **EN**: The single authoritative page for capability boundaries and trigger points — "when NOT to use it", quantitative limits, and "when to run it". Other docs link here instead of duplicating.

## 0. 三句话结论

1. 它是「**踩过的坑只踩一次**」的运行时——**不是**知识库，**不是** 100% 避坑保证。
2. 召回必须**绑死在动作节点上**（T1–T5）；指望"记得跑"必然失效（实测：相关基因能召回排 #1，却因动手前没跑召回而重复踩坑）。
3. 边界是**量化**的（见 §2），越界用法有明确替代方案（见 §1）。

## 1. 不适用场景（明确说"什么时候别指望它"）

| 场景 | 为什么不适合 | 改用什么 |
|---|---|---|
| **多台机器同时写同一个基因库** | 跨机不共享文件锁，只能靠"各自写 + Git 合并 + LWW 裁定" | 各自维护本地库，用池做单向分发 |
| **需要 100% 避开某个坑** | 注入是**软提示**，遵从度随模型而异（实测不同模型同一陷阱 0/5 vs 5/5） | 把关键修法写进项目文档/代码规范，不依赖提示层 |
| **要求实时同步的共享库** | 自建池是 Git 快照，推拉有网络延迟（秒级~分钟级） | 需要实时就换中心化服务（本项目刻意不做） |
| **一次性任务 / 无复盘场景** | 沉淀的价值靠复用摊薄，没有第二次就只剩成本 | 直接手工修，不必开围栏 |
| **把基因库当权威知识库** | 基因是**修法**，不是知识条目；来源可追溯但可能单源未验证 | 知识库用文档/向量库，基因库只放"踩过的坑与修法" |
| **给不同架构的 agent 直接复用同一条修法** | 修法有效性受模型影响（实测跨模型失败签名可能完全不重叠） | 关键修法先做**异构复现**（`report` 的 L4 跨源率）再扩散 |

> **EN**: Not a fit for: several machines writing **one shared library** concurrently (no cross-machine lock); anything needing a **100% avoidance guarantee** (injection is a soft prompt; measured 0/5 vs 5/5 on the same trap); **real-time** shared sync (the pool is a Git snapshot); one-off tasks with no follow-up; using the library as an **authoritative knowledge base**; reusing one fix across **different architectures** without independent reproduction.

## 2. 量化边界（全部标注实测状态）

| 维度 | 当前实测值 [A] | 边界说明 |
|---|---|---|
| 库规模 | 本机 **241 条记录 / 157 条已审核**（2026-10-26 实测） | 打分公式：信号匹配 +3/个、正文 token 交集 +1/个、负载均衡 ±2，**低于 2 分不注入**；召回排序对 10² 量级稳定 |
| 库规模上限 | **合成集 500/1000 条已实测**（真实宿主未验证 `[C]`） | EN: stable at 10²–10³; recalibrate beyond 1000 via L1/L2 A/B；打分对 10²–10³ 量级稳定 |
| 注入条数 | `--top` 默认 **5 条** | 只注入「已审核 + 过修法守卫 + 与查询对靶」的条目；宁缺毋滥（实测：不对靶注入比不注入更差） |
| 并发写入 | 单机多会话：文件锁（withLock，**5s 超时 fail-open**） | **跨机并发无分布式锁**——靠「各自库 + git 合并 + LWW 台账」裁定 |
| 池同步延迟 | 自建 Git 池：推拉即 git 往返（秒级~分钟级，取决于网络） | 池不是实时服务；`gene pull` 拉到的是上次快照 |
| 溯源覆盖 | deposit/register-hit/negate 自动记录 `source_model` + `source_host`（0.29 起；0.30 起自动读 `~/.evomap/source.json`） | `report` 的 L4 出「跨源率」——单源占比高 = 修法只被一个（模型｜宿主）验证过，换环境可能失效 |
| 运行时要求 | **Node ≥22**（traps 生成器另需 Python 3） | 版本过低时 pi/evolver 可能启动失败 |
| 外部依赖 | 默认 light 后端**零外部依赖** | 只有 evolver 集成（`--engine evolver`）才需 `npm install` |
| 网络可达性 | 两轴（0.43 O08 精确化）：**进程与存储**（引擎/CLI/钩子/基因库）全部本地；**模型请求**仅在两处显式 opt-in 场景外发——流程 C 编排器（任务文本/代码发给用户配置的 provider，必须显式传 provider/model/api-key）与 `--llm-refine`（**默认禁用**） | 国内 npm/GitHub 加速见 §6.4 |
| 基因有效性衰减 | 有反馈基因按**时间半衰期默认 90 天**（`EVOX_GENE_DECAY_DAYS` 可调，非法值拒绝并告警）+ 否定压力（≥2 次否定且否定率 ≥50% 再减半）打折，**地板 0.25** | 无反馈基因**不衰减**（归审核门控管）；衰减永不单独杀死基因（硬过滤仍归审核门控+守卫）；`EVOX_GENE_DECAY=0` 一键回旧行为 |
| kv 压缩同族加权 | 已知同族基因召回加分 **+1.5**（`EVOX_SAME_KV_WEIGHT` 可调，设 0 关闭） | 族别取 `generation_meta.source_kv`（`none`/`csa-s4`/`stride2`/`unknown`）：**闭源模型一律 `unknown` 不猜**；本机族未知时不加权（行为与未加权版本一致） |

## 3. 五个触发点 T1–T5（核心设计）

> 「装了技能但没人调用」是本项目最根本的失效模式——**连作者都会忘**（实测：相关基因能召回排 #1，却因为动手前没跑召回而重复踩坑）。所以不能指望"用户记得"，必须把召回**绑死在具体动作节点上**。
> **EN**: Recall must be bound to concrete action nodes, never left to memory. Integration manual: `docs/advanced.md`.

| # | 触发点 | 时机 | 命令 | 没接会怎样 |
|---|---|---|---|---|
| **T1** | 任务开始 | 拿到非平凡任务、**规划之前** | `recall --query "<任务>"` | 预防失效：该避的坑照踩 |
| **T2** | 行动前 | **即将执行第一次不可逆动作之前**（写文件/提交代码/部署/调外部接口/删改数据）；同一任务内同类动作**只触发一次** | 同上（query=**将要做的具体动作**） | 贴身预防（可选） |
| **T3** | **遇到报错** | 工具返回错误、**准备重试之前** | `recall --error "<报错原文>"` | **最可惜**：库里明明有修法，却盲目重试 |
| **T4** | 修好坑后 | 修复了一个不显而易见的坑 | `draft --error ...`（沉淀） | 经验流失，下台机器再踩 |
| **T5** | 任务结束 | 收尾 | `--register-hit --gene <id>` / `--negate --gene <id>` | 无法度量，失效修法发现不了 |

### 3.1 T2 判定口径与例子

**判定三条件**：① 动作**尚未执行**（执行完就晚了）② 动作**有副作用或不可逆**（写/提交/部署/外发/删除）③ **本任务内首次**做这类动作；纯读取/查询类动作不需要 T2。query 写**动作短语**（不是任务名）——召回按动作措辞对靶。

**3 个可直接对号的例子**：
1. 刚要 `git commit -m` 一个跨多文件的改动 → query `"提交跨文件改动前检查"`
2. 刚要跑一个会**覆盖**目标目录的部署脚本 → query `"部署前备份与干跑"`
3. 刚要把本地改动**强推到远端**（覆盖远端历史）→ query `"force push 前确认远端状态"`

不命中 ⇒ 直接执行（宁缺毋滥，T2 是可选增强，不添延迟负担）；命中 ⇒ 先读修法再动手。**反例（不必触发）**：读文件、搜代码、跑测试、查看状态——纯读取无副作用。

### 3.2 T3：报错自动触发（收益最高、却最容易被忽略）

T3 是唯一「**不用你记得**」的触发点——**报错本身就是提醒**。实测里最可惜的失效形态正是「库里明明有修法，却盲目重试」。

```bash
node code/evolver-recall.mjs --error "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 0"
```

口径：工具返回错误、**准备重试之前**，把**报错原文**直接当查询（不要自己概括）。命中后按修法重试；仍失败 → 走 T4 沉淀这条新坑。

## 4. 触发词 ↔ 命令映射

| 组 | 主词（记这一个就够） | 同义词（说了也算） | 触发点 | 具体命令（可直接复制） |
|---|---|---|---|---|
| **召回类** | **召回** | 经验召回 / 错题本 / 避坑 / recall / lessons | T1 | `node code/evolver-recall.mjs --query "<任务一句话>"` |
| **召回类（报错）** | **报错了** | 失败了 / 又挂了 / 重试 / 修一下 / error / traceback | T3 | `node code/evolver-recall.mjs --error "<报错原文>"` |
| **沉淀类** | **沉淀** | 记一笔 / 入库 / deposit / distill / 存起来 | T4 | `node code/light-cli.mjs draft --error "<报错原文>"` |
| **进化类** | **继承** | 自进化 / 经验继承 / evolver / pi-evox | T1 + T4 | 先 T1 召回，修好后 T4 沉淀 |
| **体检类** | **体检** | 自检 / 健康度 / 有没有失效 / doctor / info | 随时 | `node code/light-cli.mjs info` |
| **签名类** | **签名** | 验签 / 篡改 / provenance / identity | 跨机协作前 | `node code/light-cli.mjs verify <gene_id>` |

> **覆盖范围说明**：① 上表是**人/agent 的调用提示**，不是召回匹配机制——召回命中靠 `signals_match × query-token 重叠`（确定性对靶），触发词只告诉你"什么时候该跑一次"；② **覆盖不到所有说法是正常的**：任务开始只要判定为"非平凡"就走 T1，不需要措辞命中任何一组；③ 中文措辞走 `aliases.json` 概念别名映射到英文 canonical（0.28），两种措辞都能命中；④ 报错类（T3）不需要触发词——**报错本身就是触发**。

## 5. 多宿主 / 并发行为矩阵

| 情形 | 行为 | 依据 |
|---|---|---|
| 两个宿主同时召回同一基因 | **各自独立注入**（软提示按宿主上下文渲染，不共享状态） | 召回无跨进程状态 |
| 同一宿主多会话并发召回 | 各自独立选出 top-N，**不共享选择快照**（0.18 起按 gene_id 寻址，不再有位置漂移） | `selectList` 每次现算 |
| 同一基因被多台机器同时沉淀 | `asset_id` 去重（内容哈希）→ 只落一条；**不同内容则各落一条** | store.appendGene |
| 审核状态跨机冲突 | 各自台账 **LWW**（最后一个状态生效）——quarantine 可撤销 approve | review.jsonl |
| 一个宿主钩子重复触发（心跳/重连） | 召回幂等：重复注入不重复计命中（hits 只在 `--register-hit` 时记） | 埋点口径 |
| 钩子 env 到不了 agent 自调命令 | `persistActualSource` 把钩子透传的实测模型落 `last_source.json`，后续 deposit/hit 经它取到 | 0.32 D-2 |
| 多会话并行 register-hit | **0.18 起必须用 `--gene <asset_id\|gene_id>` 按 id 寻址**；0.17 及更早用位置编号会因共享选中集被覆盖而漂移 | 并发修复 |

## 6. 接入方式（按宿主类型选一种）

**6.1 有钩子的宿主（OpenClaw / Hermes）** — `install-hooks`
默认**只演练**（打印将复制的文件、目标路径、需手工确认的注册步骤，**不落盘**）；确认后加 `--yes` 才写入（写入前自动备份）。回滚 = 删除钩子目录。它**不会擅自改坏宿主配置**。

**6.2 有指令文件的宿主（AGENTS.md / CLAUDE.md / 系统提示）** — `install-snippet`
输出「五个触发点」操作规程，粘进指令文件即可。对**没有钩子机制的宿主**，这是最可靠的接入方式。

**6.3 补上写侧 last mile（T4 不自动沉淀的典型原因）**
技能只在被加载时影响 agent——T4 没进上下文就等于没有。解法：`install-snippet --file <项目>/AGENTS.md --yes`，把五触发点规程写进项目指令文件。

**6.4 国内网络**
npm 换国内镜像：`npm config set registry https://registry.npmmirror.com`；GitHub 克隆可用镜像代理或直接下载 Release zip。

**6.5 自检 "装了却没生效"**
```bash
node code/light-cli.mjs info      # 看「召回次数 / 命中 / 待审」
```
- **召回次数 0** ⇒ 手工跑一次召回，或 `install-hooks` 让宿主自动召回；
- **待审 > 0** ⇒ 这些基因不会注入，用 `approve <gene_id>` 放行。

> 完整接入契约（三步 + 模板）见 `docs/advanced.md`「宿主接入」节；跨机与命名池工作流见 `docs/cross-machine.md`。

## 7. 安全边界（简述，明细见 `docs/advanced.md`）

基因是注入 system prompt 的**软提示**——一条恶意基因就是一次提示词注入。因此设四道门：

| # | 门 | 管什么 | 在哪生效 |
|---|---|---|---|
| 1 | **修法守卫** | 有没有**真修法**（无可可执行成分 → 不注入） | 召回 |
| 2 | **叙述守卫** | 是不是**旁白流水**（开场白式 → 不注入；实测等效噪声 +36pp） | 召回 |
| 3 | **注入守卫** | 是不是**恶意指令**（提示词注入 → 不注入；回归 31/31 恶意拦截、11/11 正常零误杀（发布门禁每版实测、数字见发布页更新说明；完整套件按设计不随包分发，包内 selftest.mjs 为快速哨兵）） | 召回三条通道 + 导入 + 导出 |
| 4 | **脱敏闸门** | 会不会**泄私有内容**（内网 IP/家目录路径/密钥/令牌/内部代号 → 拦截不出网） | 导出 + 导入 |

> 门模块缺失时：**导出/导入 fail-closed（拒绝执行）**；`evolver-recall.mjs` 侧只跳过注入门、其余三门照常（宿主 bootstrap 不能因守卫失败而阻断使用者）。
> **文档纪律**：此处（及仓库所有注释）只描述**机制类别**、不引用触发串原文——说明文字本身会被扫描器当成注入样本（本仓有为此发版的先例）。
> **EN**: Genes are soft prompts — one malicious gene is one prompt injection. Four gates: repair-signal, narration, injection (regression 31/31 malicious caught, 11/11 legitimate zero false-kill (measured in the release gate each version, figures in the release notes; full suite not shipped, bundled selftest.mjs is a quick sentinel)), redaction (privacy, fail-closed off-machine).

## 8. 冷启动与常见误期待

| 误期待 | 实际（机制） | 怎么做 |
|---|---|---|
| 首次运行就该有东西可召回 | 库从零开始，物理上无可注入修法 | `light-cli starter` 装 20 条策展教训（装载时同样过脱敏 + 注入两道门），立刻可命中 |
| 注入后必定不踩坑 | 软提示把「多次试错」压成「最多一次教训」，**不承诺 100%** | 关键修法额外写进项目文档/规范 |
| 沉淀了很多却从没被用过 | 多半是召回没跑（次数 0）或卡在待审 | 见 §6.5 `info` 自检 |
| 自己的沉淀还要人工审核 | 审核语义统一见 SKILL.md「审核状态机」（召回侧守卫仍兜底） | 改人工：`config --auto-approve off`（共享池 `gene import` 仍按 `--tier` 判定） |
> **EN**: Review semantics live in the SKILL.md review-state-machine section (single source of truth); recall-side guards still backstop. Switch to manual via `config --auto-approve off`; pool imports still follow `--tier`.

## 相关指针

- 自检与见效路径：`examples/quickstart.md`（5 分钟闭环）
- 术语不明：`docs/glossary.md`（一页纸，每词配最小例子）
- 错误用法完整清单：`docs/common-mistakes.md` ｜ 配置错误：`docs/config-errors.md`
- 进阶（回填寻址/并发锁/共享库/宿主接入/安全门明细）：`docs/advanced.md`
- 安全与许可全文：`docs/security-and-license.md`
