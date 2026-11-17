import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

from catalog import catalog_from_raw
from gitea_api import GiteaClient
from utils import read_text_limited, repo_slug, safe_relpath, sha256_text, slugify, unique


SCP_LIKE = re.compile(r"^[^@]+@([^:]+):(.+)$")
HTTP_CREDENTIALS = re.compile(r"(https?://)([^/@:\s]+):([^/@\s]+)@")

IMPORTANT_FILENAMES = {
    "readme.md",
    "readme.rst",
    "readme.txt",
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "go.mod",
    "cargo.toml",
    "composer.json",
    "gemfile",
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "makefile",
    ".env.example",
    "application.yml",
    "application.yaml",
    "application.properties",
}

TEXT_EXTENSIONS = {
    ".c", ".cc", ".cfg", ".clj", ".cpp", ".cs", ".css", ".dockerfile", ".env",
    ".go", ".gradle", ".graphql", ".h", ".hpp", ".html", ".java", ".js", ".json",
    ".jsx", ".kt", ".lock", ".md", ".mjs", ".php", ".properties", ".py", ".rb",
    ".rs", ".rst", ".scss", ".sh", ".sql", ".swift", ".toml", ".ts", ".tsx",
    ".txt", ".vue", ".xml", ".yaml", ".yml",
}

IGNORED_PARTS = {".git", ".idea", ".next", ".nuxt", ".venv", "build", "coverage", "dist", "node_modules", "target", "vendor"}


