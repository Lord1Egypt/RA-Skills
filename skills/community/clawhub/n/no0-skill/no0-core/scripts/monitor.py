import os
import argparse
import hashlib
import time
import logging
import json
import shutil
import stat
import difflib
import uuid
import logging.handlers
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from event_logger import write_change_log, update_change_log_label


def safe_int_env(name: str, default: int) -> int:
    """读取整数环境变量，非法值回退到默认值。"""
    raw_value = os.getenv(name, str(default))
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        logging.warning(f"环境变量 {name}={raw_value} 非法，回退默认值 {default}")
        return default

# ===================== 核心配置项 =====================
SCRIPT_DIR = Path(__file__).resolve().parent.parent  # skill root (scripts/ → no0-skill/)
DEFAULT_MONITOR_DIR = SCRIPT_DIR.parent.parent  # workspace dir
DEFAULT_OUTPUT_DIR = SCRIPT_DIR  # output to skill root
MONITOR_DIR_ENV = "GUARDIAN_MONITOR_DIR"
OUTPUT_DIR_ENV = "GUARDIAN_OUTPUT_DIR"

BASE_DIR = DEFAULT_OUTPUT_DIR
COGNITIVE_DIR = DEFAULT_MONITOR_DIR
MONITOR_FILES = ["SOUL.md", "USER.md", "HEARTBEAT.md", "MEMORY.md", "TOOLS.md", "AGENTS.md"]
BACKUP_DIR = BASE_DIR / "cognitive_file_backups"
CHECK_INTERVAL = safe_int_env("GUARDIAN_CHECK_INTERVAL_SECONDS", 30)
LOG_FILE = BASE_DIR / "cognitive_file_monitor.log"
MAX_BACKUP_VERSIONS = 10
MAX_SELF_MONITOR_RECORDS = 30
BACKUP_VERIFY_INTERVAL = safe_int_env("GUARDIAN_BACKUP_VERIFY_INTERVAL", 10)
MAX_CHANGE_SIGNATURES_PER_FILE = safe_int_env("GUARDIAN_MAX_CHANGE_SIGNATURES_PER_FILE", 200)
MONITOR_VERSION = "0.2.0"

# ===================== diff 截断配置 =====================
DIFF_CONTEXT_LINES = int(os.getenv("GUARDIAN_DIFF_CONTEXT_LINES", "3"))
MAX_DIFF_LINES = int(os.getenv("GUARDIAN_MAX_DIFF_LINES", "500"))
MAX_DIFF_LINE_CHANGES = int(os.getenv("GUARDIAN_MAX_DIFF_LINE_CHANGES", "200"))
MAX_CONTENT_CHARS = int(os.getenv("GUARDIAN_MAX_CONTENT_CHARS", "12000"))

# 变更日志文件
CHANGE_LOG_JSON_FILE = BASE_DIR / "change_log.json"
CHANGE_LOG_MD_FILE = BASE_DIR / "change_log.md"

# ========== 监控状态变量 ==========
last_check_start = None
last_self_hash = None
file_hash_cache = {}
reported_change_signatures: Dict[str, List[str]] = {}
reported_new_hashes: Dict[str, List[str]] = {}
last_recorded_hashes: Dict[str, Dict[str, str]] = {}
self_monitor_records: List[Dict[str, Any]] = []
backup_verify_counter = 0

# ===================== 日志配置（自动切分，20MB，保留10个） =====================
LOG_MAX_BYTES = 20 * 1024 * 1024
LOG_BACKUP_COUNT = 10
LOG_FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


def resolve_runtime_path(raw_value: Optional[str], env_name: str, default_path: Path) -> Path:
    """优先使用命令行参数，其次环境变量，最后回退到默认路径。"""
    candidate = raw_value or os.getenv(env_name)
    if candidate:
        return Path(candidate).expanduser()
    return default_path


