# CHANGELOG

## 1.2.0 — 2026-10-23（首个公开发布版）

**更名**

- 技能由 `il-radar`（信息素养雷达）更名为 **`il-reader`**；`name` / `display_name` / 目录名 / 发布包名同步，功能与数据不变。

**新增**

- 复查单（`references/review.md`）：每道未命中题库的题，答复都附「有序步骤 + 网站表 + 产物 + 缺口」，供他人独立复核。
  - 分档：T0 题库命中（≤6 行、无 URL）／T1 轻量（8–15 行）／T2 完整（15–30 行，置信度 < 80% 强制）。
  - 阶段码 S1–S9；每步状态 `ok / empty / blocked / error / skipped`。
  - 硬规则：不得事后补编步骤；`blocked` / `error` 渠道必须入表。
- `README.md`：能力、边界、快速开始、依赖、题库说明与勘误流程、常见问题。
- `LICENSE`：MIT，附题库与站点档案的授权范围说明。

**变更**

- `SKILL.md` §答复格式：由"四行结论"扩展为"四行结论 + 复查单"，并删除旧约束"不展示工具过程、自检清单或用时"。
- `SKILL.md` 新增 §依赖与降级：`node ≥ 18`、`playwright-cli`（可选）、联网工具（未命中题库时必需）。
- `SKILL.md` frontmatter：`allowed-tools` 由 `Bash, Read` 补为 `Bash, Read, WebFetch, WebSearch`；版本 1.0.0 → 1.2.0。
- `references/answer.schema.json`：新增可选字段 `steps[] / sites[] / artifacts[] / gaps[] / review_level`（向后兼容，`required` 未变）。
- `references/retrieval.md`：§置信度与答复 同步复查单模板，明确 `empty` 仅用于确证的空结果。
- `references/exam-scope.md`：网站表 `档案` 列可引用 `sites/<站>.json`。

**修复**

- 文档漂移：`references/question-bank.md` 中引用的 `tools/build-digest.cjs`、`tools/validate-bank.cjs`、
  `tools/list-flagged.cjs` 实际不存在，改为 node 单行重算摘要 + `lookup.cjs --status` 自检。
- 移除全部个人绝对路径（`SKILL.md` 排障、`browser-playwright-cli.md`、`review.md`），统一为
  `~/ilradar-work/` 与 `command -v node` 的通用写法。

## 1.1.0 — 2026-10-23（内部版）

- 新增复查单规范与 `references/review.md`。
- 答复格式由四行扩展为两段式。
- 回归：`lookup.cjs --status` → 1017 题、eligible 1017、failures 0。

## 1.0.0 — 内部版

- 两级工作方式：本地题库（1017 题）比对 → 证据缺口检索。
- 6 张稳定规则卡、252 个站点入口档案、`playwright-cli` 浏览器工作流。
- 全文与页面核对三条硬规则（无文本层转图像、页码偏移校验、指定工具口径）。

---

### 题库勘误

（暂无。勘误合并时在此登记：题号 / 原答案 / 更正 / 依据链接 / 日期）
