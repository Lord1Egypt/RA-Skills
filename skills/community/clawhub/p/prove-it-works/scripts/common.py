#!/usr/bin/env python3
"""Shared helpers for Prove It Works.

Python 3.8+ standard library only. Read-only on the repo: git is only ever
called with read-only subcommands (see GIT_READONLY), project commands run
in the repo folder with a timeout, and the only files this skill writes are
under <repo>/.shipsnag/ (the ledger and Never Twice rules).
"""

import datetime
import fnmatch
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKIP_DIRS = {
    "node_modules", ".git", ".hg", ".svn", "bower_components", ".venv", "venv",
    "__pycache__", ".tox", ".nox", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".gradle", ".idea", "Pods", ".terraform", ".turbo", ".cache", ".parcel-cache",
    "coverage", ".nyc_output", ".pnpm-store", ".yarn", "site-packages", ".eggs",
    ".next", ".nuxt", ".svelte-kit", ".angular", "target", ".shipsnag", ".techfix", ".tinyfix",
    "dist", "build", "out",
}

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tif", ".tiff",
    ".pdf", ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".jar", ".war",
    ".class", ".so", ".dylib", ".dll", ".exe", ".bin", ".woff", ".woff2", ".ttf",
    ".otf", ".eot", ".mp3", ".mp4", ".mov", ".avi", ".webm", ".wav", ".flac",
    ".ogg", ".psd", ".sketch", ".fig", ".db", ".sqlite", ".sqlite3", ".pyc",
    ".pyo", ".o", ".a", ".lib", ".wasm", ".node", ".lockb", ".avif", ".heic",
    ".parquet", ".pkl", ".npy", ".npz", ".h5", ".onnx", ".pt", ".dump",
}

# lockfile name -> package manager (or ecosystem)
LOCKFILES = {
    "package-lock.json": "npm", "npm-shrinkwrap.json": "npm", "yarn.lock": "yarn",
    "pnpm-lock.yaml": "pnpm", "bun.lockb": "bun", "bun.lock": "bun",
    "poetry.lock": "poetry", "uv.lock": "uv", "pipfile.lock": "pipenv",
    "pdm.lock": "pdm", "cargo.lock": "cargo", "go.sum": "go",
    "gemfile.lock": "bundler", "composer.lock": "composer",
}
JS_LOCKS = {"package-lock.json": "npm", "npm-shrinkwrap.json": "npm", "yarn.lock": "yarn",
            "pnpm-lock.yaml": "pnpm", "bun.lockb": "bun", "bun.lock": "bun"}
MANIFESTS = {"package.json", "pyproject.toml", "setup.py", "setup.cfg", "pipfile",
             "cargo.toml", "go.mod", "gemfile", "composer.json"}

CODE_EXT = {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".mts", ".cts",
            ".vue", ".svelte", ".astro", ".py", ".rb", ".go", ".php", ".java",
            ".kt", ".kts", ".cs", ".rs", ".swift", ".dart", ".scala", ".ex",
            ".exs", ".lua", ".sh", ".bash"}
JS_EXT = {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte", ".astro"}
TS_EXT = {".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte"}
PY_EXT = {".py", ".pyi"}
DOC_EXT = {".md", ".mdx", ".rst", ".txt", ".adoc"}
CONFIG_EXT = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"}

GIT_READONLY = {"diff", "log", "show", "rev-parse", "ls-files", "merge-base", "status",
                "symbolic-ref", "for-each-ref", "cat-file", "show-ref", "check-ignore", "grep", "rev-list"}

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

MAX_READ = 2 * 1024 * 1024

# Environment for every project command: no network installs, no prompts.
OFFLINE_ENV = {
    "CI": "1", "FORCE_COLOR": "0", "NO_COLOR": "1", "NO_UPDATE_NOTIFIER": "1",
    "npm_config_update_notifier": "false", "npm_config_offline": "true",
    "npm_config_audit": "false", "npm_config_fund": "false",
    "COREPACK_ENABLE_NETWORK": "0", "COREPACK_ENABLE_DOWNLOAD_PROMPT": "0",
    "YARN_ENABLE_NETWORK": "0", "YARN_ENABLE_TELEMETRY": "0",
    "PIP_NO_INDEX": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1", "UV_OFFLINE": "1",
    "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1",
    "CARGO_NET_OFFLINE": "true", "GOPROXY": "off", "GOFLAGS": "-mod=readonly",
    "HUSKY": "0", "GIT_TERMINAL_PROMPT": "0", "NEXT_TELEMETRY_DISABLED": "1",
    # keep tool caches out of the repo
    "PYTEST_ADDOPTS": "-p no:cacheprovider", "MYPY_CACHE_DIR": os.devnull, "RUFF_NO_CACHE": "true",
}

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\r")


def no_em_dash(text):
    """Safety net: the skill never emits em or en dashes."""
    return text.replace(u"\u2014", "-").replace(u"\u2013", "-")


def posix(rel):
    return rel.replace("\\", "/")


def now_iso():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.date.today().isoformat()


def plural(n, word, many=None):
    return "%d %s" % (n, word if n == 1 else (many or word + "s"))


def read_text(path, limit=MAX_READ):
    """Read a file as text. Returns None for binaries or unreadable files."""
    try:
        with open(path, "rb") as fh:
            data = fh.read(limit)
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def load_json_text(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def ext_of(path):
    base = posix(path).rsplit("/", 1)[-1].lower()
    if base.startswith(".") and base.count(".") == 1:
        return ""
    return os.path.splitext(base)[1]


def base_of(path):
    return posix(path).rsplit("/", 1)[-1]


SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Stripe live secret key", re.compile(r"\b[sr]k_live_[0-9A-Za-z]{16,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_\-]{32,}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{30,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("Slack webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/]{20,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----")),
    ("SendGrid key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\b")),
    ("Database URL with password", re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s:/@'\"]+:([^\s@'\"]{6,})@[^\s'\"]+")),
]


def redact(value):
    value = value or ""
    if len(value) <= 8:
        return "****"
    return "%s...%s" % (value[:4], value[-4:])


GENERIC_OUT_SECRET_RE = re.compile(
    r"(?i)([\w.\-]*(?:passw(?:or)?d|passwd|\bpwd|secret|token|api[_\-]?key|apikey|access[_\-]?key|auth[_\-]?key|"
    r"authorization|client[_\-]?secret|private[_\-]?key|credentials?|session[_\-]?key|signing[_\-]?key)[\w.\-]*)"
    r"(\\?[\"']?\s*[:=]\s*\\?[\"']?)([^\s\"'\\,;}{)(\]\[<>]{4,})")
