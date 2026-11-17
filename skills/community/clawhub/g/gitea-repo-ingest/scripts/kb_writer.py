import json

from catalog import catalog_entry, catalog_from_raw, merge_catalog, render_index
from gitea_api import GiteaClient
from utils import extract_keywords, now, safe_relpath, sha256_text, slugify, strip_frontmatter, unique


KB_PAGE_ROOTS = {
    "overview",
    "projects",
    "papers",
    "code",
    "meetings",
    "experiments",
    "tech-notes",
    "surveys",
    "notes",
    "concepts",
    "resources",
    "qa",
}

TYPE_BY_ROOT = {
    "overview": "overview",
    "projects": "project",
    "papers": "paper",
    "code": "code",
    "meetings": "meeting",
    "experiments": "experiment",
    "tech-notes": "tech-note",
    "surveys": "survey",
    "notes": "note",
    "concepts": "concept",
    "resources": "resource",
    "qa": "qa",
}
RELATION_FIELDS = (
    ("relatedConcepts", "相关概念"),
    ("relatedResources", "相关资源"),
    ("relatedCodePages", "相关代码页"),
    ("relatedPages", "相关页面"),
)


def apply_pages(payload, pages_doc, context=None):
    validate_pages_doc(payload, pages_doc, context)
    pages = pages_doc.get("pages") or pages_doc.get("createdPages") or pages_doc.get("updatedPages") or []
    if not pages:
        raise ValueError("Missing pages[] in generated pages JSON")

    client = GiteaClient(payload)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    created = []
    updated = []
    entries = []
    commit = ""
    repo_meta = (context or {}).get("repo") or {}

    for page in pages:
        path = validate_page_path(page.get("path"))
        page["path"] = path
        page.setdefault("type", type_from_path(path))
        page.setdefault("title", title_from_page(page))
        page.setdefault("sourceIds", source_ids(payload, page))
        page.setdefault("keywords", extract_keywords((page.get("title") or "") + "\n" + (page.get("content") or "")))
        for key in ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            page[key] = normalize_relation_paths(page.get(key) or [])
        content = build_page_content(payload, page, repo_meta)
        page["contentHash"] = sha256_text(strip_frontmatter(content))
        existed = client.exists(path)
        client.upsert_text(path, content, f"OpenClaw update {path}")
        commit = client.last_commit
        entry = catalog_entry(page)
        entries.append(entry)
        target = updated if existed else created
        target.append(entry)

    source_manifest_path = write_source_manifest(client, payload, repo_meta, created + updated)
    commit = client.last_commit
    repo_source_item = source_item_result(payload, repo_meta, source_manifest_path, created + updated)

    catalog = merge_catalog(catalog, entries)
    client.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "OpenClaw update catalog.json")
    commit = client.last_commit
    client.upsert_text("index.md", render_index(catalog), "OpenClaw update index.md")
    commit = client.last_commit

    repo_url = repo_meta.get("url") or repo_url_from_payload(payload)
    snapshot = pages_doc.get("snapshot") or {
        "repoUrl": repo_url,
        "latestCommit": repo_meta.get("latestCommit") or "",
        "defaultBranch": repo_meta.get("defaultBranch") or "",
        "changedModules": repo_meta.get("changedModules") or [],
    }
    return {
        "processedSources": [repo_url],
        "createdPages": created,
        "updatedPages": updated,
        "archivedFiles": [source_manifest_path] if source_manifest_path else [],
        "skippedSources": [],
        "errors": [],
        "commitId": commit,
        "snapshot": snapshot,
        "sourceItems": [repo_source_item],
    }


