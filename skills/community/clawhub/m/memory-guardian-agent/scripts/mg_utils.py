"""memory-guardian: Shared utilities (v0.4.5).

Provides atomic save_meta/load_meta, tokenization, Jaccard distance,
memory_id generation, file locking, and index building.

Usage:
    from mg_utils import load_meta, save_meta, _now_iso, tokenize, jaccard_distance, CST
    from mg_utils import generate_memory_id, derive_file_path, file_lock_acquire
"""

import json
import locale
import os
import re
import sys
import tempfile
import builtins
import fcntl
import hashlib
import shutil
import time
import uuid
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager

# Timezone constants
CST = timezone(timedelta(hours=8))

# Default workspace path
DEFAULT_WORKSPACE = os.environ.get(
    "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
)


def workspace_path(*parts, workspace=None):
    """Resolve an absolute path within the memory workspace.

    Args:
        *parts: Path components to join under the workspace root.
        workspace: Explicit workspace path (falls back to OPENCLAW_WORKSPACE env,
                   then DEFAULT_WORKSPACE).

    Returns:
        Absolute path string.
    """
    base_workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", DEFAULT_WORKSPACE)
    return os.path.join(base_workspace, *parts)

# Quadrant TTL for case types (canonical definition — used by decay + case_grow)
CASE_TTL = {
    "absorb": 30,
    "derive": 90,
    "new_type": 180,
    "suspend": 365,
}

MEMORY_TYPE_ALPHA_DEFAULTS = {
    "static": 1.0,
    "derive": 2.0,
    "absorb": 3.0,
}

MEMORY_TYPE_BETA_CAP_DEFAULTS = {
    "static": 1.0,
    "derive": 3.0,
    "absorb": 3.5,
}

PROVENANCE_CONFIDENCE_DEFAULTS = {
    "L1": {"base": 0.6, "auth_mult": 1.0},
    "L2": {"base": 0.5, "auth_mult": 0.9},
    "L3": {"base": 0.4, "auth_mult": 0.7},
}

DEFAULT_VERIFICATION_BONUS_PER = 0.1
DEFAULT_VERIFICATION_BONUS_CAP = 0.3

# Shared cooling threshold (used by decay + ingest)
COOLING_THRESHOLD = 5


def _now_iso():
    """Return current CST time as ISO-8601 string.

    All memory-guardian modules use CST (Asia/Shanghai, UTC+8) consistently.
    """
    return datetime.now(CST).isoformat()


def read_text_file(path, encodings=None):
    """Read text files with pragmatic encoding fallbacks.

    Prefers UTF-8, but accepts common Windows local encodings so legacy
    workspace files and test fixtures do not crash the CLI.
    """
    preferred = locale.getpreferredencoding(False) or "utf-8"
    candidates = encodings or ["utf-8", "utf-8-sig", preferred, "gbk", "cp936"]
    seen = set()
    last_error = None

    for encoding in candidates:
        if not encoding or encoding in seen:
            continue
        seen.add(encoding)
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise FileNotFoundError(path)


