# Report schema

## Markdown report

Use this order. Omit empty optional sections.

```markdown
# Static Prompt Benchmark

## Verdict
- Universal quality: NN/100 (confidence)
- Target-model compatibility: NN/100 or Not assessed
- Production readiness: Ready / Conditional / Not ready
- Dynamic evaluation: Not run
- One-sentence conclusion

## Evaluation context
- Task type
- Intended use
- Target model(s)
- Assumptions

## Scorecard
| Module | Score | Weight | Confidence | Main reason |

## Priority findings
### [Severity] Finding title
- Status
- Evidence
- Impact
- Recommendation
- Confidence

## Detailed checks
### General quality
### Structure and format
### Few-shot quality
### Safety and robustness
### Target-model compatibility

## Cross-model compatibility
Compatibility matrix and portability recommendations.

## Recommended next actions
Numbered by leverage, not by document order.

## Improved prompt
Optional. State that it is not runtime validated.

## Measurement boundary
List unmeasured runtime metrics and, when useful, a proposed dynamic test plan.
```

## Readiness labels

- **Ready:** no critical or major unresolved findings; assumptions are acceptable for intended use.
- **Conditional:** usable after named changes or only under explicit assumptions.
- **Not ready:** critical issue, core contradiction, invalid contract, unsafe behavior, or inadequate information for the intended high-risk use.

## JSON report

When JSON is requested, return a single object:

```json
{
  "benchmark_type": "static",
  "universal_score": 0,
  "confidence": "medium",
  "readiness": "conditional",
  "target_models": [],
  "assumptions": [],
  "modules": [
    {
      "id": "general_quality",
      "score": 0,
      "weight": 0,
      "confidence": "medium",
      "criteria": [
        {
          "id": "goal_clarity",
          "status": "warning",
          "score": 2,
          "max_score": 4,
          "evidence": "",
          "impact": "",
          "recommendation": ""
        }
      ]
    }
  ],
  "findings": [
    {
      "severity": "major",
      "status": "fail",
      "title": "",
      "evidence": "",
      "impact": "",
      "recommendation": "",
      "confidence": "high",
      "primary_module": ""
    }
  ],
  "cross_model": [
    {
      "model": "",
      "exact_version_known": false,
      "static_compatibility_score": null,
      "portability_risk": "unknown",
      "confidence": "low",
      "required_changes": [],
      "unverified_capabilities": []
    }
  ],
  "dynamic_metrics": {
    "status": "not_run",
    "accuracy": null,
    "hallucination_rate": null,
    "format_compliance_rate": null,
    "latency": null,
    "token_usage": null,
    "cost": null,
    "consistency": null
  }
}
```

Use `null`, not estimated numbers, for unmeasured runtime metrics.
