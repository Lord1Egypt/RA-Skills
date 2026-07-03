from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests


GITEA_URL = os.getenv("GITEA_URL", "").rstrip("/")
GITEA_TOKEN = os.getenv("GITEA_ADMIN_TOKEN", "")

STOP_WORDS = {
    "写", "一篇", "一份", "关于", "综述", "专项", "报告", "梳理", "总结", "对比",
    "研究", "缺口", "知识库", "资料", "方法", "有哪些", "什么", "一下", "请",
    "review", "survey", "literature", "about", "compare", "summarize",
}


def read_task(args: argparse.Namespace) -> dict:
    if args.stdin:
        return json.load(sys.stdin)
    if args.task_json:
        return json.loads(Path(args.task_json).read_text(encoding="utf-8"))
    raise SystemExit("--stdin or --task-json is required")


def result(task: dict, success: bool, payload: dict | None = None, errors: list[dict] | None = None) -> dict:
    return {
        "protocol": "research_kb_agent_result",
        "protocolVersion": "1.0",
        "taskId": task.get("taskId", ""),
        "taskType": task.get("taskType", "kb_literature_review"),
        "success": success,
        "result": payload,
        "errors": errors or [],
    }


def validate_task(task: dict) -> list[dict]:
    errors = []
    if task.get("protocol") != "research_kb_agent_task":
        errors.append({"code": "INVALID_PROTOCOL", "message": "protocol must be research_kb_agent_task"})
    if task.get("taskType") not in {"kb_query", "kb_literature_review"}:
        errors.append({"code": "INVALID_TASK_TYPE", "message": "taskType must be kb_query or kb_literature_review"})
    if not task.get("kbTargets"):
        errors.append({"code": "INVALID_KB_TARGETS", "message": "kbTargets is required"})
    if not (task.get("payload") or {}).get("question"):
        errors.append({"code": "MISSING_QUESTION", "message": "payload.question is required"})
    return errors


def headers() -> dict[str, str]:
    return {"Authorization": f"token {GITEA_TOKEN}", "Accept": "application/json", "Content-Type": "application/json"}


def gitea_api(method: str, path: str, *, json_body=None, ok=(200, 201, 204)) -> object:
    if not GITEA_URL or not GITEA_TOKEN:
        raise RuntimeError("GITEA_URL and GITEA_ADMIN_TOKEN are required")
    response = requests.request(method, f"{GITEA_URL}{path}", headers=headers(), json=json_body, timeout=60)
    if response.status_code not in ok:
        raise RuntimeError(f"Gitea {method} {path} failed: {response.status_code} {response.text[:300]}")
    return response.json() if response.text else {}


def repo_path(owner: str, repo: str) -> str:
    return f"{quote(owner, safe='')}/{quote(repo, safe='')}"


def content_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in path.split("/") if part)


def get_file(owner: str, repo: str, path: str) -> dict | None:
    try:
        return gitea_api("GET", f"/api/v1/repos/{repo_path(owner, repo)}/contents/{content_path(path)}?ref=main")
    except Exception as exc:
        if "404" in str(exc):
            return None
        raise


def read_text(owner: str, repo: str, path: str) -> str:
    data = get_file(owner, repo, path)
    if not data:
        return ""
    content = str(data.get("content", "")).replace("\n", "")
    return base64.b64decode(content).decode("utf-8")


def put_file(owner: str, repo: str, path: str, content: str, message: str) -> None:
    existing = get_file(owner, repo, path)
    body = {
        "branch": "main",
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }
    method = "POST"
    if existing and existing.get("sha"):
        method = "PUT"
        body["sha"] = existing["sha"]
    gitea_api(method, f"/api/v1/repos/{repo_path(owner, repo)}/contents/{content_path(path)}", json_body=body)


def list_tree(owner: str, repo: str) -> list[dict]:
    branch = gitea_api("GET", f"/api/v1/repos/{repo_path(owner, repo)}/branches/main")
    sha = branch["commit"]["id"]
    data = gitea_api("GET", f"/api/v1/repos/{repo_path(owner, repo)}/git/trees/{quote(sha, safe='')}?recursive=true")
    return data.get("tree", [])


