#!/usr/bin/env python3
"""Validate and render an AI-authored novel review; never performs the review."""
import argparse
import json
import math
import sys
from pathlib import Path

DIMENSIONS = ["开篇与钩子", "人物与动机", "冲突与节奏", "情节与因果", "场景与表达", "原创与完成度"]
STATUSES = {"complete", "needs_review", "needs_more_source"}


def reject_nonfinite(value: str):
    raise ValueError(f"invalid_json: 不允许 NaN 或 Infinity（{value}）")


def parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        reject_nonfinite(value)
    return parsed


def validate_review(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("invalid_review: 顶层必须是 JSON 对象")
    if data.get("status") == "scaffold":
        raise ValueError("scaffold_not_review: 占位 scaffold 不能作为审稿结果")
    if data.get("status") not in STATUSES:
        raise ValueError("invalid_status: status 必须是 complete、needs_review 或 needs_more_source")
    if data["status"] == "needs_more_source":
        if not isinstance(data.get("message"), str) or not data["message"].strip():
            raise ValueError("invalid_review: needs_more_source 必须说明缺少什么材料")
        return data
    dims = data.get("dimensions")
    if not isinstance(dims, list) or len(dims) != 6 or any(not isinstance(x, dict) for x in dims) or [x.get("dimension") for x in dims] != DIMENSIONS:
        raise ValueError("invalid_review: 必须按规定提供六个审稿维度")
    if data["status"] == "complete" and any(x.get("status") != "reviewed" or x.get("score") is None for x in dims):
        raise ValueError("invalid_review: 六项均须完成且有分数才能标记 complete")
    for item in dims:
        score = item.get("score")
        if item.get("status") not in {"reviewed", "needs_review"}:
            raise ValueError(f"invalid_review: {item['dimension']} 必须标记 reviewed 或 needs_review")
        if score is None:
            if item["status"] != "needs_review":
                raise ValueError(f"invalid_review: {item['dimension']} 未评分时必须标记 needs_review")
        elif not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 10 or not math.isfinite(score):
            raise ValueError(f"invalid_review: {item['dimension']} 分数必须在 0-10 或 null")
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"invalid_review: {item['dimension']} 缺少证据或待确认说明")
        for ev in evidence:
            if not isinstance(ev, dict) or not isinstance(ev.get("text"), str) or not ev["text"].strip() or not isinstance(ev.get("location"), str) or not ev["location"].strip():
                raise ValueError(f"invalid_review: {item['dimension']} 的每条证据须含 text 和 location")
        if not isinstance(item.get("impact"), str) or not item["impact"].strip():
            raise ValueError(f"invalid_review: {item['dimension']} 缺少阅读影响")
        suggestions = item.get("suggestions")
        if not isinstance(suggestions, list):
            raise ValueError(f"invalid_review: {item['dimension']} suggestions 必须是数组")
        for suggestion in suggestions:
            if not isinstance(suggestion, dict) or not all(isinstance(suggestion.get(key), str) and suggestion[key].strip() for key in ("priority", "action", "verify")):
                raise ValueError(f"invalid_review: {item['dimension']} 修改建议须含 priority、action、verify")
    scores = [x["score"] for x in dims]
    expected = round(sum(scores) / len(scores), 2) if all(score is not None for score in scores) else None
    average = data.get("average")
    if average is not None and (not isinstance(average, (int, float)) or isinstance(average, bool) or not 0 <= average <= 10 or not math.isfinite(average)):
        raise ValueError("invalid_review: average 必须是有限数值或 null")
    if average != expected:
        raise ValueError(f"invalid_review: average 应为 {expected if expected is not None else 'null（至少一项未评分）'}")
    for key in ("work", "scope", "audience", "version"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"invalid_review: 缺少 {key}")
    for key in ("pending_questions", "top_actions"):
        values = data.get(key)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f"invalid_review: {key} 必须是非空字符串数组")
    if data["status"] == "complete" and any(x["status"] != "reviewed" or x["score"] is None for x in dims):
        raise ValueError("invalid_review: 六项均须完成且有分数才能标记 complete")
    return data


def render(data: dict) -> str:
    if data["status"] == "needs_more_source":
        return "# 小说审稿\n\n状态：needs_more_source\n\n" + data["message"] + "\n"
    average = f"{data['average']}/10" if data["average"] is not None else "未评分（至少一项待确认）"
    lines = [f"# 小说审稿：{data['work']}", "", f"- 范围：{data['scope']}", f"- 目标读者：{data['audience']}", f"- 版本：{data['version']}", f"- 状态：{data['status']}", f"- 六维平均分：{average}", ""]
    for item in data["dimensions"]:
        score = f"{item['score']}/10" if item["score"] is not None else "未评分"
        lines += [f"## {item['dimension']}：{score}（{item['status']}）", "", f"影响：{item['impact']}", "", "证据："]
        lines += [f"- {ev['location']}：{ev['text']}" for ev in item["evidence"]]
        lines += ["", "修改建议："]
        lines += [f"- [{s['priority']}] {s['action']}；验证：{s['verify']}" for s in item["suggestions"]]
        if not item["suggestions"]: lines.append("- 暂无；先补齐待确认信息。")
        lines.append("")
    lines += ["## 待确认", ""] + ([f"- {x}" for x in data["pending_questions"]] or ["- 无"])
    lines += ["", "## 优先动作", ""] + ([f"{i}. {x}" for i, x in enumerate(data["top_actions"], 1)] or ["- 暂无"])
    lines += ["", "> 评分为基于所给文本的编辑意见，不预测签约、收益或平台结果。"]
    return "\n".join(lines) + "\n"


def write_outputs(data: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    payloads = {
        out / "review.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        out / "review.md": render(data),
    }
    created = []
    try:
        for path, contents in payloads.items():
            with path.open("x", encoding="utf-8") as stream:
                created.append(path)
                stream.write(contents)
    except FileExistsError as exc:
        for path in created:
            path.unlink(missing_ok=True)
        raise ValueError("output_exists: 输出目录已有 review.json 或 review.md；请换新目录") from exc
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description="校验并排版 AI 已完成的审稿 JSON；本脚本不分析小说文本。")
    subs = parser.add_subparsers(dest="cmd", required=True)
    subs.add_parser("self-test")
    p = subs.add_parser("render"); p.add_argument("--input", required=True); p.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.cmd == "self-test":
        import unittest
        suite = unittest.defaultTestLoader.discover(str(Path(__file__).parents[1] / "tests"))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if result.wasSuccessful() else 1
    try:
        source = Path(args.input)
        data = validate_review(json.loads(source.read_text(encoding="utf-8"), parse_constant=reject_nonfinite, parse_float=parse_finite_float))
        out = Path(args.output)
        write_outputs(data, out)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr); return 1
    print("校验通过，已排版 AI 审稿结果：review.md 和 review.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