def set_runtime_paths(monitor_dir: Path, output_dir: Path) -> None:
    """根据启动参数刷新运行时目录。"""
    global BASE_DIR, COGNITIVE_DIR, BACKUP_DIR, LOG_FILE
    global CHANGE_LOG_JSON_FILE, CHANGE_LOG_MD_FILE, STATE_FILE

    COGNITIVE_DIR = monitor_dir.resolve()
    BASE_DIR = output_dir.resolve()
    BACKUP_DIR = BASE_DIR / "cognitive_file_backups"
    LOG_FILE = BASE_DIR / "cognitive_file_monitor.log"
    CHANGE_LOG_JSON_FILE = BASE_DIR / "change_log.json"
    CHANGE_LOG_MD_FILE = BASE_DIR / "change_log.md"
    STATE_FILE = BACKUP_DIR / "monitor_state.json"


def configure_logging() -> None:
    """按当前输出目录重建日志处理器。"""
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(LOG_FORMATTER)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LOG_FORMATTER)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# ===================== diff 辅助函数 =====================
def read_text_file(file_path: Path) -> str:
    """读取文本文件内容，遇到编码问题时替换非法字符。"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        logging.error(f"读取文本失败 {file_path}: {e}")
        return ""

def truncate_text(text: str, max_chars: int) -> Tuple[str, bool]:
    """按字符数截断文本，返回截断结果与是否发生截断。"""
    if max_chars <= 0 or len(text) <= max_chars:
        return text, False
    suffix = "\n...<truncated>"
    keep = max(0, max_chars - len(suffix))
    return text[:keep] + suffix, True

def collect_line_changes(before_lines: List[str], after_lines: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """提取新增行与删除行（含行号），用于结构化 diff 分析。"""
    matcher = difflib.SequenceMatcher(a=before_lines, b=after_lines)
    added_lines: List[Dict[str, Any]] = []
    removed_lines: List[Dict[str, Any]] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "delete"):
            for line_idx in range(i1, i2):
                removed_lines.append({
                    "line_no": line_idx + 1,
                    "content": before_lines[line_idx]
                })
        if tag in ("replace", "insert"):
            for line_idx in range(j1, j2):
                added_lines.append({
                    "line_no": line_idx + 1,
                    "content": after_lines[line_idx]
                })

    return {
        "added_lines": added_lines,
        "removed_lines": removed_lines,
    }

def build_diff_payload(file_name: str, before_content: str, after_content: str) -> Dict[str, Any]:
    """构建统一 diff 数据结构。"""
    before_lines = before_content.splitlines()
    after_lines = after_content.splitlines()

    unified_lines = list(difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=f"{file_name}.backup",
        tofile=file_name,
        lineterm="",
        n=DIFF_CONTEXT_LINES,
    ))
    diff_truncated = False
    if len(unified_lines) > MAX_DIFF_LINES:
        unified_lines = unified_lines[:MAX_DIFF_LINES] + ["...<diff_truncated>"]
        diff_truncated = True
    unified_text = "\n".join(unified_lines)

    line_changes = collect_line_changes(before_lines, after_lines)
    added_lines = line_changes["added_lines"]
    removed_lines = line_changes["removed_lines"]

    added_truncated = len(added_lines) > MAX_DIFF_LINE_CHANGES
    removed_truncated = len(removed_lines) > MAX_DIFF_LINE_CHANGES
    if added_truncated:
        added_lines = added_lines[:MAX_DIFF_LINE_CHANGES]
    if removed_truncated:
        removed_lines = removed_lines[:MAX_DIFF_LINE_CHANGES]

    return {
        "format_version": "1.0",
        "diff_type": "unified",
        "context_lines": DIFF_CONTEXT_LINES,
        "unified_diff": unified_text,
        "stats": {
            "before_line_count": len(before_lines),
            "after_line_count": len(after_lines),
            "added_line_count": len(line_changes["added_lines"]),
            "removed_line_count": len(line_changes["removed_lines"]),
            "diff_truncated": diff_truncated,
            "added_truncated": added_truncated,
            "removed_truncated": removed_truncated,
        },
        "added_lines": added_lines,
        "removed_lines": removed_lines,
    }

def now_iso() -> str:
    """返回当前时间的 ISO 8601 字符串。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def build_guardian_event(
    filename: str,
    src_path: Path,
    backup_path: Path,
    current_hash: str,
    backup_hash: str,
    check_time: str,
) -> Dict[str, Any]:
    """构建用于记录的统一事件数据结构。"""
    before_content_raw = read_text_file(backup_path)
    after_content_raw = read_text_file(src_path)

    before_content, before_truncated = truncate_text(before_content_raw, MAX_CONTENT_CHARS)
    after_content, after_truncated = truncate_text(after_content_raw, MAX_CONTENT_CHARS)

    event_id = f"evt-{datetime.now().strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}"
    diff_payload = build_diff_payload(filename, before_content_raw, after_content_raw)

    return {
        "event_id": event_id,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "monitor.py",
        "monitor_version": MONITOR_VERSION,
        "trigger_type": "file_hash_mismatch",
        "check_time": check_time,
        "file_name": filename,
        "file_path": str(src_path),
        "old_hash": backup_hash,
        "new_hash": current_hash,
        "before_content": before_content,
        "after_content": after_content,
        "content_truncated": {
            "before": before_truncated,
            "after": after_truncated,
            "max_chars": MAX_CONTENT_CHARS,
        },
        "diff": diff_payload,
        "monitor_status": {
            "expected_interval_seconds": CHECK_INTERVAL,
            "backup_exists": backup_path.exists(),
        },
    }


