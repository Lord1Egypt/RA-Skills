# Pi × EvoX Loop 项目概览

> **EN**: One-pager: coding agents re-discover the same fixes from scratch every session. PiEvoX gives them an "experience inheritance" runtime - recall validated fixes at task start, deposit new ones after fixing non-obvious failures. Local-first, MIT (zero-dep default backend), four security gates, measured gains (GBK trap: decode errors 11->4, tokens -55%; illegal JSON: errors 14->3, tokens -53%; paired control isolates the ~-22% repeat-execution baseline).

## 一句话
给编码智能体装「经验继承」：**Agent 踩过的每个坑，只踩一次。**

## 问题
- 每次新会话，Agent 都从零开始——同一个坑（编码、路径、权限、API 限流）反复踩；
- 个人/团队的经验散落在聊天记录和备忘里，无法在**下一次任务开始时自动生效**。

## 方案
- **流程 A（召回）**：任务开始/遇到报错时，`evolver-recall --query/--error` 把**已验证的修法**注入上下文（对靶过滤，不相关不注入）；
- **流程 B（沉淀）**：修好一个不显而易见的坑后，`draft --error` 引导式生成基因（含负经验 anti_patterns），过质检门后入库；
- **流程 C（可选，研究）**：受控实验量化继承收益（陷阱 → R1/R2 对比）。

## 安全属性
- **本地优先**：默认后端零依赖纯 Node；唯一外发选项 `--llm-refine` 默认禁用；
- **四道安全门**：修法守卫/叙述守卫/注入守卫（回归用例 **16/16 恶意样本拦截、7/7 正常零误杀**）/脱敏闸门；
  > **EN**: Four gates - repair-signal, narration, injection (regression suite: **16/16 malicious samples caught, 7/7 legitimate zero false-kill**), and redaction.
- **可验证的效果**：配对对照实验（扣除重复执行基线 ≈-22%）；
  > **EN**: Measurable effect via paired control runs (repeat-execution baseline of about -22% already deducted).
- **provenance 签名链**（0.21）：Ed25519 每机身份，池基因验签，篡改拒收。
  > **EN**: Provenance signature chain (0.21): per-machine Ed25519 identity, pool genes verified on import, tampered content rejected.

## 场景词表（基因分类，0.24）
`ops-deploy`（部署/服务器）· `coding-debug`（编码/解析）· `release-publish`（发布/版本）· `api-integration`（API/webhook）· `git-workflow`（git/仓库）· `agent-runtime`（宿主/管线）——拉取/策展/退役按此分；召回对靶仍由 signals 自由匹配。

## 上手路径
见 [`examples/quickstart.md`](../examples/quickstart.md)。Node ≥22，无其他依赖。

## 已知局限

> **0.34 起**：本节的量化边界与「不适用场景」已**同步收敛至 [`docs/boundary-and-triggers.md`](boundary-and-triggers.md)**（统一入口，另含触发方式 T1–T5、多宿主并发矩阵与三类接入方式）。此处保留简版供一页纸速读；两者若冲突，**以速查表为准**。
> **EN**: From 0.34, the quantified boundaries and "when not to rely on it" have been consolidated into [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) — the single entry point, also covering triggers T1-T5, the multi-host concurrency matrix and the three integration modes. This page keeps the short version for one-pager speed; if the two conflict, the quick-reference table wins.

- 修法注入是**软提示**——遵从度随模型而异，不承诺 100% 避坑；
- 库的价值随使用复利增长，冷启动需要先沉淀几条；
- 共享池是自建 opt-in 机制，不是中心化服务。