def console_safe_text(text, encoding=None):
    """Return a console-safe version of text for legacy Windows encodings."""
    replacements = {
        "—": "-",
        "–": "-",
        "―": "-",
        "−": "-",
        "→": "->",
        "←": "<-",
        "↔": "<->",
        "×": "x",
        "•": "*",
        "✓": "[OK]",
        "✗": "[X]",
        "✔": "[OK]",
        "✂": "[CUT]",
        "📁": "[META]",
        "📦": "[ARCHIVE]",
        "🗑️": "[DELETE]",
        "🗑": "[DELETE]",
        "📝": "[NOTE]",
        "👁️": "[OBSERVE]",
        "👁": "[OBSERVE]",
        "⏸️": "[PAUSE]",
        "⏸": "[PAUSE]",
        "❓": "[?]",
        "🔒": "[LOCK]",
        "⚡": "[CONFLICT]",
        "⚠️": "[WARN]",
        "⚠": "[WARN]",
        "✅": "[OK]",
        "ℹ️": "[INFO]",
        "ℹ": "[INFO]",
        "📤": "[UNARCHIVE]",
        "📌": "[PIN]",
        "🔄": "[SYNC]",
        "🔴": "[CRITICAL]",
        "🟡": "[WARN]",
        "🟢": "[OK]",
        "🔵": "[INFO]",
        "🚫": "[BLOCK]",
        "📊": "[STATS]",
        "🔍": "[SCAN]",
        "🔁": "[DEDUP]",
        "📈": "[TOTAL]",
        "💡": "[TIP]",
        "🗂️": "[ROTATE]",
        "🗂": "[ROTATE]",
        "🧹": "[CLEAN]",
        "🚰": "[FLUSH]",
        "📋": "[HISTORY]",
        "📢": "[NOTIFY]",
        "🎯": "[SIM]",
        "⬜": "[ ]",
        "█": "#",
        "─": "-",
    }

    normalized = str(text)
    for src, dst in replacements.items():
        normalized = normalized.replace(src, dst)

    target_encoding = encoding or getattr(sys.stdout, "encoding", None) or locale.getpreferredencoding(False) or "utf-8"
    return normalized.encode(target_encoding, errors="replace").decode(target_encoding)


def _should_force_console_safe(encoding):
    """Return True when a console likely cannot render rich Unicode safely."""
    if not encoding:
        return False
    normalized = str(encoding).lower().replace("_", "-")
    return not normalized.startswith("utf-")


def safe_print(*args, sep=" ", end="\n", file=None, flush=False):
    """Print with a fallback for legacy Windows console encodings."""
    target = file or sys.stdout
    encoding = getattr(target, "encoding", None)

    if _should_force_console_safe(encoding):
        text = sep.join(str(arg) for arg in args)
        target.write(console_safe_text(text, encoding=encoding))
        if end:
            target.write(console_safe_text(end, encoding=encoding))
        if flush and hasattr(target, "flush"):
            target.flush()
        return

    try:
        builtins.print(*args, sep=sep, end=end, file=file, flush=flush)
    except UnicodeEncodeError:
        text = sep.join(str(arg) for arg in args)
        target.write(console_safe_text(text, encoding=encoding))
        if end:
            target.write(console_safe_text(end, encoding=encoding))
        if flush and hasattr(target, "flush"):
            target.flush()


def load_meta(path):
    """Load meta.json with safe defaults.

    Returns:
        dict: meta.json content, or default empty structure if file missing
    """
    if not os.path.exists(path):
        return {
            "version": "0.4.5",
            "memories": [],
            "conflicts": [],
            "security_rules": [],
            "entities": {},
        }
    try:
        return json.loads(read_text_file(path))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Corrupted file — backup before returning empty to prevent data loss
        try:
            ts = datetime.now(CST).strftime("%Y%m%d%H%M%S")
            backup_path = f"{path}.corrupted.{ts}"
            shutil.copy2(path, backup_path)
        except OSError:
            pass
        return {
            "version": "0.4.5",
            "memories": [],
            "conflicts": [],
            "security_rules": [],
            "entities": {},
            "_load_error": True,
        }


