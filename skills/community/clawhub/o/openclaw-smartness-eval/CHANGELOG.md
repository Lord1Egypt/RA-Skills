# Changelog / 版本变更日志

All notable changes to this project are documented in this file.
本文件记录所有重要变更。

Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [0.2.1] - 2026-03-16

### Added / 新增
- **`scripts/state_probe.py`** — New safe probe script replacing inline `python -c` commands. Supports three probes: `quality-gate-prompt`, `latency-state-count`, `rule-candidates`.
  新增安全探针脚本，替代内联 `python -c` 命令。支持三种探针。
- **Command validation** (`validate_command()` in `eval.py`) — Multi-layer security gate before any subprocess execution: interpreter whitelist, inline code block, absolute path block, path traversal block, prefix whitelist.
  多层命令安全校验：解释器白名单、内联代码阻止、绝对路径阻止、路径穿越阻止、前缀白名单。

### Changed / 变更
- **Task suite** — Replaced all `python -c` + `exec(open(...).read())` patterns in `config/task-suite.json` with calls to `state_probe.py`. Removed all hardcoded absolute paths (`/Users/...`).
  替换所有内联代码执行和硬编码绝对路径。
- **Author** — Updated metadata author to `圆规` across `_meta.json`, `SKILL.md`, `LICENSE`.
  作者更新为"圆规"。
- **LLM judge docs** — Clarified that `--llm-judge` is off by default and requires explicit opt-in + API key. No raw data is sent externally.
  明确说明 LLM 裁判功能默认关闭。

### Security / 安全
- Blocked unsafe command patterns: `-c` flag, `exec(` string, absolute paths, `..` traversal, non-whitelisted path prefixes.
  阻止不安全命令模式。
- All test commands now pass through `validate_command()` before `subprocess.run()`.
  所有测试命令执行前必须通过安全校验。

---

## [0.2.0] - 2026-03-16

### Added / 新增
- **12-dimension evaluation framework** — Understanding, Analysis, Thinking, Reasoning, Self-iteration, Dialogue, Responsiveness + Robustness, Generalization, Policy adherence, Tool reliability, Calibration.
  12 维度评估框架。
- **28 automated tests** — Covering intent recognition, risk detection, reasoning templates, API health, cron status, benchmark pass rate, and more.
  28 项自动化测试。
- **3 evaluation modes** — `quick` (daily), `standard` (weekly), `deep` (monthly audit with pass@k).
  三种评估模式。
- **Anti-gaming probes** — Randomized test inputs injected at eval time to prevent overfitting.
  反作弊随机探针。
- **Trend comparison** — `--compare-last` flag to show dimension-level deltas vs previous run.
  趋势对比功能。
- **Optional LLM judge** — `--llm-judge` for subjective scoring via DeepSeek or OpenAI API.
  可选 LLM 裁判功能。
- **Structured output** — JSON run file, Markdown report, and JSONL history for longitudinal analysis.
  结构化输出：JSON、Markdown、JSONL 历史。
- **Detailed rubrics** — 0–5 scale with concrete criteria for all 12 dimensions in `config/rubrics.json`.
  详细评分量表。
- **Health check** — `scripts/check.py` for verifying skill structure integrity.
  技能结构健康检查。
