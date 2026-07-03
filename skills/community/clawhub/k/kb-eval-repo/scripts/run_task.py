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
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

STOP_WORDS = {
    "github", "repo", "repository", "project", "评估", "分析", "一下", "这个", "项目",
    "开源", "有用", "有没有", "是否", "帮我", "看看", "能不能", "复现", "环境",
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
        "taskType": task.get("taskType", "kb_eval_repo"),
        "success": success,
        "result": payload,
        "errors": errors or [],
    }


def validate_task(task: dict) -> list[dict]:
    errors = []
    if task.get("protocol") != "research_kb_agent_task":
        errors.append({"code": "INVALID_PROTOCOL", "message": "protocol must be research_kb_agent_task"})
    if task.get("taskType") not in {"kb_query", "kb_eval_repo"}:
        errors.append({"code": "INVALID_TASK_TYPE", "message": "taskType must be kb_query or kb_eval_repo"})
    if not task.get("kbTargets"):
        errors.append({"code": "INVALID_KB_TARGETS", "message": "kbTargets is required"})
    if not (task.get("payload") or {}).get("question"):
        errors.append({"code": "MISSING_QUESTION", "message": "payload.question is required"})
    return errors


def gh_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "research-kb"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def gitea_headers() -> dict[str, str]:
    return {"Authorization": f"token {GITEA_TOKEN}", "Accept": "application/json", "Content-Type": "application/json"}


def gitea_api(method: str, path: str, *, json_body=None, ok=(200, 201, 204)) -> object:
    if not GITEA_URL or not GITEA_TOKEN:
        raise RuntimeError("GITEA_URL and GITEA_ADMIN_TOKEN are required")
    response = requests.request(method, f"{GITEA_URL}{path}", headers=gitea_headers(), json=json_body, timeout=60)
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
                    value = line.split(":", 1)[1].strip().strip('"')
                    return value or fallback
    first_heading = re.search(r"^#\s+(.+)$", strip_frontmatter(content), re.M)
    return first_heading.group(1).strip() if first_heading else fallback


def compact(text: str, limit: int = 300) -> str:
    value = re.sub(r"\s+", " ", text or "").strip()
    return value[:limit].rstrip()


def safe_name(value: str) -> str:
    invalid = set('<>:"|*\\')
    name = "".join("-" if ch in invalid else ch for ch in (value or "")).strip().strip(".")
    name = re.sub(r"\s+", " ", name)
    return name[:160] or "repo-evaluation"


def extract_repo_ref(task: dict) -> tuple[str, str, str] | None:
    payload = task.get("payload") or {}
    text = " ".join(str(item or "") for item in [payload.get("repoUrl"), payload.get("question")])
    match = re.search(r"github\.com[:/]+([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/?#\s]|$)", text)
    if not match:
        match = re.search(r"(?<![\w.-])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?![\w.-])", text)
    if not match:
        return None
    owner, repo = match.group(1), match.group(2).removesuffix(".git")
    return owner, repo, f"https://github.com/{owner}/{repo}"


def github_get(url: str) -> dict | list | str:
    response = requests.get(url, headers=gh_headers(), timeout=30)
    if response.status_code == 404:
        raise RuntimeError("GitHub repository or file was not found")
    if response.status_code == 403:
        raise RuntimeError("GitHub rate limit or access restriction hit; configure GITHUB_TOKEN and retry")
    response.raise_for_status()
    if "application/json" in response.headers.get("content-type", ""):
        return response.json()
    return response.text