BEARER_RE = re.compile(r"(?i)\b(Bearer|Basic|Token)\s+([A-Za-z0-9._~+/=\-]{8,})")
SECRET_ENV_NAME_RE = re.compile(r"SECRET|TOKEN|PASSWORD|PASSWD|PASS$|_PASS_|API_?KEY|PRIVATE|CREDENTIAL|DATABASE_URL|_DSN$|^DSN$|AUTH|SESSION_KEY|SIGNING_KEY|ACCESS_KEY", re.I)
_BORING_VALUES = {"true", "false", "null", "none", "undefined", "1", "0", "yes", "no"}


def _env_secret_values():
    vals = []
    for k, v in os.environ.items():
        if not v or len(v) < 8 or v.lower() in _BORING_VALUES:
            continue
        if not SECRET_ENV_NAME_RE.search(k) or k in ("SSH_AUTH_SOCK", "XDG_SESSION_TYPE", "GPG_AGENT_INFO"):
            continue
        if v.startswith("/") and " " not in v and re.match(r"^[\w./\-]+$", v):
            continue  # a path, not a secret
        vals.append(v)
    return sorted(set(vals), key=len, reverse=True)


def redact_text(text):
    """Mask secret-shaped values in command output before showing it: vendor key shapes,
    `password=...` / `"token": "..."` pairs, Bearer/Basic credentials, and the literal values
    of secret-named environment variables."""
    if not text:
        return text
    for v in _env_secret_values():
        if v in text:
            text = text.replace(v, redact(v))
    for _, rx in SECRET_PATTERNS:
        text = rx.sub(lambda m: redact(m.group(0)), text)

    def _kv(m):
        val = m.group(3)
        if val.lower() in _BORING_VALUES or val.lower() in ("bearer", "basic", "token") or re.match(r"^\d{1,6}$", val) or "..." in val or val.startswith(("$", "<", "process.env", "os.environ")):
            return m.group(0)
        return m.group(1) + m.group(2) + redact(val)
    text = GENERIC_OUT_SECRET_RE.sub(_kv, text)
    text = BEARER_RE.sub(lambda m: m.group(1) + " " + redact(m.group(2)), text)
    return text


# ---------------------------------------------------------------------------
# Path classification
# ---------------------------------------------------------------------------

TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "e2e", "testing", "__snapshots__"}
TEST_NAME_RE = re.compile(
    r"(\.test\.|\.spec\.|_test\.(py|go|rb|js|ts)$|^test_.*\.py$|^tests?\.py$|^conftest\.py$|"
    r"_spec\.rb$|Tests?\.(java|kt|cs|swift)$|\.snap$)")


def is_test_path(path):
    p = posix(path)
    parts = p.lower().split("/")
    if set(parts[:-1]) & TEST_DIRS:
        return True
    return bool(TEST_NAME_RE.search(parts[-1])) or bool(TEST_NAME_RE.search(base_of(p)))


def is_snapshot(path):
    p = posix(path).lower()
    return p.endswith(".snap") or "/__snapshots__/" in "/" + p


def is_doc(path):
    p = posix(path).lower()
    base = p.rsplit("/", 1)[-1]
    return ext_of(p) in DOC_EXT or base.startswith(("readme", "changelog", "license", "contributing")) \
        or p.startswith("docs/") or "/docs/" in p


def is_lockfile(path):
    return base_of(path).lower() in LOCKFILES


def is_manifest(path):
    b = base_of(path).lower()
    return b in MANIFESTS or bool(re.match(r"^requirements([-_.][\w.-]+)?\.(txt|in)$", b))


MIGRATION_DIRS = {"migrations", "migration", "migrate", "db_migrations", "schema_migrations"}
MIGRATION_SKIP = {"__init__.py", "readme.md", "readme", "env.py", "script.py.mako",
                  "migration_lock.toml", "alembic.ini", ".gitkeep", "meta", "_journal.json"}


def is_migration(path):
    p = posix(path)
    parts = p.lower().split("/")
    base = parts[-1]
    if base in MIGRATION_SKIP or base.endswith(".md"):
        return False
    dirs = parts[:-1]
    if set(dirs) & MIGRATION_DIRS:
        return True
    if "alembic" in dirs and "versions" in dirs:
        return True
    return False


def is_env_file(path):
    b = base_of(path).lower()
    if b in (".env", ".envrc", ".dev.vars") or b.startswith(".env.") or b.endswith(".env"):
        return True
    return False


def is_env_template(path):
    return is_env_file(path) and bool(re.search(r"(example|sample|template|dist|tpl|defaults|schema)", base_of(path).lower()))


def is_cli_path(path):
    """Files where printing to stdout is the point (CLIs, scripts, tools)."""
    p = posix(path).lower()
    parts = p.split("/")
    base = parts[-1]
    if set(parts[:-1]) & {"bin", "scripts", "script", "tools", "tool", "cli", "commands", "management", "tasks", "examples", "example"}:
        return True
    return bool(re.match(r"^(cli|main|__main__|manage|run|server|index\.cli|setup|noxfile|tasks|build|release)\b", base))


def path_tokens(path):
    """Meaningful lower-case tokens of a path (dirs plus split file stem)."""
    p = posix(path)
    toks = []
    for seg in p.split("/"):
        seg = re.sub(r"\.(test|spec|stories|d)(?=\.)", "", seg)
        stem = seg.split(".")[0] if not seg.startswith(".") else seg.lstrip(".").split(".")[0]
        for t in split_ident(stem):
            toks.append(t)
    return toks


def split_ident(s):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    return [t.lower() for t in re.split(r"[^A-Za-z0-9]+", s) if t]


def stem_word(w):
    w = w.lower()
    if w.endswith("ing") and len(w) > 6:
        w = w[:-3]
        if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "lsz":
            w = w[:-1]
        return w
    if w.endswith("ed") and len(w) > 5 and not w.endswith("eed"):
        return w[:-2] if w[-3] != "i" else w[:-3] + "y"
    for suf in ("ies",):
        if w.endswith(suf) and len(w) > 4:
            return w[:-3] + "y"
    if w.endswith("es") and len(w) > 4 and w[-3] in "sxz":
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
        return w[:-1]
    return w


# ---------------------------------------------------------------------------
# Git (read-only)
# ---------------------------------------------------------------------------

def run_git(cwd, args, timeout=60):
    """Run a read-only git command. Returns (returncode, stdout bytes)."""
    sub = args[0]
    if sub not in GIT_READONLY:
        raise RuntimeError("refusing non read-only git command: %s" % sub)
    cmd = ["git", "-c", "core.quotepath=off", "-c", "core.fsmonitor=false",
           "-c", "safe.directory=*", "-c", "color.ui=false", "-c", "diff.external=",
           "-c", "core.pager=cat"] + list(args)
    env = dict(os.environ)
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
                "GIT_PAGER": "cat", "PAGER": "cat", "LC_ALL": "C"})
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout, env=env)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 127, b""


