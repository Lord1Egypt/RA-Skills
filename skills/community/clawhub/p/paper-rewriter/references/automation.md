> **何时读我**：CI/agent 门禁、批量自动化、机器可读消费。
> **回 [INDEX](INDEX.md)**

# 自动化与 CI 集成

所有判定双口径机器可读：

- **缺省口径（人读流程）**：`verify.py` 独占退出码 0/1/2（1=完整性 FAIL）；
  detect/transform/compare/pipeline 跑完恒 0，判定写在报告里。不要按它们的
  缺省退出码写分支。
- **机器口径**——detect / compare / pipeline 加 `--exit-verdict`（或等价短别名
  `--ci`，v3.1.0 起，方便 CI 里少打字）：
  `0` 干净（低档、无残留）· `3` 风格特征中及以上（需深改）· `4` 命中模型残留
  （先跑 transform）· `1` 完整性 FAIL（仅 pipeline 产出，与 verify 契约同义）·
  `2` 用法错误（不受影响）。**pipeline 是唯一 1/3/4 全档门禁**，CI 推荐：
  `pipeline.py 原稿.txt --rewrite 改稿.txt --terms terms.txt --exit-verdict`。
- **JSON**：`detect -j`（完整扫描结果）、`pipeline --json`（前后分/verify 判定/
  `exit_verdict` 字段/处置提示/深改简报）、`compare --json`（变化量+verify）、
  `plan.py --json`（句级队列+预算投影）。一行门禁示例：
  `python scripts/pipeline.py 原稿.txt --rewrite 改稿.txt --json --exit-verdict || echo "拦截: $?"`
- 两套口径的退出码全表：`references/errors.md` 第一节。

---



---

# Automation & CI integration (EN)

Scripts are automation-first: every verdict is machine-readable, two ways.

- **Default contract (human flows)**: `verify.py` alone holds exit 0/1/2
  (1 = integrity FAIL); detect/transform/compare/pipeline finish with 0 and
  put the verdict in their report. Never branch on their default exit code.
- **Machine contract** — add `--exit-verdict` (or the shorter `--ci` alias, v3.1.0)
  to detect / compare / pipeline:
  `0` clean (low, no residue) · `3` style patterns at medium or above (needs
  deep revision) · `4` model-residue hit (run transform first) · `1`
  integrity FAIL (pipeline only — same meaning as verify's 1) · `2` usage
  error (unchanged). **pipeline is the only full 1/3/4 gate** — recommended
  CI check: `pipeline.py draft.txt --rewrite rewritten.txt --terms terms.txt
  --exit-verdict`.
- **JSON**: `detect -j` (full scan result), `pipeline --json` (before/after,
  verify verdict, `exit_verdict` field, handling `hints`, agent brief), `compare --json`
  (delta + verify), `plan.py --json` (sentence queue + projections).
  Example gate in one line:
  `python scripts/pipeline.py orig.txt --rewrite new.txt --json --exit-verdict || echo "blocked: $?"`
- Exit-code tables for both contracts: `references/errors.md` §1.
