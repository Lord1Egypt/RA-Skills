from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import catalog
import frontmatter
import gitea_api as g
import kb_schema
import result_schema
import summary_templates
import task_schema
import text_extractors
from path_utils import normalize_repo_path, sanitize_filename, source_folder, stem

CODE_SUFFIXES = {
    ".py", ".java", ".js", ".mjs", ".cjs", ".ts", ".vue", ".jsx", ".tsx",
    ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rs",
    ".html", ".css", ".scss", ".less",
    ".sql", ".sh", ".ps1", ".bat",
    ".ipynb", ".r", ".kt", ".swift", ".php", ".rb", ".pl", ".scala",
    ".gradle", ".properties", ".ini", ".conf",
}

CODE_CONFIG_NAMES = {
    "package.json", "package-lock.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "yarn.lock",
    "tsconfig.json", "vite.config.ts", "vite.config.js", "electron.vite.config.ts",
    "requirements.txt", "pyproject.toml", "setup.py", "poetry.lock", "pipfile",
    "pom.xml", "build.gradle", "settings.gradle", "gradle.properties",
    "cargo.toml", "go.mod", "go.work", "composer.json", "gemfile",
    "makefile", "cmakelists.txt", "dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".env", ".env.example", ".gitignore", ".dockerignore", ".npmrc", ".yarnrc",
    ".prettierrc", ".eslintrc", ".babelrc",
}

PROJECT_MARKERS = {
    "package.json", "pnpm-workspace.yaml", "pyproject.toml", "requirements.txt",
    "pom.xml", "build.gradle", "settings.gradle", "cargo.toml", "go.mod", "go.work",
    "composer.json", "gemfile", "makefile", "cmakelists.txt", "dockerfile",
}


def read_task(args: argparse.Namespace) -> dict:
    if args.stdin:
        return json.load(sys.stdin)
    if args.task_json:
        return json.loads(Path(args.task_json).read_text(encoding="utf-8"))
    raise SystemExit("--stdin or --task-json is required")


def compact_text(value: str, max_chars: int = 260) -> str:
    text = re.sub(r"\s+", " ", (value or "")).strip()
    return text[:max_chars].rstrip()


def source_missing() -> str:
    return "来源未提及。"


def readable_lines(text: str, limit: int = 160) -> list[str]:
    lines = []
    for raw in (text or "").splitlines():
        line = compact_text(raw.strip(" \t#>-"), 260)
        if len(line) < 8:
            continue
        if line.lower().startswith(("base64", "data:image")):
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def paragraphs(text: str, limit: int = 24) -> list[str]:
    parts = [compact_text(part, 420) for part in re.split(r"\n\s*\n", text or "") if compact_text(part, 80)]
    return parts[:limit]


def markdown_bullets(items: list[str], empty: str = "") -> str:
    clean = [compact_text(item, 300) for item in items if compact_text(item, 40)]
    if not clean:
        return empty or source_missing()
    return "\n".join(f"- {item}" for item in clean)


def matching_lines(text: str, keywords: list[str], limit: int = 6) -> list[str]:
    lowered_keywords = [item.lower() for item in keywords]
    matches = []
    for line in readable_lines(text, 300):
        lower = line.lower()
        if any(keyword in lower for keyword in lowered_keywords):
            matches.append(line)
        if len(matches) >= limit:
            break
    return matches


def source_excerpt(text: str, limit: int = 5) -> list[str]:
    picks = []
    for part in paragraphs(text, 16):
        if part.startswith("|") or part.startswith("---"):
            continue
        picks.append(part)
        if len(picks) >= limit:
            break
    if picks:
        return picks
    return readable_lines(text, limit)


