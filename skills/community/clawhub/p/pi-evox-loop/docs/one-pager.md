# Pi × EvoX Loop 一页纸

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

## 信任要素（为什么敢用）
- **本地优先**：默认后端零依赖纯 Node；唯一外发选项 `--llm-refine` 默认禁用；
- **四道安全门**：修法守卫/叙述守卫/注入守卫（回归用例 **16/16 恶意样本拦截、7/7 正常零误杀**）/脱敏闸门；
  > **EN**: Four gates - repair-signal, narration, injection (regression suite: **16/16 malicious samples caught, 7/7 legitimate zero false-kill**), and redaction.
- **可验证的效果**：配对对照实验（扣除重复执行基线 ≈-22%）；
  > **EN**: Measurable effect via paired control runs (repeat-execution baseline of about -22% already deducted).
- **provenance 签名链**（0.21）：Ed25519 每机身份，池基因验签，篡改拒收。
  > **EN**: Provenance signature chain (0.21): per-machine Ed25519 identity, pool genes verified on import, tampered content rejected.

## 5 分钟上手
见 [`examples/quickstart.md`](../examples/quickstart.md)。Node ≥22，无其他依赖。

## 局限（诚实声明）
- 修法注入是**软提示**——遵从度随模型而异，不承诺 100% 避坑；
- 库的价值随使用复利增长，冷启动需要先沉淀几条；
- 共享池是自建 opt-in 机制，不是中心化服务。

## 致谢
方法论受 [numbat](https://github.com/perplexityai/numbat)（Perplexity，Apache-2.0，取证重建）与 [FlyLoRA](https://arxiv.org/abs/2510.08396)（NeurIPS 2025，负载均衡/免训练合并不干扰）启发；上游引擎 [pi-coding-agent](https://github.com/earendil-works/pi)（MIT）/ [@evomap/evolver](https://github.com/EvoMap/evolver)（GPL，可选集成）。