def fetch_github(owner: str, repo: str) -> dict:
    meta = github_get(f"https://api.github.com/repos/{owner}/{repo}")
    if not isinstance(meta, dict):
        raise RuntimeError("GitHub returned an invalid repository response")
    branch = str(meta.get("default_branch") or "main")
    wanted = [
        "README.md", "readme.md", "README.rst",
        "requirements.txt", "pyproject.toml", "environment.yml", "setup.py",
        "package.json", "pnpm-lock.yaml", "yarn.lock",
        "Dockerfile", "docker-compose.yml", "Makefile",
        "pom.xml", "build.gradle", "Cargo.toml", "go.mod",
    ]
    files = []
    combined = [f"# {owner}/{repo}", "", compact(str(meta.get("description") or ""), 800), ""]
    for name in wanted:
        try:
            item = github_get(f"https://api.github.com/repos/{owner}/{repo}/contents/{quote(name)}?ref={quote(branch)}")
            if isinstance(item, dict) and item.get("download_url"):
                text = requests.get(item["download_url"], headers=gh_headers(), timeout=30).text
                files.append(name)
                combined += [f"\n\n## {name}\n", text[:20000]]
        except Exception:
            continue
    return {
        "fullName": f"{owner}/{repo}",
        "url": str(meta.get("html_url") or f"https://github.com/{owner}/{repo}"),
        "description": str(meta.get("description") or ""),
        "language": str(meta.get("language") or ""),
        "stars": int(meta.get("stargazers_count") or 0),
        "forks": int(meta.get("forks_count") or 0),
        "openIssues": int(meta.get("open_issues_count") or 0),
        "pushedAt": str(meta.get("pushed_at") or ""),
        "license": ((meta.get("license") or {}).get("spdx_id") if isinstance(meta.get("license"), dict) else "") or "未声明",
        "archived": bool(meta.get("archived")),
        "topics": meta.get("topics") or [],
        "defaultBranch": branch,
        "filesFound": files,
        "text": "\n".join(combined),
    }


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


def normalize_path(path: str) -> str:
    clean = (path or "").replace("\\", "/").strip().lstrip("/")
    return clean.split("#", 1)[0]


def tree_markdown_paths(owner: str, repo: str) -> list[str]:
    paths = []
    for item in list_tree(owner, repo):
        path = normalize_path(str(item.get("path", "")))
        if item.get("type") == "blob" and path.endswith(".md") and not path.startswith("source_files/"):
            paths.append(path)
    return sorted(set(paths))


def read_candidates(targets: list[dict], query_terms: list[str], extra_terms: list[str]) -> list[dict]:
    candidates = []
    all_terms = query_terms + extra_terms
    for target in targets:
        owner = target["repoOwner"]
        repo = target["repoName"]
        repo_full = target.get("repoFullName", f"{owner}/{repo}")
        try:
            paths = tree_markdown_paths(owner, repo)[:260]
        except Exception:
            continue
        for path in paths:
            try:
                content = read_text(owner, repo, path)
            except Exception:
                continue
            body = strip_frontmatter(content)
            title = parse_title(content, Path(path).stem)
            score = score_page(all_terms, title, path, body)
            if score <= 0 and not path.startswith("summaries/codebases/"):
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
    return candidates[:12]


def score_page(query_terms: list[str], title: str, path: str, body: str) -> int:
    haystacks = [title.lower(), path.lower(), body.lower()]
    score = 0
    for term in query_terms:
        lower = term.lower()
        if lower in haystacks[0]:
            score += 12
        if lower in haystacks[1]:
            score += 6
        count = haystacks[2].count(lower)
        score += min(count, 5) * 2
    return score


def snippet(content: str, query_terms: list[str], limit: int = 280) -> str:
    body = strip_frontmatter(content)
    lower = body.lower()
    positions = [lower.find(term.lower()) for term in query_terms if term and lower.find(term.lower()) >= 0]
    if positions:
        start = max(0, min(positions) - 80)
        return compact(body[start : start + limit], limit)
    parts = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
    return compact(parts[0] if parts else body, limit)


def has_any(text: str, words: list[str]) -> bool:
    lower = (text or "").lower()
    return any(word.lower() in lower for word in words)