def prepare_context(payload):
    source = payload.get("source") or {}
    config = source.get("config") or {}
    repo_url = config.get("repoUrl") or source.get("repoUrl") or source.get("name") or ""
    if not repo_url:
        raise ValueError("Missing source.config.repoUrl")

    slug = repo_slug(repo_url)
    code_path = f"code/{slug}.md"
    previous = _previous_commit(source)
    clone_url = _credentialized_url(repo_url)
    remote = _ls_remote_head(clone_url)
    remote_latest = remote.get("latestCommit") or ""
    remote_branch = config.get("defaultBranch") or remote.get("defaultBranch") or ""

    if previous and remote_latest and previous == remote_latest:
        return {
            "mode": "skip",
            "repo": {
                "url": repo_url,
                "slug": slug,
                "codePagePath": code_path,
                "worktree": "",
                "defaultBranch": remote_branch,
                "latestCommit": remote_latest,
                "previousCommit": previous,
                "fileCount": 0,
                "topLevel": [],
                "languageProfile": {},
                "changedFiles": [],
                "changedModules": [],
                "diffSummary": "",
                "importantFiles": [],
            },
            "samples": [],
            "existingKb": {},
            "resultHints": {
                "codePagePath": code_path,
                "primaryPageRoots": ["code/", "concepts/", "resources/"],
                "allowedWikiRoots": ["overview/", "projects/", "papers/", "code/", "meetings/", "experiments/", "tech-notes/", "surveys/", "notes/", "concepts/", "resources/", "qa/"],
                "knowledgeGraphRule": "Before writing pages.json, make a private graph plan: code page first, then decide whether existing overview/project/concept/resource/other pages should be updated. Concepts are stable reusable abstractions from the repository; resources are concrete reusable dependencies, APIs, services, datasets, tools, or external systems; overview pages are navigation or synthesis pages for projects, systems, themes, or research areas. Do not force a page when evidence is weak, but do not skip an update when it would materially improve navigation or reuse.",
                "linkingRule": "Use relatedConcepts, relatedResources, relatedCodePages, and relatedPages to express catalog edges. relatedPages is for ordinary wiki page links such as overview/, projects/, papers/, surveys/, meetings/, experiments/, tech-notes/, notes/, and qa/. Also include explanatory wikilinks in the Markdown body.",
                "validateCommand": "python3 scripts/run_task.py validate-pages --input <payload.json> --context <context.json> --pages <pages.json>",
                "applyCommand": "python3 scripts/run_task.py apply --input <payload.json> --context <context.json> --pages <pages.json>",
            },
            "skipResult": {
                "processedSources": [repo_url],
                "skippedSources": ["仓库提交未变化"],
                "commitId": "",
                "snapshot": {
                    "repoUrl": repo_url,
                    "latestCommit": remote_latest,
                    "defaultBranch": remote_branch,
                    "changedModules": [],
                },
                "sourceItems": [
                    _repo_source_item(
                        source,
                        repo_url,
                        slug,
                        remote_latest,
                        remote_branch,
                        f"source_files/gitea_repo/{source.get('id') or payload.get('sourceId') or 'unknown'}-{slug}.md",
                        {"mode": "skip", "reason": "unchanged_commit"},
                    )
                ],
            },
        }

    work_root = _work_root(payload)
    repo_dir = work_root / "repo"
    _reset_dir(work_root)
    work_root.mkdir(parents=True, exist_ok=True)
    _clone_repo(clone_url, repo_dir)

    latest = _git(["rev-parse", "HEAD"], repo_dir)
    default_branch = _default_branch(repo_dir, config) or remote_branch
    files = _list_files(repo_dir)
    changed = _changed_files(repo_dir, previous, latest)
    changed_modules = _changed_modules(changed)

    return {
        "mode": "scan",
        "repo": {
            "url": repo_url,
            "slug": slug,
            "codePagePath": code_path,
            "worktree": str(repo_dir),
            "defaultBranch": default_branch,
            "latestCommit": latest,
            "previousCommit": previous,
            "fileCount": len(files),
            "topLevel": _top_level(files),
            "languageProfile": _language_profile(files),
            "changedFiles": changed,
            "changedModules": changed_modules,
            "diffSummary": _diff_summary(repo_dir, previous, latest),
            "importantFiles": _important_files(files),
            "largeRepository": len(files) > 250,
        },
        "samples": _collect_samples(repo_dir, files, changed, len(files)),
        "analysisLimits": _analysis_limits(len(files)),
        "existingKb": _existing_kb(payload, code_path, source.get("id") or payload.get("sourceId")),
        "resultHints": {
            "codePagePath": code_path,
            "primaryPageRoots": ["code/", "concepts/", "resources/"],
            "allowedWikiRoots": ["overview/", "projects/", "papers/", "code/", "meetings/", "experiments/", "tech-notes/", "surveys/", "notes/", "concepts/", "resources/", "qa/"],
            "knowledgeGraphRule": "Before writing pages.json, make a private graph plan: code page first, then decide whether existing overview/project/concept/resource/other pages should be updated. Concepts are stable reusable abstractions from the repository; resources are concrete reusable dependencies, APIs, services, datasets, tools, or external systems; overview pages are navigation or synthesis pages for projects, systems, themes, or research areas. Do not force a page when evidence is weak, but do not skip an update when it would materially improve navigation or reuse.",
            "linkingRule": "Use relatedConcepts, relatedResources, relatedCodePages, and relatedPages to express catalog edges. relatedPages is for ordinary wiki page links such as overview/, projects/, papers/, surveys/, meetings/, experiments/, tech-notes/, notes/, and qa/. Also include explanatory wikilinks in the Markdown body.",
            "validateCommand": "python3 scripts/run_task.py validate-pages --input <payload.json> --context <context.json> --pages <pages.json>",
            "applyCommand": "python3 scripts/run_task.py apply --input <payload.json> --context <context.json> --pages <pages.json>",
        },
    }


def _work_root(payload):
    shared = payload.get("sharedDir") or os.getenv("OPENCLAW_SHARED_DIR") or tempfile.gettempdir()
    task_id = slugify(payload.get("taskId") or sha256_text(str(payload))[:16])
    return Path(shared).expanduser().resolve() / "repo_ingest" / task_id


def _repo_source_item(source, repo_url, slug, latest_commit="", default_branch="", archived_path="", metadata=None):
    source_id = source.get("id") or ""
    item_identity = source_id or sha256_text(repo_url)[:16]
    return {
        "itemKey": f"gitea_repo:{item_identity}",
        "title": source.get("name") or slug or repo_url,
        "sourceKind": "gitea_repo",
        "kind": "repository",
        "status": "ingested",
        "sha256": latest_commit or "",
        "originalPath": repo_url,
        "archivedPath": archived_path,
        "url": repo_url,
        "externalId": latest_commit or repo_url,
        "metadata": {
            "repoUrl": repo_url,
            "repoSlug": slug,
            "defaultBranch": default_branch or "",
            "latestCommit": latest_commit or "",
            **(metadata or {}),
        },
    }


def _reset_dir(path):
    resolved = Path(path).resolve()
    if not resolved.name or resolved.anchor == str(resolved):
        raise ValueError(f"Refusing to clean unsafe path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def _git(args, cwd=None, timeout=120):
    command = ["git"] + list(args)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        env=env,
    )
    if completed.returncode != 0:
        error = completed.stderr or completed.stdout or "git command failed"
        raise RuntimeError(_redact_git_output(error.strip()))
    return completed.stdout.strip()