def dec(b):
    return b.decode("utf-8", "replace")


# ---------------------------------------------------------------------------
# Running project commands
# ---------------------------------------------------------------------------

SHELL_OPS_RE = re.compile(r"&&|\|\||[;|<>`$]|\*")


def resolve_exe(name, repo):
    """Find an executable: local node_modules/.bin (walking up), venv, then PATH."""
    if os.path.isabs(name) or "/" in name or "\\" in name:
        p = os.path.join(repo, name) if not os.path.isabs(name) else name
        return p if os.path.exists(p) else None
    d = os.path.abspath(repo)
    for _ in range(6):
        for cand in (os.path.join(d, "node_modules", ".bin", name),
                     os.path.join(d, "node_modules", ".bin", name + ".cmd")):
            if os.path.exists(cand):
                return cand
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    for venv in (".venv", "venv", "env"):
        for sub in ("bin", "Scripts"):
            for nm in (name, name + ".exe"):
                cand = os.path.join(repo, venv, sub, nm)
                if os.path.exists(cand):
                    return cand
    return shutil.which(name)


def python_exe(repo):
    for venv in (".venv", "venv"):
        for cand in (os.path.join(repo, venv, "bin", "python"),
                     os.path.join(repo, venv, "Scripts", "python.exe")):
            if os.path.exists(cand):
                return cand
    return sys.executable or shutil.which("python3") or shutil.which("python")


_RUNNING = set()
_DEADLINE = [None]


def set_deadline(seconds):
    """Global time budget for every project command of this proof (None = no budget)."""
    _DEADLINE[0] = (time.time() + seconds) if seconds else None


def time_left():
    if _DEADLINE[0] is None:
        return None
    return max(0.0, _DEADLINE[0] - time.time())


def _child_setup():
    """In the child (Linux): die with the parent, even when the parent is SIGKILLed."""
    try:
        import ctypes
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        libc.prctl(1, signal.SIGKILL)  # PR_SET_PDEATHSIG
    except Exception:
        pass


def kill_running():
    for p in list(_RUNNING):
        _kill_tree(p)
        _RUNNING.discard(p)


def install_signal_handlers():
    """When the proof itself is stopped (Bash tool timeout, hook timeout, Ctrl-C), stop the whole
    process group of the command it is running, so no test process is left behind."""
    import atexit

    def handler(signum, frame):
        kill_running()
        try:
            signal.signal(signum, signal.SIG_DFL)
        except (ValueError, OSError):
            pass
        os.kill(os.getpid(), signum)
    for name in ("SIGTERM", "SIGINT", "SIGHUP"):
        sig = getattr(signal, name, None)
        if sig is None:
            continue
        try:
            signal.signal(sig, handler)
        except (ValueError, OSError):
            pass
    atexit.register(kill_running)


SHELL_SYNTAX_RE = re.compile(r"&&|\|\||[;|<>`$*?~(){}]|^\s*\w+=")


def needs_shell(cmdline):
    """True when a command line uses shell syntax (chaining, pipes, redirects, $VARS, globs, VAR=x prefixes)."""
    return bool(SHELL_SYNTAX_RE.search(cmdline))


def split_cmd(cmdline, cwd=None):
    """Exec form (argv list, no shell) for a simple command line; the raw string only when it needs a shell."""
    if needs_shell(cmdline):
        return cmdline, True
    try:
        argv = shlex.split(cmdline)
    except ValueError:
        return cmdline, True
    if not argv:
        return cmdline, True
    if cwd is not None:
        exe = resolve_exe(argv[0], cwd)
        if exe:
            argv[0] = exe
    return argv, False


def run_cmd(cmd, cwd, timeout, shell=False, extra_env=None):
    """Run one project command with a timeout, in cwd, offline env.

    cmd is a list (exec form) or a string (shell form). Returns a dict with
    exit, seconds, timed_out, output (str, ANSI stripped). The command runs in its own
    process group; on timeout, or when this script is stopped, the whole group is killed.
    budget=True means the global time budget was used up before it could start.
    """
    left = time_left()
    if left is not None:
        if left < 2:
            return {"exit": None, "seconds": 0.0, "timed_out": False, "output": "", "error": None, "budget": True}
        if left < timeout:
            timeout = int(max(1, left))
    env = dict(os.environ)
    env.update(OFFLINE_ENV)
    env.update(extra_env or {})
    kw = {}
    if os.name == "posix":
        kw["start_new_session"] = True
        if sys.platform.startswith("linux"):
            kw["preexec_fn"] = _child_setup
    else:
        kw["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    t0 = time.time()
    try:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, env=env, shell=shell, **kw)
    except OSError as e:
        return {"exit": None, "seconds": 0.0, "timed_out": False, "output": "", "error": str(e)}
    _RUNNING.add(p)
    timed_out = False
    try:
        out, _ = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(p)
        try:
            out, _ = p.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            out = b""
    finally:
        _RUNNING.discard(p)
    # a finished command can leave background children in its group (watchers, servers)
    if os.name == "posix":
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass
    secs = time.time() - t0
    text = ANSI_RE.sub("", dec(out or b""))
    return {"exit": p.returncode, "seconds": secs, "timed_out": timed_out, "output": text, "error": None,
            "budget_cut": timed_out and left is not None and timeout < (left + 1) and time_left() is not None and time_left() < 2}


def _kill_tree(p):
    try:
        if os.name == "posix":
            os.killpg(p.pid, signal.SIGKILL)
        else:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
    except Exception:
        try:
            p.kill()
        except Exception:
            pass