SECTION_KEYWORDS = {
    "研究问题": ["problem", "challenge", "motivation", "objective", "问题", "挑战", "目标", "动机"],
    "核心贡献": ["contribution", "propose", "novel", "贡献", "提出", "创新", "核心"],
    "方法与实现": ["method", "approach", "model", "algorithm", "framework", "方法", "模型", "算法", "框架", "实现"],
    "实验与结果": ["experiment", "result", "accuracy", "baseline", "evaluation", "实验", "结果", "评估", "指标"],
    "局限与不确定性": ["limitation", "future work", "uncertain", "risk", "局限", "限制", "不足", "不确定", "风险"],
    "可复用结论": ["conclusion", "finding", "insight", "implication", "结论", "发现", "启发", "建议"],
    "范围": ["scope", "overview", "cover", "范围", "概述", "覆盖"],
    "分类框架": ["taxonomy", "category", "class", "分类", "框架", "类型"],
    "关键发现": ["finding", "result", "observation", "发现", "结论", "结果"],
    "趋势": ["trend", "future", "roadmap", "趋势", "未来", "演进"],
    "风险": ["risk", "issue", "limitation", "风险", "问题", "限制"],
    "信息缺口": ["gap", "missing", "unknown", "缺口", "未知", "未说明"],
    "团队启发": ["implication", "recommendation", "suggest", "启发", "建议", "团队"],
    "目标": ["goal", "purpose", "objective", "目标", "用途", "目的"],
    "用户与场景": ["user", "scenario", "use case", "用户", "场景", "用例"],
    "架构": ["architecture", "module", "service", "component", "架构", "模块", "组件", "服务"],
    "功能": ["feature", "function", "support", "功能", "能力", "支持"],
    "安装与测试": ["install", "setup", "test", "pytest", "npm", "运行", "安装", "测试", "部署"],
    "成熟度与风险": ["status", "maturity", "risk", "todo", "稳定", "成熟", "风险", "待办"],
    "复用建议": ["reuse", "recommend", "integration", "复用", "建议", "集成"],
    "用途": ["purpose", "usage", "overview", "用途", "使用", "概述"],
    "前置条件": ["prerequisite", "require", "dependency", "需要", "依赖", "前置"],
    "关键概念": ["concept", "definition", "term", "概念", "定义", "术语"],
    "命令或 API": ["api", "command", "cli", "endpoint", "命令", "接口", "api"],
    "配置": ["config", "setting", "env", "yaml", "json", "配置", "环境变量"],
    "示例": ["example", "sample", "demo", "示例", "例子", "样例"],
    "排障": ["trouble", "error", "exception", "debug", "错误", "异常", "排障"],
    "假设": ["hypothesis", "assumption", "假设"],
    "变量": ["variable", "factor", "parameter", "变量", "参数"],
    "环境": ["environment", "hardware", "software", "commit", "环境", "版本", "提交"],
    "数据与模型": ["dataset", "data", "model", "数据", "模型"],
    "结果": ["result", "metric", "score", "结果", "指标", "分数"],
    "异常": ["exception", "failure", "error", "异常", "失败", "错误"],
    "结论": ["conclusion", "therefore", "结论", "因此"],
    "下一步": ["next", "todo", "future", "下一步", "待办", "后续"],
    "时间与参与者": ["date", "time", "participant", "attendee", "时间", "日期", "参与者", "参会"],
    "议程": ["agenda", "议程"],
    "讨论": ["discussion", "discuss", "讨论"],
    "决议": ["decision", "resolved", "决议", "决定"],
    "行动项": ["action", "todo", "owner", "行动项", "待办", "负责人"],
    "开放问题": ["open question", "question", "问题", "待确认"],
    "背景": ["background", "context", "背景", "上下文"],
    "核心想法": ["idea", "proposal", "thought", "想法", "方案", "建议"],
    "证据": ["evidence", "quote", "source", "证据", "来源"],
    "不确定性": ["uncertain", "unknown", "todo", "不确定", "未知", "待确认"],
    "关联知识": ["related", "link", "reference", "关联", "链接", "参考"],
    "验证问题": ["validate", "verify", "question", "验证", "确认", "问题"],
}


def render_general_section(section: str, title: str, file: dict, text: str) -> str:
    if section == "一句话摘要":
        excerpt = source_excerpt(text, 1)
        if not excerpt:
            return f"根据源文件《{file.get('originalFileName', title)}》，未能提取到可读正文。"
        return f"根据源文件《{file.get('originalFileName', title)}》，这份资料主要记录：{excerpt[0]}"
    if section == "来源与可追踪性":
        return source_missing()
    keywords = SECTION_KEYWORDS.get(section, [])
    matches = matching_lines(text, keywords, 7) if keywords else []
    if matches:
        return markdown_bullets(matches)
    if section in {"关键发现", "核心想法", "证据", "用途", "目标", "背景"}:
        return markdown_bullets(source_excerpt(text, 5))
    return source_missing()


