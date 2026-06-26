import sys
import re
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import state_hash


def evaluate(workdir, transcript, fixtures):
    s_hash, d_hash = state_hash.score(workdir, {
        "files": ["output.md"],
        "required_patterns": [r"(?m)^#\s+"],
    })
    # 检查 heading 数 ≥3
    out = workdir / "output.md"
    heading_count = 0
    if out.exists():
        for line in out.read_text(errors="ignore").splitlines():
            if line.lstrip().startswith("#"):
                heading_count += 1
    if heading_count < 3:
        s_hash *= 0.5
    text = out.read_text(errors="ignore") if out.exists() else ""
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    code_fence_ok = text.count("```") >= 2 if text else False
    flag_preserved = "--" in text
    rule_score = s_hash
    if zh_chars < 80:
        rule_score *= 0.55
    if not code_fence_ok:
        rule_score *= 0.75
    if not flag_preserved:
        rule_score *= 0.85
    response = transcript.get("stdout", "")
    excerpt = (out.read_text(errors="ignore")[:3500] if out.exists() else "") + "\n---\n" + response[:500]
    return {
        "scores": {"meat": int(rule_score)},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {"heading_count": heading_count, "zh_chars": zh_chars, "code_fence_ok": code_fence_ok, "flag_preserved": flag_preserved},
            "dimensions_to_judge": ["meat", "brain", "soul"],
        },
        "details": {"state_hash": d_hash, "heading_count": heading_count, "zh_chars": zh_chars, "code_fence_ok": code_fence_ok, "flag_preserved": flag_preserved},
    }
