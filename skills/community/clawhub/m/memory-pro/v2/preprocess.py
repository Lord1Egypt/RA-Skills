try:
    from nltk.tokenize import sent_tokenize as _nltk_sent_tokenize
except Exception:
    _nltk_sent_tokenize = None
import re
import os
from datetime import datetime, timezone

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def clean_text(text):
    """
    清理文本：移除代碼塊、Markdown 鏈接、標題等
    """
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'#+\s*.*?$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _resolve_path(base_path, path_value):
    expanded = os.path.expandvars(os.path.expanduser(path_value))
    if "$" in expanded:
        return expanded
    if os.path.isabs(expanded):
        return expanded
    return os.path.normpath(os.path.join(base_path, "../../../../", expanded.lstrip('/')))


def _to_iso(ts):
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return datetime.now(tz=timezone.utc).isoformat()


def _contains_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text or ""))


def _token_len(text: str) -> int:
    """
    統一 token 長度估算：
    - 英文/數字：以詞計
    - CJK：以字元計（避免 split() 對中文近乎永遠=1）
    """
    text = (text or "").strip()
    if not text:
        return 0
    if _contains_cjk(text):
        cjk_chars = CJK_RE.findall(text)
        latin_words = WORD_RE.findall(text)
        return len(cjk_chars) + len(latin_words)
    return len(text.split())


def _is_valid_sentence(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    tlen = _token_len(text)
    # 英文句保留原本門檻；CJK 降低門檻避免誤殺
    if _contains_cjk(text):
        return tlen >= 2
    return tlen > 3


def _split_sentences(text: str) -> list[str]:
    if not text:
        return []
    if _nltk_sent_tokenize is not None:
        try:
            return _nltk_sent_tokenize(text)
        except LookupError:
            pass
    parts = re.split(r'(?<=[.!?。！？])\s*', text)
    return [part for part in parts if part.strip()]


def _infer_scope(filepath: str, source_type: str) -> str:
    p = (filepath or "").lower()
    if "/workspace/memory/" in p:
        return os.getenv("MEMORY_PRO_DAILY_SCOPE", "main")
    if "/workspace/.learnings/" in p or "/skills/self-improving-agent/.learnings/" in p:
        return "agent:self-improvement"
    if "/workspace/docs/" in p:
        return "project:docs"
    if source_type == "core":
        return "global"
    return "global"


def _collect_from_file(filepath, source_type, scope="global", importance=0.5, tags=None):
    tags = tags or []
    entries = []
    if not os.path.isfile(filepath):
        return entries

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = clean_text(content)
    mtime_iso = _to_iso(os.path.getmtime(filepath))
    resolved_scope = _infer_scope(filepath, source_type) if scope == "global" else scope

    for sent in _split_sentences(cleaned):
        sent = sent.strip()
        if not _is_valid_sentence(sent):
            continue
        entries.append({
            "text": sent,
            "source_file": filepath,
            "source_type": source_type,
            "created_at": mtime_iso,
            "scope": resolved_scope,
            "importance": importance,
            "token_len": _token_len(sent),
            "tags": tags,
        })
    return entries


def _ingest_markdown_dir(entries, dir_path, source_type="daily", scope="global"):
    if not os.path.isdir(dir_path):
        return

    for filename in os.listdir(dir_path):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(dir_path, filename)
        entries.extend(_collect_from_file(filepath, source_type=source_type, scope=scope))


def preprocess_entries():
    """
    回傳包含 metadata 的條目列表，供 build_index / hybrid retrieval 使用。
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.getenv("MEMORY_PRO_DATA_DIR", "${OPENCLAW_WORKSPACE}/memory/")

    full_dir_path = _resolve_path(base_path, data_dir)
    if not os.path.exists(full_dir_path):
        raise FileNotFoundError(f"Directory not found: {full_dir_path}")

    entries = []

    # 主來源：daily memory
    _ingest_markdown_dir(entries, full_dir_path, source_type="daily", scope="global")

    # 額外來源：self-improvement learnings / docs
    extra_md_dirs_raw = os.getenv(
        "MEMORY_PRO_EXTRA_MD_DIRS",
        "${OPENCLAW_WORKSPACE}/.learnings,${OPENCLAW_WORKSPACE}/skills/self-improving-agent/.learnings,${OPENCLAW_WORKSPACE}/docs"
    )
    extra_md_dirs = [p.strip() for p in extra_md_dirs_raw.split(',') if p.strip()]
    for extra_dir in extra_md_dirs:
        _ingest_markdown_dir(entries, _resolve_path(base_path, extra_dir), source_type="extra", scope="global")

    workspace_root = _resolve_path(base_path, os.getenv("OPENCLAW_WORKSPACE", "../../../../workspace/"))
    core_files = os.getenv("MEMORY_PRO_CORE_FILES", "MEMORY.md,SOUL.md,STATUS.md,AGENTS.md,USER.md").split(',')

    for filename in core_files:
        filepath = os.path.join(workspace_root, filename)
        entries.extend(_collect_from_file(filepath, source_type="core", scope="global"))

    # 去重：同句子只保留第一條，保持順序穩定
    seen = set()
    unique_entries = []
    for e in entries:
        t = e["text"].strip()
        if t in seen:
            continue
        seen.add(t)
        unique_entries.append(e)

    return unique_entries


def preprocess_directory():
    """
    向後相容：僅回傳句子列表（供舊流程使用）
    """
    return [e["text"] for e in preprocess_entries()]