def render_sources(file: dict, archived_path: str) -> str:
    return "\n".join([
        f"- sourceFileId: {file.get('sourceFileId', '')}",
        f"- originalPath: {file.get('relativePath', '')}",
        f"- archivedPath: {archived_path}",
        f"- sha256: {file.get('sha256', '')}",
    ])


def build_markdown(task: dict, target: dict, file: dict, type_key: str, text: str, archived_path: str) -> tuple[str, str]:
    title = sanitize_filename(stem(file.get("originalFileName") or file.get("relativePath") or "untitled"))
    now = frontmatter.now_iso()
    fm = frontmatter.render_frontmatter({
        "id": f"{target.get('kbType')}_{file.get('sourceFileId')}",
        "title": title,
        "type": type_key,
        "kbType": target.get("kbType"),
        "createdAt": now,
        "updatedAt": now,
        "generatedBy": "openclaw",
        "sourceFileId": file.get("sourceFileId"),
        "sourceId": (task.get("payload") or {}).get("sourceId"),
        "taskId": task.get("taskId"),
        "sources": [{
            "sourceId": (task.get("payload") or {}).get("sourceId", ""),
            "sourceFileId": file.get("sourceFileId", ""),
            "title": file.get("originalFileName", ""),
            "path": archived_path,
            "originalPath": file.get("relativePath", ""),
            "fileName": file.get("originalFileName", ""),
            "sourceType": file.get("fileKind", ""),
            "sha256": file.get("sha256", ""),
            "page": "",
            "url": "",
        }],
    })
    body = [f"# {title}", ""]
    for section in summary_templates.sections_for(type_key):
        body.append(f"## {section}")
        if section == "来源与可追踪性":
            body.append(render_sources(file, archived_path))
        else:
            body.append(render_general_section(section, title, file, text))
        body.append("")
    return title, fm + "\n".join(body).rstrip() + "\n"


def relative_to_root(path: str, root: str) -> str:
    clean_path = normalize_path(path)
    clean_root = normalize_path(root)
    if clean_root and clean_path.startswith(clean_root + "/"):
        return clean_path[len(clean_root) + 1 :]
    return clean_path


def render_tree(files: list[dict], root: str, limit: int = 80) -> str:
    lines = []
    for file in sorted(files, key=lambda item: item.get("relativePath", ""))[:limit]:
        lines.append(f"- `{relative_to_root(file.get('relativePath', ''), root)}`")
    if len(files) > limit:
        lines.append(f"- 其余 {len(files) - limit} 个文件未展开。")
    return "\n".join(lines) or source_missing()


def detected_stack(files: list[dict]) -> list[str]:
    names = {file_name(file) for file in files}
    suffixes = {file_suffix(file) for file in files}
    stack = []
    if {".ts", ".tsx", ".js", ".jsx", ".vue"} & suffixes or "package.json" in names:
        stack.append("JavaScript/TypeScript 前端或 Node 生态")
    if ".py" in suffixes or "requirements.txt" in names or "pyproject.toml" in names:
        stack.append("Python")
    if ".java" in suffixes or "pom.xml" in names or "build.gradle" in names:
        stack.append("Java/JVM")
    if ".go" in suffixes or "go.mod" in names:
        stack.append("Go")
    if ".rs" in suffixes or "cargo.toml" in names:
        stack.append("Rust")
    if ".cs" in suffixes or any(name.endswith((".sln", ".csproj")) for name in names):
        stack.append(".NET/C#")
    if any(name.startswith("dockerfile") or name.startswith("docker-compose") for name in names):
        stack.append("Docker/容器化配置")
    return stack