# ===================== 核心工具函数 =====================
def calculate_file_hash(file_path: Path, hash_algorithm: str = "md5") -> Optional[str]:
    """计算文件哈希值，失败返回None"""
    try:
        if not file_path.exists():
            logging.warning(f"文件不存在: {file_path}")
            return None
        hash_obj = hashlib.new(hash_algorithm)
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logging.error(f"计算哈希失败 {file_path}：{str(e)}")
        return None

def calculate_self_hash() -> Optional[str]:
    """计算monitor.py自身哈希"""
    return calculate_file_hash(Path(__file__).resolve())

def get_backup_meta_path(backup_path: Path) -> Path:
    """获取备份文件对应的元数据路径"""
    return backup_path.with_suffix(backup_path.suffix + ".meta")

def set_readonly(file_path: Path):
    """设置文件只读（跨平台）"""
    try:
        current_mode = file_path.stat().st_mode
        readonly_mode = current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        os.chmod(file_path, readonly_mode)
        logging.debug(f"已设置只读: {file_path}")
    except Exception as e:
        logging.error(f"设置只读失败 {file_path}: {e}")

def rotate_backup(backup_dir: Path, base_name: str) -> None:
    """版本轮转：将备份文件与对应元数据作为一个整体向后推移。"""
    for v in range(MAX_BACKUP_VERSIONS, 0, -1):
        current = backup_dir / f"{base_name}.v{v}"
        current_meta = get_backup_meta_path(current)
        if v == MAX_BACKUP_VERSIONS:
            if current.exists():
                try:
                    current.unlink()
                    logging.info(f"删除旧版本: {current.name}")
                except Exception as e:
                    logging.error(f"删除旧版本失败 {current}: {e}")
            if current_meta.exists():
                try:
                    current_meta.unlink()
                    logging.info(f"删除旧版本元数据: {current_meta.name}")
                except Exception as e:
                    logging.error(f"删除旧版本元数据失败 {current_meta}: {e}")
        else:
            next_v = v + 1
            next_file = backup_dir / f"{base_name}.v{next_v}"
            next_meta = get_backup_meta_path(next_file)
            if current.exists():
                try:
                    current.rename(next_file)
                except Exception as e:
                    logging.error(f"重命名 {current} -> {next_file} 失败: {e}")
            if current_meta.exists():
                try:
                    current_meta.rename(next_meta)
                except Exception as e:
                    logging.error(f"重命名 {current_meta} -> {next_meta} 失败: {e}")