def validate_pages_doc(payload, pages_doc, context=None):
    pages = pages_doc.get("pages") or pages_doc.get("createdPages") or pages_doc.get("updatedPages") or []
    if not isinstance(pages, list) or not pages:
        raise ValueError("Missing pages[] in generated pages JSON")

    limits = (context or {}).get("analysisLimits") or {}
    max_pages = int_value(limits.get("maxPages"))
    max_concepts = int_value(limits.get("maxConceptPages"))
    max_resources = int_value(limits.get("maxResourcePages"))
    max_content_chars = int_value(limits.get("maxPageContentChars"))
    errors = []
    concept_count = 0
    resource_count = 0

    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            errors.append(f"pages[{index}] must be an object")
            continue
        try:
            path = validate_page_path(page.get("path"))
        except Exception as exc:
            errors.append(f"pages[{index}].path: {exc}")
            continue
        root = path.split("/", 1)[0]
        if root == "concepts":
            concept_count += 1
        if root == "resources":
            resource_count += 1
        if not (page.get("title") or "").strip():
            errors.append(f"pages[{index}] {path}: missing title")
        content = page.get("content") or page.get("body") or ""
        if not isinstance(content, str) or not content.strip():
            errors.append(f"pages[{index}] {path}: missing content")
        if max_content_chars and isinstance(content, str) and len(content) > max_content_chars:
            errors.append(f"pages[{index}] {path}: content exceeds maxPageContentChars={max_content_chars}")

    if max_pages and len(pages) > max_pages:
        errors.append(f"pages[] has {len(pages)} pages, exceeds maxPages={max_pages}")
    if max_concepts and concept_count > max_concepts:
        errors.append(f"concept pages count {concept_count} exceeds maxConceptPages={max_concepts}")
    if max_resources and resource_count > max_resources:
        errors.append(f"resource pages count {resource_count} exceeds maxResourcePages={max_resources}")
    if errors:
        raise ValueError("; ".join(errors[:20]))
    return {
        "success": True,
        "pageCount": len(pages),
        "errors": [],
        "limits": {
            "maxPages": max_pages,
            "maxConceptPages": max_concepts,
            "maxResourcePages": max_resources,
            "maxPageContentChars": max_content_chars,
        },
    }


def validate_page_path(path):
    value = safe_relpath(path)
    if not value.endswith(".md"):
        raise ValueError(f"Page path must end with .md: {path}")
    root = value.split("/", 1)[0]
    if root not in KB_PAGE_ROOTS:
        raise ValueError(
            "gitea_repo_ingest can only write normal KB wiki pages. "
            f"Allowed roots: {', '.join(sorted(KB_PAGE_ROOTS))}. Got: {path}"
        )
    return value


def type_from_path(path):
    root = str(path or "").split("/", 1)[0]
    return TYPE_BY_ROOT.get(root, root or "wiki")


def title_from_page(page):
    path = page.get("path") or "page"
    label = path.rsplit("/", 1)[-1].replace(".md", "")
    prefix = {
        "code": "代码库",
        "concept": "概念",
        "resource": "资源",
        "project": "项目",
        "paper": "论文",
        "meeting": "会议",
        "experiment": "实验",
        "tech-note": "技术笔记",
        "survey": "综述",
        "qa": "问答",
    }.get(page.get("type") or type_from_path(path), "页面")
    return f"{prefix}：{label}"


def source_ids(payload, page):
    source = payload.get("source") or {}
    value = page.get("sourceIds") or [source.get("id") or payload.get("sourceId")]
    return unique([item for item in value if item not in (None, "")])


def normalize_relation_paths(values):
    result = []
    for raw in values or []:
        value = raw
        if isinstance(raw, dict):
            value = raw.get("path") or raw.get("target") or raw.get("href") or ""
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value.startswith("[[") and "]]" in value:
            value = value[2:value.find("]]")]
        if "|" in value:
            value = value.split("|", 1)[0].strip()
        if not value:
            continue
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        try:
            path = safe_relpath(value)
        except ValueError:
            continue
        root = path.split("/", 1)[0]
        if root not in KB_PAGE_ROOTS or path.startswith("source_files/") or "/" not in path:
            continue
        result.append(path)
    return unique(result)


def repo_url_from_payload(payload):
    source = payload.get("source") or {}
    config = source.get("config") or {}
    return config.get("repoUrl") or source.get("repoUrl") or source.get("name") or ""