def top_modules(files: list[dict], root: str) -> list[str]:
    groups: dict[str, int] = {}
    for file in files:
        rel = relative_to_root(file.get("relativePath", ""), root)
        part = rel.split("/", 1)[0] if "/" in rel else rel
        groups[part] = groups.get(part, 0) + 1
    return [f"`{name}`：{count} 个文件" for name, count in sorted(groups.items(), key=lambda item: (-item[1], item[0]))[:12]]


def codebase_section(section: str, root: str, files: list[dict], text: str) -> str:
    if section == "目标":
        readme_lines = matching_lines(text, ["readme", "overview", "purpose", "goal", "项目", "简介", "目标"], 4)
        if readme_lines:
            return markdown_bullets(readme_lines)
        stack = detected_stack(files)
        suffix_count = len({file_suffix(file) for file in files if file_suffix(file)})
        return f"根据上传文件清单，`{root or '.'}` 是一个包含 {len(files)} 个代码/配置文件、{suffix_count} 类扩展名的代码项目。{('检测到：' + '、'.join(stack) + '。') if stack else ''}"
    if section == "目录结构":
        return render_tree(files, root)
    if section == "核心模块":
        return markdown_bullets(top_modules(files, root))
    if section == "数据流":
        matches = matching_lines(text, ["route", "api", "controller", "service", "store", "database", "model", "ipc", "接口", "服务", "数据库", "模型"], 8)
        return markdown_bullets(matches)
    if section == "配置":
        config_files = [file.get("relativePath", "") for file in files if file_name(file) in CODE_CONFIG_NAMES or file_suffix(file) in {".env", ".yaml", ".yml", ".toml", ".json"}]
        return markdown_bullets([f"`{item}`" for item in config_files[:24]])
    if section == "运行与测试":
        matches = matching_lines(text, ["scripts", "npm run", "pnpm", "yarn", "pytest", "uvicorn", "mvn", "gradle", "cargo run", "cargo test", "go test", "docker", "测试", "运行"], 10)
        return markdown_bullets(matches)
    if section == "风险":
        risks = []
        if not any("test" in normalize_path(file.get("relativePath", "")).lower() or "spec" in normalize_path(file.get("relativePath", "")).lower() for file in files):
            risks.append("本次上传文件清单中没有看到明显的 test/spec 测试文件或目录。")
        if not any(file_name(file).startswith("readme") for file in files):
            risks.append("本次上传文件清单中没有看到 README 文件，项目目标和运行说明可能需要从代码中反推。")
        risks.extend(matching_lines(text, ["todo", "fixme", "hack", "risk", "deprecated", "待办", "风险"], 5))
        return markdown_bullets(risks)
    if section == "修改建议":
        suggestions = [
            "修改前先从“配置”和“运行与测试”中列出的文件核对启动、测试和依赖约束。",
            "涉及核心模块时，优先沿目录结构定位入口、服务层、数据层和配置文件的相互关系。",
        ]
        return markdown_bullets(suggestions)
    if section == "来源与可追踪性":
        return source_missing()
    return markdown_bullets(source_excerpt(text, 5))


def build_codebase_markdown(task: dict, target: dict, root: str, files: list[dict], archived_paths: dict[str, str], text: str) -> tuple[str, str]:
    source_name = (task.get("payload") or {}).get("sourceName") or "source"
    title = sanitize_filename(f"{root.replace('/', ' / ')} 代码库总览" if root else f"{source_name} 代码库总览")
    now = frontmatter.now_iso()
    sources = []
    for file in files:
        source_file_id = file.get("sourceFileId", "")
        sources.append({
            "sourceId": (task.get("payload") or {}).get("sourceId", ""),
            "sourceFileId": source_file_id,
            "title": file.get("originalFileName", ""),
            "path": archived_paths.get(source_file_id, ""),
            "originalPath": file.get("relativePath", ""),
            "fileName": file.get("originalFileName", ""),
            "sourceType": file.get("fileKind", ""),
            "sha256": file.get("sha256", ""),
            "page": "",
            "url": "",
        })
    fm = frontmatter.render_frontmatter({
        "id": f"{target.get('kbType')}_codebase_{sanitize_filename(root or source_name)}",
        "title": title,
        "type": "codebase",
        "kbType": target.get("kbType"),
        "createdAt": now,
        "updatedAt": now,
        "generatedBy": "openclaw",
        "sourceFileId": ",".join(file.get("sourceFileId", "") for file in files),
        "sourceId": (task.get("payload") or {}).get("sourceId"),
        "taskId": task.get("taskId"),
        "sources": sources,
    })
    body = [f"# {title}", ""]
    for section in summary_templates.sections_for("codebase"):
        body.append(f"## {section}")
        if section == "来源与可追踪性":
            for file in files:
                source_file_id = file.get("sourceFileId", "")
                body.append(f"- {file.get('relativePath', '')} -> {archived_paths.get(source_file_id, '')}")
        else:
            body.append(codebase_section(section, root, files, text))
        body.append("")
    return title, fm + "\n".join(body).rstrip() + "\n"