def strip_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    return content[end + 4 :].lstrip() if end >= 0 else content


def parse_title(content: str, fallback: str) -> str:
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end >= 0:
            for line in content[3:end].splitlines():
                if line.strip().startswith("title:"):
                    return line.split(":", 1)[1].strip().strip('"') or fallback
    match = re.search(r"^#\s+(.+)$", strip_frontmatter(content), re.M)
    return match.group(1).strip() if match else fallback


def compact(text: str, limit: int = 320) -> str:
    value = re.sub(r"\s+", " ", text or "").strip()
    return value[:limit].rstrip()


def safe_name(value: str) -> str:
    invalid = set('<>:"|*\\')
    name = "".join("-" if ch in invalid else ch for ch in (value or "")).strip().strip(".")
    name = re.sub(r"\s+", " ", name)
    return name[:160] or "专项综述"


def topic_from(task: dict) -> str:
    payload = task.get("payload") or {}
    if payload.get("topic"):
        return safe_name(str(payload.get("topic")))
    question = str(payload.get("question") or "")
    about = re.search(r"关于(.+?)(?:的)?(?:专项综述|文献综述|知识综述|综述|报告|$)", question)
    if about and about.group(1).strip():
        return safe_name(about.group(1).strip())
    cleaned = question
    for pattern in [
        r"写(一篇|一份)?", r"做(一篇|一份)?", r"生成(一篇|一份)?", r"请", r"帮我",
        r"专项综述", r"综述", r"文献综述", r"知识综述", r"报告", r"梳理", r"总结",
        r"知识库里", r"基于.*?知识库", r"关于",
    ]:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.I)
    cleaned = re.sub(r"[，。！？!?：:；;、]+", " ", cleaned)
    candidates = [item for item in cleaned.split() if item and item not in STOP_WORDS]
    return safe_name(" ".join(candidates[:6]) or question[:40] or "专项综述")


def terms(text: str) -> list[str]:
    out: set[str] = set()
    for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.-]*", text or ""):
        value = word.lower().strip("._-")
        if len(value) > 1 and value not in STOP_WORDS:
            out.add(value)
    for segment in re.findall(r"[\u4e00-\u9fff]+", text or ""):
        if segment not in STOP_WORDS and len(segment) >= 2:
            out.add(segment)
        for size in (2, 3, 4):
            for index in range(max(0, len(segment) - size + 1)):
                value = segment[index : index + size]
                if value not in STOP_WORDS:
                    out.add(value)
    return sorted(out, key=lambda item: (-len(item), item))


def markdown_paths(owner: str, repo: str) -> list[str]:
    paths = []
    for item in list_tree(owner, repo):
        path = str(item.get("path", "")).replace("\\", "/").lstrip("/")
        if item.get("type") == "blob" and path.endswith(".md") and not path.startswith("source_files/"):
            paths.append(path)
    priority = {"reviews": 0, "concepts": 1, "summaries": 2, "resources": 3}
    return sorted(set(paths), key=lambda p: (priority.get(p.split("/", 1)[0], 9), p))


def score_page(page_terms: list[str], title: str, path: str, body: str) -> int:
    title_l = title.lower()
    path_l = path.lower()
    headings = "\n".join(line.lstrip("#").strip() for line in body.splitlines() if line.lstrip().startswith("#")).lower()
    body_l = body.lower()
    score = 0
    for term in page_terms:
        lower = term.lower()
        if lower in title_l:
            score += 18
        if lower in path_l:
            score += 9
        if lower in headings:
            score += 7
        score += min(body_l.count(lower), 5) * 2
    if path.startswith("reviews/") or path.startswith("concepts/"):
        score += 3
    return score


