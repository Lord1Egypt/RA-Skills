import ast
import os
import json
import sys
import subprocess
import tarfile
import zipfile
import shutil
import glob

# Known default skill-installation paths per major AI agent provider.
# These can be overridden via config.json or the AGENT_SKILLS_PATH env var.
PROVIDER_DEFAULTS = {
    "claude":   "~/.claude/skills",
    "gemini":   "~/.gemini/skills",
    "codex":    "~/.copilot/skills",
    "cursor":   "~/.cursor/skills",
    "openai":   "~/.openai/skills",
    "openclaw": "~/.openclaw/skills",
    "cline":    "~/.cline/skills",
}

def get_docstring_summary(node):
    docstring = ast.get_docstring(node)
    if docstring:
        return docstring.split('\n')[0].strip()
    return ""

def parse_file(file_path, package_root):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            content = f.read()
            tree = ast.parse(content)
        except Exception:
            return []
    
    relative_path = os.path.relpath(file_path, package_root)
    results = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if isinstance(node, ast.ClassDef):
                kind = "class"
                bases = [ast.unparse(b) for b in node.bases]
                signature = f"class {node.name}({', '.join(bases)})"
            else:
                kind = "function"
                args = ast.unparse(node.args)
                signature = f"def {node.name}({args})"

            start_line = node.lineno
            end_line = node.end_lineno
            doc_summary = get_docstring_summary(node)
            
            results.append({
                "name": node.name,
                "kind": kind,
                "signature": signature,
                "doc": doc_summary,
                "file": relative_path,
                "range": [start_line, end_line]
            })
            
    return results

def download_package(package, version, tmp_dir):
    print(f"Downloading {package}=={version}...")
    cmd = ["pip", "download", "--no-binary=:all:", f"{package}=={version}", "-d", tmp_dir]
    subprocess.run(cmd, check=True)
    
    # Find the downloaded file that best matches the package name
    files = os.listdir(tmp_dir)
    # Filter for files that contain the package name and are archives
    matching_files = [f for f in files if package.replace("-", "_") in f.lower().replace("-", "_") and (f.endswith(".tar.gz") or f.endswith(".zip") or f.endswith(".whl"))]
    
    if not matching_files:
        # Fallback to the first one if we can't find a perfect match
        archive_path = os.path.join(tmp_dir, files[0])
    else:
        # Pick the one that most likely corresponds to the package (e.g. shortest name if multiple)
        matching_files.sort(key=len)
        archive_path = os.path.join(tmp_dir, matching_files[0])
    
    print(f"Extracting {archive_path}...")
    extract_path = os.path.join(tmp_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)
    
    if archive_path.endswith(".tar.gz") or archive_path.endswith(".tar.bz2"):
        with tarfile.open(archive_path) as tar:
            tar.extractall(path=extract_path)
    elif archive_path.endswith(".zip") or archive_path.endswith(".whl"):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            
    return extract_path

def find_package_root(extract_path, package_name):
    # Normalize package name (PyPI uses hyphens and underscores interchangeably sometimes)
    norm_name = package_name.lower().replace("-", "_")
    
    # Search patterns
    # We look for a directory that contains an __init__.py and matches our normalized name
    for root, dirs, files in os.walk(extract_path):
        for d in dirs:
            if d.lower().replace("-", "_") == norm_name:
                pkg_dir = os.path.join(root, d)
                if os.path.exists(os.path.join(pkg_dir, "__init__.py")):
                    return pkg_dir
    
    return None

def build_grep_map(package_root):
    grep_map = []
    # We want to maintain relative structure from the root
    for root, _, files in os.walk(package_root):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                # Skip __pycache__ etc
                if "__pycache__" in file_path:
                    continue
                grep_map.extend(parse_file(file_path, package_root))
    return grep_map

