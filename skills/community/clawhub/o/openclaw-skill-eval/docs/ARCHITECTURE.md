# OpenClaw Eval Skill Architecture

**Version**: v0.4 (2026-03-18)

---

## Three-Dimension Evaluation Framework

All skill evaluations use three unified dimensions:

```
                    ┌─────────────────────────────────┐
                    │           Skill Eval            │
                    └─────────────────────────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           ▼                       ▼                       ▼
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   Quality   │         │   Speed     │         │    Cost     │
    │  (outcome)  │         │  (latency)  │         │  (tokens)   │
    └─────────────┘         └─────────────┘         └─────────────┘
           │                       │                       │
    ┌──────┴──────┐         ┌──────┴──────┐         ┌──────┴──────┐
    │ trigger_rate│         │ p50 / p90   │         │ tokens_in   │
    │ quality_score│        │ std_dev     │         │ tokens_out  │
    │ assertions  │         │ bottleneck  │         │ api_cost    │
    │ recall      │         │ stability   │         │ $/1k_evals  │
    │ specificity │         │             │         │             │
    └─────────────┘         └─────────────┘         └─────────────┘
```

### Dimension Definitions

| Dimension | Question Answered | Key Metrics | Status |
|-----------|-------------------|-------------|--------|
| **Quality** | Can the skill complete the task? | trigger_rate, quality_score | ✅ Implemented |
| **Speed** | Is the skill fast and stable? | p50, p90, std_dev | 📋 Design complete |
| **Cost** | How much does the skill cost to run? | tokens, $/1k evals | 🔮 Deferred |

---

## Unified Data Structures

### EvalResult (single evaluation result)

```python
@dataclass
class EvalResult:
    eval_id: int
    eval_name: str
    model: str

    # Quality dimension
    quality: QualityMetrics

    # Speed dimension
    speed: SpeedMetrics

    # Cost dimension (deferred)
    cost: Optional[CostMetrics] = None

@dataclass
class QualityMetrics:
    triggered: bool
    quality_score: float          # 0-10, by grader
    assertions_passed: int
    assertions_total: int
    recall: Optional[float]       # for trigger tests
    specificity: Optional[float]  # for trigger tests

@dataclass
class SpeedMetrics:
    latency_seconds: float        # single run
    p50: Optional[float]          # across multiple runs
    p90: Optional[float]
    std_dev: Optional[float]
    stable: bool                  # std_dev < 3s
    bottleneck: Optional[str]     # step-level analysis result

@dataclass
class CostMetrics:
    tokens_in: int
    tokens_out: int
    api_cost_usd: float
    cost_per_1k_evals: float
```

### ComparisonMatrix (cross-model comparison)

```python
@dataclass
class ComparisonMatrix:
    skill_name: str
    models: list[str]
    dimensions: list[str]         # ["quality", "speed"]
    timestamp: str

    # Full results for each (eval, model) combination
    results: dict[tuple[int, str], EvalResult]

    # Aggregated statistics
    summary: dict[str, ModelSummary]

@dataclass
class ModelSummary:
    model: str
    avg_quality: float
    avg_latency: float
    trigger_rate: float
    stability: str                # "HIGH" | "MEDIUM" | "LOW"
```

---

## Tool Layering

```
┌─────────────────────────────────────────────────────────────────┐
│                    run_orchestrator.py                          │
│                    (entry point + dispatcher)                   │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌────────────────────┐
│ run_compare   │       │ run_trigger   │       │ run_model_compare  │
│ (A vs B)      │       │ (trigger rate)│       │ (cross-model+dim)  │
└───────────────┘       └───────────────┘       └────────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │     spawn_eval()      │
                    │  (core execution unit)│
                    └───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌─────────────┐         ┌─────────────┐
            │   grader    │         │   profiler  │
            │(quality score)│       │(speed stats)│
            └─────────────┘         └─────────────┘
```

### Tool Responsibilities

| Tool | Input | Output | Dimension |
|------|-------|--------|-----------|
| `run_compare.py` | evals + skill A/B | quality comparison | Quality |
| `run_trigger.py` | evals + skill | trigger_rate | Quality |
| `run_model_compare.py` | evals + skill + models | cross-model matrix | Quality + Speed |
| `run_diagnostics.py` | trigger_results + skill | diagnostics report | Quality (deep) |
| `run_latency_profile.py` | evals + skill | speed analysis | Speed (deep) |
| `analyze_triggers.py` | pre-fetched histories | trigger metrics | Quality (v2) |
| `analyze_quality.py` | pre-fetched transcripts | quality scores | Quality (v2) |
| `analyze_model_compare.py` | pre-fetched multi-model data | model matrix | Quality + Speed (v2) |
| `analyze_latency.py` | pre-saved timings | p50/p90 stats | Speed (v2) |

---

## Phase-to-Dimension Mapping

| Phase | Dimensions | Depth | Use Case |
|-------|------------|-------|----------|
| **3.1** Parallel | - | - | Accelerated execution |
| **3.2** Diagnostics | Quality | Deep | Description health diagnostics |
| **3.4** Model Compare | Quality + Speed | Broad | Model selection |
| **3.5** Latency Profile | Speed | Deep | Bottleneck identification |

**Design principles**:
- 3.4 covers breadth (multiple dimensions, multiple models)
- 3.2 / 3.5 cover depth (single dimension, deep analysis)

---

## Output File Conventions

```
workspace/
├── iteration-{N}/
│   ├── eval-{id}-{name}/
│   │   ├── with_skill_transcript.txt
│   │   ├── without_skill_transcript.txt
│   │   └── timing.json              # contains speed data
│   ├── trigger_rate_results.json    # Quality: trigger
│   ├── quality_scores.json          # Quality: grader
│   └── benchmark.md
│
├── model-compare-{N}/
│   ├── compare_matrix.json          # full matrix
│   ├── model_comparison_report.md   # human-readable
│   └── raw/
│
├── diagnostics-{N}/
│   ├── diagnosis.json
│   └── RECOMMENDATIONS.md
│
└── latency-{N}/
    ├── latency_report.json
    └── latency_report.md
```

---

## CLI Parameter Conventions

### Common Parameters

```bash
--evals         # path to evals.json
--skill-path    # path to SKILL.md
--output-dir    # output directory
--workers       # concurrency (default 6)
```

### Dimension-Specific Parameters

```bash
--dimensions quality,speed    # select evaluation dimensions (Phase 3.4)
--n-runs 5                    # speed dimension requires multiple runs
--models haiku,sonnet,opus    # model list
--step-level                  # deep speed analysis (Phase 3.5)
```

---

## Extension Points

### Adding a New Dimension

1. Add a new metrics dataclass to `EvalResult`
2. Collect data inside `spawn_eval()`
3. Add a corresponding section to the output report

### Adding a New Tool

1. Reuse the `spawn_eval()` core function
2. Implement dimension-specific analysis logic
3. Output JSON + Markdown conforming to the conventions above

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-03-17 | Initial design, single quality dimension |
| v0.3 | 2026-03-18 | Concurrent execution |
| v0.4 | 2026-03-18 | Three-dimension framework (Quality + Speed + Cost) |
| v0.5 | 2026-03-18 | Two-layer architecture (agent + scripts) |
