"""NOMOS version."""

# 0.7.0 — 破坏性变更：元因果账本五基改用因果论术语
#   meta_ledger.bases 的五个键改为全 ASCII，消费方必须同步：
#     trace_gap / parallel_convergence / narrative_occlusion /
#     bounded_audit / causal_succession
#   reason 码前缀同步收敛为 TRACE_ / CONVERGENCE_ / NARRATIVE_ /
#   AUDIT_ / SUCCESSION_。旧前缀与旧键名一并废弃，**不保留别名**——
#   留别名等于让两套词汇长期共存，那才是真正删不掉的成本。
#   同时不再逐字引用规范原文（改为改述 + 标节号），doctrine 文案随之调整。
#
# 0.6.0 — 认知审计内核由五算子升级为十算子（⊙ORI / ⊞TPG / BFC / ⇄GRF / META）。
#   新增：无规则思维拓扑（四进程校验，含公理 5 链内时序）、二元事实校验、
#         灰度反馈、元因果账本（度量，永不阻断）。
#   产物版本串随之由 GCAE-1.0.0 升至 GCAE-1.1.0（见 adapter.ADAPTER_SCANNER_VERSION）。
#   注意：NOMOS 的 DecisionRequest 契约尚无 origin / gray_levels 字段，
#   adapter 路径因此只做条件注册 —— 详见 adapter.ADAPTER_BASE_OPERATORS。
VERSION = "0.7.0"