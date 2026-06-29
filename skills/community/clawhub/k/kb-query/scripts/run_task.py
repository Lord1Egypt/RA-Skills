from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import catalog
import frontmatter
import gitea_api as g
import result_schema
import task_schema


INSUFFICIENT_ANSWER = "知识库中没有足够资料回答这个问题。"
GENERAL_FALLBACK = """以下是非知识库结论的一般性说明：

可以先补充与问题直接相关的 README、说明文档、会议记录、实验记录或论文摘要，再重新入库后查询。若问题涉及项目或代码，建议优先上传完整项目根目录，让知识库形成代码库总览页；若问题涉及论文或调研，建议上传原文、笔记和关键结论说明。"""
CATALOG_KEYS = ["documents", "concepts", "resources", "people", "projects", "reviews", "imports"]
STOP_WORDS = {
    "what", "when", "where", "which", "about", "does", "with", "from", "the", "and", "for",
    "请问", "什么", "哪些", "如何", "怎么", "是否", "这个", "问题", "一下", "请", "呢", "吗",
}


def read_task(args: argparse.Namespace) -> dict:
    if args.stdin:
        return json.load(sys.stdin)
    if args.task_json:
        return json.loads(Path(args.task_json).read_text(encoding="utf-8"))
    raise SystemExit("--stdin or --task-json is required")


def unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalize_path(path: str) -> str:
    clean = (path or "").replace("\\", "/").strip()
    clean = clean.lstrip("/")
    if "#" in clean:
        clean = clean.split("#", 1)[0]
    return clean


def question_terms(text: str) -> list[str]:
    tokens: set[str] = set()
    for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.-]*", text or ""):
        value = word.lower().strip("._-")
        if len(value) > 1 and value not in STOP_WORDS:
            tokens.add(value)
    for segment in re.findall(r"[\u4e00-\u9fff]+", text or ""):
        if segment not in STOP_WORDS and len(segment) >= 2:
            tokens.add(segment)
        for size in (2, 3, 4):
            if len(segment) < size:
                continue
            for index in range(0, len(segment) - size + 1):
                value = segment[index : index + size]
                if value not in STOP_WORDS:
                    tokens.add(value)
    return sorted(tokens, key=lambda item: (-len(item), item))


def is_identity_question(text: str) -> bool:
    lower = (text or "").lower()
    return any(
        marker in lower
        for marker in ["你是谁", "介绍一下自己", "介绍你自己", "你能做什么", "who are you", "what can you do"]
    )


def catalog_paths(cat: dict) -> list[str]:
    paths = []
    for key in CATALOG_KEYS:
        for item in cat.get(key, []) or []:
            if isinstance(item, dict):
                paths.append(normalize_path(item.get("file", "")))
    return unique(paths)


def index_paths(index_text: str) -> list[str]:
    paths = ["index.md"]
    for value in re.findall(r"\[\[([^\]|#]+)", index_text or ""):
        path = normalize_path(value)
        if path and not path.endswith(".md"):
            path += ".md"
        paths.append(path)
    for value in re.findall(r"\]\(([^)#]+\.md(?:#[^)]*)?)\)", index_text or ""):
        paths.append(normalize_path(value))
    return unique(paths)


def tree_paths(owner: str, repo: str) -> list[str]:
    paths = []
    try:
        for item in g.list_tree(owner, repo):
            path = normalize_path(str(item.get("path", "")))
            if item.get("type") == "blob" and path.endswith(".md") and not path.startswith("source_files/"):
                paths.append(path)
    except Exception:
        return []
    return unique(paths)


def heading_text(content: str) -> str:
    body = frontmatter.strip_frontmatter(content)
    return "\n".join(line.lstrip("#").strip() for line in body.splitlines() if line.lstrip().startswith("#"))


def score_candidate(terms: list[str], title: str, path: str, content: str) -> int:
    if not terms:
        return 0
    title_text = title.lower()
    path_text = path.lower()
    headings = heading_text(content).lower()
    body = frontmatter.strip_frontmatter(content).lower()
    score = 0
    for term in terms:
        lower = term.lower()
        if lower in title_text:
            score += 16
        if lower in path_text:
            score += 8
        if lower in headings:
            score += 6
        count = body.count(lower)
        if count:
            score += min(count, 4) * (3 if len(lower) >= 3 else 2)
    return score