def source_block(payload, repo_meta):
    source = payload.get("source") or {}
    return {
        "sourceId": source.get("id") or payload.get("sourceId") or "",
        "sourceType": "gitea_repo",
        "title": source.get("name") or repo_meta.get("slug") or "",
        "url": repo_meta.get("url") or repo_url_from_payload(payload),
        "commitHash": repo_meta.get("latestCommit") or "",
        "branch": repo_meta.get("defaultBranch") or "",
        "scannedAt": now(),
    }


def source_item_result(payload, repo_meta, archived_path="", page_entries=None):
    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or ""
    repo_url = repo_meta.get("url") or repo_url_from_payload(payload)
    slug = repo_meta.get("slug") or slugify(repo_url)
    item_identity = source_id or sha256_text(repo_url)[:16]
    latest_commit = repo_meta.get("latestCommit") or ""
    return {
        "itemKey": f"gitea_repo:{item_identity}",
        "title": source.get("name") or slug or repo_url,
        "sourceKind": "gitea_repo",
        "kind": "repository",
        "status": "ingested",
        "sha256": latest_commit,
        "originalPath": repo_url,
        "archivedPath": archived_path,
        "url": repo_url,
        "externalId": latest_commit or repo_url,
        "metadata": {
            "repoUrl": repo_url,
            "repoSlug": slug,
            "defaultBranch": repo_meta.get("defaultBranch") or "",
            "latestCommit": latest_commit,
            "previousCommit": repo_meta.get("previousCommit") or "",
            "fileCount": repo_meta.get("fileCount") or 0,
            "topLevel": repo_meta.get("topLevel") or [],
            "languageProfile": repo_meta.get("languageProfile") or {},
            "changedModules": repo_meta.get("changedModules") or [],
            "importantFiles": repo_meta.get("importantFiles") or [],
            "generatedPages": [entry.get("path") for entry in page_entries or [] if entry.get("path")],
        },
    }