def evaluate(repo: dict | None, candidates: list[dict], question: str) -> dict:
    repo_text = repo.get("text", "") if repo else ""
    kb_text = "\n".join(strip_frontmatter(item["content"])[:2500] for item in candidates[:8])
    question_terms = terms(question)
    overlap = sum(1 for term in question_terms if term.lower() in (repo_text + "\n" + kb_text).lower())
    relevance = min(10, max(1, 2 + overlap + min(len(candidates), 4)))
    if candidates and any(item["score"] >= 10 for item in candidates):
        relevance = max(relevance, 7)
    if repo and repo.get("description") and any(term in repo["description"].lower() for term in question_terms):
        relevance = max(relevance, 6)

    dep_files = repo.get("filesFound", []) if repo else []
    reproducible = bool(dep_files) and has_any(repo_text, ["install", "quickstart", "usage", "pip install", "npm install", "docker", "安装", "运行"])
    risky_env = []
    if repo and repo.get("archived"):
        risky_env.append("仓库已归档")
    if not dep_files:
        risky_env.append("未检测到明确依赖/环境文件")
    if has_any(repo_text, ["cuda", "gpu", "ros", "isaac", "mujoco", "pybullet"]):
        risky_env.append("可能依赖 GPU/仿真器/特定硬件环境")
    if repo and repo.get("license") == "未声明":
        risky_env.append("许可证未声明")

    stale = False
    if repo and repo.get("pushedAt"):
        try:
            pushed_year = int(str(repo["pushedAt"])[:4])
            stale = datetime.now(timezone.utc).year - pushed_year >= 3
        except Exception:
            stale = False
    if stale:
        risky_env.append("最近维护时间较久")

    if relevance <= 3:
        verdict = "暂不建议"
        reason = "与当前选择的知识库上下文交集较弱，投入产出不明确。"
    elif reproducible and not repo.get("archived") if repo else relevance >= 7:
        verdict = "值得深入"
        reason = "相关性较高，且仓库材料提供了可复现或可快速理解的工程线索。"
    else:
        verdict = "选择性参考"
        reason = "有一定相关价值，但环境、维护或资料完整度存在不确定性。"

    return {
        "relevance": relevance,
        "verdict": verdict,
        "reason": reason,
        "dependencyFiles": dep_files,
        "risks": risky_env,
        "reproducible": reproducible,
    }


def report_markdown(task: dict, repo: dict | None, evaluation: dict, candidates: list[dict]) -> tuple[str, str]:
    payload = task.get("payload") or {}
    question = payload.get("question", "")
    repo_name = repo.get("fullName") if repo else safe_name(question)
    title = f"{repo_name} 开源项目评估"
    now = datetime.now(timezone.utc).astimezone().isoformat()
    source_items = "\n".join(f"- `{item['path']}`：{item['title']}" for item in candidates[:8]) or "- 知识库暂无直接关联页面。"
    repo_meta = "未提供 GitHub 仓库。"
    if repo:
        repo_meta = (
            f"{repo['fullName']}｜语言 {repo.get('language') or '-'}｜Stars {repo.get('stars')}｜"
            f"最近提交 {repo.get('pushedAt') or '-'}｜许可证 {repo.get('license')}"
        )
    md = f"""---
title: "{title}"
type: "repo_evaluation"
createdAt: "{now}"
generatedBy: "openclaw"
sources:
  []
---

# {title}

## 用户问题

{question}

## 项目概况

{repo_meta}

## 结论：{evaluation['verdict']}

{evaluation['reason']}

## 相关性

评分：{evaluation['relevance']}/10。

本评分基于项目材料与所选知识库页面之间的关键词、主题和用途重叠，是初筛判断，不代表实际运行验证。

## 复现与环境

- 检测到的依赖/配置文件：{', '.join(evaluation['dependencyFiles']) if evaluation['dependencyFiles'] else '未检测到明确依赖/配置文件'}
- 复现风险：{'; '.join(evaluation['risks']) if evaluation['risks'] else '暂未发现明显复现风险'}

## 与知识库已有资料的关系

{source_items}

## 建议动作

1. 先阅读 README、依赖文件和示例入口，确认安装路径。
2. 对照知识库中相关页面，判断它更适合作为 baseline、工具库、数据资源还是思路参考。
3. 若涉及 GPU、ROS、仿真器或特定硬件，先做最小样例复现，不要直接投入完整实验。
"""
    return title, md


def write_report(task: dict, title: str, md: str) -> str:
    target = (task.get("kbTargets") or [])[0]
    owner = target["repoOwner"]
    repo = target["repoName"]
    path = f"reviews/{safe_name(title)}.md"
    put_file(owner, repo, path, md, f"research-kb repo evaluation: {title} [{task.get('taskId')}]")
    return path