def tail(text, n):
    lines = [l.rstrip() for l in text.splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    return lines[-n:]


DANGEROUS_CMD_RE = re.compile(
    r"\b(rm|rmdir|del|rd|mv|sudo|su|curl|wget|ssh|scp|rsync|dd|mkfs|chmod|chown|kill|pkill|"
    r"shutdown|reboot|docker|kubectl|terraform|helm|aws|gcloud|az|vercel|netlify|fly|heroku)\b|"
    r"\bgit\s+(push|reset|checkout|clean|commit|rebase|merge|stash|restore|switch|pull|fetch|tag|branch\s+-[dD])\b|"
    r"\b(install|uninstall|publish|deploy|release|upgrade|update|add|remove|unlink|link|prune|dedupe|login|logout)\b|"
    r"(^|\s)>{1,2}\s*\S|\bnpx\s+(?!--no-install)")

SAFE_RUNNERS = {"npm", "pnpm", "yarn", "bun", "make", "python", "python3", "py", "node", "pytest",
                "ruff", "mypy", "pyright", "flake8", "pylint", "black", "tsc", "eslint", "biome",
                "prettier", "vitest", "jest", "mocha", "cargo", "go", "deno", "uv", "poetry",
                "just", "npx", "pre-commit", "golangci-lint", "rubocop", "bundle", "rake", "dotnet",
                "gradle", "./gradlew", "mvn", "phpunit", "composer", "swift"}


# Auto-detected commands (package.json scripts, Makefile recipes, task tables, conventional
# scripts) are only run when their name and their expanded body look like checks.
UNSAFE_NAME_RE = re.compile(
    r"(?:^|[:_\-./])(deploy|deployment|release|publish|ship|upload|push|migrate|migrations?|seed|db|database|docker|"
    r"k8s|kube|helm|terraform|infra|prod|production|bump|version|tag|clean|reset|nuke|purge|install|uninstall|setup|"
    r"bootstrap|login|logout|start|serve|server|dev|watch|preview|storybook|sync|backup|restore|destroy|teardown|"
    r"provision|rollout|rollback|send|notify|email|mail)(?:$|[:_\-./])", re.I)
_UNSAFE_FIRST = {"sudo", "su", "curl", "wget", "ssh", "scp", "rsync", "dd", "mkfs", "chmod", "chown", "kill", "pkill",
                 "killall", "shutdown", "reboot", "docker", "docker-compose", "podman", "kubectl", "terraform", "helm",
                 "aws", "gcloud", "az", "vercel", "netlify", "fly", "flyctl", "heroku", "firebase", "serverless", "sls",
                 "eas", "gh", "twine", "mv", "del", "rd", "rmdir", "ftp", "sftp", "nc", "psql", "mysql", "mongo", "mongosh",
                 "redis-cli", "supabase", "pulumi", "ansible", "ansible-playbook", "cdk", "sam", "expo", "fastlane"}
_PM_UNSAFE = re.compile(r"^(?:install|i|ci|add|remove|rm|uninstall|publish|unpublish|version|login|logout|deploy|link|"
                        r"unlink|update|upgrade|up|dedupe|prune|pack|release|init|create|dlx)$")
_TOOL_UNSAFE = [
    (re.compile(r"^git$"), re.compile(r"^(push|reset|checkout|clean|commit|rebase|merge|stash|restore|switch|pull|fetch|tag|am|apply|rm|mv|branch|worktree|submodule|gc)$")),
    (re.compile(r"^(pip|pip3|pipx|poetry|pdm|hatch|rye|conda|mamba|gem|bundle|composer|cargo|go|dotnet|mvn|gradle|\./gradlew|\./mvnw)$"),
     re.compile(r"^(install|add|remove|uninstall|lock|update|upgrade|publish|deploy|release|get|login|yank|push|nuget|restore)$")),
    (re.compile(r"^(prisma)$"), re.compile(r"^(migrate|db)$")),
    (re.compile(r"^(drizzle-kit)$"), re.compile(r"^(push|migrate|drop|up)$")),
    (re.compile(r"^(knex|sequelize|typeorm|alembic|flyway|liquibase|dbmate|goose)$"), re.compile(r".")),
    (re.compile(r"^(wrangler)$"), re.compile(r"^(deploy|publish|d1|kv|r2|secret|delete|rollback|versions)$")),
]


def auto_command_unsafe(body, name=None):
    """Why an auto-detected command must not be run automatically, or None when it looks like a check.
    body: the command text with package-manager scripts and Makefile recipes already expanded."""
    if name and UNSAFE_NAME_RE.search(name):
        return "its name (`%s`) says it deploys, publishes, migrates, installs or starts something" % name
    for seg in re.split(r"&&|\|\||;|\n|(?<![|>])\|(?!\|)", body or ""):
        seg = seg.strip().lstrip("@-+").strip()
        if not seg or seg.startswith("#"):
            continue
        if re.search(r"(?:^|[^\d&>])>{1,2}\s*(?!/dev/null|&)[\w./~$\-]", seg):
            return "it writes to a file with a shell redirect (`%s`)" % seg[:60]
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            toks = seg.split()
        while toks and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]) or toks[0] in ("cross-env", "env", "dotenv", "env-cmd", "time", "nice", "exec", "--")):
            toks = toks[1:]
        if not toks:
            continue
        t0 = os.path.basename(toks[0]) if "/" in toks[0] and not toks[0].startswith("./") else toks[0]
        rest = [t for t in toks[1:] if not t.startswith("-")]
        if t0 in _UNSAFE_FIRST:
            return "it runs `%s`" % " ".join(toks[:3])[:60]
        if t0 in ("rm", "rimraf", "del-cli", "shx") and t0 != "rimraf":
            targets = [t for t in toks[1:] if not t.startswith("-") and t != "rm"]
            if not targets or any(t.startswith(("/", "~", "..", "$")) or ".." in t or t in (".", "*", "./", "./*") for t in targets):
                return "it deletes files outside the build folders (`%s`)" % " ".join(toks[:4])[:60]
            continue
        if t0 in ("npm", "pnpm", "yarn", "bun", "npx", "bunx", "pnpx"):
            if t0 == "yarn" and not rest:
                return "a bare `yarn` installs dependencies"
            if rest and _PM_UNSAFE.match(rest[0]) and t0 not in ("npx", "bunx", "pnpx"):
                return "it runs `%s %s`" % (t0, rest[0])
            if t0 in ("npm", "pnpm", "yarn", "bun") and rest and rest[0] in ("run", "run-script") and len(rest) > 1 and UNSAFE_NAME_RE.search(rest[1]):
                return "it runs the `%s` script" % rest[1]
            continue
        if t0 in ("python", "python3", "py") and len(toks) > 2 and toks[1] == "-m" and toks[2] in ("pip", "twine", "build"):
            return "it runs `python -m %s`" % toks[2]
        if t0 in ("python", "python3") and rest and base_of(rest[0]) == "manage.py" and len(rest) > 1 and rest[1] in ("migrate", "flush", "loaddata", "runserver", "createsuperuser", "dbshell", "collectstatic"):
            return "it runs `manage.py %s`" % rest[1]
        for tool_rx, sub_rx in _TOOL_UNSAFE:
            if tool_rx.match(t0) and rest and sub_rx.match(rest[0]):
                return "it runs `%s %s`" % (t0, rest[0])
        if t0 in ("rails", "rake", "bin/rails") and rest and rest[0].startswith("db:"):
            return "it runs `%s %s`" % (t0, rest[0])
    return None


def command_is_safe(cmd):
    """Required commands from rule files must look like checks, never installs or deletes."""
    c = cmd.strip()
    if not c or DANGEROUS_CMD_RE.search(c):
        return False
    for seg in re.split(r"&&|\|\||;", c):
        seg = seg.strip()
        if not seg:
            continue
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            return False
        while toks and re.match(r"^[A-Z_][A-Z0-9_]*=", toks[0]):
            toks = toks[1:]
        if not toks or toks[0] not in SAFE_RUNNERS:
            return False
    return True


