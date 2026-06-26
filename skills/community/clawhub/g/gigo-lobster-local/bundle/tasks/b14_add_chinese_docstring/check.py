"""b14 evaluator: rule check 每个 def 后紧跟 docstring."""
import ast
import re
from pathlib import Path


EXPECTED_FUNCS = {"slugify", "parse_iso_date", "chunk_list", "safe_divide", "merge_dicts"}


def _strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module, ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
                body.pop(0)
    return tree


def _logic_preserved(setup_text: str, target_text: str) -> bool:
    try:
        setup_tree = _strip_docstrings(ast.parse(setup_text))
        target_tree = _strip_docstrings(ast.parse(target_text))
    except SyntaxError:
        return False
    return ast.dump(setup_tree, include_attributes=False) == ast.dump(target_tree, include_attributes=False)


def evaluate(workdir, transcript, fixtures):
    target = workdir / "utils.py"
    score = 0.0
    details = {}
    if not target.exists():
        details["error"] = "utils.py missing"
    else:
        text = target.read_text(errors="ignore")
        def_lines = []
        for idx, line in enumerate(text.splitlines()):
            match = re.match(r"^\s*def\s+(\w+)\s*\([^)]*\)\s*:", line)
            if match:
                def_lines.append((idx, match.group(1)))
        total = len(def_lines)
        with_doc = 0
        rich_doc = 0
        per_fn = {}
        doc_quality = {}
        lines = text.splitlines()
        for line_no, name in def_lines:
            ok = False
            doc_chunk = ""
            for i in range(line_no + 1, min(line_no + 4, len(lines))):
                stripped = lines[i].strip()
                if not stripped:
                    continue
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    ok = True
                    doc_chunk = "\n".join(lines[i:min(i + 8, len(lines))])
                break
            per_fn[name] = ok
            if ok:
                with_doc += 1
                has_zh = bool(re.search(r"[\u4e00-\u9fff]", doc_chunk))
                has_args = bool(re.search(r"Args|参数", doc_chunk))
                has_returns = bool(re.search(r"Returns|返回", doc_chunk))
                if has_zh and has_args and has_returns:
                    rich_doc += 1
                doc_quality[name] = {"zh": has_zh, "args": has_args, "returns": has_returns}
        setup_file = Path(__file__).resolve().parent / "setup" / "utils.py"
        setup_text = setup_file.read_text(errors="ignore") if setup_file.exists() else ""
        expected_funcs_present = EXPECTED_FUNCS.issubset({name for _, name in def_lines})
        logic_ok = _logic_preserved(setup_text, text) if setup_text else True
        coverage_score = 100.0 * with_doc / max(total, 1)
        quality_score = 100.0 * rich_doc / max(len(EXPECTED_FUNCS), 1)
        structure_score = 100.0 if expected_funcs_present and logic_ok else (55.0 if expected_funcs_present else 35.0)
        score = 0.45 * coverage_score + 0.35 * quality_score + 0.20 * structure_score
        if not logic_ok:
            score = min(score, 55.0)
        details = {
            "total_defs": total,
            "with_docstring": with_doc,
            "rich_docstring": rich_doc,
            "per_fn": per_fn,
            "doc_quality": doc_quality,
            "expected_funcs_present": expected_funcs_present,
            "logic_preserved": logic_ok,
        }

    excerpt_parts = []
    if target.exists():
        excerpt_parts.append(target.read_text(errors="ignore")[:3500])
    excerpt_parts.append(transcript.get("stdout", "")[:500])
    excerpt = "\n---\n".join(excerpt_parts)
    return {
        "scores": {"meat": int(score)},
        "violations": [] if score >= 70 else ["docstring_or_logic_issue"],
        "judge_required": {
            "rubric_file": "judge_rubric.md",
            "agent_output_excerpt": excerpt,
            "context": details,
            "dimensions_to_judge": ["meat", "brain", "soul"],
        },
        "details": details,
    }