def save_backup_metadata(backup_path: Path, source_path: Path) -> None:
    """保存备份文件的元数据（原始路径、修改时间、哈希）"""
    try:
        meta_path = get_backup_meta_path(backup_path)
        src_stat = source_path.stat()
        metadata = {
            "original_path": str(source_path),
            "original_mtime": src_stat.st_mtime,
            "backup_time": datetime.now().timestamp(),
            "backup_hash": calculate_file_hash(backup_path),
            "source_hash": calculate_file_hash(source_path)
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        logging.debug(f"备份元数据已保存: {meta_path}")
    except Exception as e:
        logging.error(f"保存备份元数据失败 {backup_path}: {e}")

def verify_backup_integrity(backup_path: Path) -> bool:
    """校验备份文件的完整性：对比当前哈希与元数据中记录的哈希"""
    meta_path = get_backup_meta_path(backup_path)
    if not meta_path.exists():
        logging.critical(f"⚠️ 备份元数据不存在：{meta_path}")
        return False

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        recorded_hash = metadata.get("backup_hash")
        if not recorded_hash:
            logging.critical(f"⚠️ 元数据中无哈希记录：{meta_path}")
            return False

        current_hash = calculate_file_hash(backup_path)
        if current_hash is None:
            logging.error(f"无法计算备份哈希: {backup_path}")
            return False

        if current_hash != recorded_hash:
            logging.critical(f"⚠️ 备份文件完整性校验失败！{backup_path.name}")
            logging.critical(f"   记录哈希: {recorded_hash[:16]}...")
            logging.critical(f"   当前哈希: {current_hash[:16]}...")
            return False
        return True
    except Exception as e:
        logging.error(f"校验备份完整性时出错 {backup_path}: {e}")
        return False

def init_readonly_backup(source_path: Path, force_refresh: bool = False) -> bool:
    """创建只读备份。"""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        base_name = source_path.name
        backup_v1 = BACKUP_DIR / f"{base_name}.v1"

        if not source_path.exists():
            logging.error(f"源文件不存在: {source_path}")
            return False

        if backup_v1.exists():
            if not force_refresh:
                logging.debug(f"备份已是最新: {backup_v1}")
                return True
            rotate_backup(BACKUP_DIR, base_name)

        shutil.copy2(source_path, backup_v1)
        set_readonly(backup_v1)
        save_backup_metadata(backup_v1, source_path)

        logging.info(f"创建备份成功: {backup_v1}")
        return True
    except Exception as e:
        logging.error(f"备份失败 {source_path}：{str(e)}")
        return False

def get_latest_backup(filename: str) -> Path:
    """获取最新备份文件路径"""
    return BACKUP_DIR / f"{filename}.v1"

def cleanup_old_backups():
    """清理多余备份，确保每个文件备份数量不超过 MAX_BACKUP_VERSIONS"""
    for base_name in MONITOR_FILES:
        versions = []
        for f in BACKUP_DIR.glob(f"{base_name}.v*"):
            if f.name.endswith(".meta"):
                continue
            try:
                version_token = f.name.rsplit(".v", 1)[1]
                num = int(version_token)
                versions.append((num, f))
            except (IndexError, ValueError):
                continue
        versions.sort(reverse=True)
        if len(versions) > MAX_BACKUP_VERSIONS:
            for num, f in versions[MAX_BACKUP_VERSIONS:]:
                try:
                    f.unlink()
                    logging.info(f"清理多余备份: {f.name}")
                    meta = get_backup_meta_path(f)
                    if meta.exists():
                        meta.unlink()
                        logging.info(f"清理多余备份元数据: {meta.name}")
                except Exception as e:
                    logging.error(f"删除旧备份失败 {f}: {e}")

# ===================== 自身监控记录持久化 =====================
STATE_FILE = BACKUP_DIR / "monitor_state.json"

def load_state():
    """加载持久化状态（自身哈希和监控记录）"""
    global last_self_hash, self_monitor_records, file_hash_cache, reported_change_signatures, reported_new_hashes, last_recorded_hashes
    if not STATE_FILE.exists():
        return
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        last_self_hash = state.get("last_self_hash")
        self_monitor_records = state.get("self_monitor_records", [])
        loaded_hash_cache = state.get("file_hash_cache", {})
        if isinstance(loaded_hash_cache, dict):
            file_hash_cache = {
                str(name): str(signature)
                for name, signature in loaded_hash_cache.items()
                if isinstance(name, str) and isinstance(signature, str)
            }
        else:
            file_hash_cache = {}

        last_recorded_hashes = {}
        loaded_last_recorded_hashes = state.get("last_recorded_hashes", {})
        if isinstance(loaded_last_recorded_hashes, dict):
            for name, value in loaded_last_recorded_hashes.items():
                if not isinstance(name, str) or not isinstance(value, dict):
                    continue
                old_hash = value.get("old_hash")
                new_hash = value.get("new_hash")
                if not isinstance(old_hash, str) or not isinstance(new_hash, str):
                    continue
                normalized_value: Dict[str, str] = {
                    "old_hash": old_hash,
                    "new_hash": new_hash,
                }
                recorded_at = value.get("recorded_at")
                if isinstance(recorded_at, str):
                    normalized_value["recorded_at"] = recorded_at
                last_recorded_hashes[name] = normalized_value

        reported_change_signatures = {}
        loaded_reported_signatures = state.get("reported_change_signatures", {})
        if isinstance(loaded_reported_signatures, dict):
            for name, signatures in loaded_reported_signatures.items():
                if not isinstance(name, str) or not isinstance(signatures, list):
                    continue
                normalized_signatures: List[str] = []
                seen_signatures = set()
                for signature in signatures:
                    if not isinstance(signature, str):
                        continue
                    if signature in seen_signatures:
                        continue
                    normalized_signatures.append(signature)
                    seen_signatures.add(signature)
                if len(normalized_signatures) > MAX_CHANGE_SIGNATURES_PER_FILE:
                    normalized_signatures = normalized_signatures[-MAX_CHANGE_SIGNATURES_PER_FILE:]
                reported_change_signatures[name] = normalized_signatures

        reported_new_hashes = {}
        loaded_reported_new_hashes = state.get("reported_new_hashes", {})
        if isinstance(loaded_reported_new_hashes, dict):
            for name, hashes in loaded_reported_new_hashes.items():
                if not isinstance(name, str) or not isinstance(hashes, list):
                    continue
                normalized_hashes: List[str] = []
                seen_hashes = set()
                for hash_value in hashes:
                    if not isinstance(hash_value, str):
                        continue
                    if hash_value in seen_hashes:
                        continue
                    normalized_hashes.append(hash_value)
                    seen_hashes.add(hash_value)
                if len(normalized_hashes) > MAX_CHANGE_SIGNATURES_PER_FILE:
                    normalized_hashes = normalized_hashes[-MAX_CHANGE_SIGNATURES_PER_FILE:]
                reported_new_hashes[name] = normalized_hashes

        if len(self_monitor_records) > MAX_SELF_MONITOR_RECORDS:
            self_monitor_records = self_monitor_records[-MAX_SELF_MONITOR_RECORDS:]
        logging.info(
            "已加载状态: last_self_hash=%s... | file_hash_cache=%s | last_recorded_hashes=%s | reported_signatures=%s",
            last_self_hash[:16] if last_self_hash else None,
            len(file_hash_cache),
            len(last_recorded_hashes),
            sum(len(items) for items in reported_change_signatures.values()),
        )
    except Exception as e:
        logging.error(f"加载状态失败: {e}")

def save_state():
    """保存当前状态"""
    global last_self_hash, self_monitor_records, file_hash_cache, reported_change_signatures, reported_new_hashes, last_recorded_hashes
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "last_self_hash": last_self_hash,
            "self_monitor_records": self_monitor_records,
            "file_hash_cache": file_hash_cache,
            "last_recorded_hashes": last_recorded_hashes,
            "reported_change_signatures": reported_change_signatures,
            "reported_new_hashes": reported_new_hashes,
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        logging.debug("状态已保存")
    except Exception as e:
        logging.error(f"保存状态失败: {e}")


def has_reported_change_signature(filename: str, change_signature: str) -> bool:
    return change_signature in reported_change_signatures.get(filename, [])

def remember_change_signature(filename: str, change_signature: str) -> None:
    signatures = reported_change_signatures.setdefault(filename, [])
    if change_signature in signatures:
        return
    signatures.append(change_signature)
    if len(signatures) > MAX_CHANGE_SIGNATURES_PER_FILE:
        del signatures[: len(signatures) - MAX_CHANGE_SIGNATURES_PER_FILE]

def has_reported_new_hash(filename: str, new_hash: str) -> bool:
    return new_hash in reported_new_hashes.get(filename, [])

def remember_reported_new_hash(filename: str, new_hash: str) -> None:
    hashes = reported_new_hashes.setdefault(filename, [])
    if new_hash in hashes:
        return
    hashes.append(new_hash)
    if len(hashes) > MAX_CHANGE_SIGNATURES_PER_FILE:
        del hashes[: len(hashes) - MAX_CHANGE_SIGNATURES_PER_FILE]

def is_duplicate_with_last_record(filename: str, backup_hash: str, current_hash: str) -> bool:
    last_record = last_recorded_hashes.get(filename)
    if not isinstance(last_record, dict):
        return False
    last_new_hash = last_record.get("new_hash")
    if not isinstance(last_new_hash, str):
        return False
    if last_new_hash != current_hash:
        return False
    last_old_hash = last_record.get("old_hash")
    if isinstance(last_old_hash, str) and last_old_hash == backup_hash:
        logging.info(f"检测到与上次记录 old/new hash 完全重复，跳过记录: {filename}")
    else:
        logging.info(f"检测到 new_hash 与上次记录重复，跳过记录: {filename}")
    return True

def remember_last_recorded_hash(filename: str, backup_hash: str, current_hash: str) -> None:
    last_recorded_hashes[filename] = {
        "old_hash": backup_hash,
        "new_hash": current_hash,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def add_self_monitor_record(self_hash: str, file_path: str):
    """添加自身监控记录，自动保存"""
    global self_monitor_records
    record = {
        "monitor_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_path": file_path,
        "hash_format": "MD5",
        "self_hash": self_hash
    }
    self_monitor_records.append(record)
    if len(self_monitor_records) > MAX_SELF_MONITOR_RECORDS:
        self_monitor_records.pop(0)
    save_state()
    logging.info(f"【自身监控记录】最新{len(self_monitor_records)}/{MAX_SELF_MONITOR_RECORDS}条")
    logging.info(f"【自身监控详情】{json.dumps(record, ensure_ascii=False)}")

# ===================== 核心检测 =====================
def check_cognitive_file_changes():
    """检查认知文件变化（仅告警，不自动恢复）"""
    global last_self_hash, file_hash_cache
    now = datetime.now()
    check_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 1. 检测自身哈希
    self_path = str(Path(__file__).resolve())
    self_hash = calculate_self_hash()
    if self_hash:
        previous_self_hash = last_self_hash
        add_self_monitor_record(self_hash, self_path)
        if previous_self_hash and self_hash != previous_self_hash:
            logging.critical(f"🚨 主人！监控脚本被篡改！")
            logging.critical(f"   原哈希：{previous_self_hash}")
            logging.critical(f"   新哈希：{self_hash}")
            logging.critical(f"   文件位置：{self_path}")
        last_self_hash = self_hash
        save_state()

    # 2. 检测认知文件
    for filename in MONITOR_FILES:
        src = COGNITIVE_DIR / filename
        backup = get_latest_backup(filename)

        if not src.exists():
            logging.critical(f"🚨 主人！认知文件缺失：{filename}")
            logging.critical(f"   预期路径：{src}")
            if backup.exists():
                logging.critical(f"   可用备份：{backup}")
            else:
                logging.critical(f"   可用备份：无")
            continue

        if not backup.exists():
            logging.warning(f"备份不存在，正在初始化基线：{filename}")
            if not init_readonly_backup(src):
                logging.error(f"无法为 {filename} 创建初始备份，跳过本轮检测")
                continue
            backup = get_latest_backup(filename)

        if not backup.exists():
            logging.error(f"备份仍不存在，跳过比对: {filename}")
            continue

        current_hash = calculate_file_hash(src)
        backup_hash = calculate_file_hash(backup)
        if current_hash is None or backup_hash is None:
            logging.error(f"哈希计算失败，跳过比对: {filename}")
            continue

        logging.info(f"【比对记录】{check_time} | {filename} | 当前:{current_hash[:16]}... | 备份:{backup_hash[:16]}...")

        if current_hash == backup_hash:
            if filename in file_hash_cache:
                file_hash_cache.pop(filename, None)
                save_state()
            continue

        change_signature = f"{backup_hash}->{current_hash}"
        if file_hash_cache.get(filename) == change_signature:
            logging.info(f"检测到重复异常状态，跳过重复上报: {filename}")
            continue

        if has_reported_change_signature(filename, change_signature):
            logging.info(f"检测到历史相同 old->new hash 变更，跳过重复上报: {filename}")
            file_hash_cache[filename] = change_signature
            save_state()
            continue

        if has_reported_new_hash(filename, current_hash):
            logging.info(f"检测到历史相同 new_hash，跳过重复上报: {filename}")
            file_hash_cache[filename] = change_signature
            save_state()
            continue

        if is_duplicate_with_last_record(filename, backup_hash, current_hash):
            file_hash_cache[filename] = change_signature
            save_state()
            continue

        file_hash_cache[filename] = change_signature
        save_state()

        logging.critical(f"🚨 主人！认知文件被篡改：{filename}")
        logging.critical(f"   当前哈希：{current_hash}")
        logging.critical(f"   备份哈希：{backup_hash}")

        # 保存篡改前快照：轮转备份，旧 v1（干净版本）→ v2，当前文件（被篡改）→ 新 v1
        # 回滚时：/no0 rollback <file> v2 即可恢复到篡改前的干净状态
        try:
            init_readonly_backup(src, force_refresh=True)
            logging.info(f"已保存篡改前快照: {filename} (干净版本已轮转至 v2)")
        except Exception as e:
            logging.error(f"保存篡改前快照失败 {filename}: {e}")

        # 构建事件并写入变更日志（由本地 agent 分析，不再调用远程 API）
        try:
            event_payload = build_guardian_event(
                filename=filename,
                src_path=src,
                backup_path=backup,
                current_hash=current_hash,
                backup_hash=backup_hash,
                check_time=check_time,
            )
            diff_stats = event_payload.get("diff", {}).get("stats", {})
            logging.critical(
                "   diff统计：+%s / -%s | before=%s行 | after=%s行",
                diff_stats.get("added_line_count", 0),
                diff_stats.get("removed_line_count", 0),
                diff_stats.get("before_line_count", 0),
                diff_stats.get("after_line_count", 0),
            )

            record_time = now_iso()
            write_change_log(
                record_time=record_time,
                event_id=event_payload["event_id"],
                file_name=filename,
                event_payload=event_payload,
                json_file_path=CHANGE_LOG_JSON_FILE,
                md_file_path=CHANGE_LOG_MD_FILE,
                record_type="detected",
            )

            remember_change_signature(filename, change_signature)
            remember_reported_new_hash(filename, current_hash)
            remember_last_recorded_hash(filename, backup_hash, current_hash)
            save_state()
        except Exception as e:
            logging.error(f"处理篡改事件失败 {filename}: {e}", exc_info=True)

# ===================== 备份完整性定期校验 =====================
def verify_all_backups():
    """校验所有备份文件的完整性"""
    logging.info("开始备份完整性校验...")
    for filename in MONITOR_FILES:
        backup = get_latest_backup(filename)
        if backup.exists():
            if not verify_backup_integrity(backup):
                logging.critical(f"备份文件损坏！{filename} 的备份可能已损坏，请检查。")
    logging.info("备份完整性校验完成")

# ===================== 主循环 =====================
def monitor_loop(run_once: bool = False):
    global last_check_start, backup_verify_counter
    logging.info("===== OpenClaw 认知文件监控已启动 =====")
    logging.info(f"监控器版本：{MONITOR_VERSION}")
    logging.info(f"自身监控记录保留：最近 {MAX_SELF_MONITOR_RECORDS} 条")
    logging.info(f"备份版本数限制：{MAX_BACKUP_VERSIONS}")
    logging.info(f"备份校验间隔：每 {BACKUP_VERIFY_INTERVAL} 次循环")
    logging.info(f"日志文件最大大小：{LOG_MAX_BYTES // (1024*1024)} MB，最多保留 {LOG_BACKUP_COUNT} 个文件")
    logging.info(f"监听目录：{COGNITIVE_DIR}")
    logging.info(f"输出目录：{BASE_DIR}")
    logging.info(f"变更日志 JSON：{CHANGE_LOG_JSON_FILE}")
    logging.info(f"变更日志 Markdown：{CHANGE_LOG_MD_FILE}")

    # 创建目录
    COGNITIVE_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # 加载持久化状态
    load_state()

    # 清理多余备份（启动时执行一次）
    cleanup_old_backups()

    # 初始化所有存在的文件的备份
    for f in MONITOR_FILES:
        fp = COGNITIVE_DIR / f
        if fp.exists():
            init_readonly_backup(fp)

    last_check_start = time.time()
    backup_verify_counter = 0
    first_cycle = True

    while True:
        try:
            current_time = time.time()
            real_interval = current_time - last_check_start

            if not first_cycle and abs(real_interval - CHECK_INTERVAL) > 2:
                logging.critical(f"🚨 主人！检测间隔异常！预期30秒，实际{real_interval:.1f}秒")

            check_cognitive_file_changes()

            backup_verify_counter += 1
            if backup_verify_counter >= BACKUP_VERIFY_INTERVAL:
                verify_all_backups()
                backup_verify_counter = 0

            last_check_start = current_time

            if run_once:
                logging.info("run-once 模式：本轮检测已完成，程序退出。")
                break

            cost = time.time() - current_time
            wait = max(0, CHECK_INTERVAL - cost)
            first_cycle = False
            time.sleep(wait)

        except KeyboardInterrupt:
            logging.info("监控已手动停止")
            break
        except Exception as e:
            logging.error(f"运行异常: {e}", exc_info=True)
            time.sleep(CHECK_INTERVAL)

def parse_args():
    parser = argparse.ArgumentParser(description="OpenClaw 认知文件监控器")
    parser.add_argument("--run-once", action="store_true", help="只执行一轮检测后退出")
    parser.add_argument("--monitor-dir", help=f"监听目录，默认读取 {MONITOR_DIR_ENV}")
    parser.add_argument("--output-dir", help=f"输出目录，默认读取 {OUTPUT_DIR_ENV}")
    return parser.parse_args()


def configure_runtime(args: argparse.Namespace) -> None:
    monitor_dir = resolve_runtime_path(args.monitor_dir, MONITOR_DIR_ENV, DEFAULT_MONITOR_DIR)
    output_dir = resolve_runtime_path(args.output_dir, OUTPUT_DIR_ENV, DEFAULT_OUTPUT_DIR)
    set_runtime_paths(monitor_dir, output_dir)
    configure_logging()


if __name__ == "__main__":
    args = parse_args()
    configure_runtime(args)
    monitor_loop(run_once=args.run_once)
