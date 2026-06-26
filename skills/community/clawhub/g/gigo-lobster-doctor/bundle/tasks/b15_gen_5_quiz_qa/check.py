"""b15 evaluator: 检查 stdout 含 ## 题目 1 .. ## 题目 5"""
import re


def evaluate(workdir, transcript, fixtures):
    response = transcript.get("stdout", "")
    found = []
    missing = []
    option_blocks = 0
    answer_blocks = 0
    explanation_blocks = 0
    for n in range(1, 6):
        if re.search(rf"##\s*题目\s*{n}\b", response):
            found.append(n)
        else:
            missing.append(n)
        block_match = re.search(rf"##\s*题目\s*{n}\b(.*?)(?=##\s*题目\s*{n + 1}\b|$)", response, re.S)
        block = block_match.group(1) if block_match else ""
        if all(re.search(rf"(?m)^{letter}\.\s+", block) for letter in "ABCD"):
            option_blocks += 1
        if re.search(r"\*\*答案：\*\*\s*[A-D]", block):
            answer_blocks += 1
        if re.search(r"\*\*解析：\*\*\s*.{6,}", block):
            explanation_blocks += 1
    score = 0.35 * (100.0 * len(found) / 5) + 0.3 * (100.0 * option_blocks / 5) + 0.2 * (100.0 * answer_blocks / 5) + 0.15 * (100.0 * explanation_blocks / 5)
    excerpt = response[:4000]
    return {
        "scores": {"meat": int(score)},
        "violations": [] if not missing else [f"missing_q{n}" for n in missing],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": {"found_questions": found, "missing": missing, "option_blocks": option_blocks, "answer_blocks": answer_blocks, "explanation_blocks": explanation_blocks},
            "dimensions_to_judge": ["meat", "brain"],
        },
        "details": {"found": found, "missing": missing, "option_blocks": option_blocks, "answer_blocks": answer_blocks, "explanation_blocks": explanation_blocks},
    }