def read_candidates(task: dict, topic: str) -> list[dict]:
    page_terms = terms(topic + " " + str((task.get("payload") or {}).get("question", "")))
    candidates = []
    for target in task.get("kbTargets") or []:
        owner = target["repoOwner"]
        repo = target["repoName"]
        repo_full = target.get("repoFullName", f"{owner}/{repo}")
        try:
            paths = markdown_paths(owner, repo)[:300]
        except Exception:
            continue
        for path in paths:
            try:
                content = read_text(owner, repo, path)
            except Exception:
                continue
            body = strip_frontmatter(content)
            title = parse_title(content, Path(path).stem)
            score = score_page(page_terms, title, path, body)
            if score <= 0:
                continue
            candidates.append({
                "score": score,
                "kbType": target.get("kbType"),
                "repoFullName": repo_full,
                "repoOwner": owner,
                "repoName": repo,
                "path": path,
                "title": title,
                "content": content,
            })
    candidates.sort(key=lambda item: (item["score"], item["title"]), reverse=True)
    return candidates[:14]


def snippet(content: str, page_terms: list[str], limit: int = 280) -> str:
    body = strip_frontmatter(content)
    lower = body.lower()
    positions = [lower.find(term.lower()) for term in page_terms if term and lower.find(term.lower()) >= 0]
    if positions:
        start = max(0, min(positions) - 90)
        return compact(body[start : start + limit], limit)
    parts = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    return compact(parts[0] if parts else body, limit)


def classify_methods(candidates: list[dict]) -> list[str]:
    buckets: dict[str, int] = {}
    rules = {
        "模型与算法路线": ["model", "algorithm", "方法", "模型", "算法", "framework"],
        "系统与工程实现": ["system", "architecture", "代码", "实现", "部署", "工程", "service"],
        "实验与评测": ["experiment", "evaluation", "benchmark", "实验", "评测", "指标", "baseline"],
        "数据与资源": ["dataset", "data", "resource", "数据", "资源", "语料"],
        "应用场景": ["application", "case", "scenario", "应用", "场景", "用例"],
    }
    for item in candidates:
        text = (item["title"] + "\n" + strip_frontmatter(item["content"])[:4000]).lower()
        for label, keys in rules.items():
            if any(key.lower() in text for key in keys):
                buckets[label] = buckets.get(label, 0) + 1
    if not buckets:
        return ["主题资料综述"]
    return [label for label, _count in sorted(buckets.items(), key=lambda item: (-item[1], item[0]))[:5]]


def source_line(item: dict) -> str:
    return f"- `{item['path']}`：{item['title']}。{snippet(item['content'], terms(item['title']), 180)}"


def generate_review(task: dict, topic: str, candidates: list[dict]) -> tuple[str, str, list[str]]:
    now = datetime.now(timezone.utc).astimezone().isoformat()
    title = f"{topic} 专项综述"
    method_groups = classify_methods(candidates)
    key_sources = candidates[:8]
    source_lines = "\n".join(source_line(item) for item in key_sources)
    method_lines = "\n".join(f"- {group}：由本次读取资料中的相关标题、章节和摘要线索归纳。" for group in method_groups)
    gap_hints = []
    for item in key_sources:
        body = strip_frontmatter(item["content"])
        for line in body.splitlines():
            line_clean = compact(line.strip(" #-"), 220)
            if any(key in line_clean.lower() for key in ["limitation", "future", "gap", "risk", "局限", "不足", "未来", "缺口", "风险"]):
                gap_hints.append(f"- {line_clean}（来源：{item['title']}）")
                break
        if len(gap_hints) >= 5:
            break
    if not gap_hints:
        gap_hints = ["- 本次读取页面中没有形成明确、可交叉验证的研究缺口；建议继续补充相关论文、实验记录或项目评测。"]

    md = f"""---
title: "{title}"
type: "literature_review"
createdAt: "{now}"
generatedBy: "openclaw"
sources:
  []
---

# {title}

## 综述范围

本综述只基于所选知识库中本次读取的 {len(key_sources)} 个相关页面，主题为「{topic}」。

## 领域概述

从已有资料看，该主题目前主要围绕以下资料展开：  
{source_lines}

## 主流方法分类

{method_lines}

## 优势与局限

- 优势：知识库中已有资料能够提供若干可复用的概念、项目或实验线索，可作为继续阅读和方案选择的入口。
- 局限：本次综合依赖已入库页面的覆盖范围；未入库或未被读取的材料不会出现在结论中。

## 矛盾与争议

本次脚本没有发现可以可靠归纳的明确冲突结论。若需要更细的争议分析，建议补充对比实验、失败案例和方法评测材料后重新生成。

## 研究缺口 / 尚未解决的问题

{chr(10).join(gap_hints)}

## 对所选知识库上下文的启示

1. 优先阅读和补全本综述列出的核心来源页面。
2. 对方法类资料，应进一步补充实验设置、评价指标和失败案例。
3. 对项目类资料，应进一步补充环境复现记录和适配成本。

## 已综合的库内资料

{source_lines}
"""
    summary = [
        f"本次围绕「{topic}」综合了 {len(key_sources)} 个知识库页面。",
        f"主要方法/资料类别：{'、'.join(method_groups)}。",
        "研究缺口：" + compact("；".join(line.lstrip("- ") for line in gap_hints), 260),
    ]
    return title, md, summary