def save_meta(path, meta, use_lock=True):
    """Atomically save meta.json using write-to-temp + rename.

    Prevents data corruption from concurrent writes or interrupted writes.
    On POSIX systems, rename() is atomic within the same filesystem.

    Args:
        path: Path to meta.json.
        meta: Dict to serialize.
        use_lock: If True (default), acquire file lock before writing.

    Falls back to direct write if temp file + rename fails (e.g., cross-device).
    """
    if meta.get("_load_error"):
        raise ValueError(
            "Refusing to save meta: previous load_meta() detected a corrupted file. "
            "Inspect the backup file and manually repair meta.json before saving."
        )

    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Ensure JSON-serializable
    content = json.dumps(meta, ensure_ascii=True, indent=2)

    def _write_content():
        try:
            # Write to temp file in same directory (same filesystem for atomic rename)
            fd, tmp_path = tempfile.mkstemp(
                suffix=".tmp",
                prefix=".meta_",
                dir=dir_name or ".",
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(content)
                # Atomic rename
                os.replace(tmp_path, path)
            except Exception:
                # Clean up temp file if rename failed
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        except Exception:
            # Fallback: direct write (non-atomic but better than losing data)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    if use_lock:
        with file_lock_acquire(path):
            _write_content()
    else:
        _write_content()


def _coerce_decay_config(meta_or_decay_config):
    """Accept either a meta dict or a decay_config dict."""
    if not isinstance(meta_or_decay_config, dict):
        return {}
    if isinstance(meta_or_decay_config.get("decay_config"), dict):
        return meta_or_decay_config["decay_config"]
    return meta_or_decay_config


def infer_importance_from_usage(mem):
    """Infer a soft importance floor from real usage when importance is missing."""
    if not isinstance(mem, dict):
        return 0.0
    trigger_count = max(mem.get("trigger_count", 0), 0)
    access_count = max(mem.get("access_count", 0), 0)
    inferred = 0.05 + min(trigger_count * 0.04 + access_count * 0.015, 0.55)
    return round(min(inferred, 0.6), 3)


def get_effective_importance(mem):
    """Return stored importance, or a usage-derived floor for zero/empty values."""
    if not isinstance(mem, dict):
        return 0.5
    importance = mem.get("importance")
    if importance is None:
        return infer_importance_from_usage(mem)
    try:
        importance_val = float(importance)
    except (TypeError, ValueError):
        return infer_importance_from_usage(mem)
    if importance_val <= 0:
        return infer_importance_from_usage(mem)
    return importance_val


def get_memory_type_decay_profile(memory_type, decay_config=None):
    """Resolve alpha/beta-cap for one memory type from canonical or legacy config."""
    config = _coerce_decay_config(decay_config)
    nested = config.get("memory_types", {}) if isinstance(config.get("memory_types"), dict) else {}
    mem_type = memory_type if memory_type in MEMORY_TYPE_ALPHA_DEFAULTS else "derive"
    global_beta_cap = config.get("beta_cap", MEMORY_TYPE_BETA_CAP_DEFAULTS["derive"])

    if mem_type == "static":
        nested_static = nested.get("static", {}) if isinstance(nested.get("static"), dict) else {}
        alpha = nested_static.get("alpha", MEMORY_TYPE_ALPHA_DEFAULTS["static"])
        beta_cap = nested_static.get(
            "beta_cap",
            config.get("static_beta_max", MEMORY_TYPE_BETA_CAP_DEFAULTS["static"]),
        )
    elif mem_type == "absorb":
        nested_absorb = nested.get("absorb", {}) if isinstance(nested.get("absorb"), dict) else {}
        alpha = nested_absorb.get("alpha", config.get("absorb_beta_default", MEMORY_TYPE_ALPHA_DEFAULTS["absorb"]))
        beta_cap = nested_absorb.get(
            "beta_cap",
            max(config.get("absorb_beta_max", global_beta_cap), alpha),
        )
    else:
        nested_derive = nested.get("derive", {}) if isinstance(nested.get("derive"), dict) else {}
        alpha = nested_derive.get("alpha", config.get("derive_beta_default", MEMORY_TYPE_ALPHA_DEFAULTS["derive"]))
        beta_cap = nested_derive.get(
            "beta_cap",
            max(config.get("derive_beta_max", global_beta_cap), alpha),
        )

    return {
        "memory_type": mem_type,
        "alpha": float(alpha),
        "beta_cap": float(beta_cap),
    }


def compute_provenance_confidence(provenance_level, verification_count=0, decay_config=None):
    """Compute provenance confidence from schema-driven defaults or overrides."""
    config = _coerce_decay_config(decay_config)
    nested = config.get("provenance", {}) if isinstance(config.get("provenance"), dict) else {}
    legacy = PROVENANCE_CONFIDENCE_DEFAULTS.get(
        provenance_level,
        PROVENANCE_CONFIDENCE_DEFAULTS["L2"],
    )

    if provenance_level == "L1":
        base = nested.get("authoritative_base", config.get("provenance_auth_base", legacy["base"]))
        auth_mult = nested.get(
            "authoritative_multiplier",
            config.get("provenance_auth_mult", legacy["auth_mult"]),
        )
    elif provenance_level == "L3":
        base = nested.get("non_authoritative_base", config.get("provenance_nonauth_base", legacy["base"]))
        auth_mult = nested.get(
            "non_authoritative_multiplier",
            config.get("provenance_nonauth_mult", legacy["auth_mult"]),
        )
    else:
        base = nested.get("system_base", legacy["base"])
        auth_mult = nested.get("system_multiplier", legacy["auth_mult"])

    verification_step = nested.get(
        "verification_step",
        config.get("provenance_verify_step", DEFAULT_VERIFICATION_BONUS_PER),
    )
    verification_cap = nested.get(
        "verification_cap",
        config.get("provenance_verify_cap", DEFAULT_VERIFICATION_BONUS_CAP),
    )
    verification_mult = 1.0 + min(verification_cap, verification_count * verification_step)
    result = base * auth_mult * verification_mult
    return round(max(0.0, min(1.0, result)), 3)



def split_memory_heading(content):
    """Split bootstrapped memory content into heading/body parts."""
    text = (content or "").strip()
    bracket = re.match(r"^\[(.+?)\]\s*(.*)$", text, re.S)
    if bracket:
        return bracket.group(1).strip(), bracket.group(2).strip()

    heading = re.match(r"^##\s+(.+?)\s*$", text)
    if heading:
        lines = text.splitlines()
        return heading.group(1).strip(), "\n".join(lines[1:]).strip()

    first_line, _, rest = text.partition("\n")
    return first_line.strip()[:80], rest.strip() or text


def classify_bootstrap_memory_type(mem):
    """Classify bootstrap memories into static/derive/absorb buckets."""
    tags = set(mem.get("tags", []))
    importance = mem.get("importance", 0.5)
    content = ((mem.get("content", "") or "") + " " + " ".join(tags)).lower()

    static_keywords = [
        "人设", "偏好", "规则", "规范", "身份", "安全", "禁止", "最高优先级", "core",
    ]
    derive_keywords = [
        "经验", "教训", "修正", "决策", "踩坑", "设计", "架构", "策略", "发现", "结论",
    ]

    if mem.get("memory_type") in {"static", "derive", "absorb"}:
        return mem["memory_type"]
    if importance >= 0.8 or any(keyword in content for keyword in static_keywords):
        return "static"
    if importance >= 0.5 or any(keyword in content for keyword in derive_keywords):
        return "derive"
    return "absorb"


def is_bootstrap_memory_candidate(mem):
    """Return True if a memory should be migrated into a canonical case."""
    if not isinstance(mem, dict):
        return False
    memory_id = mem.get("id", "")
    tags = set(mem.get("tags", []))
    return (
        memory_id.startswith("mem_")
        and mem.get("status") == "active"
        and "bootstrapped" in tags
    )

def is_protected_memory(mem):
    """Return True for memories that should not be auto-archived or deleted."""
    if not isinstance(mem, dict):
        return False
    if mem.get("pinned"):
        return True
    return float(mem.get("importance", 0)) >= 0.9
# ─── Tokenization & Distance ────────────────────────────────

def tokenize(text):
    """CJK bigram + English word tokenization.

    Handles:
    - English words (>1 char)
    - CJK bigrams (2-char sliding window)
    - CJK single characters (preserved as tokens)
    """
    tokens = []
    segments = re.findall(
        r"[a-zA-Z0-9]+|[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]+",
        (text or "").lower(),
    )
    for seg in segments:
        if re.match(r"[a-zA-Z0-9]+", seg):
            if len(seg) > 1:
                tokens.append(seg)
        else:
            chars = list(seg)
            if len(chars) == 1:
                tokens.append(seg)
            else:
                for i in range(len(chars) - 1):
                    tokens.append(chars[i] + chars[i + 1])
    return tokens


def jaccard_distance(set_a, set_b):
    """1 - Jaccard similarity. 0 = identical, 1 = completely different.

    Returns 0.0 for empty inputs (no distance).
    """
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return 1.0 - (intersection / union)


# ─── v0.4.5: Memory ID & File Path ─────────────────────────

# Tag → directory mapping
TAG_DIR_MAP = {
    "project": "project",
    "项目": "project",
    "social": "social",
    "社区": "social",
    "tech": "tech",
    "技术": "tech",
    "personal": "personal",
    "个人": "personal",
}

# Special tags that don't map to directories
_SPECIAL_TAGS = frozenset({
    "bootstrapped", "migrated", "v0.4.2", "v0.4.3", "v0.4.4", "v0.4.5",
    "MEMORY.md", "manual", "auto", "pinned", "frozen",
})

# Default category for unclassifiable memories
_DEFAULT_CATEGORY = "misc"


def generate_memory_id(content, existing_ids=None):
    """Generate a unique memory_id from content hash + timestamp suffix.

    Format: mem_<md5_first12>_<timestamp_last4>

    Args:
        content: Memory content string.
        existing_ids: Optional set of existing memory_ids for uniqueness check.

    Returns:
        str: Unique memory_id.
    """
    content_str = (content or "").strip()
    hash_part = hashlib.md5(content_str.encode("utf-8")).hexdigest()[:12]
    ts_part = str(int(datetime.now(CST).timestamp()))[-4:]
    candidate = f"mem_{hash_part}_{ts_part}"

    if existing_ids and candidate in existing_ids:
        # Append a counter suffix to resolve collision
        for i in range(1, 100):
            candidate = f"mem_{hash_part}_{ts_part}_{i}"
            if candidate not in existing_ids:
                break
        else:
            # Exhausted collision slots — use uuid4 as last resort
            candidate = f"mem_{uuid.uuid4().hex}"

    return candidate


def resolve_primary_tag(tags, content=""):
    """Resolve the primary (directory-mapping) tag from a list of tags.

    Priority:
    1. First tag that maps to a known directory via TAG_DIR_MAP
    2. First tag that is not in _SPECIAL_TAGS
    3. Default category "misc"

    Args:
        tags: List of tag strings.
        content: Optional content for fallback keyword matching.

    Returns:
        str: Directory name (e.g. "project", "tech", "misc").
    """
    if not tags:
        return _DEFAULT_CATEGORY

    # Try exact TAG_DIR_MAP match first
    for tag in tags:
        if tag in TAG_DIR_MAP:
            return TAG_DIR_MAP[tag]

    # Try first non-special tag
    for tag in tags:
        if tag not in _SPECIAL_TAGS:
            return re.sub(r'[^\w-]', '_', tag).strip('_')

    # Fallback: keyword match in content
    if content:
        content_lower = (content or "").lower()
        keyword_map = [
            ("project", ["项目", "project", "开发", "版本", "v0.", "release"]),
            ("tech", ["技术", "tech", "架构", "api", "算法", "设计", "编码"]),
            ("social", ["社区", "social", "帖子", "评论", "讨论", "回复", "推广"]),
            ("personal", ["个人", "personal", "偏好", "习惯", "日常"]),
        ]
        for dir_name, keywords in keyword_map:
            if any(kw in content_lower for kw in keywords):
                return dir_name

    return _DEFAULT_CATEGORY


def derive_file_path(memory_id, tags, content="", base_dir="memory"):
    """Derive file path from memory_id and tags.

    Args:
        memory_id: Memory ID string.
        tags: List of tag strings.
        content: Optional content for fallback classification.
        base_dir: Base memory directory (default: "memory").

    Returns:
        str: Relative file path, e.g. "memory/project/mem_a1b2c3d4.md".
    """
    primary_tag = resolve_primary_tag(tags, content)
    return os.path.join(base_dir, primary_tag, f"{memory_id}.md")


def classify_confidence_level(confidence):
    """Map classification confidence to action level.

    Args:
        confidence: float in [0, 1].

    Returns:
        tuple: (action, label)
        - ("direct", "high") if confidence >= 0.8
        - ("review", "medium") if 0.5 <= confidence < 0.8
        - ("inbox", "low") if confidence < 0.5
    """
    if confidence >= 0.8:
        return ("direct", "high")
    elif confidence >= 0.5:
        return ("review", "medium")
    else:
        return ("inbox", "low")


# ─── v0.4.5: File Locking ──────────────────────────────────

@contextmanager
def file_lock_acquire(path, timeout=10.0):
    """Acquire an exclusive file lock using fcntl.flock.

    Args:
        path: File path to lock (a .lock sibling file is created).
        timeout: Maximum seconds to wait for lock acquisition.

    Yields:
        None when lock is acquired.

    Raises:
        TimeoutError if lock cannot be acquired within timeout.
    """
    lock_path = path + ".lock"
    fd = None
    try:
        fd = open(lock_path, "w")
        # Non-blocking attempt with polling
        deadline = datetime.now(CST).timestamp() + timeout
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (IOError, OSError):
                if datetime.now(CST).timestamp() > deadline:
                    raise TimeoutError(
                        f"Cannot acquire file lock for {path} within {timeout}s"
                    )
                time.sleep(0.05)
        yield
    finally:
        if fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
                fd.close()
            except (IOError, OSError):
                pass


# ─── v0.4.5: Global Index ──────────────────────────────────

def build_global_index(meta):
    """Build a Markdown pointer index from meta.json.

    Groups memories by primary tag directory, showing counts and recent entries.

    Args:
        meta: meta.json dict.

    Returns:
        str: Markdown formatted index content.
    """
    memories = meta.get("memories", [])
    tag_groups = {}  # dir_name -> [mem, ...]

    for mem in memories:
        tags = mem.get("tags", [])
        file_path = mem.get("file_path", "")
        if not file_path:
            file_path = derive_file_path(
                mem.get("memory_id", mem.get("id", "")),
                tags,
                mem.get("content", ""),
            )
        primary_tag = resolve_primary_tag(tags, mem.get("content", ""))
        tag_groups.setdefault(primary_tag, []).append(mem)

    lines = ["# Memory Index\n", f"Total: {len(memories)} entries\n"]
    lines.append(f"Generated: {_now_iso()}\n")

    for dir_name in sorted(tag_groups.keys()):
        mems = tag_groups[dir_name]
        lines.append(f"\n## {dir_name} ({len(mems)})\n")
        for mem in sorted(mems, key=lambda m: m.get("importance", 0), reverse=True)[:20]:
            mid = mem.get("memory_id", mem.get("id", "?"))
            fp = mem.get("file_path", f"memory/{dir_name}/{mid}.md")
            imp = mem.get("importance", "?")
            status = mem.get("status", "?")
            lines.append(f"- [{mid}]({fp}) imp={imp} status={status}")

    return "\n".join(lines)


def build_inverted_index(meta):
    """Build an inverted keyword index from meta.json.

    Returns:
        dict: {keyword: [memory_id, ...]} for dedup O(1) lookup.
    """
    memories = meta.get("memories", [])
    index = {}
    for mem in memories:
        mid = mem.get("memory_id", mem.get("id", ""))
        tokens = tokenize(mem.get("content", ""))
        for token in tokens:
            index.setdefault(token, set()).add(mid)
    return index