def normalize_path(value: str) -> str:
    return (value or "").replace("\\", "/").strip("/")


def path_parts(value: str) -> list[str]:
    return [part for part in normalize_path(value).split("/") if part]


def parent_dir(value: str) -> str:
    parts = path_parts(value)
    return "/".join(parts[:-1])


def is_under(path: str, root: str) -> bool:
    clean_path = normalize_path(path)
    clean_root = normalize_path(root)
    if not clean_root:
        return True
    return clean_path == clean_root or clean_path.startswith(clean_root + "/")


def reduce_roots(paths: list[str]) -> list[str]:
    roots: list[str] = []
    for path in sorted(set(paths), key=lambda item: (len(path_parts(item)), item)):
        if any(path == root or is_under(path, root) for root in roots):
            continue
        roots.append(path)
    return roots


def file_name(file: dict) -> str:
    return Path(file.get("originalFileName") or file.get("relativePath") or "").name.lower()


def file_suffix(file: dict) -> str:
    return Path(file.get("originalFileName") or file.get("relativePath") or "").suffix.lower()


def is_code_related(file: dict) -> bool:
    kind = (file.get("fileKind") or "").lower()
    name = file_name(file)
    suffix = file_suffix(file)
    return (
        suffix in CODE_SUFFIXES
        or name in CODE_CONFIG_NAMES
        or name.startswith(".env.")
        or suffix in {".sln", ".csproj"}
        or kind in {suffix.lstrip(".") for suffix in CODE_SUFFIXES}
    )


def is_project_marker(file: dict) -> bool:
    name = file_name(file)
    suffix = file_suffix(file)
    return name in PROJECT_MARKERS or suffix in {".sln", ".csproj"}


def fallback_root(relative_path: str) -> str:
    parts = path_parts(relative_path)
    for marker in ("src", "app", "lib", "backend", "frontend", "electron"):
        lowered = [part.lower() for part in parts]
        if marker in lowered and lowered.index(marker) > 0:
            return "/".join(parts[:lowered.index(marker)])
    if len(parts) > 1:
        return parts[0]
    return ""


def code_project_groups(files: list[dict]) -> list[tuple[str, list[dict]]]:
    code_files = [file for file in files if is_code_related(file)]
    if not code_files:
        return []
    marker_roots = [parent_dir(file.get("relativePath", "")) for file in code_files if is_project_marker(file)]
    roots = reduce_roots(marker_roots)
    if "" in roots:
        return [("", code_files)]
    fallback_roots = [
        fallback_root(file.get("relativePath", ""))
        for file in code_files
        if not any(is_under(file.get("relativePath", ""), root) for root in roots)
    ]
    roots = reduce_roots(roots + fallback_roots)
    groups = []
    for root in roots:
        group = [file for file in code_files if is_under(file.get("relativePath", ""), root)]
        if group:
            groups.append((root, sorted(group, key=lambda item: item.get("relativePath", ""))))
    return groups