def write_review(task: dict, title: str, md: str) -> str:
    target = (task.get("kbTargets") or [])[0]
    owner = target["repoOwner"]
    repo = target["repoName"]
    path = f"reviews/{safe_name(title)}.md"
    put_file(owner, repo, path, md, f"research-kb literature review: {title} [{task.get('taskId')}]")
    return path


def run(task: dict) -> dict:
    errors = validate_task(task)
    if errors:
        return result(task, False, None, errors)

    topic = topic_from(task)
    candidates = read_candidates(task, topic)
    scopes = [target.get("kbType", "") for target in task.get("kbTargets", [])]
    if len(candidates) < 2:
        payload = {
            "answer": f"知识库中关于「{topic}」的资料还不够支撑一篇专项综述。当前只找到 {len(candidates)} 个相关页面；建议先补充更多论文、项目说明、实验记录或调研材料，再重新生成。",
            "citations": [],
            "usedScopes": scopes,
            "readPages": [],
            "mode": "literature_review",
            "generatedPage": "",
        }
        return result(task, True, payload, [])

    title, md, summary = generate_review(task, topic, candidates)
    generated_path = ""
    write_error = ""
    options = (task.get("payload") or {}).get("options") or {}
    if options.get("writeReview", True):
        try:
            generated_path = write_review(task, title, md)
        except Exception as exc:
            write_error = f"综述写入失败：{exc}"

    citations = []
    read_pages = []
    if generated_path:
        first = (task.get("kbTargets") or [])[0]
        citations.append({
            "kbType": first.get("kbType"),
            "repoFullName": first.get("repoFullName"),
            "path": generated_path,
            "title": title,
            "snippet": "；".join(summary),
            "anchor": "",
        })
        read_pages.append({
            "kbType": first.get("kbType"),
            "repoFullName": first.get("repoFullName"),
            "path": generated_path,
            "title": title,
        })

    page_terms = terms(topic)
    for item in candidates[:8]:
        citations.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
            "snippet": snippet(item["content"], page_terms),
            "anchor": "",
        })
        read_pages.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
        })

    answer_lines = [
        f"已生成《{title}》。" if generated_path else f"已完成《{title}》草稿，但没有写入知识库。",
        "",
        *summary,
        "",
        "详细来源见下方来源清单。",
    ]
    if write_error:
        answer_lines.append(write_error)

    payload = {
        "answer": "\n".join(answer_lines),
        "citations": citations,
        "usedScopes": scopes,
        "readPages": read_pages,
        "mode": "literature_review",
        "generatedPage": generated_path,
    }
    return result(task, True, payload, [])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--task-json", default="")
    args = parser.parse_args()
    print(json.dumps(run(read_task(args)), ensure_ascii=False))


if __name__ == "__main__":
    main()
