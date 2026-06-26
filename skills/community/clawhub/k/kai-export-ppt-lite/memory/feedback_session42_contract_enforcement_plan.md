# Session 42：report-creator guard/eval/contract-checks 迁移方案

日期：2026-04-24

## 触发背景

`Chinese Chan` 导出已到 `9.68/10`，但用户明确指出剩余差距主要不是结构，而是：

1. 字体气质不对
2. authored 换行没有保住表达节奏

进一步复盘后确认：

- `slide-creator` reference 里其实明确写了 typography 契约
- 源 HTML 也确实带了字体链接和字体栈
- exporter 的问题不是“拿不到信息”，而是：
  - contract sync 没同步 typography
  - 没有 render 前 contract enforcement
  - 没有字体 / 换行 fidelity gate

## 本轮结论

参考了 `report-creator` 的 4 条已落地链路：

- `scripts/guard_validate.py`
- `evals/contract_checks.py`
- `scripts/run-report-evals.py`
- README §6-8 的设计原则

决定把这套思路迁到 exporter，但首轮只聚焦：

- preset typography fidelity
- authored break fidelity

## 方案核心

### 1. Render 前 Guard

从：

`HTML -> parse -> layout -> render`

升级为：

`HTML -> contract enrich -> guard(validate + downgrade) -> layout -> render`

### 2. Zero-Drift Resolver

guard / renderer / eval 共享：

- `resolve_text_contract()`
- `resolve_break_policy()`

避免：

- guard 认为该用 serif
- renderer 最后又写成 sans

### 3. Graceful Degradation

禁止粗暴 shrink-fit。

优先级：

1. 扩文本框
2. 扩卡片高度
3. 调整组件槽位 gap
4. 仅在 contract 明确允许时 shrink-fit

字体降级也必须在气质家族内：

- `cn_serif` 不能退成 sans
- `en_serif` 不能退成 sans

### 4. Eval Boundary

新增 typed gate：

- `producer_contract`
- `typography_fidelity`
- `break_fidelity`
- `component_integrity`
- `render_integrity`

## 自评后的收紧项

1. parse 阶段必须保留 `source_text_raw` 和 `has_authored_breaks`
2. typography contract 不能只写字体名，必须写：
   - `family_mode`
   - `candidate_stack`
   - `safe_fallback_policy`
3. break policy 必须分级：
   - `preserve`
   - `prefer_preserve`
   - `allow_reflow`
4. traceability 首轮只做 sidecar JSON，不直接写 PPTX metadata
5. eval 首轮增量接入，不替代现有 visual compare
6. guard 输出分级：
   - `fatal`
   - `downgraded`

## 本轮评审状态

- 自我对抗性评审：已完成，见 `docs/session42-self-adversarial-review.md`
- Claude 对抗性评审：已尝试启动，但本轮不作为阻塞项；先按自评结果把主方案收紧，再进入实现

## 下一步

1. 让 Claude 对该方案做一轮对抗性评审
2. 将评审结论折回主方案
3. 再进入实现阶段：
   - `Chinese Chan` contract
   - typography sync
   - break fidelity guard