def _redact_git_output(text):
    redacted = str(text or "")
    token = os.getenv("GITEA_BOT_TOKEN") or ""
    username = os.getenv("GITEA_BOT_USERNAME") or ""
    if token:
        redacted = redacted.replace(token, "<redacted-token>")
    if username:
        redacted = redacted.replace(urllib.parse.quote(username, safe=""), "<redacted-user>")
    return HTTP_CREDENTIALS.sub(r"\1<redacted-user>:<redacted-token>@", redacted)


def _ls_remote_head(repo_url):
    try:
        output = _git(["ls-remote", "--symref", repo_url, "HEAD"], timeout=45)
    except Exception as exc:
        text = str(exc)
        if "schannel" in text.lower() or "sec_e_no_credentials" in text.lower() or "acquirecredentialshandle" in text.lower():
            output = _git(["-c", "http.sslBackend=openssl", "ls-remote", "--symref", repo_url, "HEAD"], timeout=45)
        else:
            raise
    default_branch = ""
    latest = ""
    for line in output.splitlines():
        if line.startswith("ref: refs/heads/") and line.endswith("\tHEAD"):
            default_branch = line[len("ref: refs/heads/"):-len("\tHEAD")]
        elif line.endswith("\tHEAD"):
            latest = line.split()[0]
    return {"defaultBranch": default_branch, "latestCommit": latest}


def _clone_repo(repo_url, target):
    attempts = [["clone", "--depth", "80", "--filter=blob:none", repo_url, str(target)], ["clone", "--depth", "80", repo_url, str(target)]]
    last_error = ""
    for args in attempts:
        try:
            return _git(args, timeout=300)
        except Exception as exc:
            last_error = str(exc)
            if target.exists():
                shutil.rmtree(target)
    if "schannel" in last_error.lower() or "sec_e_no_credentials" in last_error.lower() or "acquirecredentialshandle" in last_error.lower():
        return _git(["-c", "http.sslBackend=openssl"] + attempts[-1], timeout=300)
    raise RuntimeError(_redact_git_output(last_error))


def _credentialized_url(repo_url):
    gitea_base = (os.getenv("GITEA_URL") or "").rstrip("/")
    parsed_gitea = urllib.parse.urlparse(gitea_base)
    configured_host = (parsed_gitea.hostname or "").lower()
    repo_host = _repo_host(repo_url).lower()
    if not configured_host or repo_host != configured_host:
        return repo_url
    token = os.getenv("GITEA_BOT_TOKEN") or ""
    username = os.getenv("GITEA_BOT_USERNAME") or "oauth2"
    if not token:
        return repo_url
    http_url = _to_configured_gitea_http_url(repo_url, gitea_base)
    parsed = urllib.parse.urlparse(http_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return repo_url
    if parsed.username:
        return http_url
    auth = f"{urllib.parse.quote(username, safe='')}:{urllib.parse.quote(token, safe='')}"
    return urllib.parse.urlunparse(parsed._replace(netloc=f"{auth}@{parsed.netloc}"))


def _repo_host(repo_url):
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.hostname:
        return parsed.hostname
    match = SCP_LIKE.match(repo_url)
    return match.group(1) if match else ""


def _to_configured_gitea_http_url(repo_url, gitea_base):
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.scheme in {"http", "https"}:
        return repo_url
    if parsed.scheme == "ssh" and parsed.hostname:
        repo_path = parsed.path.lstrip("/")
        return f"{gitea_base}/{repo_path}"
    match = SCP_LIKE.match(repo_url)
    if match:
        return f"{gitea_base}/{match.group(2).lstrip('/')}"
    return repo_url


def _default_branch(repo_dir, config):
    configured = config.get("defaultBranch") or ""
    if configured:
        return configured
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo_dir)
    return "" if branch == "HEAD" else branch


def _previous_commit(source):
    snapshot = source.get("lastSnapshot") or source.get("last_snapshot") or {}
    if isinstance(snapshot, dict):
        return snapshot.get("latestCommit") or snapshot.get("commit") or ""
    return ""


def _list_files(repo_dir):
    output = _git(["ls-tree", "-r", "--name-only", "HEAD"], repo_dir)
    return [safe_relpath(line) for line in output.splitlines() if line.strip()]