### 规模的量化边界（0.29 补，全部标注实测状态）
| 维度 | 当前实测值 [A] | 边界说明 |
|---|---|---|
| 库规模 | 本机 217 条记录 / **133 条活跃（已审核）**（2026-10-21） | 打分公式：信号匹配 +3/个、正文 token 交集 +1/个、负载均衡 ±2，**低于 2 分不注入**；召回排序对 10² 量级稳定 |
| 库规模上限 | **合成集 500/1000 条已实测**（真实宿主未验证 `[C]`） | EN: stable at 10²–10³; recalibrate top-N beyond 1000 via L1/L2 A/B；打分对 10²–10³ 量级稳定（见 `_scale_0420_report.md`） |
| 注入条数 | `--top` 默认 5 条 | 只注入「已审核 + 过修法守卫 + 与查询对靶」的条目；宁缺毋滥（实测：不对靶注入比不注入更差） |
| 并发写入 | 单机多会话：文件锁（withLock，5s 超时 fail-open） | **跨机并发无分布式锁**——靠「各自库 + git 合并 + LWW 台账」裁定，不适合多机同时写同一库 |
| 池同步延迟 | 自建 Git 池：推拉即 git 往返（秒级~分钟级，取决于网络） | 池不是实时服务；`gene pull` 拉到的是上次快照 |
| 溯源覆盖 | deposit/register-hit/negate 自动记录 `source_model` + `source_host`（0.29 起；0.30 起自动读 `~/.evomap/source.json`） | `report` 的 L4 出「跨源率」——单源占比高 = 修法只被一个（模型｜宿主）验证过，换环境可能失效 |

> **EN**: Not a fit for: (1) several machines writing **one shared library** at the same time - no cross-machine locking; (2) anything requiring a **100% avoidance guarantee** - injection is a soft prompt and compliance varies by model (measured: 0/5 vs 5/5 on the same trap); (3) **real-time** library sync - the pool is a Git snapshot; (4) one-off tasks with no follow-up - the value only amortises on reuse; (5) using the gene library as an **authoritative knowledge base** - genes are *fixes*, not knowledge entries; (6) applying one fix across **different architectures** without independent reproduction - check the L4 cross-source rate first.
### **不适用场景**（0.30 补：明确说"什么时候别指望它"；完整 6 类 + 量化边界 + 触发方式见 [`docs/boundary-and-triggers.md`](boundary-and-triggers.md) §1）
| 场景 | 为什么不适合 | 改用什么 |
|---|---|---|
| **多台机器同时写同一个基因库** | 跨机不共享文件锁，只能靠"各自写 + Git 合并 + LWW 裁定" | 各自维护本地库，用池做单向分发 |
| **需要 100% 避开某个坑** | 注入是**软提示**，遵从度随模型而异（实测不同模型同一陷阱 0/5 vs 5/5） | 把关键修法写进项目文档/代码规范，不依赖提示层 |
| **要求实时同步的共享库** | 自建池是 Git 快照，推拉有网络延迟（秒级~分钟级） | 需要实时就换中心化服务（本项目刻意不做） |
| **一次性任务 / 无复盘场景** | 沉淀的价值靠复用摊薄，没有第二次就只剩成本 | 直接手工修，不必开围栏 |
| **把基因库当权威知识库** | 基因是**修法**，不是知识条目；来源可追溯但可能单源未验证 | 知识库用文档/向量库，基因库只放"踩过的坑与修法" |
| **给不同架构的 agent 直接复用同一条修法** | 修法的有效性受模型影响（实测跨模型失败签名可能完全不重叠） | 关键修法做**异构复现**（`report` 的 L4 跨源率）再扩散到更多宿主 |

## 致谢
方法论受 [numbat](https://github.com/perplexityai/numbat)（Perplexity，Apache-2.0，取证重建）与 [FlyLoRA](https://arxiv.org/abs/2510.08396)（NeurIPS 2025，负载均衡/免训练合并不干扰）启发；上游引擎 [pi-coding-agent](https://github.com/earendil-works/pi)（MIT）/ [@evomap/evolver](https://github.com/EvoMap/evolver)（GPL，可选集成）。

## 发布态单一数据源声明（0.38 生成）

<!-- evox-038-meta: upstream=pi@1.5.2,evolver@2.0.51; scan=baseline-ok; selftest=shipped; version=0.42.0 -->

本版上游实测、扫描基线与随包自检状态由生成器统一写入；判据 C40/C41/C42 直接读取本行，防止文档与实现漂移。
**EN**: Upstream versions, scan baseline and packaged self-test status are emitted from one generator; gates C40/C41/C42 read this marker to prevent drift.
