# CHANGELOG

## v1.0.0 — Public Release (2026-03-19)

### Core Features
- **Trigger Rate Testing**: Detect whether skill descriptions cause correct SKILL.md reads
- **Quality Compare**: With-skill vs without-skill output comparison
- **Model Comparison**: Quality + speed across haiku/sonnet/opus
- **Latency Profiling**: p50/p90/std_dev statistics
- **Description Diagnosis**: Identify gaps in skill description coverage

### Architecture
- Two-layer design: agent drives workflows, Python scripts analyze data
- No `claude` CLI dependency — runs entirely via `sessions_spawn` + `sessions_history`
- Parallel evaluation support (6-8 workers, 5-10x speedup)

### Tooling
- `resolve_paths.py`: Auto-detect skill paths from openclaw.json
- `analyze_triggers.py`: Trigger detection with description diagnosis
- `analyze_quality.py`: Assertion-based quality scoring
- HTML report viewer for interactive result browsing
- Unit tests (24 tests, pytest)

### Documentation
- Agent-driven workflows in `USAGE.md`
- Bundled `weather` and `fake-tool` evals for quick validation
- CLI wrapper eval template

---

## Pre-release History

- v0.5: Description diagnostics + latency profiling
- v0.4: Model comparison framework
- v0.3: Parallel execution
- v0.2: HTML visualization
- v0.1: Initial trigger rate + quality compare