def _changed_files(repo_dir, previous, latest):
    if not previous or previous == latest:
        return []
    try:
        _git(["cat-file", "-e", f"{previous}^{{commit}}"], repo_dir)
    except Exception:
        try:
            _git(["fetch", "--depth", "1", "origin", previous], repo_dir, timeout=180)
        except Exception:
            return []
    try:
        output = _git(["diff", "--name-status", previous, latest], repo_dir, timeout=180)
    except Exception:
        return []
    changed = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            changed.append({"status": parts[0], "path": parts[-1]})
    return changed


def _diff_summary(repo_dir, previous, latest):
    if not previous or previous == latest:
        return ""
    try:
        return _git(["diff", "--stat", previous, latest], repo_dir, timeout=180)[:12000]
    except Exception:
        return ""


def _changed_modules(changed):
    modules = []
    for item in changed or []:
        path = item.get("path") or ""
        modules.append(path.split("/", 1)[0] if "/" in path else path)
    return unique(modules)[:50]


def _top_level(files):
    roots = []
    for path in files:
        roots.append(path.split("/", 1)[0] if "/" in path else path)
    return unique(sorted(roots))[:80]


def _language_profile(files):
    counts = {}
    for path in files:
        suffix = Path(path).suffix.lower() or "(no extension)"
        counts[suffix] = counts.get(suffix, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20])


def _important_files(files):
    selected = []
    for path in files:
        name = Path(path).name.lower()
        lowered = path.lower()
        if name in IMPORTANT_FILENAMES or lowered.startswith(".github/workflows/"):
            selected.append(path)
    return selected[:80]


def _analysis_limits(file_count):
    large = file_count > 250
    return {
        "largeRepository": large,
        "maxAdditionalFilesToRead": 16 if large else 48,
        "maxPages": 5 if large else 14,
        "maxConceptPages": 2 if large else 6,
        "maxResourcePages": 2 if large else 6,
        "maxPageContentChars": 6000 if large else 14000,
        "guidance": "Use sampled evidence and inspect only a small set of high-signal files; do not read the full worktree or generate exhaustive file-by-file pages." if large else "Use samples first, then inspect only files needed to explain the repository accurately.",
    }


def _collect_samples(repo_dir, files, changed, file_count=0):
    large = file_count > 250
    max_candidates = 28 if large else 45
    max_total_chars = 50000 if large else 90000
    max_sample_chars = 4000 if large else 6000
    candidates = []
    important = _important_files(files)
    changed_paths = [item.get("path") for item in changed or [] if item.get("path")]
    for path in important + changed_paths:
        if _should_sample(path):
            candidates.append(path)
    for path in files:
        if len(candidates) >= max_candidates:
            break
        if _should_sample(path) and _looks_structural(path):
            candidates.append(path)

    samples = []
    total = 0
    for path in unique(candidates):
        if total >= max_total_chars:
            break
        content = read_text_limited(repo_dir / path, max_chars=max_sample_chars)
        if not content.strip():
            continue
        samples.append({"path": path, "chars": len(content), "content": content})
        total += len(content)
    return samples


def _should_sample(path):
    parts = set(str(path).replace("\\", "/").split("/"))
    if parts & IGNORED_PARTS:
        return False
    suffix = Path(path).suffix.lower()
    name = Path(path).name.lower()
    return suffix in TEXT_EXTENSIONS or name in IMPORTANT_FILENAMES


def _looks_structural(path):
    lowered = path.lower()
    parts = lowered.split("/")
    if len(parts) <= 2:
        return True
    return any(part in {"src", "app", "lib", "server", "backend", "frontend", "api", "routes", "controllers", "services", "models", "tests", "test"} for part in parts)


def _existing_kb(payload, code_path, source_id):
    client = GiteaClient(payload)
    raw_catalog = client.read_text("catalog.json")
    catalog = catalog_from_raw(raw_catalog)
    related_pages = []
    source_id_text = str(source_id or "")
    for page in catalog.get("pages") or []:
        path = page.get("path") or ""
        if path == code_path or code_path in (page.get("relatedCodePages") or []) or source_id_text in {str(item) for item in (page.get("sourceIds") or [])}:
            related_pages.append(page)
    return {"catalogPageCount": len(catalog.get("pages") or []), "relatedPages": related_pages[:80], "existingCodePage": client.read_text(code_path)[:30000]}