def archive_source(task: dict, target: dict, file: dict) -> tuple[str, dict]:
    uploaded = Path(file["uploadedPath"])
    if not uploaded.exists():
        raise FileNotFoundError(str(uploaded))
    owner = target["repoOwner"]
    repo = target["repoName"]
    source_file_key = sanitize_filename(file.get("sourceFileId") or uploaded.stem)
    folder = "code" if is_code_related(file) else source_folder(file.get("fileKind", ""), file.get("originalFileName", ""))
    archived_path = normalize_repo_path(f"source_files/{folder}/{source_file_key}-{sanitize_filename(file.get('originalFileName') or uploaded.name)}")
    if (task.get("payload") or {}).get("options", {}).get("archiveSourceFile", True):
        g.put_file(owner, repo, archived_path, uploaded.read_bytes(), f"research-kb archive source: {uploaded.name} [{task.get('taskId')}]")
    return archived_path, {"sourceFileId": file.get("sourceFileId"), "path": archived_path}


def collect_codebase_text(files: list[dict], root: str) -> str:
    max_chars = int(os.getenv("CODE_PROJECT_MAX_CHARS", "160000"))
    max_file_chars = int(os.getenv("CODE_PROJECT_FILE_MAX_CHARS", "12000"))
    lines = [
        f"Project root: {root or '.'}",
        "",
        "File manifest:",
    ]
    for file in files:
        lines.append(f"- {file.get('relativePath', '')} | {file.get('sha256', '')} | {file.get('sizeBytes', 0)} bytes")
    lines.append("")
    lines.append("Selected file contents:")
    remaining = max_chars
    for file in files:
        if remaining <= 0:
            break
        uploaded = Path(file["uploadedPath"])
        try:
            text = text_extractors.extract_text(str(uploaded), min(max_file_chars, remaining))
        except Exception as exc:
            text = f"[Could not extract text: {exc}]"
        if not text.strip():
            continue
        header = f"\n\n### {file.get('relativePath', '')}\n\n"
        chunk = text[:min(max_file_chars, remaining)]
        lines.append(header + chunk)
        remaining -= len(chunk)
    if remaining <= 0:
        lines.append("\n[Code project text truncated.]")
    return "\n".join(lines)


