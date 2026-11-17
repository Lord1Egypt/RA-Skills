# -*- coding: utf-8 -*-
# session_to_sqlite.py - 会话 JSONL 转换为 SQLite（支持 FTS5 全文检索）
# 调用：python session_to_sqlite.py --session-key KEY --session-file FILE --output-dir DIR [--append [--db-path FILE]]
# 作者：Pondsi
# 版本：v2.8 (2026-09-09) — --append 改为完整文件名匹配 + 只读身份校验（T09）

import io
import json
import sqlite3
import sys
import os
import re
import stat
import argparse
import tempfile
import hashlib

# T09 (v2.4): 归档目录/文件强制 owner-only 权限（同目录模块，随包分发）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secure_fs  # noqa: E402

# T09 权限策略（v2.4）：默认 Fail-Closed——无法保证 owner-only 即中止，
# 只有显式 --allow-insecure-storage 才降级为警告继续，并在结果中如实标注。
_ALLOW_INSECURE_STORAGE = False
_INSECURE_WARNINGS: list = []


class RedactionConfigError(RuntimeError):
    """脱敏规则不可信：必须中止，绝不写入未经脱敏的数据。"""


def _harden(action, label):
    """执行一次权限加固；失败时默认抛出，显式降级时记录警告并返回 False。"""
    try:
        action()
        return True
    except secure_fs.UnsafeArchiveError as exc:
        if _ALLOW_INSECURE_STORAGE:
            _INSECURE_WARNINGS.append(f"{label}: {exc}")
            print(f"SECURITY_WARN: INSECURE_STORAGE {label}: {exc}", file=sys.stderr)
            return False
        raise


def _abort_unsecured(db_path, conn, is_new_db, exc):
    """Fail-Closed 回滚。

    先回滚/关闭 SQLite 句柄（Windows 下否则文件被锁无法删除），再**仅**销毁本次
    新建的数据库与旁文件——追加模式下的历史归档绝不能被删除。
    """
    if conn is not None:
        try:
            conn.rollback()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
    if is_new_db:
        for target in (db_path, f"{db_path}-wal", f"{db_path}-shm"):
            try:
                if target and os.path.exists(target):
                    os.remove(target)
            except OSError:
                pass
    print(json.dumps({
        'status': 'error',
        'mode': 'archive',
        'error': f'aborted: {exc}',
        'removed_new_db': bool(is_new_db)
    }))
    sys.exit(6)


# ============================================================================
# T09 安全修复（v2.5）：脱敏链路全链路 Fail-Closed + 数据最小化
#   - 规则文件损坏 / 字段类型错误 / 正则无法编译 → 启动即中止（不建库、不写文件）
#   - 正则启动期预编译；运行期替换失败同样中止，绝不 continue 跳过
#   - session_key 在任何路径/文件名生成之前完成净化（白名单直通，否则脱敏+不透明哈希）
#   - 先在内存完成全量脱敏，再建库并在单事务内写入；失败回滚且不误删历史库
#   - 超长原文掐头去尾（MAX_ARCHIVE_LENGTH），兼顾数据最小化与 ReDoS 防护
# ============================================================================

# 本地存档最大字符数（掐头去尾），防止无限制存储
MAX_ARCHIVE_LENGTH = 20000
# 单条消息最大字符数（防止单条巨文本绕过总量限制）
MAX_MESSAGE_CHARS = 8000
# T09 (v2.6): 摄入上限——先限流再解析，内存与正则开销有界（ClawdHub 复审 1.6.1）
MAX_SESSION_BYTES = 64 * 1024 * 1024       # 单个轨迹文件读取上限 64 MiB
MAX_LINE_BYTES = 1 * 1024 * 1024           # 单行（单条消息）上限 1 MiB
MAX_MESSAGES = 200000                      # 单次摄入消息条数上限
MAX_TOTAL_CHARS = 64 * 1024 * 1024         # 累计正文字符上限
MAX_REDACT_FILE_BYTES = 64 * 1024 * 1024   # 原地脱敏单文件上限

# v2.7（1.8.0）：保留期上限——归档不再是无限期累积。每次摄入都会清掉超过
# 保留期的旧片段；0 表示无限期保留，必须显式 --allow-unbounded-retention。
DEFAULT_RETENTION_DAYS = 30
MAX_RETENTION_DAYS = 3650
ARCHIVE_DISABLE_ENV = 'INFINITY_CONTEXT_NO_ARCHIVE'

# T09 (v2.7): 归档身份标记——cleanup.py 只对带此标记的目录执行删除
MARKER_NAME = '.infinity-context-archive'
MARKER_APP = 'infinity-context'
MARKER_VERSION = 1

# session_key 安全白名单：符合则原样使用（仍会过一遍脱敏），否则替换为不透明标识
SESSION_KEY_SAFE_RE = re.compile(r'^[A-Za-z0-9:_\-.@]{1,128}$')

DEFAULT_REDACT_RULES = [
    # OpenAI 风格 API Key
    (r'(sk-[a-zA-Z0-9]{20,})', 'sk-[REDACTED]'),
    # GitHub Token
    (r'(gh[pousr]_[a-zA-Z0-9]{20,})', 'gh*_[REDACTED]'),
    # Bearer / Authorization
    (r'(?i)(Bearer\s+)[a-zA-Z0-9\-\._~\+/]+=*', r'\1[REDACTED]'),
    (r'(?i)(authorization\s*:\s*)[^\r\n]+', r'\1[REDACTED]'),
    # 常见密码/密钥字段（值直到空白/分隔符）
    (r'(?i)(password|passwd|secret|pwd|api_key|apikey|access_key|private_key|client_secret)["\'\s:=]+([^\s,;\}"\']+)', r'\1=[REDACTED]'),
    # JWT
    (r'(eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,})', '[JWT_REDACTED]'),
    # AWS Access Key
    (r'(AKIA[0-9A-Z]{16})', '[AWS_KEY_REDACTED]'),
    # Google API Key
    (r'(AIza[0-9A-Za-z_\-]{35})', '[GOOGLE_KEY_REDACTED]'),
    # Slack Token
    (r'(xox[baprs]-[0-9A-Za-z\-]{10,})', '[SLACK_TOKEN_REDACTED]'),
    # PEM 私钥块
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----', '[PRIVATE_KEY_REDACTED]'),
    # 数据库/中间件连接串
    (r'(?i)((?:mysql|postgres|postgresql|mongodb|redis|mssql|amqp|smtp)(?:\+\w+)?://)[^\s"\']+', r'\1[REDACTED]'),
    # Cookie
    (r'(?i)((?:set-)?cookie\s*:\s*)[^\r\n]+', r'\1[REDACTED]'),
    # Webhook（Slack/Discord/Telegram）
    (r'(?i)(https?://[^\s"\']*?(?:hooks\.slack\.com|discord(?:app)?\.com/api/webhooks|api\.telegram\.org/bot)[^\s"\']*)', '[WEBHOOK_REDACTED]'),
    # PII：手机号 / 邮箱
    (r'(?<!\d)(1[3-9]\d{9})(?!\d)', '[PHONE_REDACTED]'),
    (r'([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})', '[EMAIL_REDACTED]'),
]