# ---------------------------------------------------------------------------
# Minimal TOML reader (tomllib when available)
# ---------------------------------------------------------------------------

def load_toml(text):
    try:
        import tomllib  # Python 3.11+
        return tomllib.loads(text)
    except ImportError:
        pass
    except Exception:
        return {}
    return _mini_toml(text)


def _mini_toml(text):
    """Enough TOML for pyproject sections, string/array/inline-table values."""
    root = {}
    cur = root
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].split(" #")[0].strip() if not lines[i].strip().startswith("#") else ""
        i += 1
        if not line:
            continue
        m = re.match(r"^\[\[?([^\]]+)\]\]?$", line)
        if m:
            cur = root
            for k in [x.strip().strip('"') for x in m.group(1).split(".")]:
                cur = cur.setdefault(k, {})
            continue
        m = re.match(r"^([\w.\-\"']+)\s*=\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1).strip('"\''), m.group(2).strip()
        if val.startswith("[") and val.count("[") > val.count("]"):
            while i < len(lines) and val.count("[") > val.count("]"):
                val += " " + lines[i].split(" #")[0].strip()
                i += 1
        cur[key] = _mini_val(val)
    return root


def _mini_val(v):
    v = v.strip()
    if v.startswith(('"""', "'''")):
        return v.strip("\"'")
    if v.startswith(("\"", "'")):
        return v[1:v.rfind(v[0])] if v.rfind(v[0]) > 0 else v.strip("\"'")
    if v.startswith("["):
        return [x for x in (s.strip().strip("\"'") for s in re.findall(r"\"[^\"]*\"|'[^']*'", v)) if x]
    if v.startswith("{"):
        d = {}
        for k, s in re.findall(r"([\w\-]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^,}]+)", v):
            d[k] = s.strip().strip("\"'")
        return d
    if v in ("true", "false"):
        return v == "true"
    return v


# ---------------------------------------------------------------------------
# The change: working tree vs a base ref
# ---------------------------------------------------------------------------

class FileChange(object):
    __slots__ = ("path", "old_path", "status", "binary", "added", "removed", "untracked", "size", "hunks", "folder_files",
                 "skip")

    def __init__(self, path, status, old_path=None):
        self.path = path
        self.old_path = old_path or path
        self.status = status          # A, M, D, R
        self.binary = False
        self.added = []               # [(new_lineno, text)]
        self.removed = []             # [(old_lineno, text)]
        self.untracked = False
        self.size = 0
        self.hunks = []               # [{"removed": [...], "added": [...]}] per diff hunk
        self.folder_files = 0         # >0: a whole untracked folder, reported as one entry
        self.skip = None              # why line checks skip this file (minified, generated, vendored)

    def to_json(self):
        d = {"path": self.path, "old_path": self.old_path if self.old_path != self.path else None,
             "status": self.status, "binary": self.binary, "untracked": self.untracked,
             "added_lines": len(self.added), "removed_lines": len(self.removed), "size": self.size}
        if self.folder_files:
            d["folder_files"] = self.folder_files
        return d


class Change(object):
    def __init__(self):
        self.ok = False
        self.reason = ""
        self.base = None
        self.base_label = ""
        self.how = ""
        self.files = []
        self.repo = None
        self._old = {}
        self.nochange = False     # nothing to inspect (clean tree, nothing new since the base)
        self.notes = []           # plain-English caveats about how the change was chosen
        self.shallow = None
        self.commits = 0          # commits between the base and HEAD that are part of the change
        self.dirty = False
        self.head = None

    def by_path(self):
        return {f.path: f for f in self.files}

    def old_text(self, path):
        """File content at the base ref (None if absent)."""
        if path in self._old:
            return self._old[path]
        txt = None
        if self.base and self.base != EMPTY_TREE:
            code, out = run_git(self.repo, ["show", "%s:./%s" % (self.base, path)])
            if code == 0 and b"\0" not in out[:8192]:
                txt = dec(out)
        self._old[path] = txt
        return txt

    def new_text(self, path):
        return read_text(os.path.join(self.repo, path))