def build_page_content(payload, page, repo_meta):
    body = strip_frontmatter(page.get("content") or page.get("body") or "")
    title = page.get("title") or title_from_page(page)
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}".strip()
    body = append_relation_section(body, page)

    data = {
        "id": page.get("id") or page.get("path", "").replace("/", "-").replace(".md", ""),
        "title": title,
        "type": page.get("type") or type_from_path(page.get("path")),
        "kbType": page.get("kbType") or "wiki",
        "projectIds": page.get("projectIds") or ["general"],
        "tags": page.get("tags") or [],
        "keywords": page.get("keywords") or extract_keywords(title + "\n" + body),
        "createdAt": page.get("createdAt") or now(),
        "updatedAt": now(),
        "generatedBy": "OpenClaw",
        "contentHash": sha256_text(body),
        "sourceStatus": page.get("sourceStatus") or "active",
        "relatedConcepts": unique(page.get("relatedConcepts") or []),
        "relatedResources": unique(page.get("relatedResources") or []),
        "relatedCodePages": unique(page.get("relatedCodePages") or []),
        "relatedPages": unique(page.get("relatedPages") or []),
        "sources": page.get("sources") or [source_block(payload, repo_meta)],
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def append_relation_section(body, page):
    if any(heading in body for heading in ("## 关联页面", "## 知识关联", "## 相关页面")):
        return body
    lines = []
    seen = set()
    for field, label in RELATION_FIELDS:
        for raw in page.get(field) or []:
            path, title = relation_target(raw)
            if not path or path in seen:
                continue
            seen.add(path)
            lines.append(f"- {label}: [[{path}|{title}]]")
    if not lines:
        return body
    return body.rstrip() + "\n\n## 关联页面\n\n" + "\n".join(lines)


def relation_target(raw):
    title = ""
    value = raw
    if isinstance(raw, dict):
        title = str(raw.get("title") or raw.get("label") or "")
        value = raw.get("path") or raw.get("target") or ""
    if not isinstance(value, str):
        return "", ""
    value = value.strip()
    if value.startswith("[[") and "]]" in value:
        value = value[2:value.find("]]")]
    if "|" in value:
        value, alias = value.split("|", 1)
        title = title or alias.strip()
    if value.endswith(".md"):
        value = value[:-3]
    try:
        path = safe_relpath(value)
    except ValueError:
        return "", ""
    if not path or path.startswith("source_files/"):
        return "", ""
    return path, title or title_from_page({"path": path})


def write_source_manifest(client, payload, repo_meta, page_entries):
    source = payload.get("source") or {}
    config = source.get("config") or {}
    source_id = source.get("id") or payload.get("sourceId") or "unknown"
    repo_url = repo_meta.get("url") or repo_url_from_payload(payload)
    slug = repo_meta.get("slug") or slugify(repo_url)
    path = f"source_files/gitea_repo/{source_id}-{slug}.md"
    manifest = {
        "schema": "research-kb/gitea-repo-source-manifest@1",
        "sourceType": "gitea_repo",
        "sourceId": source_id,
        "sourceName": source.get("name") or "",
        "repoUrl": repo_url,
        "accessMode": config.get("accessMode") or "",
        "defaultBranch": repo_meta.get("defaultBranch") or config.get("defaultBranch") or "",
        "latestCommit": repo_meta.get("latestCommit") or "",
        "previousCommit": repo_meta.get("previousCommit") or "",
        "verifiedLatestCommit": config.get("verifiedLatestCommit") or "",
        "verifiedAt": config.get("verifiedAt") or "",
        "scannedAt": now(),
        "fileCount": repo_meta.get("fileCount") or 0,
        "topLevel": repo_meta.get("topLevel") or [],
        "languageProfile": repo_meta.get("languageProfile") or {},
        "changedFiles": (repo_meta.get("changedFiles") or [])[:200],
        "changedModules": repo_meta.get("changedModules") or [],
        "diffSummary": repo_meta.get("diffSummary") or "",
        "importantFiles": repo_meta.get("importantFiles") or [],
        "generatedPages": [entry.get("path") for entry in page_entries if entry.get("path")],
    }
    content = render_source_manifest_markdown(manifest)
    client.upsert_text(path, content, f"Record repository source manifest {path}")
    return path


def int_value(value):
    try:
        return int(value)
    except Exception:
        return 0


def render_source_manifest_markdown(manifest):
    title = f"代码仓库来源登记：{manifest.get('sourceName') or manifest.get('repoUrl') or manifest.get('sourceId')}"
    changed_files = manifest.get("changedFiles") or []
    important_files = manifest.get("importantFiles") or []
    generated_pages = manifest.get("generatedPages") or []
    lines = [
        f"# {title}",
        "",
        "## 仓库信息",
        "",
        f"- 资料源 ID：`{manifest.get('sourceId')}`",
        f"- 资料源名称：{manifest.get('sourceName') or ''}",
        f"- 仓库地址：{manifest.get('repoUrl') or ''}",
        f"- 访问模式：`{manifest.get('accessMode') or ''}`",
        f"- 默认分支：`{manifest.get('defaultBranch') or ''}`",
        f"- 本次 commit：`{manifest.get('latestCommit') or ''}`",
        f"- 上次 commit：`{manifest.get('previousCommit') or ''}`",
        f"- 扫描时间：{manifest.get('scannedAt') or ''}",
        "",
        "## 仓库结构摘要",
        "",
        f"- 文件数量：{manifest.get('fileCount') or 0}",
        f"- 顶层路径：{', '.join(manifest.get('topLevel') or []) or '未记录'}",
        f"- 变更模块：{', '.join(manifest.get('changedModules') or []) or '无或未记录'}",
        "",
        "## 重要文件",
        "",
    ]
    lines.extend([f"- `{item}`" for item in important_files[:80]] or ["- 未记录"])
    lines.extend(["", "## 变更文件", ""])
    lines.extend([f"- `{item.get('status', '')}` `{item.get('path', '')}`" for item in changed_files[:120]] or ["- 初次扫描、无变化或未记录 diff"])
    lines.extend(["", "## 生成或更新页面", ""])
    lines.extend([f"- `{item}`" for item in generated_pages] or ["- 未记录"])
    lines.extend([
        "",
        "## 机器可读登记",
        "",
        "```json",
        json.dumps(manifest, ensure_ascii=False, indent=2),
        "```",
        "",
        "本文件只登记代码仓库来源元信息，不归档仓库源码文件。",
    ])
    return "\n".join(lines).strip() + "\n"
