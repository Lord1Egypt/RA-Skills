# eval/results/archive — 历史评测产物存档

> ⛔ 本目录全部文件不可作为现行口径引用（历史档案）。现行基线见 `../CURRENT.md`。

本目录存放已被后续评测取代或作废的历史结果。**文件名中的标记含义：**

- `*.STALE-cache-poisoned.json` — 2026-10-02 评测缓存污染事故的**作废结果**（v36 时代：缓存键未绑定模型指纹导致陈旧分复放）。这些 JSON 里的数字**无效**，仅作为事故证据保留；事故根因与结构性修复见 `CHANGELOG.md` v4.4.0 节（缓存键绑定模型 md5 + `check_leak.py` 数据卫生闸）。

**现行口径唯一权威 = 上一级目录的 [`eval/results/CURRENT.md`](../CURRENT.md)**（v7.4.0 起物理分层）：
可引用基线只有 `v35ctl_oldgen.json` / `v35ctl_gen2026.json` / `golden_detection.json` 三个（指纹绑定）。
本目录内所有文件（含历史上曾被称作"基线"的 `v480_rules_*` / `v500*` 等）均已**不可引用**，
只作过程留痕；如需了解现行口径的判定规则，读 CURRENT.md，勿据本目录任何文件下结论。