def generate_skill(package, version, grep_map, package_root, output_dir):
    skill_name = f"{package}-{version}".lower().replace("_", "-")
    skill_dir = os.path.join(output_dir, skill_name)
    os.makedirs(skill_dir, exist_ok=True)
    
    ref_dir = os.path.join(skill_dir, "references")
    os.makedirs(ref_dir, exist_ok=True)
    
    # Copy source files to references/
    for item in grep_map:
        src_file = os.path.join(package_root, item['file'])
        dst_file = os.path.join(ref_dir, item['file'])
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        if not os.path.exists(dst_file):
            try:
                shutil.copy2(src_file, dst_file)
            except Exception as e:
                print(f"Error copying {src_file}: {e}")

    # Build SKILL.md
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, "w") as f:
        f.write(f"---\nname: {skill_name}\ndescription: Deterministic API mirror for {package} v{version}. Use this skill to grounded exploration of {package} API when uncertainty is high.\n---\n\n")
        f.write(f"# {package} v{version} Grep Map\n\n")
        f.write("This map provides a deterministic coordinate system for the package source. All paths are relative to `references/`.\n\n")
        
        # Organize by file
        by_file = {}
        for item in grep_map:
            by_file.setdefault(item['file'], []).append(item)
            
        for file_path, items in sorted(by_file.items()):
            f.write(f"## File: `{file_path}`\n\n")
            # Sort items by line range to be deterministic
            items.sort(key=lambda x: x['range'][0])
            for item in items:
                f.write(f"- **`{item['signature']}`**\n")
                f.write(f"  - Range: `lines {item['range'][0]}-{item['range'][1]}`\n")
                if item['doc']:
                    f.write(f"  - Doc: {item['doc']}\n")
            f.write("\n")

    print(f"Skill generated at: {skill_dir}")
    return skill_dir

def detect_provider():
    """Detect the active AI agent provider from well-known environment variables."""
    # Explicit override always wins
    if "AGENT_PROVIDER" in os.environ:
        return os.environ["AGENT_PROVIDER"].lower()
    # Presence-based detection via provider-specific env vars
    if "ANTHROPIC_API_KEY" in os.environ or "CLAUDE_API_KEY" in os.environ:
        return "claude"
    if "GEMINI_API_KEY" in os.environ or "GOOGLE_GENERATIVEAI_API_KEY" in os.environ:
        return "gemini"
    if "OPENAI_API_KEY" in os.environ:
        return "openai"
    if "CODEX_API_KEY" in os.environ or "GITHUB_COPILOT_TOKEN" in os.environ:
        return "codex"
    return None


def get_config():
    # Try to load config from the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(script_dir), "config.json")

    config = {
        "provider": None,
        "provider_defaults": PROVIDER_DEFAULTS.copy(),
    }

    user_config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                user_config = json.load(f)
            # Deep-merge provider_defaults so callers can extend the table
            if "provider_defaults" in user_config:
                config["provider_defaults"].update(user_config.pop("provider_defaults"))
            config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not read config.json: {e}")

    # Resolve provider: env var detection takes priority over config file value
    # (detect_provider() checks AGENT_PROVIDER first, then API-key env vars)
    provider = detect_provider() or config.get("provider")
    if provider:
        config["provider"] = provider

    # Apply provider default path only when no explicit path was configured
    explicit_path_in_config = "skills_path" in user_config
    if provider and provider in config["provider_defaults"] and not explicit_path_in_config:
        config["skills_path"] = os.path.expanduser(config["provider_defaults"][provider])

    # Fall back to CWD .skills/ if still no path was determined
    if "skills_path" not in config:
        config["skills_path"] = os.path.join(os.getcwd(), ".skills")

    # Environment variable override – highest priority
    if "AGENT_SKILLS_PATH" in os.environ:
        config["skills_path"] = os.environ["AGENT_SKILLS_PATH"]

    return config

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate_mirror.py <package> <version> [output_path]")
        sys.exit(1)
        
    pkg = sys.argv[1]
    ver = sys.argv[2]
    
    config = get_config()
    
    # Priority: 1. CLI Arg, 2. Env Var/Config, 3. Default (.skills/)
    if len(sys.argv) >= 4:
        skills_dir = sys.argv[3]
    else:
        skills_dir = config["skills_path"]
        
    # Expand ~ in paths
    skills_dir = os.path.expanduser(skills_dir)
    
    tmp = "tmp_download"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    
    try:
        extract_path = download_package(pkg, ver, tmp)
        pkg_root = find_package_root(extract_path, pkg)

        if not pkg_root:
            print(f"Could not find package root for {pkg} in {extract_path}")
            sys.exit(1)

        print(f"Found package root at: {pkg_root}")
        g_map = build_grep_map(pkg_root)
        generate_skill(pkg, ver, g_map, pkg_root, skills_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