def run(task: dict) -> dict:
    errors = validate_task(task)
    if errors:
        return result(task, False, None, errors)

    payload = task.get("payload") or {}
    question = str(payload.get("question", ""))
    repo_ref = extract_repo_ref(task)
    repo = None
    fetch_error = ""
    extra = []
    if repo_ref:
        owner, name, _url = repo_ref
        extra = [owner.lower(), name.lower(), f"{owner}/{name}".lower()]
        try:
            repo = fetch_github(owner, name)
        except Exception as exc:
            fetch_error = str(exc)

    query_terms = terms(question)
    candidates = read_candidates(task.get("kbTargets") or [], query_terms, extra)
    if not repo and not candidates:
        payload_out = {
            "answer": "我需要一个 GitHub 仓库链接或明确的开源项目名，才能评估它是否对你有用。请把 `https://github.com/owner/repo` 发给我，并说明你想从复现、方法参考还是工程复用哪个角度评估。",
            "citations": [],
            "usedScopes": [target.get("kbType", "") for target in task.get("kbTargets", [])],
            "readPages": [],
            "mode": "repo_evaluation",
            "generatedPage": "",
        }
        return result(task, True, payload_out, [])

    evaluation = evaluate(repo, candidates, question)
    title, md = report_markdown(task, repo, evaluation, candidates)
    generated_path = ""
    options = payload.get("options") or {}
    if options.get("writeReview", True):
        try:
            generated_path = write_report(task, title, md)
        except Exception as exc:
            fetch_error = (fetch_error + "; " if fetch_error else "") + f"评估报告写入失败：{exc}"

    citations = []
    read_pages = []
    if generated_path:
        first = (task.get("kbTargets") or [])[0]
        citations.append({
            "kbType": first.get("kbType"),
            "repoFullName": first.get("repoFullName"),
            "path": generated_path,
            "title": title,
            "snippet": f"{evaluation['verdict']}：{evaluation['reason']}",
            "anchor": "",
        })
        read_pages.append({
            "kbType": first.get("kbType"),
            "repoFullName": first.get("repoFullName"),
            "path": generated_path,
            "title": title,
        })
    for item in candidates[:6]:
        citations.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
            "snippet": snippet(item["content"], query_terms + extra),
            "anchor": "",
        })
        read_pages.append({
            "kbType": item["kbType"],
            "repoFullName": item["repoFullName"],
            "path": item["path"],
            "title": item["title"],
        })

    repo_line = ""
    if repo:
        repo_line = f"{repo['fullName']}（{repo.get('language') or '-'}｜Stars {repo.get('stars')}｜最近提交 {repo.get('pushedAt') or '-'}）"
    elif fetch_error:
        repo_line = f"GitHub 抓取失败：{fetch_error}"
    answer = "\n".join([
        f"结论：{evaluation['verdict']}",
        "",
        evaluation["reason"],
        "",
        f"项目：{repo_line or '未提供可抓取的 GitHub 仓库，以下主要依据知识库相关页面判断。'}",
        f"相关性：{evaluation['relevance']}/10",
        f"环境与复现：{'; '.join(evaluation['risks']) if evaluation['risks'] else '暂未发现明显环境风险；仍建议先做最小样例验证。'}",
        f"与知识库关系：已参考 {len(candidates)} 个相关页面。" if candidates else "与知识库关系：暂未找到直接相关页面。",
        "",
        "说明：这是基于 GitHub 仓库材料和所选知识库页面的初筛评估，不代表已经实际安装或运行。",
        "来源清单见回答下方。" if citations else "",
    ]).strip()

    payload_out = {
        "answer": answer,
        "citations": citations,
        "usedScopes": [target.get("kbType", "") for target in task.get("kbTargets", [])],
        "readPages": read_pages,
        "mode": "repo_evaluation",
        "generatedPage": generated_path,
    }
    return result(task, True, payload_out, [])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--task-json", default="")
    args = parser.parse_args()
    print(json.dumps(run(read_task(args)), ensure_ascii=False))


if __name__ == "__main__":
    main()