def run(task: dict) -> dict:
    errors = task_schema.validate_task(task)
    if errors:
        return result_schema.result(task, False, None, errors)
    target = task["kbTargets"][0]
    payload = task["payload"]
    owner = target["repoOwner"]
    repo = target["repoName"]
    kb_type = target["kbType"]
    created = []
    updated = []
    archived = []
    failed = []
    cat = catalog.read(owner, repo)
    all_files = list(payload.get("files", []))
    handled_source_ids: set[str] = set()

    for root, group_files in code_project_groups(all_files):
        valid_files = []
        archived_paths: dict[str, str] = {}
        try:
            for file in group_files:
                source_file_id = file.get("sourceFileId", "")
                try:
                    archived_path, archived_item = archive_source(task, target, file)
                    archived.append(archived_item)
                    archived_paths[source_file_id] = archived_path
                    valid_files.append(file)
                except Exception as exc:
                    failed.append({"sourceFileId": source_file_id, "fileName": file.get("originalFileName", ""), "reason": str(exc)})
                    handled_source_ids.add(source_file_id)
            if not valid_files:
                continue
            text = collect_codebase_text(valid_files, root)
            title, md = build_codebase_markdown(task, target, root, valid_files, archived_paths, text)
            group_key = sanitize_filename(root or f"{payload.get('sourceName', 'source')} codebase")
            doc_path = normalize_repo_path(f"{kb_schema.folder_for('codebase')}/{title}-{group_key}.md")
            existed = g.get_file(owner, repo, doc_path) is not None
            g.put_file(owner, repo, doc_path, md, f"research-kb ingest codebase: {title} [{task.get('taskId')}]")
            entry = {
                "title": title,
                "file": doc_path,
                "type_key": "codebase",
                "brief": title,
                "scope": kb_type,
                "source_id": payload.get("sourceId"),
                "source_file_id": ",".join(file.get("sourceFileId", "") for file in valid_files),
                "source_path": root or ".",
                "archived_source_path": "",
                "updated_at": frontmatter.now_iso(),
            }
            replaced = catalog.upsert_document(cat, entry)
            target_list = updated if existed or replaced else created
            for file in valid_files:
                target_list.append({"sourceFileId": file.get("sourceFileId"), "path": doc_path, "title": title, "type": "codebase"})
                handled_source_ids.add(file.get("sourceFileId", ""))
        except Exception as exc:
            for file in group_files:
                source_file_id = file.get("sourceFileId", "")
                if source_file_id not in handled_source_ids:
                    failed.append({"sourceFileId": source_file_id, "fileName": file.get("originalFileName", ""), "reason": str(exc)})

    for file in all_files:
        if file.get("sourceFileId", "") in handled_source_ids:
            continue
        try:
            uploaded = Path(file["uploadedPath"])
            archived_path, archived_item = archive_source(task, target, file)
            archived.append(archived_item)
            max_chars = int(os.getenv("PAPERKB_MAX_CHARS", "60000"))
            if file.get("fileKind") == "code_pack":
                max_chars = max(max_chars, int(os.getenv("CODE_PACK_MAX_CHARS", "120000")))
            text = text_extractors.extract_text(str(uploaded), max_chars)
            type_key = kb_schema.detect_type(file.get("fileKind", ""), file.get("originalFileName", ""), text)
            title, md = build_markdown(task, target, file, type_key, text, archived_path)
            source_file_key = sanitize_filename(file.get("sourceFileId") or uploaded.stem)
            doc_path = normalize_repo_path(f"{kb_schema.folder_for(type_key)}/{title}-{source_file_key}.md")
            existed = g.get_file(owner, repo, doc_path) is not None
            g.put_file(owner, repo, doc_path, md, f"research-kb ingest: {title} [{task.get('taskId')}]")
            entry = {
                "title": title,
                "file": doc_path,
                "type_key": type_key,
                "brief": title,
                "scope": kb_type,
                "source_id": payload.get("sourceId"),
                "source_file_id": file.get("sourceFileId"),
                "source_path": file.get("relativePath"),
                "archived_source_path": archived_path,
                "updated_at": frontmatter.now_iso(),
            }
            replaced = catalog.upsert_document(cat, entry)
            target_list = updated if existed or replaced else created
            target_list.append({"sourceFileId": file.get("sourceFileId"), "path": doc_path, "title": title, "type": type_key})
        except Exception as exc:
            failed.append({"sourceFileId": file.get("sourceFileId", ""), "fileName": file.get("originalFileName", ""), "reason": str(exc)})

    catalog.write(owner, repo, cat)
    catalog.regen_index(owner, repo, repo, cat)
    report_path = ""
    if len(payload.get("files", [])) > 1:
        report_path = write_report(task, target, created, updated, failed)
    payload_result = {
        "ingestionId": payload.get("ingestionId", ""),
        "kbTarget": {"kbType": kb_type, "repoFullName": target.get("repoFullName", f"{owner}/{repo}"), "branch": target.get("branch", "main")},
        "processedFiles": len(payload.get("files", [])),
        "createdMarkdownFiles": created,
        "updatedMarkdownFiles": updated,
        "createdExtraPages": [],
        "archivedSourceFiles": archived,
        "skippedFiles": [],
        "failedSourceFiles": failed,
        "catalogUpdated": True,
        "indexUpdated": True,
        "importReportPath": report_path,
    }
    return result_schema.result(task, True, payload_result, [])


def write_report(task: dict, target: dict, created: list, updated: list, failed: list) -> str:
    owner = target["repoOwner"]
    repo = target["repoName"]
    name = sanitize_filename(f"{task.get('taskId')} import report")
    path = f"imports/{name}.md"
    now = frontmatter.now_iso()
    md = frontmatter.render_frontmatter({
        "id": f"import_{task.get('taskId')}",
        "title": "导入报告",
        "type": "import",
        "kbType": target.get("kbType"),
        "createdAt": now,
        "updatedAt": now,
        "generatedBy": "openclaw",
        "sources": [],
    })
    md += f"# 导入报告\n\n- 新建 Markdown: {len(created)}\n- 更新 Markdown: {len(updated)}\n- 失败源文件: {len(failed)}\n"
    g.put_file(owner, repo, path, md, f"research-kb import report: {task.get('taskId')}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--task-json", default="")
    args = parser.parse_args()
    task = read_task(args)
    print(json.dumps(run(task), ensure_ascii=False))


if __name__ == "__main__":
    main()