def _unquote(p):
    p = p.strip()
    if p.startswith('"') and p.endswith('"'):
        p = p[1:-1]
        try:
            p = bytes(p, "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
        except Exception:
            pass
    return p


def git_info(repo):
    code, out = run_git(repo, ["rev-parse", "--is-inside-work-tree"])
    if code != 0 or out.strip() != b"true":
        return None
    info = {"has_head": run_git(repo, ["rev-parse", "--verify", "-q", "HEAD"])[0] == 0}
    code, out = run_git(repo, ["rev-parse", "--show-toplevel"])
    info["toplevel"] = dec(out).strip() if code == 0 else repo
    code, out = run_git(repo, ["symbolic-ref", "-q", "--short", "HEAD"])
    info["branch"] = dec(out).strip() if code == 0 else None
    code, out = run_git(repo, ["rev-parse", "--is-shallow-repository"])
    info["shallow"] = dec(out).strip() == "true" if code == 0 else None
    return info


def repo_root(path):
    """The git top-level folder for path, or None."""
    code, out = run_git(path, ["rev-parse", "--show-toplevel"])
    if code != 0:
        return None
    return dec(out).strip() or None


def default_branch(repo):
    code, out = run_git(repo, ["symbolic-ref", "-q", "refs/remotes/origin/HEAD"])
    if code == 0 and out.strip():
        return dec(out).strip().replace("refs/remotes/", "")
    for name in ("main", "master", "trunk", "develop"):
        for ref in ("refs/heads/" + name, "refs/remotes/origin/" + name):
            if run_git(repo, ["rev-parse", "--verify", "-q", ref])[0] == 0:
                return ref.replace("refs/heads/", "").replace("refs/remotes/", "")
    return None


def is_dirty(repo, ignore):
    code, out = run_git(repo, ["status", "--porcelain", "-z", "--untracked-files=normal", "--", "."])
    if code != 0:
        return False
    for ent in dec(out).split("\0"):
        if len(ent) < 4:
            continue
        p = posix(ent[3:])
        if p.startswith((".shipsnag/", ".techfix/")) or p in ignore:
            continue
        return True
    return False


def _rev(repo, ref):
    code, out = run_git(repo, ["rev-parse", "--verify", "-q", ref + "^{commit}"])
    return dec(out).strip() if code == 0 else None


def _same_branch(branch, db):
    return bool(branch and db and (branch == db or branch == db.split("/", 1)[-1]))


def _ago(ts):
    secs = max(0, time.time() - ts)
    if secs < 3600:
        return "%d minutes ago" % max(1, secs // 60)
    if secs < 172800:
        return "%d hours ago" % (secs // 3600)
    return "%d days ago" % (secs // 86400)


RECENT_COMMIT_SECS = 24 * 3600


def choose_base(ch, info, base=None, ignore=(), since_ref=None):
    """Pick the base ref of the change. Sets ch.base/base_label/how/nochange/notes and returns
    False when the change cannot be inspected (ch.reason set)."""
    repo = ch.repo
    ch.dirty = is_dirty(repo, ignore)
    ch.shallow = info.get("shallow")
    ch.head = _rev(repo, "HEAD") if info["has_head"] else None
    if base:
        b = _rev(repo, base)
        if not b:
            ch.reason = "base ref %r not found" % base
            return False
        ch.base, ch.base_label = b, base
        ch.how = "working tree vs %s (--base)" % base
        return True
    if not info["has_head"]:
        ch.base, ch.base_label = EMPTY_TREE, "empty tree"
        ch.how = "no commits yet: every file is new"
        return True
    if since_ref and since_ref != ch.head:
        ch.base, ch.base_label = since_ref, "session start"
        ch.how = "work since this session started (commits%s)" % (" and uncommitted changes" if ch.dirty else "")
        return True
    branch = info.get("branch")
    db = default_branch(repo)
    mb = None
    if db:
        code, out = run_git(repo, ["merge-base", "HEAD", db])
        if code == 0:
            mb = dec(out).strip()
        elif ch.shallow:
            ch.notes.append("Shallow clone: the merge-base with %s is not in the local history, so commits on this branch were not inspected (run `git fetch --unshallow` to include them)." % db)
    where = ("branch `%s`" % branch) if branch else "detached HEAD"
    if mb and mb != ch.head:
        code, out = run_git(repo, ["rev-list", "--count", "%s..HEAD" % mb])
        ch.commits = int(dec(out).strip() or 0) if code == 0 else 0
        ch.base, ch.base_label = mb, "merge-base with %s" % db
        if _same_branch(branch, db):
            what = "%d local commit%s not yet on %s" % (ch.commits, "" if ch.commits == 1 else "s", db)
        else:
            what = "%d commit%s since the merge-base with %s" % (ch.commits, "" if ch.commits == 1 else "s", db)
        ch.how = "%s: %s%s" % (where, what, " plus uncommitted changes" if ch.dirty else "")
        return True
    if ch.dirty:
        ch.base, ch.base_label = ch.head, "HEAD"
        ch.how = "uncommitted changes vs HEAD" + ("" if branch else " (detached HEAD)")
        return True
    # clean tree at the tip of the default branch (or detached there): is there a change at all?
    code, out = run_git(repo, ["log", "-1", "--format=%P%x00%ct%x00%h"])
    parts = dec(out).strip().split("\0") if code == 0 else []
    parents = parts[0].split() if parts else []
    when = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    short = parts[2] if len(parts) > 2 else "HEAD"
    label = where if (not branch or not _same_branch(branch, db or branch)) else "`%s`" % branch
    if len(parents) >= 2:
        ch.nochange = True
        ch.how = "clean tree on %s and the last commit (%s) is a merge: no change of yours to inspect" % (label, short)
        ch.notes.append("No change to prove: the working tree is clean and HEAD is a merge commit, so its first-parent diff is someone else's work. Pass --base <ref> to inspect earlier commits.")
        return True
    if not parents and ch.shallow:
        ch.nochange = True
        ch.how = "clean tree in a shallow clone; HEAD's parent is not available: no change to inspect"
        ch.notes.append("Shallow clone: HEAD's parent is not in the local history, so there is no diff to inspect (the whole repo is not \"the change\"). Pass --base <ref> or run `git fetch --unshallow`.")
        return True
    if not parents and not (when and time.time() - when > RECENT_COMMIT_SECS):
        ch.base, ch.base_label = EMPTY_TREE, "empty tree"
        ch.how = "clean tree with a single commit: checked that commit"
        return True
    if not parents:
        ch.nochange = True
        ch.how = "clean tree with a single commit from %s: no recent change to inspect" % _ago(when)
        ch.notes.append("No change to prove: nothing is uncommitted and the only commit is %s old. Pass --base <ref> to inspect it." % _ago(when).replace(" ago", ""))
        return True
    prev = _rev(repo, "HEAD~1")
    if not prev:
        ch.nochange = True
        ch.how = "clean tree on %s; the parent commit is not in this shallow clone: no change to inspect" % label
        ch.notes.append("Shallow clone: HEAD's parent is not available, so there is no diff to inspect. Pass --base <ref> or run `git fetch --unshallow`.")
        return True
    if when and time.time() - when > RECENT_COMMIT_SECS:
        ch.nochange = True
        ch.how = "clean tree on %s; the last commit (%s) is from %s: no recent change to inspect" % (label, short, _ago(when))
        ch.notes.append("No change to prove: nothing is uncommitted and the last commit is %s old. Pass --base <ref> to inspect committed work." % _ago(when).replace(" ago", ""))
        return True
    ch.base, ch.base_label = prev, "HEAD~1"
    ch.how = "clean tree on %s: checked the last commit (%s, %s)" % (label, short, _ago(when) if when else "time unknown")
    return True


def _count_files(path, cap):
    n = 0
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        n += len(filenames)
        if n > cap:
            return n
    return n


UNTRACKED_FOLDER_GROUP = 20


def load_change(repo, base=None, ignore=(), since_ref=None):
    """Work out the change to inspect and parse it into FileChange objects."""
    ch = Change()
    ch.repo = os.path.abspath(repo)
    ignore = set(posix(i) for i in ignore)
    info = git_info(ch.repo)
    if not info:
        ch.reason = "not a git repository, so the change could not be inspected"
        return ch
    if not choose_base(ch, info, base, ignore, since_ref):
        return ch
    if run_git(ch.repo, ["rev-parse", "-q", "--verify", "MERGE_HEAD"])[0] == 0:
        ch.notes.append("A merge is in progress: the change includes everything the merge brings in.")
    if os.path.isfile(os.path.join(info.get("toplevel") or ch.repo, ".gitmodules")):
        ch.notes.append("Submodules exist: changes inside them are not inspected.")
    if ch.nochange:
        ch.ok = True
        return ch
    excl = [":(exclude).shipsnag", ":(exclude).techfix"] + [":(exclude)%s" % i for i in ignore]
    code, out = run_git(ch.repo, ["diff", "--no-color", "--no-ext-diff", "-U0", "-M",
                                  "--src-prefix=a/", "--dst-prefix=b/", "--relative",
                                  "--ignore-submodules", ch.base, "--", "."] + excl, timeout=120)
    if code != 0:
        ch.reason = "git diff failed"
        return ch
    ch.files = _parse_patch(dec(out))
    code, out = run_git(ch.repo, ["ls-files", "-z", "--others", "--exclude-standard", "--directory", "--no-empty-directory", "--", "."])
    if code == 0:
        seen = set(f.path for f in ch.files)
        for p in sorted(set(posix(x) for x in dec(out).split("\0") if x)):
            if p in seen or p.startswith((".shipsnag/", ".techfix/")) or p in ignore or p.rstrip("/") in ignore:
                continue
            full = os.path.join(ch.repo, p)
            if p.endswith("/"):
                n = _count_files(full, 100000)
                if n > UNTRACKED_FOLDER_GROUP:
                    fc = FileChange(p.rstrip("/"), "A")
                    fc.untracked = True
                    fc.binary = True
                    fc.folder_files = n
                    ch.files.append(fc)
                    continue
                code2, out2 = run_git(ch.repo, ["ls-files", "-z", "--others", "--exclude-standard", "--", p])
                subs = sorted(set(posix(x) for x in dec(out2).split("\0") if x)) if code2 == 0 else []
            else:
                subs = [p]
            for q in subs:
                if q in seen or q in ignore:
                    continue
                fullq = os.path.join(ch.repo, q)
                if os.path.islink(fullq) or not os.path.isfile(fullq):
                    continue
                fc = FileChange(q, "A")
                fc.untracked = True
                txt = read_text(fullq)
                if txt is None or ext_of(q) in BINARY_EXT:
                    fc.binary = True
                else:
                    fc.added = [(i + 1, l) for i, l in enumerate(txt.splitlines())]
                ch.files.append(fc)
    for f in ch.files:
        try:
            f.size = os.path.getsize(os.path.join(ch.repo, f.path)) if f.status != "D" and not f.folder_files else 0
        except OSError:
            f.size = 0
    ch.ok = True
    return ch


HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _parse_patch(text):
    files = []
    cur = None
    old_ln = new_ln = 0
    for line in text.split("\n"):
        if line.startswith("diff --git "):
            m = re.match(r'^diff --git (?:"?a/)(.*?)"? (?:"?b/)(.*?)"?$', line)
            a = b = None
            if m:
                a, b = _unquote(m.group(1)), _unquote(m.group(2))
            cur = FileChange(posix(b or ""), "M", posix(a or ""))
            files.append(cur)
            continue
        if cur is None:
            continue
        if line.startswith("new file mode"):
            cur.status = "A"
        elif line.startswith("deleted file mode"):
            cur.status = "D"
        elif line.startswith("rename from "):
            cur.old_path = posix(_unquote(line[len("rename from "):]))
            cur.status = "R"
        elif line.startswith("rename to "):
            cur.path = posix(_unquote(line[len("rename to "):]))
        elif line.startswith("Binary files ") or line.startswith("GIT binary patch"):
            cur.binary = True
        elif line.startswith("--- "):
            src = line[4:]
            if src.strip() != "/dev/null":
                cur.old_path = posix(_unquote(src)[2:] if _unquote(src).startswith("a/") else _unquote(src))
        elif line.startswith("+++ "):
            dst = line[4:]
            if dst.strip() != "/dev/null":
                cur.path = posix(_unquote(dst)[2:] if _unquote(dst).startswith("b/") else _unquote(dst))
            else:
                cur.path = cur.old_path
        elif line.startswith("@@"):
            m = HUNK_RE.match(line)
            if m:
                old_ln = int(m.group(1))
                new_ln = int(m.group(3))
                cur.hunks.append({"removed": [], "added": []})
        elif line.startswith("+"):
            cur.added.append((new_ln, line[1:]))
            if cur.hunks:
                cur.hunks[-1]["added"].append((new_ln, line[1:]))
            new_ln += 1
        elif line.startswith("-"):
            cur.removed.append((old_ln, line[1:]))
            if cur.hunks:
                cur.hunks[-1]["removed"].append((old_ln, line[1:]))
            old_ln += 1
        elif line.startswith(" "):
            old_ln += 1
            new_ln += 1
    return [f for f in files if f.path]


# ---------------------------------------------------------------------------
# Files whose lines are not hand-written (skipped by the line checks)
# ---------------------------------------------------------------------------

VENDOR_DIRS = {"vendor", "vendors", "third_party", "third-party", "thirdparty", "node_modules", "bower_components",
               "external", "externals", "site-packages", "jspm_packages", "web_modules"}
GENERATED_DIRS = {"generated", "__generated__", "codegen", "autogen", "auto-generated", "gen-src"}
MINIFIED_NAME_RE = re.compile(r"[.\-_](?:min|bundle|chunk|umd|prod|production)\.(?:js|mjs|cjs|css)$|\.min\.\w+$|"
                              r"\.pb\.go$|_pb2(?:_grpc)?\.pyi?$|\.g\.dart$|\.freezed\.dart$|\.generated\.\w+$|"
                              r"\.gen\.(?:ts|js|go|py)$|(?:^|/)worker-configuration\.d\.ts$", re.I)
GENERATED_MARK_RE = re.compile(r"@generated\b|\bDO NOT EDIT\b|\bdo not edit\b|\bauto-?generated\b|\bautogenerated\b|"
                               r"\bgenerated (?:by|from|with|automatically)\b|this file (?:is|was|has been) (?:auto-?)?generated|"
                               r"Code generated .* DO NOT EDIT", re.I)
LONG_LINE = 2000


def generated_marker(text, lines=8):
    """The generated-file marker in a file's first lines, or None."""
    if not text:
        return None
    head = "\n".join(text.splitlines()[:lines])[:4000]
    m = GENERATED_MARK_RE.search(head)
    return m.group(0) if m else None


def content_skip_reason(path, added, head_text=None):
    """Why the line checks should not read this file: minified, generated or vendored.
    added: [(lineno, text)]; head_text: the first lines of the new file (for markers)."""
    p = posix(path)
    parts = [x.lower() for x in p.split("/")]
    if set(parts[:-1]) & VENDOR_DIRS:
        return "vendored code"
    if set(parts[:-1]) & GENERATED_DIRS:
        return "generated code (generated/ folder)"
    if MINIFIED_NAME_RE.search(p):
        return "minified or generated (file name)"
    longest = max([len(t) for _, t in added[:5000]] or [0])
    if longest > 20000 or (added and sum(len(t) for _, t in added[:2000]) / float(min(len(added), 2000)) > 400):
        return "minified (very long lines)"
    mark = generated_marker(head_text if head_text is not None else "\n".join(t for _, t in added[:8]))
    if mark:
        return "generated (\"%s\" in its header)" % mark
    return None


# ---------------------------------------------------------------------------
# Searching the working tree (git grep: fast, respects .gitignore, no file cap)
# ---------------------------------------------------------------------------

DOC_EXCLUDES = [":(exclude)*.md", ":(exclude)*.mdx", ":(exclude)*.rst", ":(exclude)*.txt", ":(exclude)*.adoc"]


def _grep_variants(needle):
    words = split_ident(needle)
    out = {needle}
    if len(words) > 1:
        out |= {"_".join(words), "-".join(words), "".join(words)}
    return sorted(out)


def tree_has(repo, needle, skip_paths=(), docs=True, code_only=False, variants=True, ignore_case=True):
    """Does any text file in the working tree (tracked or untracked, not ignored) contain needle?
    Compared without case and with user_id / userId / user-id treated alike.
    Returns True/False, or None when git grep is not available (not a git repo)."""
    args = ["grep", "-q", "-I", "-F", "--untracked"]
    if ignore_case:
        args.append("-i")
    for v in (_grep_variants(needle) if variants else [needle]):
        args += ["-e", v]
    args += ["--", "."]
    if not docs:
        args += DOC_EXCLUDES
    if code_only:
        args += [":(exclude)*.json", ":(exclude)*.lock", ":(exclude)*.yaml", ":(exclude)*.yml"]
    for sp in sorted(skip_paths or ())[:50]:
        args.append(":(exclude,literal)%s" % sp)
    code, _ = run_git(repo, args, timeout=60)
    if code == 0:
        return True
    if code == 1:
        return False
    return None


def tree_files_with(repo, needles, skip_paths=(), limit=300):
    """Files (tracked or untracked, not ignored) containing any needle (case-insensitive), or None."""
    args = ["grep", "-l", "-I", "-F", "-i", "--untracked"]
    for n in needles:
        for v in _grep_variants(n):
            args += ["-e", v]
    args += ["--", "."]
    for sp in sorted(skip_paths or ())[:50]:
        args.append(":(exclude,literal)%s" % sp)
    code, out = run_git(repo, args, timeout=60)
    if code == 1:
        return []
    if code != 0:
        return None
    return [posix(x) for x in dec(out).splitlines() if x][:limit]


# ---------------------------------------------------------------------------
# Task text
# ---------------------------------------------------------------------------

STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "when", "then", "than",
        "should", "must", "will", "can", "not", "are", "was", "were", "have", "has", "add",
        "make", "sure", "also", "only", "all", "any", "but", "use", "using", "new", "fix",
        "update", "change", "file", "files", "code", "please", "our", "your", "you", "its",
        "it's", "each", "per", "via", "out", "off", "let", "get", "set", "one", "two"}


def task_words(text):
    words = set()
    for raw in re.findall(r"[A-Za-z_$][\w$\-]*", text or ""):
        for t in split_ident(raw) + [raw.lower()]:
            if len(t) >= 3 and t not in STOP:
                words.add(t)
                words.add(stem_word(t))
    return words


PATH_TOKEN_RE = re.compile(r"(?:\./)?(?:[\w.@\-]+/)+[\w.@\-*]*|[\w@\-]+\.(?:js|mjs|cjs|jsx|ts|tsx|py|rb|go|rs|java|kt|cs|php|sql|json|ya?ml|toml|md|css|scss|html|vue|svelte|sh|txt|cfg|ini|lock)\b")


def task_paths(text):
    out = []
    for m in PATH_TOKEN_RE.finditer(text or ""):
        p = m.group(0).strip("./") if m.group(0).startswith("./") else m.group(0)
        p = p.rstrip(".,;:)")
        if p.startswith(("http", "www.")) or "://" in p or len(p) < 3:
            continue
        if re.match(r"^\d", p):
            continue
        out.append(posix(p))
    return out


# ---------------------------------------------------------------------------
# Ledger
# ---------------------------------------------------------------------------

def write_ledger(repo_root, skill, verdict, extra):
    """Append one line to <repo>/.shipsnag/ledger.md. Never code or secrets."""
    d = os.path.join(repo_root, ".shipsnag")
    try:
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "ledger.md")
        new = not os.path.exists(path)
        with open(path, "a", encoding="utf-8") as fh:
            if new:
                fh.write("# ShipSnag ledger\n\n")
            fh.write(no_em_dash("- %s | %s | %s | %s\n" % (now_iso(), skill, verdict, extra)))
        return path
    except OSError:
        return None


def glob_match(path, pattern):
    """Match a repo-relative path against a rule glob or directory prefix."""
    path = posix(path).lstrip("./")
    pat = posix(pattern).strip()
    if pat.startswith("./"):
        pat = pat[2:]
    pat = pat.lstrip("/")
    if not pat:
        return False
    if pat.endswith("/"):
        return path.startswith(pat)
    if any(c in pat for c in "*?["):
        if fnmatch.fnmatchcase(path, pat):
            return True
        if pat.endswith("/**") and path.startswith(pat[:-3]):
            return True
        if "/" not in pat and fnmatch.fnmatchcase(base_of(path), pat):
            return True
        return False
    if path == pat or path.startswith(pat.rstrip("/") + "/"):
        return True
    return False


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

def finding(cause, title, finding_text, evidence, impact, fix, file=None, line=None,
            tier="problem", also=(), files=(), key=None):
    """One finding in the 4-part format. tier: problem (blocks PROVEN) or check.
    Evidence passes through redact_text, so no line can carry a full secret."""
    causes = [cause] + [c for c in also if c != cause]
    allf = []
    for p in ([file] if file else []) + list(files):
        if p and p not in allf:
            allf.append(p)
    gtitle = title
    for p in allf:
        gtitle = gtitle.replace(p, "<file>")
    return {"cause": cause, "causes": causes, "tier": tier, "file": file, "line": line,
            "files": allf, "title": title, "finding": finding_text,
            "evidence": [redact_text(e) for e in evidence if e], "impact": impact,
            "fix": fix if isinstance(fix, list) else [fix], "key": key or "%s:%s:%s" % (cause, file, line),
            "id": "%s-%s:%s" % (cause, file or "repo", line or 0), "group": "%d:%s" % (cause, gtitle)}


def is_comment_line(text):
    s = text.strip()
    return s.startswith(("//", "#", "/*", "*", "<!--", "--", ";;")) and not s.startswith("#!")


def strip_strings_comments(line, ext):
    """Remove string literals and trailing comments from one code line (rough)."""
    s = re.sub(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`", "\"\"", line)
    if ext in PY_EXT or ext in (".rb", ".sh", ".bash", ".toml", ".yaml", ".yml"):
        s = s.split("#", 1)[0]
    else:
        s = re.sub(r"//.*$", "", s)
        s = re.sub(r"/\*.*?\*/", "", s)
    return s