def compact(text: str) -> str:
    cleaned = re.sub(r"^#+\s*", "", text or "", flags=re.MULTILINE)
    return re.sub(r"\s+", " ", cleaned).strip()


def best_snippet(content: str, terms: list[str], max_chars: int = 280) -> str:
    body = frontmatter.strip_frontmatter(content).strip()
    if not body:
        return ""
    lower = body.lower()
    positions = [lower.find(term.lower()) for term in terms if term and lower.find(term.lower()) >= 0]
    if positions:
        start = max(0, min(positions) - 80)
        end = min(len(body), start + max_chars)
        snippet = body[start:end]
    else:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        snippet = paragraphs[0] if paragraphs else body[:max_chars]
    return compact(snippet)[:max_chars]


def read_candidates(target: dict, question: str) -> list[dict]:
    owner = target["repoOwner"]
    repo = target["repoName"]
    repo_full = target.get("repoFullName", f"{owner}/{repo}")
    candidates: list[dict] = []
    cat = catalog.read(owner, repo)
    try:
        index_text = g.read_text(owner, repo, "index.md")
    except Exception:
        index_text = ""
    paths = unique(catalog_paths(cat) + index_paths(index_text) + tree_paths(owner, repo))
    if not paths:
        return []
    terms = question_terms(question)
    for path in paths[:240]:
        if not path.endswith(".md"):
            continue
        try:
            content = g.read_text(owner, repo, path)
        except Exception:
            continue
        title = frontmatter.parse_title(content, Path(path).stem)
        candidates.append({
            "score": score_candidate(terms, title, path, content),
            "kbType": target.get("kbType"),
            "repoFullName": repo_full,
            "path": path,
            "title": title,
            "content": content,
        })
    candidates.sort(key=lambda item: (item["score"], item["title"]), reverse=True)
    return candidates


def insufficient_payload(task: dict) -> dict:
    return {
        "answer": INSUFFICIENT_ANSWER + "\n\n" + GENERAL_FALLBACK,
        "citations": [],
        "usedScopes": unique([t.get("kbType", "") for t in task.get("kbTargets", [])]),
        "readPages": [],
    }


def run(task: dict) -> dict:
    errors = task_schema.validate_task(task)
    if errors:
        return result_schema.result(task, False, None, errors)

    question = task["payload"]["question"]
    terms = question_terms(question)
    max_citations = max(1, min(int(task["payload"].get("maxCitations", 8)), 12))
    all_candidates: list[dict] = []
    for target in task["kbTargets"]:
        try:
            all_candidates.extend(read_candidates(target, question))
        except Exception:
            continue

    all_candidates.sort(key=lambda item: (item["score"], item["title"]), reverse=True)
    selected = [item for item in all_candidates if item["score"] >= 3][:max_citations]
    if is_identity_question(question):
        identity_pages = [
            item for item in all_candidates
            if item["path"].lower() in {"readme.md", "agents.md", "index.md", "identity.md"}
        ]
        if identity_pages:
            selected = identity_pages[:max_citations]
    non_index_selected = [item for item in selected if item["path"].lower() != "index.md"]
    if non_index_selected:
        selected = non_index_selected[:max_citations]
    if not selected:
        return result_schema.result(task, True, insufficient_payload(task), [])

    citations = []
    read_pages = []
    answer_lines = ["根据知识库中已读页面，可以得到以下回答：", ""]
    for index, item in enumerate(selected, start=1):
        snippet = best_snippet(item["content"], terms)
        if not snippet:
            continue
        citations.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
            "snippet": snippet,
            "anchor": "",
        })
        read_pages.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
        })
        answer_lines.append(f"{index}. {item['title']}：{snippet}")

    if not citations:
        return result_schema.result(task, True, insufficient_payload(task), [])

    answer_lines.append("")
    answer_lines.append("以上内容只来自本次读取的知识库页面；来源清单见回答下方。")
    payload = {
        "answer": "\n".join(answer_lines),
        "citations": citations,
        "usedScopes": unique([t.get("kbType", "") for t in task.get("kbTargets", [])]),
        "readPages": read_pages,
    }
    return result_schema.result(task, True, payload, [])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--task-json", default="")
    args = parser.parse_args()
    print(json.dumps(run(read_task(args)), ensure_ascii=False))


if __name__ == "__main__":
    main()
