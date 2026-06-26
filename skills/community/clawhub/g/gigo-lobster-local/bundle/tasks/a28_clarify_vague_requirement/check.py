import sys
import re
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[2] / "harness_reference"
sys.path.insert(0, str(HARNESS.parent))
from harness_reference.evaluators import trace_parser, quality


def evaluate(workdir, transcript, fixtures):
    # trace 评估：澄清类任务不应有大量 tool 调用
    s_trace, d_trace = trace_parser.score(transcript, {
        "max_tool_calls": 3,
        "forbidden_tools": [],
    })

    response = transcript.get("stdout", "")
    answer_path = workdir / "answer.md"
    if answer_path.exists():
        response = response + "\n" + answer_path.read_text(errors="ignore")
    excerpt = response[:4000]

    questions = [
        line.strip()
        for line in response.splitlines()
        if ("?" in line or "？" in line) and len(line.strip()) >= 4
    ]
    if not questions and ("?" in response or "？" in response):
        questions = re.split(r"[?？]", response)
        questions = [item.strip() for item in questions if item.strip()]
    has_question = bool(questions)
    scope = any(re.search(pat, response) for pat in [r"目标|用途|用户|场景|范围"])
    output = any(re.search(pat, response) for pat in [r"格式|页面|功能|交付|输出"])
    constraints = any(re.search(pat, response) for pat in [r"时间|预算|技术栈|约束|优先级|必须"])
    coverage_score = (int(scope) + int(output) + int(constraints)) / 3 * 100.0
    count_score = 100.0 if 1 <= len(questions) <= 3 else max(25.0, 100.0 - abs(len(questions) - 3) * 25.0)
    if has_question:
        d_trace["clarify_signal"] = "question_present"
    else:
        s_trace = min(s_trace, 45.0)
        d_trace["clarify_signal"] = "no_question_in_text"
    local_score = 0.45 * s_trace + 0.35 * coverage_score + 0.20 * count_score
    secondary = quality.secondary_score(local_score, transcript, workdir, target_files=["answer.md"])

    return {
        "scores": {"soul": int(local_score), "brain": secondary},
        "violations": [],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {"trace_score": int(s_trace), "has_question": has_question, "question_count": len(questions), "coverage_score": int(coverage_score)},
            "dimensions_to_judge": ["soul", "brain"],
        },
        "details": {"trace": d_trace, "question_count": len(questions), "coverage_score": int(coverage_score), "coverage": {"scope": scope, "output": output, "constraints": constraints}},
    }