# 启动期预编译后的规则：(已编译正则, 替换串)
_COMPILED_RULES = None


def _rules_path():
    """规则文件位置：环境变量 INFINITY_CONTEXT_REDACT_RULES 优先，否则脚本同目录。"""
    override = os.environ.get('INFINITY_CONTEXT_REDACT_RULES')
    if override:
        return os.path.abspath(override)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'redact_rules.json')


def _load_redact_rules():
    """加载并**预编译**脱敏规则；任何问题都抛 RedactionConfigError（Fail-Closed）。

    错误信息只包含索引与异常类型，不回显 pattern 内容（规则本身可能含敏感信息）。
    """
    raw = list(DEFAULT_REDACT_RULES)
    cfg_path = _rules_path()

    if os.path.isfile(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8-sig') as f:
                cfg = json.load(f)
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
            raise RedactionConfigError(
                f"redact_rules.json unreadable or malformed ({type(exc).__name__}); "
                "aborting to avoid unredacted archiving"
            ) from exc
        if not isinstance(cfg, dict):
            raise RedactionConfigError(
                "redact_rules.json top-level structure must be an object; aborting")
        custom = cfg.get('custom_redact_rules', [])
        if custom is None:
            custom = []
        if not isinstance(custom, list):
            raise RedactionConfigError("'custom_redact_rules' must be a list; aborting")
        for idx, item in enumerate(custom):
            if not isinstance(item, dict):
                raise RedactionConfigError(f"custom rule #{idx} must be an object; aborting")
            pat = item.get('pattern')
            rep = item.get('replace', '[REDACTED]')
            if not isinstance(pat, str) or not pat:
                raise RedactionConfigError(
                    f"custom rule #{idx}: 'pattern' must be a non-empty string; aborting")
            if not isinstance(rep, str):
                raise RedactionConfigError(
                    f"custom rule #{idx}: 'replace' must be a string; aborting")
            raw.append((pat, rep))

    compiled = []
    for idx, (pat, rep) in enumerate(raw):
        try:
            compiled.append((re.compile(pat), rep))
        except re.error as exc:
            raise RedactionConfigError(
                f"rule #{idx} failed to compile ({exc.msg} at position {exc.pos}); "
                "aborting to avoid unredacted archiving"
            ) from exc
    return compiled


def _ensure_rules():
    """惰性初始化并缓存预编译规则；失败时抛出 RedactionConfigError。"""
    global _COMPILED_RULES
    if _COMPILED_RULES is None:
        _COMPILED_RULES = _load_redact_rules()
    return _COMPILED_RULES


def redact_sensitive_info(text):
    """遮蔽常见敏感凭据 / PII 格式（API Key、Token、密码、私钥、连接串、Webhook、手机号、邮箱）。

    规则已在启动期预编译；运行期替换失败同样抛出，绝不静默跳过。
    """
    if not text:
        return text
    rules = _ensure_rules()
    for idx, (pattern, replacement) in enumerate(rules):
        try:
            text = pattern.sub(replacement, text)
        except re.error as exc:
            raise RedactionConfigError(
                f"rule #{idx} failed at application time ({type(exc).__name__}); "
                "aborting redaction"
            ) from exc
    return text


def sanitize_session_key(raw_key):
    """在任何路径/文件名生成之前净化 session_key。

    1. 白名单格式（字母数字与 :_- .@）且脱敏后不变 → 原样使用；
    2. 否则（含敏感内容或不安全字符）→ 不透明哈希，原文绝不落盘/入库/入 FTS。
    """
    if not isinstance(raw_key, str) or not raw_key.strip():
        raise ValueError("session_key must be a non-empty string")
    if SESSION_KEY_SAFE_RE.match(raw_key):
        if redact_sensitive_info(raw_key) == raw_key:
            return raw_key
    digest = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()[:16]
    return f"opaque-{digest}"


def is_high_entropy(word):
    """高熵候选（可能是密钥/哈希）不进入关键词索引。"""
    if len(word) < 24:
        return False
    has_lower = any(c.islower() for c in word)
    has_upper = any(c.isupper() for c in word)
    has_digit = any(c.isdigit() for c in word)
    if has_lower and has_upper and has_digit:
        return True
    # 长十六进制串
    if re.fullmatch(r'[0-9a-fA-F]{32,}', word):
        return True
    return False


def truncate_for_archive(text, limit=MAX_ARCHIVE_LENGTH):
    """数据最小化：超长内容掐头去尾，中间丢弃（保留头尾上下文）。"""
    if text is None or len(text) <= limit:
        return text
    head = text[: limit // 2]
    tail = text[-(limit // 2):]
    dropped = len(text) - limit
    return f"{head}\n\n...[内容因数据最小化原则被截断，中间 {dropped} 字符未保存]...\n\n{tail}"


def redact_file_in_place(path, allow_dir=None):
    """对给定文件原地脱敏（供轨迹备份复用同一套规则），返回字节数。

    T09-2：拒绝符号链接（目标与父目录）与外来账号目录；使用不可预测的
    临时文件（mkstemp，内核 O_EXCL）消除可预测名与 TOCTOU；写入后 fsync；
    替换前后均收紧权限；任何异常都不留临时文件。
    """
    abs_target = os.path.abspath(path)
    parent = os.path.dirname(abs_target)

    if os.path.islink(abs_target):
        raise ValueError(f"refusing to redact a symbolic link: {abs_target}")
    if os.path.islink(parent):
        raise ValueError(f"refusing to redact inside a symbolic link directory: {parent}")
    if not os.path.isfile(abs_target):
        raise ValueError(f"not a regular file: {abs_target}")

    file_size = os.path.getsize(abs_target)
    if file_size > MAX_REDACT_FILE_BYTES:
        raise ValueError(
            f"refusing to redact {abs_target}: {file_size} bytes exceeds the "
            f"{MAX_REDACT_FILE_BYTES}-byte in-place limit")

    getuid = getattr(os, 'getuid', None)
    if getuid is not None and os.lstat(parent).st_uid != getuid():
        raise ValueError(f"parent directory {parent} is owned by another account")

    if allow_dir:
        allowed = os.path.abspath(allow_dir)
        # 1) 词法包含：先挡住 ../ 之类的明显越界
        try:
            inside = os.path.commonpath([abs_target, allowed]) == allowed
        except ValueError:
            inside = False
        if not inside:
            raise ValueError(f"refusing to redact outside {allowed}: {abs_target}")

        # 2) 解析符号链接后的真实路径必须仍在允许目录内
        #    （防止「允许目录内的符号链接祖先」把写入重定向到目录之外）
        real_target = os.path.realpath(abs_target)
        real_allowed = os.path.realpath(allowed)
        try:
            inside_real = os.path.commonpath([real_target, real_allowed]) == real_allowed
        except ValueError:
            inside_real = False
        if not inside_real:
            raise ValueError(
                f"refusing to redact: resolved path {real_target} escapes {real_allowed}")

        # 3) 允许目录内部不得发生符号链接跳转：词法相对路径与真实相对路径必须一致
        try:
            lex_rel = os.path.relpath(abs_target, allowed)
            real_rel = os.path.relpath(real_target, real_allowed)
        except ValueError as exc:
            raise ValueError(f"refusing to redact: cannot resolve the path safely ({exc})") from exc
        if lex_rel != real_rel:
            raise ValueError(
                "refusing to redact: a symbolic link inside the allowed directory "
                "would redirect the write")

    with open(abs_target, 'r', encoding='utf-8-sig', errors='replace') as f:
        data = f.read(MAX_REDACT_FILE_BYTES + 1)
    redacted = redact_sensitive_info(data)

    # 同目录创建不可预测临时文件（mkstemp 内部使用 O_CREAT|O_EXCL，默认 0600）
    fd, tmp_path = tempfile.mkstemp(
        prefix='.infinity-redact-', suffix='.tmp', dir=parent, text=True
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(redacted)
            f.flush()
            os.fsync(f.fileno())
        _harden(lambda: secure_fs.secure_file(tmp_path), 'redact-temp-file')
        os.replace(tmp_path, abs_target)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass

    _harden(lambda: secure_fs.secure_file(abs_target), 'redact-target-file')
    return len(redacted)


def _check_limits(pairs):
    """Validate configurable limits: positive ints within the hard ceilings.

    The constants above are immutable ceilings; callers may only ask for
    something stricter. ``max_bytes = -1`` would otherwise reach
    ``file.read(-1)`` and load the whole transcript into memory.
    """
    for name, value, hard_max in pairs:
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= hard_max:
            raise ValueError(f"{name} must be an integer between 1 and {hard_max}")


def ensure_archive_marker(archive_dir):
    """在已加固的归档目录写入 owner-only 身份标记（幂等）。

    cleanup.py 拒绝清理没有该标记的目录，因此误把 --archive-dir 指向用户目录时
    也不会递归删除别人的文件。v1.8.4：标记内新增随机 ``archive_id``，写入数据库的
    ``archive_metadata`` 必须与它一致，才能执行保留期清理。
    """
    marker = os.path.join(archive_dir, MARKER_NAME)
    if os.path.exists(marker):
        return marker
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0)
    try:
        fd = os.open(marker, flags, 0o600)
    except FileExistsError:
        return marker
    from datetime import datetime, timezone
    import uuid
    with os.fdopen(fd, 'w', encoding='utf-8') as handle:
        json.dump({
            'app': MARKER_APP,
            'marker_version': MARKER_VERSION,
            'archive_id': uuid.uuid4().hex,
            'created_utc': datetime.now(timezone.utc).isoformat(),
        }, handle, indent=2)
        handle.write('\n')
    _harden(lambda: secure_fs.secure_file(marker), 'archive-marker')
    return marker


def verify_archive_marker(archive_dir):
    """校验目录确实属于本技能（owner-only 标记文件），否则拒绝写入/清理。

    v2.7：保留期清理同样只作用于带标记的归档目录，因此误把 --output-dir
    指向别人的目录时，绝不会去删人家的数据库行。
    """
    marker = os.path.join(archive_dir, MARKER_NAME)
    try:
        st = os.lstat(marker)
    except OSError as exc:
        raise secure_fs.UnsafeArchiveError(
            f'archive marker missing ({MARKER_NAME}); refusing to touch this directory')
    if os.path.islink(marker) or not stat.S_ISREG(st.st_mode):
        raise secure_fs.UnsafeArchiveError('archive marker is not a regular file')
    try:
        with open(marker, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise secure_fs.UnsafeArchiveError(f'archive marker unreadable: {exc}')
    if not isinstance(data, dict) or data.get('app') != MARKER_APP:
        raise secure_fs.UnsafeArchiveError('archive marker app id mismatch')
    return data


def purge_expired(cursor, retention_days):
    """删除超过保留期的归档片段（含 FTS 镜像），返回删除条数。

    v2.7：保留期是真正的上限，而不是“文档里写的建议”——每次摄入与
    ``--purge-only`` 都会执行，超出保留期的片段不会留在磁盘上。
    ``retention_days <= 0`` 表示不清理（调用方必须先通过显式开关）。
    """
    if retention_days <= 0:
        return 0
    cursor.execute(
        "SELECT chunk_id FROM session_chunks WHERE created_at < datetime('now', ?)",
        (f'-{int(retention_days)} days',))
    ids = [row[0] for row in cursor.fetchall()]
    if not ids:
        return 0
    for start in range(0, len(ids), 500):
        batch = ids[start:start + 500]
        placeholders = ','.join('?' * len(batch))
        cursor.execute(f'DELETE FROM chunk_fts WHERE chunk_id IN ({placeholders})', batch)
        cursor.execute(f'DELETE FROM session_chunks WHERE chunk_id IN ({placeholders})', batch)
    return len(ids)


ARCHIVE_FORMAT_VERSION = 2
SUPPORTED_FORMAT_VERSIONS = (1, 2)
PURGE_ARTIFACT_RE = re.compile(r'^[A-Za-z0-9_-]+-\d{8}-\d{6}\.db$')
REQUIRED_CHUNK_COLUMNS = {
    'chunk_id', 'session_key', 'start_msg_id', 'end_msg_id', 'summary',
    'keywords', 'anchor_questions', 'raw_content', 'created_at',
}


def db_identity_ok(db_path, session_key=None, marker_id=None, require_metadata=False):
    """只读校验候选数据库确实是本应用的归档（1.8.3/1.8.4）。

    T09：
      * --append 以前用 ``f.startswith(safe_key)`` 选库，``agent`` 会误命中
        ``agent-admin-*.db``；现在文件名必须完整匹配，并在写入前校验身份。
      * ``--purge-only`` 以前枚举所有 ``*.db`` 并直接读写；现在只接受产物文件名，
        且必须先只读确认 ``archive_metadata`` 的 app / format_version /
        （若标记里有）archive_id 一致。

    参数：
      session_key      不为 None 时，要求该 key 在库内有身份记录。
      marker_id        目录标记的 archive_id；不为空时要求与库内一致。
      require_metadata True 时必须有合法的 archive_metadata（旧库会被跳过）。
    返回 (ok, reason)。
    """
    if os.path.islink(db_path) or not os.path.isfile(db_path):
        return False, 'candidate is not a regular file'
    try:
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    except sqlite3.Error as exc:
        return False, f'cannot open candidate read-only: {exc}'
    try:
        cur = conn.cursor()
        names = {row[0] for row in cur.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        if not {'session_chunks', 'chunk_fts'}.issubset(names):
            return False, 'candidate is not an InfinityContext database'
        cols = {row[1] for row in cur.execute('PRAGMA table_info(session_chunks)')}
        if not REQUIRED_CHUNK_COLUMNS.issubset(cols):
            return False, 'session_chunks schema mismatch'

        meta_names = {'session_key', 'format_version'}
        has_meta = 'archive_metadata' in names
        if has_meta:
            meta_cols = {row[1] for row in cur.execute('PRAGMA table_info(archive_metadata)')}
            has_meta = meta_names.issubset(meta_cols)
        if require_metadata and not has_meta:
            return False, 'archive_metadata missing (run an append to upgrade this archive)'
        if has_meta:
            rows = list(cur.execute(
                'SELECT session_key, format_version, '
                'COALESCE(app, \'\'), COALESCE(archive_id, \'\') FROM archive_metadata'))
            if not rows:
                return False, 'archive_metadata is empty'
            for key, ver, app, aid in rows:
                if app and app != MARKER_APP:
                    return False, f'archive_metadata app mismatch: {app!r}'
                if ver not in SUPPORTED_FORMAT_VERSIONS:
                    return False, f'unsupported archive format version: {ver!r}'
                if marker_id and aid and aid != marker_id:
                    return False, 'archive_id does not match the directory marker'
            if session_key is not None and not any(r[0] == session_key for r in rows):
                return False, 'archive_metadata does not contain this session key'
            return True, ''

        if require_metadata:
            return False, 'archive_metadata missing'
        row = cur.execute(
            'SELECT COUNT(*) FROM session_chunks WHERE session_key = ?',
            (session_key,)).fetchone()
        if row and row[0]:
            return True, ''
        return False, 'candidate database holds no rows for this session key'
    except sqlite3.Error as exc:
        return False, f'candidate check failed: {exc}'
    finally:
        conn.close()


def purge_only(output_dir, retention_days):
    """对归档目录内每个 InfinityContext 数据库执行一次保留期清理。

    T09（v1.8.4）：候选必须是**完整产物文件名** ``{key}-YYYYMMDD-HHMMSS.db``，
    且先只读通过身份校验（app / format_version / archive_id / 必需列），再
    ``lstat`` 复核设备号与 inode 未变，最后才以读写模式打开。任何一步不通过就
    跳过并如实上报，绝不修改。
    """
    marker = verify_archive_marker(output_dir)
    marker_id = (marker or {}).get('archive_id') or None
    targets = sorted(
        name for name in os.listdir(output_dir)
        if PURGE_ARTIFACT_RE.fullmatch(name)
        and not os.path.islink(os.path.join(output_dir, name))
        and os.path.isfile(os.path.join(output_dir, name))
    )
    report = []
    total_purged = 0
    for name in targets:
        candidate_path = os.path.join(output_dir, name)
        try:
            st_before = os.lstat(candidate_path)
        except OSError as exc:
            report.append({'db': name, 'skipped': f'lstat failed: {exc}'})
            continue
        if stat.S_ISLNK(st_before.st_mode) or not stat.S_ISREG(st_before.st_mode):
            report.append({'db': name, 'skipped': 'not a regular file'})
            continue
        ok, why = db_identity_ok(candidate_path, marker_id=marker_id, require_metadata=True)
        if not ok:
            report.append({'db': name, 'skipped': why})
            continue
        try:
            st_after = os.lstat(candidate_path)
        except OSError as exc:
            report.append({'db': name, 'skipped': f'lstat failed: {exc}'})
            continue
        if (st_before.st_dev, st_before.st_ino) != (st_after.st_dev, st_after.st_ino):
            report.append({'db': name, 'skipped': 'file replaced between checks'})
            continue
        conn = sqlite3.connect(f'file:{candidate_path}?mode=rw', uri=True)
        try:
            st_open = os.lstat(candidate_path)
            if (st_before.st_dev, st_before.st_ino) != (st_open.st_dev, st_open.st_ino):
                report.append({'db': name, 'skipped': 'file replaced before opening'})
                continue
            cursor = conn.cursor()
            with conn:
                purged = purge_expired(cursor, retention_days)
            total_purged += purged
            report.append({'db': name, 'purged_chunks': purged})
        except (sqlite3.Error, OSError) as exc:
            report.append({'db': name, 'skipped': f'purge failed: {exc}'})
        finally:
            conn.close()
    return {'status': 'ok', 'mode': 'purge-only', 'archive_dir': output_dir,
            'retention_days': retention_days, 'purged_chunks': total_purged,
            'databases': report}


def read_messages(session_file, max_bytes=MAX_SESSION_BYTES,
                  max_line_bytes=MAX_LINE_BYTES, max_messages=MAX_MESSAGES,
                  max_total_chars=MAX_TOTAL_CHARS):
    """解析轨迹 JSONL；BOM 由 utf-8-sig 透明吞掉。

    T09（v2.6）：所有上限都在**摄入过程中**生效，而不是摄入完成之后——
      1. 只从文件头读取 max_bytes+1 字节，绝不把整个文件读进内存；
      2. 超长单行在 json/正则之前就被丢弃（统计到 skipped_oversized_lines）；
      3. 消息条数 / 累计字符数达到上限立即停止解析。
    返回 (messages, stats)；stats 如实记录触发了哪一个上限，绝不静默截断。
    """
    _check_limits((
        ('max_bytes', max_bytes, MAX_SESSION_BYTES),
        ('max_line_bytes', max_line_bytes, MAX_LINE_BYTES),
        ('max_messages', max_messages, MAX_MESSAGES),
        ('max_total_chars', max_total_chars, MAX_TOTAL_CHARS),
    ))

    stats = {
        'file_bytes': 0,
        'bytes_read': 0,
        'messages': 0,
        'skipped_oversized_lines': 0,
        'truncated': False,
        'truncated_reason': '',
    }
    try:
        stats['file_bytes'] = os.path.getsize(session_file)
    except OSError:
        stats['file_bytes'] = 0

    with open(session_file, 'rb') as raw:
        head = raw.read(max_bytes + 1)
    if len(head) > max_bytes:
        stats['truncated'] = True
        stats['truncated_reason'] = f'file-size-limit:{max_bytes}'
        head = head[:max_bytes]
        cut = head.rfind(b'\n')
        head = head[:cut + 1] if cut >= 0 else b''
    stats['bytes_read'] = len(head)

    messages = []
    total_chars = 0
    for line_num, raw_line in enumerate(io.StringIO(head.decode('utf-8-sig', errors='replace')), 1):
        line = raw_line.strip()
        if not line:
            continue
        if len(line.encode('utf-8', errors='replace')) > max_line_bytes:
            stats['skipped_oversized_lines'] += 1
            continue
        if len(messages) >= max_messages:
            stats['truncated'] = True
            stats['truncated_reason'] = f'message-count-limit:{max_messages}'
            break
        if total_chars >= max_total_chars:
            stats['truncated'] = True
            stats['truncated_reason'] = f'total-chars-limit:{max_total_chars}'
            break
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = data.get('message', {})
        if not message:
            message = data.get('data', {}).get('message', data.get('data', {}))
        role = message.get('role', 'unknown')
        content = message.get('content', '')
        timestamp = data.get('ts', data.get('timestamp', ''))

        content_text = ''
        has_thinking = 0
        has_tool_calls = 0
        if isinstance(content, str):
            content_text = content
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        content_text += item.get('text', '')
                    elif item.get('type') == 'thinking':
                        has_thinking = 1
                    elif item.get('type') == 'toolCall':
                        has_tool_calls = 1

        if content_text:
            total_chars += len(content_text)
            messages.append({
                'id': line_num,
                'role': role,
                'content': content_text,
                'timestamp': timestamp,
                'has_thinking': has_thinking,
                'has_tool_calls': has_tool_calls
            })

    stats['messages'] = len(messages)
    return messages, stats


def build_records(session_key, messages):
    """在内存中完成分块 + 脱敏 + 派生字段。

    此函数在任何数据库/文件创建之前调用；任何 RedactionConfigError 都会向上抛出，
    调用方随即中止，因此不会留下半脱敏的数据。
    """
    records = []
    chunk_size = 10
    for i in range(0, len(messages), chunk_size):
        chunk = messages[i:i+chunk_size]
        if not chunk:
            continue
        start_msg_id = chunk[0]['id']
        end_msg_id = chunk[-1]['id']

        safe_chunk = []
        for msg in chunk:
            safe_msg = dict(msg)
            safe_msg['content'] = truncate_for_archive(
                redact_sensitive_info(msg.get('content', '')), MAX_MESSAGE_CHARS
            )
            safe_chunk.append(safe_msg)

        try:
            roles = set(msg['role'] for msg in safe_chunk)
            has_thinking = any(msg['has_thinking'] for msg in safe_chunk)
            has_tool_calls = any(msg['has_tool_calls'] for msg in safe_chunk)

            summary_parts = []
            if 'user' in roles:
                summary_parts.append('user')
            if 'assistant' in roles:
                summary_parts.append('assistant')
            if has_thinking:
                summary_parts.append('thinking')
            if has_tool_calls:
                summary_parts.append('tool_calls')
            summary = ', '.join(summary_parts) if summary_parts else 'dialogue'

            keywords = set()
            for msg in safe_chunk:
                words = msg['content'].split()
                for word in words:
                    if len(word) > 2 and word.isalnum() and not is_high_entropy(word):
                        keywords.add(word.lower())
            keywords_str = ', '.join(list(keywords)[:5])

            anchor_set = set()
            for msg in safe_chunk:
                content = msg['content']
                for m in re.finditer(r'[a-zA-Z0-9_-]+\.[a-zA-Z]{2,4}', content):
                    anchor_set.add(m.group())
                for m in re.finditer(r'[a-zA-Z_][a-zA-Z0-9_]+\(\)', content):
                    anchor_set.add(m.group())
                for m in re.finditer(r'[\u4e00-\u9fa5]{2,6}', content):
                    anchor_set.add(m.group())
            anchor_questions = ', '.join(list(anchor_set)[:8])
        except RedactionConfigError:
            raise
        except Exception:
            summary = 'dialogue (metadata error)'
            keywords_str = ''
            anchor_questions = ''

        # 数据最小化：拼装后再次截断（防止多消息累计超限）
        raw_content = '\n'.join([f"[{msg['role']}] {msg['content']}" for msg in safe_chunk])
        raw_content = truncate_for_archive(raw_content, MAX_ARCHIVE_LENGTH)

        # 入库前对每个文本列做最后一道脱敏（防御性双保险）
        summary = redact_sensitive_info(summary)
        keywords_str = redact_sensitive_info(keywords_str)
        anchor_questions = redact_sensitive_info(anchor_questions)
        raw_content = redact_sensitive_info(raw_content)

        records.append((
            session_key, start_msg_id, end_msg_id,
            summary, keywords_str, anchor_questions, raw_content
        ))
    return records


def main():
    parser = argparse.ArgumentParser(description='Convert session JSONL to SQLite with FTS5')
    parser.add_argument('--session-key', required=False, help='Session key')
    parser.add_argument('--session-file', required=False, help='Path to events.jsonl')
    parser.add_argument('--output-dir', required=False, help='Output directory for SQLite files')
    parser.add_argument('--append', action='store_true', help='Append to existing SQLite file')
    parser.add_argument('--db-path', default=None,
                        help='with --append: exact database file to append to; must live inside '
                             '--output-dir and pass the identity check')
    parser.add_argument('--redact-file', help='Redact sensitive data in-place in the given file, then exit')
    parser.add_argument('--allow-dir', default=None,
                        help='with --redact-file: refuse any path outside this directory')
    parser.add_argument('--max-session-bytes', type=int, default=MAX_SESSION_BYTES,
                        help='maximum bytes read from the transcript (default 64 MiB)')
    parser.add_argument('--max-line-bytes', type=int, default=MAX_LINE_BYTES,
                        help='maximum bytes per transcript line (default 1 MiB)')
    parser.add_argument('--max-messages', type=int, default=MAX_MESSAGES,
                        help='maximum number of messages ingested (default 200000)')
    parser.add_argument('--max-total-chars', type=int, default=MAX_TOTAL_CHARS,
                        help='maximum cumulative content characters (default 64 MiB)')
    parser.add_argument('--allow-dir-fallback', action='store_true', default=False,
                        help='DANGEROUS: if --output-dir is not ASCII-safe, archive into '
                             '~/.openclaw/sqlite-data instead of aborting.')
    parser.add_argument('--allow-insecure-storage', action='store_true', default=False,
                        help='DANGEROUS: keep archiving even if owner-only permissions '
                             'cannot be enforced. Only for trusted single-user filesystems.')
    parser.add_argument('--retention-days', type=int, default=DEFAULT_RETENTION_DAYS,
                        help='purge archived chunks older than N days on every run '
                             f'(1..{MAX_RETENTION_DAYS}; 0 keeps them forever and requires '
                             '--allow-unbounded-retention)')
    parser.add_argument('--allow-unbounded-retention', action='store_true', default=False,
                        help='DANGEROUS: allow --retention-days 0 (keep the archive forever)')
    parser.add_argument('--purge-only', action='store_true', default=False,
                        help='apply the retention policy to every archive database in '
                             '--output-dir, then exit without ingesting anything')
    args = parser.parse_args()

    global _ALLOW_INSECURE_STORAGE
    _ALLOW_INSECURE_STORAGE = bool(args.allow_insecure_storage)

    # 阶段 -1：可配置上限必须先通过校验，才允许任何文件操作
    try:
        _check_limits((
            ('--max-session-bytes', args.max_session_bytes, MAX_SESSION_BYTES),
            ('--max-line-bytes', args.max_line_bytes, MAX_LINE_BYTES),
            ('--max-messages', args.max_messages, MAX_MESSAGES),
            ('--max-total-chars', args.max_total_chars, MAX_TOTAL_CHARS),
        ))
    except ValueError as exc:
        parser.error(str(exc))

    # 阶段 -1.5：保留期必须是有界值；无限期保留需要显式开关
    if args.retention_days == 0:
        if not args.allow_unbounded_retention:
            parser.error('--retention-days 0 keeps every chunk forever; pass '
                         '--allow-unbounded-retention to accept unbounded local retention')
    elif not 1 <= args.retention_days <= MAX_RETENTION_DAYS:
        parser.error(f'--retention-days must be 0 or 1..{MAX_RETENTION_DAYS}')

    # 阶段 0：脱敏引擎必须在任何文件/数据库操作之前就绪（Fail-Closed）
    try:
        _ensure_rules()
    except RedactionConfigError as exc:
        print(json.dumps({'status': 'error', 'mode': 'startup', 'error': str(exc)}))
        sys.exit(2)

    # 轨迹备份脱敏模式（文件修改必须限定范围：--allow-dir 必填）
    if args.redact_file:
        if not args.allow_dir:
            print(json.dumps({
                'status': 'error', 'mode': 'redact-file',
                'error': '--allow-dir is required with --redact-file: '
                         'file mutation must be scoped to a declared directory'
            }))
            sys.exit(7)
        try:
            n = redact_file_in_place(args.redact_file, allow_dir=args.allow_dir)
            print(json.dumps({'status': 'ok', 'mode': 'redact-file', 'bytes': n}))
        except Exception as e:
            print(json.dumps({'status': 'error', 'mode': 'redact-file', 'error': str(e)}))
            sys.exit(1)
        return

    # 保留期清理模式：只清理，不摄入（清理同样只作用于带标记的归档目录）
    if args.purge_only:
        if not args.output_dir:
            parser.error('--output-dir is required with --purge-only')
        try:
            print(json.dumps(purge_only(args.output_dir, args.retention_days),
                             ensure_ascii=False))
        except secure_fs.UnsafeArchiveError as exc:
            print(json.dumps({'status': 'error', 'mode': 'purge-only', 'error': str(exc)}))
            sys.exit(3)
        except (sqlite3.Error, OSError) as exc:
            print(json.dumps({'status': 'error', 'mode': 'purge-only', 'error': str(exc)}))
            sys.exit(4)
        return

    # 归档总开关：设 INFINITY_CONTEXT_NO_ARCHIVE=1 后本脚本不再写入任何归档
    if os.environ.get(ARCHIVE_DISABLE_ENV, '').strip().lower() in ('1', 'true', 'yes', 'on'):
        print(json.dumps({'status': 'disabled', 'mode': 'archive', 'archived': False,
                          'reason': f'{ARCHIVE_DISABLE_ENV} is set'}, ensure_ascii=False))
        return

    if not (args.session_key and args.session_file and args.output_dir):
        parser.error('--session-key, --session-file and --output-dir are required unless --redact-file is used')

    # 阶段 1：先净化 session_key（在任何路径 / 文件名生成之前）
    try:
        session_key = sanitize_session_key(args.session_key)
    except (ValueError, RedactionConfigError) as exc:
        print(json.dumps({'status': 'error', 'phase': 'init_key', 'error': str(exc)}))
        sys.exit(3)

    session_file = args.session_file
    output_dir = args.output_dir
    append_mode = args.append
    # 记录用户请求的目录；若因非 ASCII 回退，必须显式告知，不得静默改道
    requested_dir = output_dir
    archive_dir_fallback = False

    # 阶段 2.5：输出目录必须能安全交给 sqlite3（Windows 下非 ASCII 路径不可用）。
    # Fail-Closed：默认直接拒绝改道，只有显式 --allow-dir-fallback 才回退到
    # ASCII 目录，并在 stderr 与 JSON 结果中如实标注。
    try:
        output_dir.encode('ascii')
    except UnicodeEncodeError:
        if not args.allow_dir_fallback:
            print(json.dumps({
                'status': 'error', 'mode': 'archive',
                'error': 'output directory is not ASCII-safe; pass an ASCII path or '
                         'rerun with --allow-dir-fallback to use the fallback directory',
                'requested_dir': requested_dir,
            }))
            sys.exit(8)
        output_dir = os.path.join(os.path.expanduser('~'), '.openclaw', 'sqlite-data')
        archive_dir_fallback = True
        print(f"SECURITY_WARN: ARCHIVE_DIR_FALLBACK requested={requested_dir} "
              f"effective={output_dir} reason=non-ascii-path", file=sys.stderr)

    # 阶段 2：读取轨迹并在内存中完成全量脱敏（此时尚未创建任何数据库文件）
    try:
        messages, ingest = read_messages(
            session_file,
            max_bytes=args.max_session_bytes,
            max_line_bytes=args.max_line_bytes,
            max_messages=args.max_messages,
            max_total_chars=args.max_total_chars,
        )
    except OSError as exc:
        print(json.dumps({'status': 'error', 'mode': 'archive',
                          'error': f'cannot read transcript: {exc}'}))
        sys.exit(4)
    if ingest['truncated']:
        print(f"SECURITY_WARN: INGEST_TRUNCATED reason={ingest['truncated_reason']} "
              f"messages={ingest['messages']}", file=sys.stderr)
    if ingest['skipped_oversized_lines']:
        print(f"SECURITY_WARN: INGEST_SKIPPED_OVERSIZED_LINES "
              f"count={ingest['skipped_oversized_lines']}", file=sys.stderr)

    try:
        records = build_records(session_key, messages)
    except RedactionConfigError as exc:
        print(json.dumps({'status': 'error', 'mode': 'archive',
                          'error': f'redaction aborted: {exc}'}))
        sys.exit(5)

    # 阶段 3：归档目录强制 owner-only（不存在则创建，已存在则收紧/拒绝）
    try:
        permissions_enforced = _harden(
            lambda: secure_fs.secure_directory(output_dir), 'archive-directory')
    except secure_fs.UnsafeArchiveError as exc:
        print(json.dumps({'status': 'error', 'mode': 'archive', 'error': str(exc)}))
        sys.exit(3)

    # 阶段 3.5：写入归档身份标记（cleanup.py 只清理带标记的目录）
    try:
        ensure_archive_marker(output_dir)
        marker_payload = verify_archive_marker(output_dir)
    except (OSError, secure_fs.UnsafeArchiveError) as exc:
        print(json.dumps({'status': 'error', 'mode': 'archive',
                          'error': f'cannot write archive marker: {exc}'}))
        sys.exit(3)
    marker_id = marker_payload.get('archive_id') or None

    # 文件名只由已净化的 key 生成（安全字符集，不会泄漏敏感信息）
    safe_key = re.sub(r'[^a-zA-Z0-9_-]', '_', session_key)

    from datetime import datetime
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    if append_mode:
        reserve_exclusive = False
        # T09（v2.8）：只接受完整文件名 ``{safe_key}-YYYYMMDD-HHMMSS.db``，
        # 并在读写之前做只读身份校验；歧义或多候选一律拒绝。
        if args.db_path:
            db_path = os.path.abspath(args.db_path)
            if os.path.dirname(db_path) != os.path.abspath(output_dir):
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': '--db-path must live inside --output-dir'}))
                sys.exit(9)
            if not os.path.exists(db_path):
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': f'--db-path does not exist: {db_path}'}))
                sys.exit(9)
            ok, why = db_identity_ok(db_path, session_key, marker_id=marker_id)
            if not ok:
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': f'--db-path rejected: {why}',
                                  'db_path': db_path}))
                sys.exit(9)
        else:
            artifact_re = re.compile(rf'^{re.escape(safe_key)}-\d{{8}}-\d{{6}}\.db$')
            candidates = sorted(
                name for name in os.listdir(output_dir)
                if artifact_re.fullmatch(name)
                and not os.path.islink(os.path.join(output_dir, name))
            )
            if len(candidates) > 1:
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': 'ambiguous append target: several databases match '
                                           'this session key; pass --db-path to choose one',
                                  'candidates': candidates}))
                sys.exit(9)
            if candidates:
                candidate = os.path.join(output_dir, candidates[0])
                ok, why = db_identity_ok(candidate, session_key, marker_id=marker_id)
                if not ok:
                    print(json.dumps({'status': 'error', 'mode': 'archive',
                                      'error': f'append target rejected: {why}',
                                      'db_path': candidate}))
                    sys.exit(9)
                db_path = candidate
            else:
                db_path = os.path.join(output_dir, f'{safe_key}-{stamp}.db')
                reserve_exclusive = True
    else:
        if args.db_path:
            parser.error('--db-path requires --append')
        db_path = os.path.join(output_dir, f'{safe_key}-{stamp}.db')
        # T09（v1.8.4）：非 append 模式必须原子独占创建；同名文件存在时拒绝，
        # 绝不复用/修改已存在的库（即使它“看起来”是本应用的库）。
        reserve_exclusive = True

    # 关键：在任何文件创建之前记录该库是否为本轮新建——决定失败时能否物理删除
    is_new_db = reserve_exclusive or not os.path.exists(db_path)

    # 阶段 4：建库 + 单事务写入（失败回滚；新建库才清理，历史库绝不动）
    conn = None
    purged_chunks = 0
    try:
        if reserve_exclusive:
            # T09（v1.8.4）：新建库必须原子独占创建（O_CREAT|O_EXCL|O_NOFOLLOW, 0600），
            # 绝不复用已存在的同名文件；同名冲突直接报错，而不是去修改别人的库。
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0)
            try:
                fd = os.open(db_path, flags, 0o600)
                os.close(fd)
            except FileExistsError:
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': 'archive filename collision: this exact file already '
                                           'exists; use --append to add to it, or retry in a '
                                           'moment for a new timestamp',
                                  'db_path': db_path}))
                sys.exit(10)
            except OSError as exc:
                print(json.dumps({'status': 'error', 'mode': 'archive',
                                  'error': f'cannot reserve archive file: {exc}'}))
                sys.exit(10)
        _harden(lambda: secure_fs.secure_file(db_path), 'database-file')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('PRAGMA journal_mode = WAL')
        cursor.execute('PRAGMA busy_timeout = 5000')
        cursor.execute('PRAGMA synchronous = NORMAL')
        _harden(lambda: secure_fs.secure_sidecars(db_path), 'wal-sidecars')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_chunks (
            chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key TEXT NOT NULL,
            start_msg_id INTEGER NOT NULL,
            end_msg_id INTEGER NOT NULL,
            summary TEXT NOT NULL,
            keywords TEXT NOT NULL,
            anchor_questions TEXT NOT NULL DEFAULT '',
            raw_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        try:
            cursor.execute('ALTER TABLE session_chunks ADD COLUMN anchor_questions TEXT NOT NULL DEFAULT ""')
        except sqlite3.Error:
            pass
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS archive_metadata (
            session_key TEXT PRIMARY KEY,
            format_version INTEGER NOT NULL,
            app TEXT NOT NULL DEFAULT 'infinity-context',
            archive_id TEXT NOT NULL DEFAULT ''
        )
        ''')
        for ddl in ('ALTER TABLE archive_metadata ADD COLUMN app TEXT NOT NULL DEFAULT "infinity-context"',
                    'ALTER TABLE archive_metadata ADD COLUMN archive_id TEXT NOT NULL DEFAULT ""'):
            try:
                cursor.execute(ddl)
            except sqlite3.Error:
                pass
        cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
            chunk_id UNINDEXED,
            session_key,
            keywords,
            summary,
            anchor_questions,
            raw_content,
            tokenize = 'trigram'
        )
        ''')
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_chunk_insert AFTER INSERT ON session_chunks BEGIN
            INSERT INTO chunk_fts(chunk_id, session_key, keywords, summary, anchor_questions, raw_content)
            VALUES (new.chunk_id, new.session_key, new.keywords, new.summary, new.anchor_questions, new.raw_content);
        END
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_key ON session_chunks(session_key)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON session_chunks(created_at)')
        try:
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_chunk_unique ON session_chunks(session_key, start_msg_id, end_msg_id)')
        except sqlite3.Error:
            pass

        # 单事务写入：保留期清理与本次写入同属一个事务，要么全部生效，要么全部回滚
        with conn:
            cursor.execute(
                'INSERT OR IGNORE INTO archive_metadata '
                '(session_key, format_version, app, archive_id) VALUES (?, ?, ?, ?)',
                (session_key, ARCHIVE_FORMAT_VERSION, MARKER_APP, marker_id or ''))
            cursor.execute(
                'UPDATE archive_metadata SET app = ?, archive_id = ? '
                'WHERE session_key = ? AND (app <> ? OR archive_id = ?)',
                (MARKER_APP, marker_id or '', session_key, MARKER_APP, ''))
            purged_chunks = purge_expired(cursor, args.retention_days)
            cursor.executemany('''
                INSERT OR IGNORE INTO session_chunks
                    (session_key, start_msg_id, end_msg_id, summary, keywords, anchor_questions, raw_content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', records)

        cursor.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        _harden(lambda: secure_fs.secure_sidecars(db_path), 'wal-sidecars-final')

        cursor.execute('SELECT COUNT(*) FROM session_chunks WHERE session_key = ?', (session_key,))
        total_chunks = cursor.fetchone()[0]
        cursor.execute('SELECT MIN(chunk_id), MAX(chunk_id) FROM session_chunks WHERE session_key = ?', (session_key,))
        min_id, max_id = cursor.fetchone()
        cursor.execute('SELECT MIN(start_msg_id), MAX(end_msg_id) FROM session_chunks WHERE session_key = ?', (session_key,))
        min_msg, max_msg = cursor.fetchone()
        conn.close()
        conn = None
    except secure_fs.UnsafeArchiveError as exc:
        _abort_unsecured(db_path, conn, is_new_db, exc)
    except (sqlite3.Error, OSError) as exc:
        _abort_unsecured(db_path, conn, is_new_db, exc)

    result = {
        'status': 'ok',
        'db_path': db_path,
        'total_chunks': total_chunks,
        'chunk_id_range': [min_id, max_id],
        'msg_id_range': [min_msg, max_msg],
        'append_mode': append_mode,
        'archive_dir': output_dir,
        'requested_dir': requested_dir,
        'archive_dir_fallback': archive_dir_fallback,
        'permissions_enforced': bool(permissions_enforced),
        'ingest': ingest,
        'retention_days': args.retention_days,
        'purged_chunks': purged_chunks,
        'insecure_storage': bool(_INSECURE_WARNINGS),
        'warnings': list(_INSECURE_WARNINGS)
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
