#!/usr/bin/env python3
"""
GitHub / 本地 Git 仓库自动分析脚本

功能：
1. 提取 README 内容摘要
2. 扫描项目目录结构，识别技术栈
3. 提取依赖信息（requirements.txt, package.json, go.mod, Cargo.toml, pom.xml, etc.）
4. 识别入口文件（CLI / Server）
5. 统计代码量，识别核心模块

用法：
  python analyze_repo.py <github_url|local_path>

输出：JSON 格式的项目分析报告
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import urllib.request


def is_github_url(url: str) -> bool:
    return "github.com" in url or url.startswith("https://github.com/") or url.startswith("http://github.com/")


def parse_github_url(url: str) -> tuple:
    """解析 GitHub URL 返回 (owner, repo)"""
    path = urlparse(url).path.strip("/")
    parts = path.split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None


def fetch_github_readme(owner: str, repo: str) -> str:
    """通过 GitHub API 获取 README 内容"""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github.v3.raw"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"[Error fetching README: {e}]"


def fetch_github_repo_info(owner: str, repo: str) -> dict:
    """通过 GitHub API 获取仓库元数据"""
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "language": data.get("language", "Unknown"),
                "license": data.get("license", {}).get("spdx_id", "Unknown") if data.get("license") else "Unknown",
                "last_updated": data.get("updated_at", "Unknown"),
                "description": data.get("description", ""),
                "default_branch": data.get("default_branch", "main"),
                "topics": data.get("topics", []),
            }
    except Exception as e:
        return {"error": str(e)}


def fetch_github_tree(owner: str, repo: str, branch: str = "main") -> list:
    """通过 GitHub API 获取仓库文件树（前100个文件）"""
    # 先尝试获取默认分支
    info_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = urllib.request.Request(info_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            info = json.loads(resp.read().decode("utf-8"))
            branch = info.get("default_branch", branch)
    except Exception:
        pass
    
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    try:
        req = urllib.request.Request(tree_url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("tree", [])
    except Exception as e:
        return [{"error": str(e)}]


def analyze_github_remote(owner: str, repo: str) -> dict:
    """纯 GitHub API 远程分析（不 clone）"""
    result = {
        "source": f"https://github.com/{owner}/{repo}",
        "is_remote": True,
        "repo_name": repo,
    }
    
    # 1. 仓库元数据
    result["github_info"] = fetch_github_repo_info(owner, repo)
    
    # 2. README
    result["readme"] = fetch_github_readme(owner, repo)[:3000]
    
    # 3. 文件树
    tree = fetch_github_tree(owner, repo)
    if tree and "error" not in tree[0]:
        files = [t["path"] for t in tree if t.get("type") == "blob"]
        dirs = list(set(t["path"].split("/")[0] for t in tree if "/" in t.get("path", "")))
        
        result["structure"] = {
            "directories": sorted(d for d in dirs if not d.startswith(".")),
            "top_level_files": sorted(f for f in files if "/" not in f and not f.startswith(".")),
            "all_files": files[:200],  # 限制数量
            "language_stats": {},  # 远程无法统计行数
        }
        
        # 4. 识别依赖文件
        dep_files = {k: [] for k in [
            "python", "nodejs", "go", "rust", "java", "ruby", "php", "docker"
        ]}
        dep_map = {
            "python": ["requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "poetry.lock"],
            "nodejs": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
            "go": ["go.mod", "go.sum"],
            "rust": ["Cargo.toml", "Cargo.lock"],
            "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "ruby": ["Gemfile", "Gemfile.lock"],
            "php": ["composer.json", "composer.lock"],
            "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        }
        for f in files:
            basename = f.split("/")[-1]
            for lang, patterns in dep_map.items():
                if basename in patterns:
                    dep_files[lang].append(f)
        result["dependency_files"] = dep_files
        
        # 5. 尝试获取依赖内容（只获取根目录的）
        deps = {}
        for lang, files_list in dep_files.items():
            for f in files_list:
                if "/" in f:
                    continue  # 只取根目录的
                basename = f.split("/")[-1]
                try:
                    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{result.get('github_info',{}).get('default_branch','main')}/{f}"
                    req = urllib.request.Request(raw_url)
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        content = resp.read().decode("utf-8", errors="replace")
                        if basename == "requirements.txt":
                            deps["python"] = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")][:50]
                        elif basename == "package.json":
                            try:
                                pkg = json.loads(content)
                                all_deps = {}
                                all_deps.update(pkg.get("dependencies", {}))
                                all_deps.update(pkg.get("devDependencies", {}))
                                deps["nodejs"] = list(all_deps.keys())[:50]
                                deps["_nodejs_entry"] = {
                                    "main": pkg.get("main"),
                                    "bin": pkg.get("bin"),
                                    "scripts": pkg.get("scripts", {}),
                                }
                            except Exception:
                                pass
                        elif basename == "go.mod":
                            go_deps = [l.strip().split()[0] for l in content.splitlines() if l.strip().startswith("github.com") or l.strip().startswith("golang.org")]
                            deps["go"] = go_deps[:50]
                        elif basename == "Cargo.toml":
                            crate_deps = re.findall(r'^([a-zA-Z0-9_-]+)\s*=\s*["{]', content, re.MULTILINE)
                            deps["rust"] = crate_deps[:50]
                        elif basename == "pom.xml":
                            java_deps = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                            deps["java"] = java_deps[:50]
                        elif basename == "pyproject.toml":
                            dep_match = re.search(r'\[project\].*?dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                            if dep_match:
                                dep_str = dep_match.group(1)
                                dep_lines = re.findall(r'"([^"]+)"', dep_str)
                                if dep_lines:
                                    deps["python"] = dep_lines[:50]
                            if "python" not in deps:
                                dep_match = re.search(r'\[tool\.poetry\].*?dependencies\s*=\s*\{(.*?)\}', content, re.DOTALL)
                                if dep_match:
                                    dep_str = dep_match.group(1)
                                    dep_lines = re.findall(r'^\s*([a-zA-Z0-9_-]+)\s*=\s*"', dep_str, re.MULTILINE)
                                    if dep_lines:
                                        deps["python"] = dep_lines[:50]
                except Exception:
                    pass
        result["dependencies"] = deps
        
        # 6. 识别入口
        primary_language = result.get("github_info", {}).get("language", "Unknown")
        result["primary_language"] = primary_language
        result["entry_points"] = []
        
        # 根据语言推测入口
        if primary_language == "Python":
            for f in files:
                if f in ["__main__.py", "cli.py", "main.py", "app.py", "server.py", "run.py", "manage.py"]:
                    result["entry_points"].append(f)
        elif primary_language in ["JavaScript", "TypeScript"]:
            if "_nodejs_entry" in deps:
                entry_info = deps.pop("_nodejs_entry")
                if entry_info.get("bin"):
                    result["entry_points"].append(f"bin: {entry_info['bin']}")
                if entry_info.get("scripts"):
                    for s, c in entry_info["scripts"].items():
                        if s in ["start", "dev", "serve", "build"]:
                            result["entry_points"].append(f"npm run {s}: {c}")
        elif primary_language == "Go":
            for f in files:
                if f.endswith("main.go") or f.startswith("cmd/"):
                    result["entry_points"].append(f)
        elif primary_language == "Rust":
            for f in files:
                if f in ["src/main.rs"] or f.startswith("src/bin/"):
                    result["entry_points"].append(f)
        
        # 7. 核心模块推测
        core_keywords = ["core", "src", "lib", "pkg", "internal", "engine", "algorithm", "model", "service"]
        candidates = []
        for d in dirs:
            if d.lower() in core_keywords:
                candidates.append(d)
        candidates.append(f"主要语言: {primary_language}")
        result["core_modules"] = candidates
    else:
        result["structure"] = {"directories": [], "top_level_files": [], "all_files": [], "language_stats": {}}
        result["dependency_files"] = {}
        result["dependencies"] = {}
        result["entry_points"] = []
        result["core_modules"] = []
        result["primary_language"] = "Unknown"
    
    return result

    """如果是 GitHub URL 则 clone 到临时目录，如果是本地路径则直接使用"""
    if is_github_url(url_or_path):
        owner, repo = parse_github_url(url_or_path)
        if not owner or not repo:
            raise ValueError(f"Invalid GitHub URL: {url_or_path}")
        tmpdir = tempfile.mkdtemp(prefix=f"repo_analysis_{repo}_")
        clone_url = f"https://github.com/{owner}/{repo}.git"
        print(f"Cloning {clone_url} ...", file=sys.stderr)
        subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, tmpdir],
            capture_output=True,
            check=True,
        )
        return Path(tmpdir)
    else:
        p = Path(url_or_path)
        if not p.exists():
            raise FileNotFoundError(f"Path not found: {url_or_path}")
        return p


def find_dependency_files(repo_path: Path) -> dict:
    """扫描项目中的依赖文件"""
    dep_files = {
        "python": ["requirements.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "poetry.lock"],
        "nodejs": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "ruby": ["Gemfile", "Gemfile.lock"],
        "php": ["composer.json", "composer.lock"],
        "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    }
    found = {k: [] for k in dep_files}
    for root, _dirs, files in os.walk(repo_path):
        # Skip .git and common hidden dirs
        rel_root = Path(root).relative_to(repo_path)
        if any(part.startswith(".") for part in rel_root.parts):
            continue
        for f in files:
            for lang, patterns in dep_files.items():
                if f in patterns:
                    found[lang].append(str(rel_root / f))
    return found


def extract_dependencies(repo_path: Path, dep_files: dict) -> dict:
    """提取依赖列表"""
    deps = {}
    
    # Python
    if dep_files.get("python"):
        for f in dep_files["python"]:
            fp = repo_path / f
            if fp.name == "requirements.txt" and fp.exists():
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    lines = [l.strip() for l in fh if l.strip() and not l.startswith("#")]
                    deps["python"] = lines[:50]  # 限制数量
            elif fp.name == "pyproject.toml" and fp.exists():
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                        # 匹配 PEP 621 [project] dependencies
                        dep_match = re.search(r'\[project\].*?dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                        if dep_match:
                            dep_str = dep_match.group(1)
                            dep_lines = re.findall(r'"([^"]+)"', dep_str)
                            if dep_lines:
                                deps["python"] = dep_lines[:50]
                        # 也尝试旧的 [tool.poetry] 格式
                        if "python" not in deps:
                            dep_match = re.search(r'\[tool\.poetry\].*?dependencies\s*=\s*\{(.*?)\}', content, re.DOTALL)
                            if dep_match:
                                dep_str = dep_match.group(1)
                                dep_lines = re.findall(r'^\s*([a-zA-Z0-9_-]+)\s*=\s*"', dep_str, re.MULTILINE)
                                if dep_lines:
                                    deps["python"] = dep_lines[:50]
                except Exception:
                    pass
    
    # Node.js
    if dep_files.get("nodejs"):
        for f in dep_files["nodejs"]:
            fp = repo_path / f
            if fp.name == "package.json" and fp.exists():
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        pkg = json.load(fh)
                        all_deps = {}
                        all_deps.update(pkg.get("dependencies", {}))
                        all_deps.update(pkg.get("devDependencies", {}))
                        deps["nodejs"] = list(all_deps.keys())[:50]
                        # 提取入口
                        deps["_nodejs_entry"] = {
                            "main": pkg.get("main"),
                            "bin": pkg.get("bin"),
                            "scripts": pkg.get("scripts", {}),
                        }
                except Exception:
                    pass
    
    # Go
    if dep_files.get("go"):
        for f in dep_files["go"]:
            fp = repo_path / f
            if fp.name == "go.mod" and fp.exists():
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    lines = fh.readlines()
                    go_deps = [l.strip().split()[0] for l in lines if l.strip().startswith("github.com") or l.strip().startswith("golang.org")]
                    deps["go"] = go_deps[:50]
    
    # Rust
    if dep_files.get("rust"):
        for f in dep_files["rust"]:
            fp = repo_path / f
            if fp.name == "Cargo.toml" and fp.exists():
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                        crate_deps = re.findall(r'^([a-zA-Z0-9_-]+)\s*=\s*["{]', content, re.MULTILINE)
                        deps["rust"] = crate_deps[:50]
                except Exception:
                    pass
    
    # Java
    if dep_files.get("java"):
        for f in dep_files["java"]:
            fp = repo_path / f
            if fp.name == "pom.xml" and fp.exists():
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                        java_deps = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                        deps["java"] = java_deps[:50]
                except Exception:
                    pass
    
    return deps


def find_entry_points(repo_path: Path, language: str, deps: dict) -> list:
    """识别可能的入口文件"""
    entries = []
    
    if language == "Python":
        patterns = [
            "__main__.py", "cli.py", "main.py", "app.py", "server.py",
            "run.py", "manage.py", "entrypoint.py",
        ]
        for p in patterns:
            matches = list(repo_path.rglob(p))
            for m in matches:
                rel = str(m.relative_to(repo_path))
                if not any(part.startswith(".") for part in Path(rel).parts):
                    entries.append(rel)
        # 检查 pyproject.toml 的 console_scripts
        pyproject = repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "r") as f:
                    content = f.read()
                    scripts = re.findall(r'\[project\.scripts\].*?\n\n', content, re.DOTALL)
                    if scripts:
                        entries.append(f"pyproject.toml console_scripts: {scripts[0].strip()}")
            except Exception:
                pass
    
    elif language == "JavaScript" or language == "TypeScript":
        # package.json 中的信息已经在 deps 里了
        if "_nodejs_entry" in deps:
            entry_info = deps.pop("_nodejs_entry")
            if entry_info.get("bin"):
                entries.append(f"package.json bin: {entry_info['bin']}")
            if entry_info.get("main"):
                entries.append(f"package.json main: {entry_info['main']}")
            if entry_info.get("scripts"):
                for script_name, cmd in entry_info["scripts"].items():
                    if script_name in ["start", "dev", "serve", "build"]:
                        entries.append(f"npm run {script_name}: {cmd}")
        # 再找 bin 目录
        for bin_dir in ["bin", "cli", "cmd"]:
            p = repo_path / bin_dir
            if p.exists():
                entries.append(f"Directory: {bin_dir}/")
    
    elif language == "Go":
        mains = list(repo_path.rglob("main.go"))
        for m in mains:
            rel = str(m.relative_to(repo_path))
            if not any(part.startswith(".") for part in Path(rel).parts):
                entries.append(rel)
        # cmd 目录
        cmd_dir = repo_path / "cmd"
        if cmd_dir.exists():
            for sub in cmd_dir.iterdir():
                if sub.is_dir():
                    entries.append(f"cmd/{sub.name}/")
    
    elif language == "Rust":
        # src/main.rs 或 src/bin/
        main_rs = repo_path / "src" / "main.rs"
        if main_rs.exists():
            entries.append("src/main.rs")
        bin_dir = repo_path / "src" / "bin"
        if bin_dir.exists():
            for f in bin_dir.iterdir():
                if f.suffix == ".rs":
                    entries.append(f"src/bin/{f.name}")
    
    return entries[:10]


def scan_directory_structure(repo_path: Path) -> dict:
    """扫描目录结构，统计各目录代码量"""
    structure = {"directories": [], "top_level_files": [], "language_stats": {}}
    
    # 顶层目录和文件
    for item in sorted(repo_path.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            structure["directories"].append(item.name)
        else:
            structure["top_level_files"].append(item.name)
    
    # 统计各语言代码行数（简单估算）
    lang_extensions = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".go": "Go", ".rs": "Rust", ".java": "Java",
        ".cpp": "C++", ".c": "C", ".h": "C/C++",
        ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
        ".kt": "Kotlin", ".scala": "Scala",
    }
    
    for root, _dirs, files in os.walk(repo_path):
        rel_root = Path(root).relative_to(repo_path)
        if any(part.startswith(".") for part in rel_root.parts):
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in lang_extensions:
                lang = lang_extensions[ext]
                fp = Path(root) / f
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                        lines = len(fh.readlines())
                        structure["language_stats"][lang] = structure["language_stats"].get(lang, 0) + lines
                except Exception:
                    pass
    
    return structure


def identify_core_modules(repo_path: Path, structure: dict) -> list:
    """基于目录名和代码量推测核心模块"""
    candidates = []
    
    # 常见核心目录名
    core_keywords = [
        "core", "src", "lib", "pkg", "internal", "engine",
        "algorithm", "model", "service", "handler", "controller",
        "domain", "entity", "usecase", "application",
    ]
    
    for d in structure.get("directories", []):
        if d.lower() in core_keywords:
            candidates.append(d)
    
    # 按代码量推断主要语言
    lang_stats = structure.get("language_stats", {})
    if lang_stats:
        primary_lang = max(lang_stats, key=lang_stats.get)
        candidates.append(f"主要语言: {primary_lang} ({lang_stats[primary_lang]} 行)")
    
    return candidates



def analyze_repo(url_or_path: str) -> dict:
    """主分析函数"""
    is_remote = is_github_url(url_or_path)
    owner, repo = None, None
    
    if is_remote:
        owner, repo = parse_github_url(url_or_path)
    
    if is_remote and owner and repo:
        # 优先用纯 API 分析，避免 clone
        return analyze_github_remote(owner, repo)
    
    # 本地分析
    repo_path = clone_or_use_local(url_or_path)
    
    # 收集信息
    result = {
        "source": url_or_path,
        "is_remote": False,
        "repo_name": repo_path.name,
    }
    
    # 本地读取 README
    for readme_name in ["README.md", "README.rst", "README.txt", "README"]:
        readme_path = repo_path / readme_name
        if readme_path.exists():
            with open(readme_path, "r", encoding="utf-8", errors="replace") as f:
                result["readme"] = f.read()[:3000]
            break
    
    # 2. 目录结构
    structure = scan_directory_structure(repo_path)
    result["structure"] = structure
    
    # 3. 依赖
    dep_files = find_dependency_files(repo_path)
    result["dependency_files"] = dep_files
    deps = extract_dependencies(repo_path, dep_files)
    result["dependencies"] = deps
    
    # 4. 入口
    primary_language = "Unknown"
    if structure.get("language_stats"):
        primary_language = max(structure["language_stats"], key=structure["language_stats"].get)
    
    result["entry_points"] = find_entry_points(repo_path, primary_language, deps)
    result["primary_language"] = primary_language
    
    # 5. 核心模块推测
    result["core_modules"] = identify_core_modules(repo_path, structure)
    
    return result



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_repo.py <github_url|local_path>")
        sys.exit(1)
    
    target = sys.argv[1]
    report = analyze_repo(target)
    print(json.dumps(report, indent=2, ensure_ascii=False))
