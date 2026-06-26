"""b16 evaluator: 校验 bug_report.json schema."""
import json
import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import state_hash  # noqa: E402

REQUIRED_FIELDS = {"title", "severity", "steps", "expected", "actual"}
VALID_SEVERITY = {"P0", "P1", "P2", "P3"}


def evaluate(workdir, transcript, fixtures):
    target = workdir / "bug_report.json"
    score = 0.0
    violations = []
    schema_details = {}
    excerpt = ""

    s_hash, d_hash = state_hash.score(workdir, {"files": ["bug_report.json"]})

    if not target.exists():
        violations.append("bug_report.json missing")
        schema_details = {"error": "file missing"}
    else:
        raw = target.read_text(errors="ignore")
        excerpt = raw[:3500]
        try:
            data = json.loads(raw)
            score = 100.0
            missing = REQUIRED_FIELDS - set(data.keys())
            if missing:
                score -= 20 * len(missing)
                violations.append(f"missing_fields:{sorted(missing)}")
            sev = data.get("severity")
            if sev not in VALID_SEVERITY:
                score -= 15
                violations.append(f"invalid_severity:{sev}")
            steps = data.get("steps")
            if not isinstance(steps, list) or len(steps) < 2:
                score -= 20
                violations.append("steps_invalid")
            title = str(data.get("title", ""))
            if len(title) > 30 or not re.search(r"PDF|导出|网络异常|转圈", title):
                score -= 12
                violations.append("title_weak")
            expected = str(data.get("expected", ""))
            actual = str(data.get("actual", ""))
            joined_steps = "\n".join(str(item) for item in steps) if isinstance(steps, list) else ""
            evidence_hits = sum([
                bool(re.search(r"Chrome|Windows|lihua@hengda\.cn", joined_steps)),
                bool(re.search(r"PDF", joined_steps + title + actual)),
                bool(re.search(r"Word", actual + joined_steps)),
                bool(re.search(r"5|6|五|六|多次|连续", actual + joined_steps)),
                bool(re.search(r"30s|30 秒|合理时间|下载", expected)),
            ])
            if sev != "P1":
                score -= 12
                violations.append("severity_not_p1")
            if evidence_hits < 4:
                score -= (4 - evidence_hits) * 8
                violations.append(f"weak_feedback_evidence:{evidence_hits}")
            score = max(0.0, score)
            schema_details = {
                "fields": sorted(data.keys()),
                "severity": sev,
                "steps_count": len(steps) if isinstance(steps, list) else 0,
                "title_length": len(title),
                "evidence_hits": evidence_hits,
            }
        except json.JSONDecodeError as e:
            violations.append(f"json_decode_error:{e}")
            score = 0.0
            schema_details = {"error": str(e)}

    excerpt = excerpt + "\n---\n" + transcript.get("stdout", "")[:500]
    return {
        "scores": {"meat": int(score)},
        "violations": violations,
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": schema_details,
            "dimensions_to_judge": ["meat", "brain"],
        },
        "details": {"schema": schema_details, "state_hash": d_hash},
    }
