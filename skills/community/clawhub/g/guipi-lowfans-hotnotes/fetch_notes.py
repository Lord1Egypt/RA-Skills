"""Fetch low-fans-hot notes from the liuchuan-data public API.

Single file, requests-only. API key resolution order:
  1. --key argument
  2. LIUCHUAN_API_KEY environment variable (legacy YAUNDIAN_API_KEY is
     still read as a fallback, with a rename warning)

Upstream limits measured 2026-11-25 (all three bite at once):
  * 20 rows per request (page_size is clamped to 20)
  * 1 request / minute
  * 1000 rows / day per key ("daily notes quota exhausted")
So rows are pulled page by page into a local cache that accumulates across
runs; a warm cache costs zero quota.

Keyless (anonymous) requests carry an X-Client-Id header: a per-device
UUID cached at ~/.liuchuan_client_id, auto-generated on first run. The
server pairs it with the per-IP quota (dual-track, smaller remaining
wins), so rotating IPs does not refill the anonymous allowance.

Account positioning (two server-side filters, combined as
category AND keyword):
  * --category <名称或ID>  SERVER-side filter on the official huitun
    category tree (笔记分类, /v1/categories). Comma-separated names/ids
    allowed (multi-category, OR). A parent covers its whole subtree
    (美食饮品 incl. 咖啡/酒类/...). Category coverage is ~74% of the
    12h window after the 2026-11-25 full-tree backfill (was ~24%);
    older windows and pre-backfill rows may still lack it.
  * --position <定位词>    NOT a server param: matches the user's account
    positioning words against the official tree and prints a numbered
    confirmation list via --plan (zero quota). Pure tree matching, no
    synonym table: exact name first, then substring on level-1/2 names.
    Users pick from official names (--list-categories) or candidates.
  * --body-keyword <词>    SERVER-side filter on the note body (desc_text),
    comma-separated words OR'd, literal match (no wildcards). Narrows
    the category recall.

Quota is charged on rows actually returned after server-side filtering,
so a narrow filter costs proportionally less.

Exit codes: 0 ok (possibly partial), 1 usage/config error,
2 network/rate-limit error, 3 api error, 4 daily quota exhausted with
nothing to show.
"""

import argparse
import contextlib
import html as html_lib
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import uuid
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:  # 沙箱/精简环境：--help / --selfcheck / --menu 不依赖 requests
    requests = None

# 通用客户端版：端点走环境变量，未配置时保持占位符（不发起任何请求）。
# 包内不出现真实 IP 与明文 HTTP——占位符域名 example.com 为保留域名。
PLACEHOLDER_BASE_URL = "https://your-liuchuan-api.example.com/liuchuan/api/v1"
BASE_URL = os.environ.get("LIUCHUAN_BASE_URL") or PLACEHOLDER_BASE_URL
LEGACY_BASE_URL = (os.environ.get("LIUCHUAN_LEGACY_BASE_URL")
                   or "https://your-liuchuan-api.example.com/yaundian/api/v1")
LEGACY_CACHE_DIR = Path.home() / ".yaundian_cache"  # 旧缓存目录，一次性迁到新目录
TIME_RANGES = ("12h", "24h", "yesterday", "3d", "7d")
SORTS = ("rank", "like", "collect", "comment", "share",
         "interaction", "updated")

# 编号选择：用户直接回 1/2/3 时由脚本自己换算，agent 不用记映射表
TIME_RANGE_BY_NO = {"1": "12h", "2": "24h", "3": "yesterday",
                    "4": "3d", "5": "7d"}          # 24h 当前上游异常


def parse_time_range(value: str) -> str:
    """--time-range 接编号 1-5 或 12h/yesterday/3d/7d 均可。"""
    v = (value or "").strip().lower()
    return TIME_RANGE_BY_NO.get(v, v)

PAGE_SIZE = 20           # upstream effective cap per request
DEFAULT_ROWS = 40        # 2 pages: enough for a category to show up, ~1.5 min
MAX_ROWS = 1000          # daily quota ceiling
TAG_CHIP_LIMIT = 40      # 标签筛选区最多列多少个标签胶囊（Top N，按样本内出现次数）
RETRIES = 4
PAGE_GAP = 62            # seconds between pages (1 request/minute upstream)
LAST_QUOTA = {"remaining": None, "at": ""}   # 最近一次额度头 X-Quota-Remaining-Notes


def _quota_file() -> Path:
    return CACHE_DIR / "quota.json"          # 落盘：缓存命中时也能答「剩余额度」


def store_quota(remaining, at: str) -> None:
    """把最近一次拿到的剩余额度落盘，跨进程/跨缓存命中都能读。"""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _quota_file().write_text(json.dumps({"remaining": remaining, "at": at},
                                           ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def load_quota() -> None:
    try:
        blob = json.loads(_quota_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if blob.get("remaining") is not None:
        LAST_QUOTA["remaining"] = blob["remaining"]
        LAST_QUOTA["at"] = blob.get("at") or ""
ANON_ROWS = 5            # 匿名体验档：单次封顶 5 条，单排序
ANON_DAILY = 10          # 匿名档每日配额（服务端 v1.24 起 5 → 10）
STALE_MINUTES = 15       # 入库超过这么多分钟就提醒「数据可能不是最新的」
CACHE_TTL = 3600         # seconds; quota is scarce, cache wants to be long


def _platform_dir(env_name: str, win_sub: str, other_sub: str) -> Path:
    """Windows 用 %LOCALAPPDATA%/%APPDATA%，其它系统用 ~/.cache / ~/.config。"""
    if os.name == "nt":
        base = os.environ.get(env_name) or str(
            Path.home() / "AppData" / ("Local" if env_name == "LOCALAPPDATA"
                                       else "Roaming"))
        return Path(base) / "liuchuan-data" / win_sub
    return Path.home() / other_sub / "liuchuan-data"


DEFAULT_CACHE_DIR = _platform_dir("LOCALAPPDATA", "cache", ".cache")
DEFAULT_CONFIG_DIR = _platform_dir("APPDATA", "config", ".config")
# 换路径的「指针」放固定位置，保证下次启动能找到用户改过的目录
PATHS_FILE = (_platform_dir("APPDATA", "", ".config") / "paths.json")
LEGACY_CACHE_DIR = Path.home() / ".liuchuan_cache"   # v1.34 以前的家目录缓存
try:
    _pointer = json.loads(PATHS_FILE.read_text(encoding="utf-8"))
    _pointer_cache = (_pointer.get("cache_dir") or "").strip()
except (OSError, ValueError):
    _pointer_cache = ""
CACHE_DIR = Path(
    os.environ.get("LIUCHUAN_CACHE_DIR")
    or os.environ.get("YAUNDIAN_CACHE_DIR")       # 旧变量名兜底
    or _pointer_cache
    or DEFAULT_CACHE_DIR)
CONFIG_DIR = Path(os.environ.get("LIUCHUAN_CONFIG_DIR") or DEFAULT_CONFIG_DIR)
HISTORY_DIR = CACHE_DIR / "history"    # 每次真实取数的时间戳快照（v1.30）
PROFILE_FILE = CONFIG_DIR / "profile.json"    # 固定下来的人设定位（v1.32）
LAST_RUN_FILE = CONFIG_DIR / "last_run.json"  # 最近一次成功取数的参数（只做推荐）
TAGS_FILE = CACHE_DIR / "theme_cache.json"   # 主题筛选的累积缓存（v1.33）


def _read_json(path: Path) -> dict:
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
        return blob if isinstance(blob, dict) else {}
    except (OSError, ValueError):
        return {}


def load_profile() -> dict:
    """读已固定的人设；没有就返回 {}。"""
    return _read_json(PROFILE_FILE)


def save_profile(blob: dict) -> None:
    PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_FILE.write_text(json.dumps(blob, ensure_ascii=False, indent=2),
                            encoding="utf-8")


def clear_profile() -> bool:
    try:
        PROFILE_FILE.unlink()
        return True
    except OSError:
        return False


def load_last_run() -> dict:
    return _read_json(LAST_RUN_FILE)


def record_last_run(blob: dict) -> None:
    try:
        LAST_RUN_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_RUN_FILE.write_text(json.dumps(blob, ensure_ascii=False),
                                 encoding="utf-8")
    except OSError:
        pass


def _refresh_path_globals() -> None:
    """路径改了之后，把依赖它们的全局常量一起重算。"""
    global HISTORY_DIR, PROFILE_FILE, LAST_RUN_FILE, TAGS_FILE
    HISTORY_DIR = CACHE_DIR / "history"
    PROFILE_FILE = CONFIG_DIR / "profile.json"
    LAST_RUN_FILE = CONFIG_DIR / "last_run.json"
    TAGS_FILE = CACHE_DIR / "theme_cache.json"


def configure_paths(cache_dir: str = "", config_dir: str = "") -> None:
    """按 命令行 > 环境变量 > paths.json 指针 > 平台默认 的顺序定目录。"""
    global CACHE_DIR, CONFIG_DIR
    if cache_dir:
        CACHE_DIR = Path(cache_dir).expanduser()
    if config_dir:
        CONFIG_DIR = Path(config_dir).expanduser()
    for d in (CACHE_DIR, CONFIG_DIR):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
    _refresh_path_globals()


def migrate_legacy_paths() -> str:
    """把 v1.34 以前的 ~/.liuchuan_cache 复制到新目录（只复制、不删除）。"""
    marker = CONFIG_DIR / ".paths_migrated"
    if marker.exists():
        return ""
    copied = 0
    try:
        if LEGACY_CACHE_DIR.exists() and CACHE_DIR != LEGACY_CACHE_DIR:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            for f in LEGACY_CACHE_DIR.glob("notes_*.json"):
                dst = CACHE_DIR / f.name
                if not dst.exists():
                    shutil.copy2(f, dst)
                    copied += 1
            if (LEGACY_CACHE_DIR / "history").exists():
                HISTORY_DIR.mkdir(parents=True, exist_ok=True)
                for f in (LEGACY_CACHE_DIR / "history").glob("*.json"):
                    dst = HISTORY_DIR / f.name
                    if not dst.exists():
                        shutil.copy2(f, dst)
                        copied += 1
            for name in ("theme_cache.json", "quota.json", "serve.json"):
                src = LEGACY_CACHE_DIR / name
                if src.exists() and not (CACHE_DIR / name).exists():
                    shutil.copy2(src, CACHE_DIR / name)
                    copied += 1
        # 人设 / 上次参数以前也放在缓存目录，迁到配置目录
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        for name, dst in (("profile.json", PROFILE_FILE),
                          ("last_run.json", LAST_RUN_FILE)):
            src = LEGACY_CACHE_DIR / name
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
                copied += 1
        marker.write_text(datetime.now().strftime("%Y-%m-%d %H:%M"),
                          encoding="utf-8")
    except OSError:
        return ""
    return (f"已把旧缓存复制到新目录：{copied} 个文件"
            f"（{LEGACY_CACHE_DIR} 原样保留，未删除）。") if copied else ""


def set_cache_dir(new_dir: str) -> str:
    """用户显式改缓存目录：复制现有文件过去，并写指针供以后启动读取。"""
    global CACHE_DIR
    new = Path(new_dir).expanduser()
    if not new.is_absolute():
        new = (Path.cwd() / new).resolve()
    try:
        new.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return f"ERROR: 目录不可用：{new}（{exc}）"
    copied = 0
    try:
        for f in CACHE_DIR.glob("notes_*.json"):
            if not (new / f.name).exists():
                shutil.copy2(f, new / f.name)
                copied += 1
        if HISTORY_DIR.exists():
            (new / "history").mkdir(exist_ok=True)
            for f in HISTORY_DIR.glob("*.json"):
                if not (new / "history" / f.name).exists():
                    shutil.copy2(f, new / "history" / f.name)
                    copied += 1
        if TAGS_FILE.exists() and not (new / "theme_cache.json").exists():
            shutil.copy2(TAGS_FILE, new / "theme_cache.json")
            copied += 1
        PATHS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PATHS_FILE.write_text(json.dumps({"cache_dir": str(new)},
                                         ensure_ascii=False, indent=2),
                              encoding="utf-8")
    except OSError as exc:
        return f"ERROR: 复制缓存失败：{exc}"
    CACHE_DIR = new
    _refresh_path_globals()
    return (f"缓存目录已改为：{new}（复制了 {copied} 个文件；"
            f"指针写进 {PATHS_FILE}）。人设/配置仍在 {CONFIG_DIR}。")


def theme_scope(category: str) -> str:
    return (category or "").strip() or "全库"


def load_theme_cache(category: str) -> dict:
    """读该类目累积下来的主题组与原始标签频次（v1.33）。"""
    blob = _read_json(TAGS_FILE)
    return (blob.get("scopes") or {}).get(theme_scope(category), {}) or {}


def merge_theme_cache(category: str, groups: list, items: list,
                      batch_id: str, stamp: str) -> None:
    """把本批主题组 / 原始标签并进本地缓存，同一批只累加一次。

    - groups：agent 提炼的 [(主题名, [词...]), ...]，词取并集，老组永不丢
    - raw：原始标签 → 累计出现的笔记数，供「没被任何主题覆盖」的标签单独成胶囊
    """
    blob = _read_json(TAGS_FILE)
    scopes = blob.setdefault("scopes", {})
    sc = scopes.setdefault(theme_scope(category),
                           {"groups": [], "raw": {}, "last_batch": ""})
    new_batch = bool(batch_id) and sc.get("last_batch") != batch_id
    by_name = {g.get("name"): g for g in sc.setdefault("groups", [])}
    if new_batch:
        for it in items:
            for tag in (it.get("tags") or []):
                tag = str(tag).strip()
                if not tag:
                    continue
                rec = sc.setdefault("raw", {}).setdefault(
                    tag, {"n": 0, "last": ""})
                rec["n"] += 1
                rec["last"] = stamp
    for gname, members in groups or []:
        g = by_name.get(gname)
        fresh = g is None
        if fresh:
            g = {"name": gname, "terms": [], "seen": 0}
            sc["groups"].append(g)
            by_name[gname] = g
        known = {str(x).lower() for x in g["terms"]}
        for m in members:
            m = str(m).strip()
            if m and m.lower() not in known:
                g["terms"].append(m)
                known.add(m.lower())
        # 新组补记一次命中；老组只在「新一批」时累加，避免重渲染重复计数
        if fresh or new_batch:
            lows = [str(x).lower() for x in g["terms"]]
            g["seen"] = (g.get("seen") or 0) + sum(
                1 for it in items
                if any(w in _note_hay(it) for w in lows))
    sc["last_batch"] = batch_id
    sc["updated_at"] = stamp
    blob["updated_at"] = stamp
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        TAGS_FILE.write_text(json.dumps(blob, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    except OSError:
        pass


def profile_label(prof: dict) -> str:
    """人设的一句话描述，给问卷/确认文案复用。"""
    cat = prof.get("category") or "全库"
    pos = "、".join(prof.get("position") or []) or "-"
    kw = prof.get("body_keyword") or "-"
    return f"类目 {cat}｜定位 {pos}｜正文词 {kw}"


def filter_of(prof: dict) -> str:
    """min_like / max_fans → 问卷第 5 题的选项号。"""
    lo = prof.get("min_like") or 0
    hi = prof.get("max_fans") or 0
    if not lo and not hi:
        return "1"
    if lo and not hi and lo == 1000:
        return "2"
    if hi and not lo and hi == 1000:
        return "3"
    if lo == 1000 and hi == 1000:
        return "4"
    return "5"


def rows_option(rows) -> str:
    try:
        rows = int(rows)
    except (TypeError, ValueError):
        rows = DEFAULT_ROWS
    if rows <= 20:
        return "1"
    if rows <= 40:
        return "2"
    if rows >= MAX_ROWS:
        return "3"
    return "4"


def mix_option(mix) -> str:
    mix = tuple(mix or ("like", "collect"))
    if len(mix) >= 3:
        return "4"
    if len(mix) == 1:
        return "2" if mix[0] == "like" else "3"
    return "1"


def migrate_legacy_cache() -> None:
    """把旧缓存目录 ~/.yaundian_cache 里缺的历史取数结果补到新目录。

    逐文件比对：新目录缺哪份 notes_*.json 就复制哪份，已存在的一律不覆盖；
    旧目录原样保留（不删）。quota / serve 这类运行态文件不迁，免得把旧的
    额度数字或端口状态带进新目录。
    """
    try:
        if CACHE_DIR.name != ".liuchuan_cache":
            return                      # 用户显式指定了别的目录，不动
        if not LEGACY_CACHE_DIR.exists():
            return
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        copied = 0
        for f in LEGACY_CACHE_DIR.glob("notes_*.json"):
            dst = CACHE_DIR / f.name
            if not dst.exists():
                shutil.copy2(f, dst)    # 复制不搬移，旧目录留着备查
                copied += 1
        if copied:
            print(f"... 已从 {LEGACY_CACHE_DIR} 补 {copied} 份历史缓存到 "
                  f"{CACHE_DIR}（旧目录保留）", file=sys.stderr)
    except OSError:
        pass                            # 迁移失败不影响主流程，最多重新取数

EXIT_QUOTA = 4

# --type values map to the server note_type filter: "" (all) / normal /
# video. Rows with a NULL note_type (pre-2026-11-25 legacy rows) only show
# up under "all" - unknown type is never guessed into a bucket.
TYPE_LABEL = {"": "全部", "normal": "图文", "video": "视频"}
# 编号选择：菜单【内容类型】回 1/2/3 或中文/英文名都能吃
TYPE_BY_NO = {"1": "all", "2": "video", "3": "normal",
              "all": "all", "全部": "all", "video": "video", "视频": "video",
              "normal": "normal", "图文": "normal", "image": "normal"}


def parse_type(value: str) -> str:
    """--type 接 1/2/3 编号，或 all/video/normal、全部/视频/图文。"""
    v = (value or "").strip().lower()
    return TYPE_BY_NO.get(v, v)

def normalize(text: str) -> str:
    return (text or "").strip().lower()


# ---------------------------------------------------------------- local cache

def cache_slug(category: str = "", keyword: str = "",
               note_type: str = "") -> str:
    return "_".join(p for p in (_safe_name(category) if category else "all",
                                _safe_name(keyword) if keyword else "all",
                                _safe_name(note_type) if note_type else "all"))


def cache_file(time_range: str, sort: str, category: str = "",
               keyword: str = "", note_type: str = "") -> Path:
    # note_type in the slug: a type-filtered query must never read a cache
    # written by an all-types pull (or the other type) - that would serve
    # mixed rows for a video-only ask.
    return CACHE_DIR / (f"notes_{time_range}_{sort}_"
                        f"{cache_slug(category, keyword, note_type)}.json")


def load_cache(time_range: str, sort: str, ttl: int,
               category: str = "", keyword: str = "",
               note_type: str = "") -> dict:
    f = cache_file(time_range, sort, category, keyword, note_type)
    if not f.exists():
        return {}
    try:
        blob = json.loads(f.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    if time.time() - blob.get("saved_at", 0) > ttl:
        return {}
    return blob


def save_cache(time_range: str, sort: str, items: list, meta: dict,
               saved_at: float, category: str = "", keyword: str = "",
               note_type: str = "") -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path = cache_file(time_range, sort, category, keyword, note_type)
        path.write_text(
            json.dumps({
                "saved_at": saved_at,
                "meta": {k: meta.get(k) for k in ("time_range",
                                                  "data_updated_at", "total",
                                                  "note_type",
                                                  "quota_remaining")},
                "items": items,
            }, ensure_ascii=False), encoding="utf-8")
        # 历史快照（v1.30）：真实取数落一份带时间戳副本，供「筛选时间」回看
        try:
            HISTORY_DIR.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y%m%d_%H%M",
                                  time.localtime(saved_at or time.time()))
            snap = HISTORY_DIR / f"{path.stem}__{stamp}.json"
            if not snap.exists():
                shutil.copy2(path, snap)
        except OSError:
            pass
    except OSError:
        pass  # cache is best-effort, never fail the query over it


def fmt_fetch(ts: float) -> str:
    """取数/缓存快照时间 → 「YYYY-MM-DD HH:MM」（看板上的获取时间）。"""
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts else ""


def load_cache_history(scope: str, exclude: list = None) -> list:
    """读同一取数范围（同 category，或同 keyword/类型的完整 slug）的历史快照。

    优先读 history/ 下的时间戳快照；顺带读主缓存目录里同范围的其它文件
    （例如同一查询的另一种排序），都按 saved_at 标记获取时间。
    exclude 是本次查询自己的缓存文件，避免重复。
    """
    skip = {Path(p).resolve() for p in (exclude or []) if p}
    found = {}
    cands = []
    pat = f"notes_*_*_{scope}*.json"
    if HISTORY_DIR.exists():
        cands += list(HISTORY_DIR.glob(pat))
    if CACHE_DIR.exists():
        cands += list(CACHE_DIR.glob(pat))
    for f in cands:
        try:
            if f.resolve() in skip:
                continue
            blob = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        rows = blob.get("items") or []
        if not rows:
            continue
        ts = blob.get("saved_at") or 0
        if not ts:
            try:
                ts = f.stat().st_mtime
            except OSError:
                ts = 0
        found[str(f.resolve())] = (ts, rows)
    return sorted(found.values(), key=lambda x: x[0])


def seed_history_from_cache() -> None:
    """把已有的主缓存文件补一份到 history/（只补缺、不覆盖）。

    历史快照功能是 v1.30 才加的，早先的缓存没有快照；这里按各文件自己的
    saved_at 生成时间戳副本，让「筛选时间」马上就有历史可看。
    """
    try:
        if not CACHE_DIR.exists():
            return
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        added = 0
        for f in CACHE_DIR.glob("notes_*.json"):
            try:
                blob = json.loads(f.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            ts = blob.get("saved_at") or 0
            if not ts:
                try:
                    ts = f.stat().st_mtime
                except OSError:
                    continue
            stamp = time.strftime("%Y%m%d_%H%M", time.localtime(ts))
            snap = HISTORY_DIR / f"{f.stem}__{stamp}.json"
            if not snap.exists():
                shutil.copy2(f, snap)
                added += 1
        if added:
            print(f"... 已为 {added} 份既有缓存补建历史快照", file=sys.stderr)
    except OSError:
        pass


def clear_local_cache() -> str:
    """清除本地已取到的数据缓存（notes_*.json + 历史快照），额度/预览状态保留。"""
    if not CACHE_DIR.exists():
        return "本地缓存目录不存在，无需清除。"
    files = sorted(CACHE_DIR.glob("notes_*.json"))
    if HISTORY_DIR.exists():
        files += sorted(HISTORY_DIR.glob("*.json"))
    if TAGS_FILE.exists():
        files.append(TAGS_FILE)          # 主题筛选缓存跟着样本一起清，避免空壳主题
    size = 0
    removed = 0
    for f in files:
        try:
            size += f.stat().st_size
            f.unlink()
            removed += 1
        except OSError:
            pass
    return (f"已清除本地取数缓存：{removed} 个缓存文件 / "
            f"{size / 1024 / 1024:.2f} MB；额度快照与预览服务状态保留。")


# ------------------------------------------------------------------ transport

CLIENT_ID_PATH = Path.home() / ".liuchuan_client_id"
_CLIENT_ID_WARNED = False        # 双轨退化只提醒一次/进程


def _client_id() -> str:
    """Stable per-device id sent as X-Client-Id on keyless requests.

    Generated on first run and cached on disk (~/.liuchuan_client_id,
    0600); the user never has to look at it. The server pairs it with
    the per-IP quota as a second track, so rotating IPs does not refill
    the anonymous allowance. A read-only home degrades to no header
    (server falls back to per-IP tracking only) — that's silent on the
    wire, so we warn once on stderr instead.
    """
    global _CLIENT_ID_WARNED
    try:
        if CLIENT_ID_PATH.exists():
            cid = CLIENT_ID_PATH.read_text(encoding="utf-8").strip()
            if re.match(r"^[A-Za-z0-9_-]{8,64}$", cid):
                return cid
        cid = uuid.uuid4().hex
        CLIENT_ID_PATH.write_text(cid, encoding="utf-8")
        try:
            os.chmod(CLIENT_ID_PATH, 0o600)
        except OSError:
            pass
        return cid
    except OSError as e:
        if not _CLIENT_ID_WARNED:
            _CLIENT_ID_WARNED = True
            print(f"WARN: 无法写入 {CLIENT_ID_PATH}（{e.strerror or e}）：本次不带 "
                  "X-Client-Id，匿名档配额只能按单个 IP 计。", file=sys.stderr)
        return ""


def probe_meta(base_url: str, key: str = "") -> dict:
    """GET /v1/meta —— 公开端点，零配额、不计匿名预算、不受 UA 闸门限制。

    只用来探活 + 看数据新鲜度（last_ingest_at / 各维度 updated_at）。
    """
    if requests is None:
        return {}
    try:
        resp = requests.get(f"{base_url.rstrip('/')}/meta",
                            headers={"X-API-Key": key} if key else {},
                            timeout=12)
        if resp.status_code != 200:
            return {}
        return ((resp.json() or {}).get("data") or {})
    except (requests.RequestException, ValueError):
        return {}


def stale_note(meta: dict, limit_min: int = STALE_MINUTES) -> str:
    """入库超过 limit_min 分钟就返回一句提醒（采集端可能停了）。"""
    ts = (meta or {}).get("last_ingest_at") or ""
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        return ""
    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    gap_min = int((now - dt).total_seconds() // 60)
    if gap_min < limit_min:
        return ""
    rng = ((meta.get("ranges") or {}).get("12h") or {}).get("updated_at") or ""
    return (f"数据可能不是最新的：服务端最近入库 {ts[:16]}，距今约 {gap_min} 分钟"
            + (f"（12h 榜更新于 {rng[:16]}）" if rng else "")
            + "，采集端可能停了，本次拿到的会是旧榜。")


class FetchError(Exception):
    def __init__(self, kind: str, message: str, wait: int = 0):
        super().__init__(message)
        self.kind = kind          # 'key' | 'quota' | 'rate' | 'network' | 'api'
        self.message = message
        self.wait = wait


def _need_requests() -> None:
    """requests 缺失时给出可操作报错（不裸 AttributeError）。"""
    if requests is None:
        raise FetchError("network",
                         "当前环境未安装 requests 库，请先执行 pip install requests")


def fetch_page(base_url: str, key: str, time_range: str, sort: str,
               page: int, category: str = "", keyword: str = "",
               note_type: str = "") -> dict:
    """One GET /notes call. Retries 429 (rate only), 5xx and broken bodies."""
    _need_requests()
    url = f"{base_url.rstrip('/')}/notes"
    params = {"time_range": time_range, "sort": sort,
              "page": page, "page_size": PAGE_SIZE}
    if category:
        params["category"] = category
    if keyword:
        params["keyword"] = keyword
    if note_type:
        params["note_type"] = note_type
    for attempt in range(1, RETRIES + 1):
        try:
            hdrs = {}
            if key:
                hdrs["X-API-Key"] = key
            else:
                cid = _client_id()   # 匿名档设备标识，服务端双轨配额用
                if cid:
                    hdrs["X-Client-Id"] = cid
            resp = requests.get(url, params=params,
                                headers=hdrs, timeout=25)
        except requests.RequestException as e:
            if attempt == RETRIES:
                raise FetchError("network", f"network error: {e}")
            time.sleep(2 * attempt)
            continue

        if resp.status_code == 401:
            raise FetchError("key", "api key rejected (invalid or expired)")
        if resp.status_code == 429:
            try:
                detail = str((resp.json() or {}).get("detail", ""))
            except ValueError:
                detail = resp.text or ""
            low = detail.lower()
            if "user-agent" in low or "blocked" in low:
                # 匿名档 UA 闸门（服务端风控，非故障）：同一 UA 重试无用
                raise FetchError(
                    "key",
                    "匿名档拦截脚本 UA（服务端风控，重试无用）：配置 "
                    "LIUCHUAN_API_KEY 后即可正常访问；已配置仍报此错，检查是否"
                    "被旧变量 YAUNDIAN_API_KEY 覆盖。服务端原文：" + detail)
            if "budget" in low:
                raise FetchError(
                    "quota",
                    "匿名档的全局日预算（2000 条）已被用尽，今天所有匿名请求都会"
                    "被拒，与你的 Key 无关；配 Key 不受影响，否则等次日 0 点。"
                    "服务端原文：" + detail)
            if "daily request limit" in low:
                raise FetchError(
                    "quota",
                    "本机 IP 今日的匿名请求次数（30 次）已用完；配 Key 或等次日 "
                    "0 点重置。服务端原文：" + detail)
            if ("quota" in low or "rows used" in low or "exhausted" in low
                    or "free tier" in low):
                raise FetchError("quota", detail)   # 匿名 10 条/Key 日配额
            m = re.search(r"retry in (\d+)s", detail, re.I)
            wait = (int(m.group(1)) + 20) if m else 75
            if attempt == RETRIES:
                raise FetchError("rate", "still rate limited", wait)
            print(f"... 触发限流，等待 {wait}s（接口限速 1 请求/分钟）",
                  file=sys.stderr)
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            if attempt == RETRIES:
                raise FetchError("network", f"http {resp.status_code}")
            time.sleep(2 * attempt)
            continue
        if resp.status_code != 200:
            raise FetchError("api", f"http {resp.status_code}: "
                                    f"{resp.text[:120]}")
        try:
            body = resp.json()
        except ValueError:
            if attempt == RETRIES:
                raise FetchError("api", f"non-json body: {resp.text[:60]!r}")
            time.sleep(2 * attempt)
            continue
        if body.get("code") != 0:
            raise FetchError("api", f"api code={body.get('code')} "
                                    f"msg={body.get('message', '')}")
        rem = (resp.headers.get("X-Quota-Remaining-Notes") or "").strip()
        data = body.get("data") or {}
        rows_now = len(data.get("items") or [])
        # 服务端刚重启时额度计数器未初始化，会先回一个 0 但照样返回数据；
        # 这种"0 条额度还能出数据"显然不可信，丢掉不写盘、不覆盖已有快照。
        if rem and not (rem == "0" and rows_now > 0):
            LAST_QUOTA["remaining"] = rem      # 服务端回报的当日剩余条数
            LAST_QUOTA["at"] = time.strftime("%Y-%m-%d %H:%M",
                                             time.localtime())
            store_quota(rem, LAST_QUOTA["at"])   # 落盘，缓存命中时也能报额度
        return data
    raise FetchError("network", "request failed")


def fetch_categories(base_url: str, key: str) -> list:
    """GET /v1/categories (flat). Reference data, costs no row quota."""
    _need_requests()
    url = f"{base_url.rstrip('/')}/categories"
    resp = requests.get(url, params={"flat": 1},
                        headers={"X-API-Key": key} if key else {}, timeout=25)
    if resp.status_code != 200:
        raise FetchError("api", f"categories http {resp.status_code}: "
                                f"{resp.text[:120]}")
    body = resp.json()
    if body.get("code") != 0:
        raise FetchError("api", f"categories code={body.get('code')}")
    return (body.get("data") or {}).get("items") or []


def print_categories(items: list) -> None:
    """Print the official tree: level-1 with their level-2 children."""
    by_parent = {}
    for it in items:
        by_parent.setdefault(it.get("parent_id"), []).append(it)
    print("官方笔记分类（--category 传名称或 ID；父类自动覆盖全部子类）：")
    for root in by_parent.get(None, []):
        kids = by_parent.get(root["id"], [])
        print(f"{root['id']:>6}  {root['name']}"
              f"（{len(kids)} 个二级）")
        for k in kids[:12]:
            print(f"          └ {k['id']:>6}  {k['name']}")
        if len(kids) > 12:
            print(f"          └ ...另 {len(kids) - 12} 个二级")


def match_position_categories(position_tokens: list, cat_items: list) -> list:
    """Match account-positioning words against the official tree.

    Pure official-tree matching, no synonym table:
      1. exact name hit, level-1 preferred (家居家装 hits, 家居装修 misses)
      2. substring either way on level-1/2 names ("母婴" -> 母婴育儿,
         "美妆护肤" -> 美妆 + 护肤)
    Level-3 leaves only join via an exact hit. Returns deduped candidates
    sorted level-1 first, capped at 15, each carrying its match source.
    """
    ordered = sorted(cat_items, key=lambda x: x.get("level") or 9)
    by_name = {}
    for it in ordered:
        if it.get("name"):
            by_name.setdefault(normalize(it["name"]), it)
    lv12 = [it for it in ordered if it.get("level") in (1, 2)]

    cands, seen_ids = [], set()

    def add(node: dict, source: str) -> None:
        if node["id"] in seen_ids or len(cands) >= 15:
            return
        seen_ids.add(node["id"])
        cands.append({"id": node["id"], "name": node["name"],
                      "level": node["level"], "path": node.get("path") or "",
                      "source": source})

    for raw in position_tokens:
        t = normalize(raw)
        if len(t) < 2:
            continue
        node = by_name.get(t)
        if node:
            add(node, "精确")
        for it in lv12:
            n = normalize(it["name"])
            if n and n != t and (t in n or n in t):
                add(it, "模糊")
    cands.sort(key=lambda c: (c["level"], c["id"]))
    return cands


def print_position_plan(position_tokens: list, cat_items: list) -> None:
    """Print the numbered confirmation list for position -> category."""
    if not position_tokens:
        print("--plan 需要 --position（账号定位词，如 --position 职场）")
        return
    cands = match_position_categories(position_tokens, cat_items)
    print(f"账号定位「{'、'.join(position_tokens)}」→ 官方分类候选"
          f"（零配额，确认后用 --category 正式取数）：")
    print()
    for i, c in enumerate(cands, 1):
        lv = "一级" if c["level"] == 1 else ("二级" if c["level"] == 2 else "三级")
        print(f"  {i:>2} [{lv}·{c['source']}] {c['path'] or c['name']}")
    print()
    if not cands:
        print("（无候选：官方分类树里没有该定位词。先跑 --list-categories "
              "看 31 个一级分类全名，或直接用 --body-keyword 按正文词检索）")
        return
    exact = [c["name"] for c in cands if c["source"] == "精确"]
    if exact:
        print(f"推荐直接采用精确命中：--category \"{','.join(exact)}\"")
    print("用户回复编号后，用 --category \"<选中类名逗号分隔>\" 正式取数；"
          "服务端对该类目子树全量过滤，按返回条数扣费。")


def collect_for_sort(base_url: str, key: str, time_range: str, sort: str,
                     rows: int, refresh: bool,
                     category: str = "", keyword: str = "",
                     note_type: str = "") -> tuple:
    """Accumulate `rows` rows for one sort order into its own cache file.

    Returns (items, meta, from_cache). Partial results are normal here: the
    daily quota can cut a pull short, and whatever arrived stays usable.
    """
    blob = {} if refresh else load_cache(time_range, sort, CACHE_TTL,
                                         category, keyword, note_type)
    items = list(blob.get("items") or [])
    meta = dict(blob.get("meta") or {})
    saved_at = blob.get("saved_at") or time.time()
    from_cache = bool(blob)

    while len(items) < rows:
        page = len(items) // PAGE_SIZE + 1
        try:
            data = fetch_page(base_url, key, time_range, sort, page,
                              category, keyword, note_type)
        except FetchError as e:
            if e.kind == "quota":
                print(f"NOTE: 配额已用尽（{e.message}）。"
                      f"手头 {len(items)} 条仍可用。", file=sys.stderr)
                break
            if e.kind == "rate":
                print(f"NOTE: 仍被限流，手头 {len(items)} 条先返回；"
                      f"约 {e.wait}s 后可再试。", file=sys.stderr)
                break
            if e.kind == "key":
                print(f"ERROR: {e.message}. 检查 LIUCHUAN_API_KEY"
                      "（旧名 YAUNDIAN_API_KEY 已停用）或联系发放方。",
                      file=sys.stderr)
                sys.exit(3)
            if items:
                print(f"NOTE: 取数中断（{e.message}），返回手头 "
                      f"{len(items)} 条。", file=sys.stderr)
                break
            print(f"ERROR: {e.message}", file=sys.stderr)
            sys.exit(2 if e.kind == "network" else 3)

        meta.update({k: data.get(k) for k in
                     ("time_range", "data_updated_at", "total")})
        if LAST_QUOTA["remaining"] is not None:
            meta["quota_remaining"] = LAST_QUOTA["remaining"]
        got = data.get("items") or []
        if not got:
            break
        seen = {i.get("note_id") for i in items}
        items.extend([i for i in got if i.get("note_id") not in seen])
        saved_at = time.time()
        save_cache(time_range, sort, items, meta, saved_at, category,
                   keyword, note_type)

        total = meta.get("total") or 0
        if len(items) >= total or len(items) >= MAX_ROWS:
            break
        if len(items) < rows:
            print(f"... [{sort}] 已取 {len(items)}/{rows} 条，等待 {PAGE_GAP}s "
                  "取下一页（接口 1 请求/分钟）", file=sys.stderr)
            time.sleep(PAGE_GAP)

    meta["pulled"] = len(items)
    meta["cached_at"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(saved_at))
    return items, meta, from_cache


def collect(base_url: str, key: str, time_range: str, mix: tuple,
            rows: int, refresh: bool, category: str = "",
            keyword: str = "", note_type: str = "") -> tuple:
    """Pull rows across several sort orders, then merge into one pool.

    A single sort only ever surfaces its own head, so one ordering gives a
    narrow slice (top-likes are mostly entertainment). Splitting the quota
    across like + collect widens the content mix, which is what makes a
    category actually show up in a 40-row sample.
    """
    per = max(PAGE_SIZE, rows // max(1, len(mix)))
    pool, metas, cached = [], [], []
    for sort in mix:
        items, meta, from_cache = collect_for_sort(
            base_url, key, time_range, sort, per, refresh, category,
            keyword, note_type)
        pool.extend(items)
        metas.append(meta)
        cached.append(from_cache)

    seen, merged = set(), []
    for it in pool:
        nid = it.get("note_id")
        if nid in seen:
            continue
        seen.add(nid)
        merged.append(it)

    meta = {
        "time_range": time_range,
        "total": max((m.get("total") or 0) for m in metas) if metas else 0,
        "data_updated_at": max((m.get("data_updated_at") or "")
                               for m in metas) if metas else "",
        "pulled": len(merged),
        "pulled_by_sort": {s: m.get("pulled") for s, m in zip(mix, metas)},
        "cached_at": (metas[0] or {}).get("cached_at", ""),
        "quota_remaining": next((m.get("quota_remaining") for m in metas
                                 if m.get("quota_remaining") is not None),
                                LAST_QUOTA["remaining"]),
        "quota_at": LAST_QUOTA.get("at") or "",
    }
    return merged, meta, all(cached)


# ------------------------------------------------------------------- filtering

def parse_tag_groups(spec: str) -> list:
    """把「主题=标签a,标签b;主题2=标签c」解析成 [(主题, [标签...])]。

    看板标签筛选不写死：agent 取完数、看过样本的 tags 分布后，自己归组再传
    进来；同一篇笔记命中组内任一标签即算该组命中。
    """
    out = []
    for chunk in (spec or "").replace("\n", ";").split(";"):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk:
            continue
        name, members = chunk.split("=", 1)
        name = name.strip()
        members = [m.strip() for m in
                   members.replace("|", ",").replace("、", ",").split(",")
                   if m.strip()]
        if name and members:
            out.append((name, members))
    return out


def filter_items(items: list, min_like: int, max_fans: int) -> list:
    """Client-side filters the server API does not support."""
    out = items
    if min_like > 0:
        out = [it for it in out if (it.get("like_count") or 0) >= min_like]
    if max_fans > 0:
        # fans_count == 0 passes: upstream may not report fans for every
        # note, and a missing value must not drop a genuinely low-fans hit.
        out = [it for it in out
               if (it.get("fans_count") or 0) == 0
               or (it.get("fans_count") or 0) <= max_fans]
    return out


def sort_field(sort: str) -> str:
    return "interaction" if sort == "interaction" else f"{sort}_count"


def sort_items(items: list, sort: str) -> list:
    """Local sort over the cached rows.

    rank goes ascending so rank 1 (board head) comes first; the server's own
    rank sort is descending, i.e. board tail first, which is not what users
    mean by "榜内排名".
    """
    if sort == "rank":
        return sorted(items, key=lambda i: i.get("rank_no") or 0)
    if sort == "updated":
        return sorted(items, key=lambda i: i.get("last_seen_at") or "",
                      reverse=True)
    return sorted(items, key=lambda i: i.get(sort_field(sort)) or 0,
                  reverse=True)


def print_table(items: list) -> None:
    for it in items:
        tags = ",".join(it.get("tags") or [])[:20]
        tmark = {"video": "[视频]", "normal": "[图文]"}.get(
            it.get("note_type") or "", "")
        print(f"#{it.get('rank_no'):>4} | {tmark:<4}{it.get('title', '')[:26]:<26} | "
              f"author={it.get('author', '')[:10]:<10} | "
              f"like={it.get('like_count', 0):>5} | "
              f"coll={it.get('collect_count', 0):>4} | "
              f"cmt={it.get('comment_count', 0):>4} | "
              f"fans={it.get('fans_count', 0):>5} | {tags}")


TOP_CATEGORIES = ("美妆", "护肤", "个护香氛", "母婴育儿", "时尚", "潮流",
                  "美食饮品", "家居家装", "二次元", "户外", "萌宠动物",
                  "健身减肥", "婚嫁", "教育学习", "影音娱乐", "新闻资讯",
                  "体育运动", "生活记录", "职场", "情感", "艺术", "人文社科",
                  "兴趣爱好", "摄影", "游戏", "科技数码", "星座命理",
                  "出行旅游", "医疗养生", "汽车交通", "素材")


def print_menu() -> None:
    """零配额打印「一次性问卷」，供 agent 原样贴给用户，用户一轮答完。

    v1.32：每题都带一个 ★ 推荐项。已固定人设时推荐项=人设参数，问题 1 也可
    直接回 0 沿用；没固定时退到「上次成功取数」的参数，再退到脚本默认。
    """
    prof = load_profile()
    last = load_last_run()
    base = prof or last
    rec_cat = (base.get("category") or "")
    rec_time = (base.get("time_range") or "12h")
    rec_mix = base.get("mix") or ["like", "collect"]
    rec_rows = base.get("rows") or DEFAULT_ROWS
    rec_filter = filter_of(base)
    rec_type = base.get("note_type") or "all"
    rec_no = {
        "cat": next((str(i) for i, n in enumerate(TOP_CATEGORIES, 1)
                     if n == rec_cat), str(len(TOP_CATEGORIES) + 1)),
        "time": next((no for no, n in TIME_RANGE_BY_NO.items()
                      if n == rec_time), "1"),
        "mix": mix_option(rec_mix),
        "rows": rows_option(rec_rows),
        "filter": rec_filter,
        "type": {"all": "1", "video": "2", "normal": "3"}.get(rec_type, "1"),
    }
    src = "已固定人设" if prof else ("上次取数" if last else "默认")

    print("【一次性问卷】所有问题一次列完，按顺序回编号即可，"
          "例如 1-19 2-1 3-1 4-2 5-1 6-1；每题带 ★ 的是推荐项，"
          "回「推荐」/「默认」即按星号选项执行。")
    if prof:
        print(f"人设已固定：{profile_label(prof)}（{prof.get('saved_at', '')}）"
              "——问题 1 回 0 即沿用，不必再描述定位。")
    elif last:
        print(f"上次取数：{profile_label(last)}（仅作推荐，未固定）")

    print(f"\n问题 1 · 选择类别〔可其他〕（{len(TOP_CATEGORIES)} 个一级分类，"
          f"编号=官方树序）")
    if prof:
        print("   0. 沿用已固定人设（不用再选类别）")
    for i, name in enumerate(TOP_CATEGORIES, 1):
        flag = f"  ← ★ 推荐（{src}）" if str(i) == rec_no["cat"] else ""
        print(f"  {i:>2}. {name}{flag}")
    other_flag = ""
    if not rec_cat:
        other_flag = f"  ← ★ 推荐（{src}：还没有类目数据，用「其他」描述方向）"
    print(f"  {len(TOP_CATEGORIES) + 1:>2}. 其他（我的方向不在上面，"
          f"如「穿搭」「搞钱」「探店」「好物开箱」）{other_flag}")

    print("\n问题 2 · 榜单时间维度〔无其他，服务端只支持这五档〕")
    for no, name in TIME_RANGE_BY_NO.items():
        tip = "  ← 上游当前异常偏少，不建议" if name == "24h" else ""
        flag = f"  ← ★ 推荐（{src}）" if no == rec_no["time"] else ""
        print(f"  {no}. {name}{flag}{tip}")

    print("\n问题 3 · 采样方式（点赞版 / 收藏版）〔无其他，只有这四种组合〕")
    for no, text in (("1", "点赞 + 收藏（2 页 / 40 条配额，内容面最宽）"),
                     ("2", "只要点赞榜（1 页 / 20 条配额，爆款最集中但偏娱乐）"),
                     ("3", "只要收藏榜（1 页 / 20 条配额，偏实用干货）"),
                     ("4", "点赞 + 收藏 + 评论（3 页 / 60 条配额，最全）")):
        flag = f"  ← ★ 推荐（{src}）" if no == rec_no["mix"] else ""
        print(f"  {no}. {text}{flag}")

    print("\n问题 4 · 取数规模〔可其他〕（配额按接口返回的条数计，"
          "服务端过滤后返回几条扣几条）")
    for no, text in (
            ("1", "20 条 / 1 次请求 / 扣 ≤20 条（最快试水）"),
            ("2", "40 条 / 2 次请求 / 扣 ≤40 条"),
            ("3", "1000 条 / 50 次请求 / 扣 ≤1000 条（当天额度用满，约 52 分钟）"),
            ("4", "其他（自定义条数，按 20 条/页向上取整，上限 1000）")):
        flag = f"  ← ★ 推荐（{src}）" if no == rec_no["rows"] else ""
        print(f"  {no}. {text}{flag}")

    print("\n问题 5 · 附加过滤〔可其他〕（本地筛选，不退还配额）")
    for no, text in (("1", "不加过滤"), ("2", "点赞 ≥ 1000"),
                     ("3", "粉丝 ≤ 1000（更低粉）"),
                     ("4", "点赞 ≥ 1000 且 粉丝 ≤ 1000"),
                     ("5", "其他（自定义阈值，如「点赞≥500」「粉丝≤5000」）")):
        flag = f"  ← ★ 推荐（{src}）" if no == rec_no["filter"] else ""
        print(f"  {no}. {text}{flag}")

    print("\n问题 6 · 内容类型〔无其他，服务端只认这三类〕")
    for no, text in (("1", "全部（图文 + 视频混排）"),
                     ("2", "只要视频（视频是榜内主体，12h 约 2/3）"),
                     ("3", "只要图文")):
        flag = f"  ← ★ 推荐（{src}）" if no == rec_no["type"] else ""
        print(f"  {no}. {text}{flag}")

    print("\n【其他项怎么补齐】问题 1 选其他 → 先跑 "
          "--position \"<你的词>\" --plan 出官方类目候选（零配额），"
          "用户确认后再取数；问题 4 选其他 → 问具体条数；"
          "问题 5 选其他 → 问具体阈值。补齐前不发起取数请求。")



def _esc(value) -> str:
    return html_lib.escape(str(value if value is not None else ""))


def _fmt_count(n) -> str:
    n = n or 0
    if n >= 10000:
        return f"{n / 10000:.1f}w"
    return str(n)


HTML_CSS = """
:root{--ink:#141414;--muted:#7b7770;--line:#e8e4dc;--accent:#ff2e4d;
--bg:#f6f4ef;--card:#fff;--shadow:0 1px 2px rgba(20,20,20,.06),
0 8px 24px -12px rgba(20,20,20,.18);}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC",
"Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:40px 24px 64px}
.top{display:flex;gap:24px;align-items:flex-end;justify-content:space-between;
border-bottom:1px solid var(--line);padding-bottom:24px;flex-wrap:wrap}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
h1{margin:10px 0 8px;font-size:34px;line-height:1.25;letter-spacing:-.01em}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--muted);font-size:13px}
.sub b{color:var(--ink);font-weight:600}
mark{background:#ffe9ec;color:#d81b35;font-weight:600;padding:1px 6px;border-radius:4px}
.position{background:var(--card);border:1px solid var(--line);border-radius:14px;
padding:14px 18px;margin:20px 0 0;display:flex;flex-wrap:wrap;gap:8px 28px;
align-items:baseline;box-shadow:var(--shadow)}
.position .pt{font-size:12px;color:var(--muted);letter-spacing:.04em}
.position .pr{font-size:13px;display:flex;gap:8px;align-items:baseline}
.position .pr span{color:var(--muted)}
.position .pr b{font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:28px 0 8px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;
box-shadow:var(--shadow)}
.kpi .k{font-size:12px;color:var(--muted);letter-spacing:.04em}
.kpi .v{font-size:26px;font-weight:700;margin-top:6px;letter-spacing:-.01em}
.kpi .v small{font-size:12px;font-weight:500;color:var(--muted);margin-left:4px}
.kpi .n{font-size:12px;color:var(--muted);margin-top:4px;
overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tagsbox{margin:26px 0 6px;background:var(--card);border:1px solid var(--line);
border-radius:14px;padding:18px 20px;box-shadow:var(--shadow)}
.tagsbox h2{margin:0 0 14px;font-size:14px;font-weight:600;color:var(--muted);
letter-spacing:.02em}
.bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
gap:10px 22px}
.bar{display:flex;align-items:center;gap:10px;font-size:13px;cursor:pointer;
border-radius:8px;padding:4px 6px;margin:-4px -6px;transition:background .15s ease}
.bar:hover{background:#fbf6ef}
.bar:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.bar.on{background:#ffe9ec}
.bar.on span.t{color:#c81e37;font-weight:600}
.bar span.t{width:88px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar .track{flex:1;height:6px;background:#f0ece4;border-radius:3px;overflow:hidden}
.bar .fill{height:100%;background:linear-gradient(90deg,#ff8fa0,var(--accent));
border-radius:3px}
.bar .c{width:28px;text-align:right;color:var(--muted)}
.tagsbox .hintline{margin-top:10px;font-size:12px;color:#a8a29a}
.tab.dim{opacity:.42}
.fstate{margin:10px 0 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap;
font-size:12px;color:var(--muted)}
.fstate b{color:var(--ink);font-weight:600}
.fstate .reset{border:1px solid var(--line);background:#faf8f3;color:#5f5a52;
font:12px inherit;font-family:inherit;padding:3px 10px;border-radius:6px;cursor:pointer}
.fstate .reset:hover{background:#141414;color:#fff;border-color:#141414}
.taglink{cursor:pointer}
.taglink:hover{background:#ffe9ec;color:#c81e37}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;
align-items:start}
.tabs{display:flex;gap:8px;margin:22px 0 0;flex-wrap:wrap;align-items:center}
.tabs .pt{font-size:12px;color:var(--muted);letter-spacing:.04em;margin-right:4px}
.tab{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:6px 14px;font:13px inherit;font-family:inherit;color:#5f5a52;cursor:pointer;
display:inline-flex;gap:6px;align-items:center;box-shadow:var(--shadow)}
.tab span{font-size:11px;color:#a8a29a}
.tab:hover{border-color:#c9c2b6}
.tab.on{background:#141414;color:#fff;border-color:#141414}
.tab.on span{color:#cfcac2}
.tab-note{font-size:11px;color:#a8a29a}
.chipwrap{flex:1 1 100%;display:flex;flex-wrap:wrap;gap:8px;overflow:hidden;
transition:max-height .25s ease;max-height:none}
.chipwrap.cut{mask-image:linear-gradient(180deg,#000 78%,transparent 100%)}
.tab.more{display:none;border-style:dashed;color:#8a8378}
.tdate{display:inline-flex;gap:6px;align-items:center;font-size:12px;color:#8a8378}
.tdate input{border:1px solid var(--line);border-radius:8px;padding:3px 6px;
font:12px inherit;font-family:inherit;color:#5f5a52;background:var(--card)}
#tag-more.show{display:inline-flex}
.tab-empty{display:none;margin-top:16px;font-size:13px;color:var(--muted);
background:var(--card);border:1px dashed #d9d3c8;border-radius:12px;padding:14px 18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;
overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;
transition:transform .18s ease,box-shadow .18s ease}
.card:hover{transform:translateY(-2px);box-shadow:0 12px 32px -14px rgba(20,20,20,.3)}
.cover{position:relative;aspect-ratio:3/4;background:
linear-gradient(135deg,#f3efe7,#e6e0d4)}
.cover img{width:100%;height:100%;object-fit:cover;display:block}
.rank{position:absolute;top:10px;left:10px;background:rgba(20,20,20,.82);
color:#fff;font-size:12px;font-weight:600;padding:3px 8px;border-radius:6px;
backdrop-filter:blur(4px)}
.nt{position:absolute;top:10px;right:10px;font-size:12px;font-weight:600;
padding:3px 8px;border-radius:6px;backdrop-filter:blur(4px)}
.nt-video{background:#c81e37;color:#fff}
a.nt{display:inline-block;text-decoration:none;cursor:pointer}
a.nt-video:hover{background:#a5182c}
.nt-normal{background:rgba(20,20,20,.75);color:#fff}
.cover .playmark{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
width:46px;height:46px;border-radius:50%;background:rgba(16,16,16,.52);color:#fff;
display:flex;align-items:center;justify-content:center;font-size:17px;
pointer-events:none;border:1px solid rgba(255,255,255,.35);
backdrop-filter:blur(2px)}
.body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.title{font-size:15px;font-weight:600;line-height:1.45;margin:0;
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.title a{color:inherit;text-decoration:none}
.title a:hover{color:var(--accent)}
.author{font-size:12px;color:var(--muted);display:flex;gap:8px;align-items:center;
flex-wrap:wrap}
.chip{background:#f4f1ea;border-radius:6px;padding:1px 6px;font-size:11px;color:#5f5a52}
.chip.hot{background:#ffe9ec;color:#c81e37}
.stats{display:flex;gap:12px;font-size:12px;color:#3c3a36;
border-top:1px dashed var(--line);padding-top:9px}
.stats span b{font-weight:700}
.tagrow{display:flex;gap:6px;flex-wrap:wrap}
.meta{display:flex;justify-content:space-between;align-items:center;gap:8px}
.meta .time{margin-right:auto}
.time{font-size:11px;color:#a8a29a}
.fetch{font-size:11px;color:#8d867c;border:1px solid var(--line);
border-radius:5px;padding:1px 6px;background:#fbfaf6;white-space:nowrap}
.open{font-size:11px;color:var(--accent);text-decoration:none;letter-spacing:.02em}
.open:hover{text-decoration:underline}
.copy{border:1px solid var(--line);background:#faf8f3;color:#5f5a52;
font-size:11px;font-family:inherit;padding:2px 9px;border-radius:6px;cursor:pointer;
transition:background .15s ease,color .15s ease,border-color .15s ease}
.copy:hover{background:#141414;color:#fff;border-color:#141414}
.copy.done{background:#e9f7ee;color:#1f7a44;border-color:#bfe6cd}
.empty{background:var(--card);border:1px dashed #d9d3c8;border-radius:16px;
padding:32px;text-align:center;color:var(--muted);margin-top:26px;line-height:1.9}
footer{margin-top:34px;border-top:1px solid var(--line);padding-top:18px;
color:var(--muted);font-size:12px;line-height:1.9}
footer .service{margin-top:8px;font-size:12px;color:#8a8378;letter-spacing:.2px}
footer .service b{color:#5f5a52;font-weight:600}
@media (max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}
.kpis{grid-template-columns:repeat(2,1fr)}h1{font-size:28px}}
@media (max-width:640px){.grid{grid-template-columns:1fr}.wrap{padding:26px 16px 48px}}
/* ---- 点击预览：小红书式浮层 ---- */
.card{cursor:pointer}
.card:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.cover .miss{position:absolute;inset:0;display:flex;align-items:center;
justify-content:center;font-size:12px;color:#9c9488;letter-spacing:.04em}
.sheet{position:fixed;inset:0;z-index:60;display:none}
.sheet.on{display:block}
.sheet-bg{position:absolute;inset:0;background:rgba(18,16,14,.62);
backdrop-filter:blur(2px)}
.sheet-panel{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
width:min(940px,94vw);max-height:88vh;background:#fff;border-radius:18px;
box-shadow:0 30px 80px -20px rgba(0,0,0,.5);display:flex;overflow:hidden}
.sheet-media{flex:0 0 44%;background:#f2eee6;position:relative;min-height:320px}
.sheet-media img{width:100%;height:100%;object-fit:contain;display:block}
.sheet-media video{width:100%;height:100%;object-fit:contain;background:#000;
display:none}
.sheet-body{flex:1;padding:22px 24px 26px;overflow-y:auto;position:relative}
.sheet-x{position:absolute;top:12px;right:14px;z-index:2;border:0;background:#f3efe8;
color:#6b6459;width:32px;height:32px;border-radius:50%;font-size:15px;cursor:pointer}
.sheet-x:hover{background:#e8e2d6;color:#141414}
#s-title{margin:0 26px 10px 0;font-size:19px;line-height:1.45;font-weight:700}
.sheet-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;
font-size:12px;color:var(--muted)}
.sheet-desc{margin:16px 0 14px;font-size:14px;line-height:1.85;color:#3c3a36;
white-space:pre-wrap;word-break:break-word}
.sheet-desc.clamp{display:-webkit-box;-webkit-line-clamp:8;-webkit-box-orient:vertical;
overflow:hidden}
.sheet-more{border:0;background:none;color:var(--accent);font-size:12px;
cursor:pointer;padding:0;margin-bottom:14px}
.sheet-tags{margin-bottom:16px}
.sheet-stats{display:flex;gap:18px;font-size:13px;color:#413e39;
border-top:1px solid var(--line);padding-top:14px;margin-bottom:16px}
.sheet-stats b{font-size:15px;font-weight:700}
.sheet-open{display:inline-block;background:var(--accent);color:#fff;
text-decoration:none;font-size:13px;font-weight:600;padding:9px 18px;border-radius:999px}
.sheet-open:hover{filter:brightness(1.06)}
.sheet-open.vid{background:#c81e37}
.sheet-open.vid:hover{background:#a5182c}
.sheet-actions{display:flex;gap:10px;align-items:center}
.copy.big{padding:9px 18px;font-size:13px;border-radius:999px}
@media (max-width:760px){.sheet-panel{flex-direction:column;width:94vw}
.sheet-media{flex:0 0 auto;height:38vh;min-height:0}
.sheet-body{padding:16px 18px 22px}}
"""


def _video_secs(it: dict) -> int:
    """视频时长（秒），从 raw_json.duration 读；图文/老数据返回 0。
    接口只给封面首帧，不给播放地址，时长是能拿到的唯一视频元信息。"""
    if it.get("note_type") != "video":
        return 0
    raw = it.get("raw_json")
    try:
        obj = json.loads(raw) if isinstance(raw, str) else (raw or {})
        return int(float(obj.get("duration") or 0))
    except (ValueError, TypeError):
        return 0


def _dur_text(secs: int) -> str:
    if not secs:
        return ""
    return f"{secs // 60}:{secs % 60:02d}" if secs >= 60 else f"0:{secs:02d}"


def _card(it: dict, idx: int = -1) -> str:
    nid = _esc(it.get("note_id"))
    url = f"https://www.xiaohongshu.com/explore/{nid}"
    cover = _esc(it.get("cover_url"))
    rank = it.get("rank_no")
    fans = it.get("fans_count") or 0
    fans_txt = f"粉丝 {_fmt_count(fans)}" if fans else "粉丝 —"
    tags = "".join(
        f'<span class="chip taglink" data-tag="{_esc(t)}"'
        f' title="按该标签筛选"'
        f' onclick="event.stopPropagation();pickTag(this.dataset.tag)">{_esc(t)}</span>'
        for t in (it.get("tags") or [])[:4])
    cat = it.get("category_name")
    cat_chip = (f'<span class="chip hot">{_esc(cat)}</span>'
                if cat else "")
    pub = _esc((it.get("publish_time") or "")[:16])
    fetch_at = it.get("_fetch_at") or ""
    fetch_short = ("本次 " + fetch_at[5:]) if it.get("_cur") and fetch_at else fetch_at[5:]
    nt = it.get("note_type")
    secs = _video_secs(it)
    vurl = it.get("video_url") or ""
    playmark = ('<span class="playmark" aria-hidden="true">&#9654;</span>'
                if (nt == "video" and vurl) else "")
    if nt == "video":
        label = "&#9654; 视频" + (f" {_dur_text(secs)}" if secs else "")
        if vurl:
            # badge doubles as a direct link to the mp4 (v1.24)
            type_badge = (f'<a class="nt nt-video" href="{_esc(vurl)}"'
                          f' target="_blank" rel="noreferrer"'
                          f' onclick="event.stopPropagation()"'
                          f' title="打开视频直链">{label}</a>')
        else:
            type_badge = f'<span class="nt nt-video">{label}</span>'
    elif nt == "normal":
        type_badge = '<span class="nt nt-normal">图文</span>'
    else:
        type_badge = ""   # legacy NULL rows: unknown, not labeled
    cover_html = (f'<img src="{cover}" loading="eager" decoding="async" alt=""'
                  ' onerror="this.style.display=\'none\';'
                  'this.parentNode.querySelector(\'.miss\').style.display=\'flex\'">'
                  '<span class="miss" style="display:none">封面加载失败</span>'
                  if cover else '<span class="miss" style="display:flex">无封面</span>')
    return f"""
<article class="card" data-idx="{idx}" data-type="{_esc(nt or '')}" role="button" tabindex="0"
  data-seq="{idx}" data-rank="{_esc(rank if rank is not None else '')}"
  data-like="{it.get('like_count') or 0}"
  data-collect="{it.get('collect_count') or 0}"
  data-comment="{it.get('comment_count') or 0}"
  data-share="{it.get('share_count') or 0}"
  data-fetch="{_esc(fetch_at[:10])}" data-cur="{1 if it.get('_cur') else 0}"
  onclick="openNote({idx})" onkeydown="if(event.key==='Enter')openNote({idx})">
  <div class="cover">
    {cover_html}
    {playmark}
    <span class="rank">#{_esc(rank)}</span>
    {type_badge}
  </div>
  <div class="body">
    <h3 class="title">{_esc(it.get("title"))}</h3>
    <div class="author">@{_esc(it.get("author") or "未知作者")}
      <span class="chip{' hot' if 0 < fans <= 1000 else ''}">{fans_txt}</span>
      {cat_chip}
    </div>
    <div class="stats">
      <span>赞 <b>{_fmt_count(it.get("like_count"))}</b></span>
      <span>藏 <b>{_fmt_count(it.get("collect_count"))}</b></span>
      <span>评 <b>{_fmt_count(it.get("comment_count"))}</b></span>
      <span>转 <b>{_fmt_count(it.get("share_count"))}</b></span>
    </div>
    <div class="tagrow">{tags or '<span class="chip">无标签</span>'}</div>
    <div class="meta"><span class="time">{pub}</span>
      <span class="fetch" title="该条笔记在本地缓存里的获取时间">获取 {_esc(fetch_short or '—')}</span>
      <button class="copy" type="button"
        onclick="event.stopPropagation();copyNote({idx},this)">复制</button>
      <a class="open" href="{url}" target="_blank" rel="noreferrer"
         onclick="event.stopPropagation()">打开笔记 ↗</a></div>
  </div>
</article>"""


def _note_hay(it: dict) -> str:
    """主题匹配用的检索文本：标题 + 正文 + 标签，小写拼接。"""
    return " ".join([it.get("title") or "", it.get("desc_text") or "",
                     " ".join(it.get("tags") or [])]).lower()


def render_html(items: list, meta: dict, label: str, out_path: Path,
                note: str = "") -> Path:
    """Write a self-contained HTML board for the rows that matched."""
    tr = _esc(meta.get("time_range"))
    updated = _esc(meta.get("data_updated_at") or "—")
    pulled = meta.get("pulled") or 0
    # 本期数据（KPI / 类型计数 / 标签计数都只看本期）；卡片墙额外含历史池
    cur_items = [i for i in items if i.get("_cur")] or items
    hist_n = sum(1 for i in items if not i.get("_cur"))
    matched = len(cur_items)
    src = "本地缓存" if meta.get("from_cache") else "实时取数"
    likes = [i.get("like_count") or 0 for i in cur_items]
    fans = [i.get("fans_count") or 0 for i in cur_items if i.get("fans_count")]
    avg_like = int(sum(likes) / len(likes)) if likes else 0
    med_fans = int(sorted(fans)[len(fans) // 2]) if fans else 0
    top = max(cur_items, key=lambda i: i.get("like_count") or 0) if cur_items else {}
    top_like = top.get("like_count") or 0

    tag_counts = Counter(t for i in cur_items
                         for t in (i.get("tags") or []) if t)
    tags_top = tag_counts.most_common(8)
    bars = "".join(
        f'<div class="bar" data-tag="{_esc(t)}" role="button" tabindex="0"'
        f' title="点击按「{_esc(t)}」筛选"'
        f' onclick="pickTag(this.dataset.tag)"'
        f' onkeydown="if(event.key===\'Enter\')pickTag(this.dataset.tag)">'
        f'<span class="t">{_esc(t)}</span>'
        f'<span class="track"><span class="fill" style="width:'
        f'{max(8, int(c * 100 / (tags_top[0][1] if tags_top else 1)))}%">'
        f'</span></span><span class="c">{c}</span></div>'
        for t, c in tags_top)

    cards = "".join(_card(i, n) for n, i in enumerate(items))
    n_video = sum(1 for i in cur_items if i.get("note_type") == "video")
    n_normal = sum(1 for i in cur_items if i.get("note_type") == "normal")
    n_unknown = matched - n_video - n_normal
    type_tabs = (
        '<section class="tabs" id="type-tabs">'
        + '<div class="pt">内容类型</div>'
        + f'<button class="tab on" type="button" data-t="all"'
          f' onclick="filterType(\'all\',this)">全部 <span>{matched}</span></button>'
        + f'<button class="tab" type="button" data-t="video"'
          f' onclick="filterType(\'video\',this)">&#9654; 视频 <span>{n_video}</span></button>'
        + f'<button class="tab" type="button" data-t="normal"'
          f' onclick="filterType(\'normal\',this)">图文 <span>{n_normal}</span></button>'
        + (f'<span class="tab-note">另有 {n_unknown} 条历史条目未标类型，仅在「全部」可见</span>'
           if n_unknown else '')
        + '</section>'
    )
    # 主题筛选（可多选，v1.33）：本地缓存累积所有主题组，本批只做增量补充；
    # 展示时按「本批命中数 → 历史累计命中数」从高到低排，未命中的也留着（暗显）
    groups = meta.get("tag_groups") or []
    cached = load_theme_cache(meta.get("category") or "")
    defs = {}
    for g in (cached.get("groups") or []):
        defs[g.get("name")] = {"terms": list(g.get("terms") or []),
                               "seen": g.get("seen") or 0}
    for gname, members in groups:
        d = defs.setdefault(gname, {"terms": [], "seen": 0})
        known = {str(x).lower() for x in d["terms"]}
        for m in members:
            if str(m).lower() not in known:
                d["terms"].append(str(m))
                known.add(str(m).lower())
    if defs:
        tag_items = []
        for gname, d in defs.items():
            if not d["terms"]:
                continue
            lows = [str(x).lower() for x in d["terms"]]
            n = sum(1 for it in cur_items
                    if any(w in _note_hay(it) for w in lows))
            tag_items.append({"id": f"g:{gname}", "label": gname,
                              "tags": d["terms"], "count": n,
                              "seen": d["seen"]})
        tag_items.sort(key=lambda x: (-x["count"], -x["seen"], x["label"]))

        def _covered(tag):
            low = str(tag).lower()
            return any(low == str(m).lower() or str(m).lower() in low
                       for d in defs.values() for m in d["terms"])

        # 没被任何主题覆盖的高频原始标签，单独成一枚胶囊，别让它们只在卡片里
        raw_hist = cached.get("raw") or {}
        extra = []
        for tag in set(raw_hist) | set(tag_counts):
            if _covered(tag):
                continue
            n_cur = tag_counts.get(tag, 0)
            n_hist = (raw_hist.get(tag) or {}).get("n", 0)
            if n_cur >= 2 or (n_cur and n_hist >= 2):
                extra.append({"id": f"t:{tag}", "label": tag, "tags": [tag],
                              "count": n_cur, "seen": n_hist})
        extra.sort(key=lambda x: (-x["count"], -x["seen"], x["label"]))
        tag_items += extra[:60]
        tag_note = (f'<span class="tab-note">累计 {len(defs)} 个主题 + '
                    f'{min(len(extra), 60)} 个高频单标签（本地缓存累积、本批增量），'
                    f'按本批命中从高到低排；暗色=本批 0 命中</span>')
    else:
        tag_items = [{"id": f"t:{t}", "label": t, "tags": [t], "count": c,
                      "seen": c}
                     for t, c in tag_counts.most_common(TAG_CHIP_LIMIT)]
        tag_note = (f'<span class="tab-note">按样本标签频次取 Top '
                    f'{TAG_CHIP_LIMIT}（共 {len(tag_counts)} 个），可多选</span>'
                    if len(tag_counts) > TAG_CHIP_LIMIT else
                    '<span class="tab-note">按样本标签频次生成，可多选</span>')
    n_no_tag = sum(1 for it in cur_items if not (it.get("tags") or []))
    if cur_items and n_no_tag:
        tag_items.append({"id": "__none__", "label": "无标签",
                          "tags": [], "count": n_no_tag})
    chip_parts = []
    for ti in tag_items:
        if not ti["count"] and ti["id"] == "__none__":
            continue
        iid = _esc(ti["id"])
        lbl = _esc(ti["label"])
        tip = _esc("、".join(ti["tags"][:8]))
        cnt = ti["count"]
        dim = ' dim' if not cnt else ''
        chip_parts.append(
            f'<button class="tab{dim}" type="button" data-id="{iid}"'
            f' title="{tip}" onclick="toggleTag(this)">{lbl}'
            f' <span>{cnt}</span></button>')
    chips = "".join(chip_parts)
    tag_filter = (
        '<section class="tabs" id="tag-filter">'
        + f'<div class="pt">主题筛选（标题·正文·标签提炼，可多选）</div>'
        + '<button class="tab" type="button" id="tag-mode"'
          ' onclick="toggleTagMode()" title="切换多选标签的匹配方式">'
          '匹配：任一</button>'
        + '<button class="tab" type="button" onclick="clearTags()">清空主题</button>'
        + f'<div class="chipwrap" id="tag-chips">{chips}</div>'
        + '<button class="tab more" type="button" id="tag-more"'
          ' onclick="toggleTagExpand()">展开全部</button>'
        + tag_note
        + '</section>'
        + '<div class="fstate" id="fstate">'
        + '<span id="fstate-txt">当前：全部内容 · 无主题筛选</span>'
        + '<button class="reset" type="button" onclick="clearFilter()">清除全部筛选</button>'
        + '</div>'
        + '<div class="tab-empty" id="tab-empty">'
        + '当前筛选组合下没有命中内容，点「清除全部筛选」回到全部。</div>'
    )
    # 筛选时间（v1.31）：今天 / 昨天 / 近1周 / 近1个月 / 近3个月 / 自定义时间，
    # 按每条笔记的「获取时间」筛选；本地缓存里的历史批次也能按这些窗口回看
    cur_at = meta.get("cached_at") or ""
    today = date.today()
    fetch_days = sorted({(i.get("_fetch_at") or "")[:10] for i in items
                         if (i.get("_fetch_at") or "")[:10]})
    d_from = fetch_days[0] if fetch_days else today.isoformat()
    time_opts = [("today", "今天"), ("yesterday", "昨天"),
                 ("7d", "近1周"), ("30d", "近1个月"), ("90d", "近3个月")]
    time_chip_parts = []
    if items:
        for key, lab in time_opts:
            time_chip_parts.append(
                f'<button class="tab{" on" if key == "today" else ""}"'
                f' type="button" data-t="{key}" onclick="filterTime(this)">'
                f'{lab} <span class="n">0</span></button>')
        time_chip_parts.append(
            '<button class="tab" type="button" data-t="custom"'
            ' onclick="filterTime(this)">自定义时间 <span class="n">0</span></button>'
            f'<span class="tdate"><input type="date" id="tf-from" value="{d_from}"'
            f' data-def="{d_from}" onchange="onCustomDate()"> ~ '
            '<input type="date" id="tf-to"'
            f' value="{today.isoformat()}" data-def="{today.isoformat()}"'
            ' onchange="onCustomDate()"></span>')
    time_filter = (
        '<section class="tabs" id="time-filter">'
        + '<div class="pt">筛选时间（按获取时间）</div>'
        + "".join(time_chip_parts)
        + '</section>'
    ) if items else ''
    # 排序条（v1.29）：点赞 / 收藏 / 评论 / 转发四个指标，含降序与升序切换，
    # 默认「默认顺序」=榜单原始顺序，保证不点排序时页面与以前完全一致
    sort_bar = (
        '<section class="tabs" id="sort-bar">'
        + '<div class="pt">排序</div>'
        + '<button class="tab on" type="button" data-k="none"'
          ' onclick="setSort(\'none\')" title="恢复榜单原始顺序">默认顺序</button>'
        + '<button class="tab" type="button" data-k="like"'
          ' onclick="setSort(\'like\')" title="按点赞数排序">点赞</button>'
        + '<button class="tab" type="button" data-k="collect"'
          ' onclick="setSort(\'collect\')" title="按收藏数排序">收藏</button>'
        + '<button class="tab" type="button" data-k="comment"'
          ' onclick="setSort(\'comment\')" title="按评论数排序">评论</button>'
        + '<button class="tab" type="button" data-k="share"'
          ' onclick="setSort(\'share\')" title="按转发数排序">转发</button>'
        + '<button class="tab" type="button" id="sort-dir"'
          ' onclick="toggleSortDir()" title="在降序 / 升序之间切换">—</button>'
        + '<span class="tab-note" id="sort-note">'
          '默认按榜单原始顺序；点指标按降序排，再点右侧按钮切升序</span>'
          '</section>'
    )
    tag_data_js = json.dumps(tag_items, ensure_ascii=False).replace("</", "<\\/")
    notes_payload = [{
        "title": i.get("title") or "",
        "author": i.get("author") or "未知作者",
        "fans": i.get("fans_count") or 0,
        "cat": i.get("category_name") or "",
        "type": i.get("note_type") or "",
        "dur": _dur_text(_video_secs(i)),
        "desc": i.get("desc_text") or "",
        "tags": i.get("tags") or [],
        "like": i.get("like_count") or 0,
        "collect": i.get("collect_count") or 0,
        "comment": i.get("comment_count") or 0,
        "share": i.get("share_count") or 0,
        "pub": (i.get("publish_time") or "")[:16],
        "fetch": i.get("_fetch_at") or "",
        "cur": bool(i.get("_cur")),
        "cover": i.get("cover_url") or "",
        "video_url": i.get("video_url") or "",
        "url": f"https://www.xiaohongshu.com/explore/{i.get('note_id')}",
    } for i in items]
    notes_js = json.dumps(notes_payload, ensure_ascii=False).replace("</", "<\\/")
    position_rows = []
    if meta.get("position"):
        position_rows.append(("账号定位", "、".join(meta["position"])))
    if meta.get("category"):
        position_rows.append(("官方类目", meta["category"]))
    if meta.get("body_keyword"):
        position_rows.append(("正文词 desc", meta["body_keyword"]))
    if meta.get("note_type"):
        position_rows.append(("内容类型",
                              TYPE_LABEL.get(meta["note_type"],
                                             meta["note_type"])))
    if tag_items:
        n_tag_opts = len([x for x in tag_items if x["id"] != "__none__"])
        position_rows.append(("标签筛选",
                              f"{n_tag_opts} 项（可多选）"
                              + (f" · 归组自 {len(tag_counts)} 个原始标签"
                                 if meta.get("tag_groups") else
                                 f" · 样本原始标签 {len(tag_counts)} 个")))
    if n_video:
        n_vurl = sum(1 for i in cur_items if i.get("video_url"))
        position_rows.append(("视频直链", f"{n_vurl}/{n_video} 条可站内播放"
                             + ("" if n_vurl == n_video else
                                "（其余直链未采到，只能跳原帖）")))
    if hist_n:
        position_rows.append(("历史数据池", f"{hist_n} 条（本地缓存，按获取时间筛选）"))
    position_rows.append(("库内命中总量", f"{meta.get('total')} 条"
                          "（服务端 类目 AND 正文词 过滤后）"))
    position_html = ('<section class="position"><div class="pt">定位解析</div>'
                     + "".join(f'<div class="pr"><span>{_esc(k)}</span>'
                               f'<b>{_esc(v)}</b></div>'
                               for k, v in position_rows)
                     + "</section>")
    if not items:
        body = f"""<div class="empty">
      服务端过滤后 0 命中（库内总量 <b>{meta.get('total')}</b> 条）。<br>
      官方类目覆盖率约 74%（12h 窗，2026-11-25 全量补采后），老维度与历史
      条目可能缺类目：换 12h/yesterday 维度、去掉 <code>--category</code> 改用
      <code>--body-keyword</code> 正文词检索，或用 <code>--plan</code> 重新确认类目。
      若加了 <code>--type</code>（只要视频／只要图文），先去掉该参数，确认不是
      类型收窄把结果滤空。
      {_esc(note)}</div>"""
    else:
        body = f'<div class="grid">{cards}</div>'

    sheet_html = """
<div class="sheet" id="sheet">
  <div class="sheet-bg" onclick="closeNote()"></div>
  <div class="sheet-panel" role="dialog" aria-modal="true">
    <button class="sheet-x" onclick="closeNote()" aria-label="关闭">✕</button>
    <div class="sheet-media">
      <video id="s-vplayer" controls playsinline preload="metadata"
             poster="" style="display:none"></video>
      <img id="s-cover" alt="">
      <span class="miss" id="s-miss" style="display:none">封面加载失败</span>
    </div>
    <div class="sheet-body">
      <h2 id="s-title"></h2>
      <div class="sheet-meta">
        <span id="s-author"></span>
        <span class="chip" id="s-fans"></span>
        <span class="chip hot" id="s-cat" style="display:none"></span>
        <span class="chip" id="s-type" style="display:none"></span>
      </div>
      <div class="sheet-desc clamp" id="s-desc"></div>
      <button class="sheet-more" id="s-more" style="display:none">展开全文 ↓</button>
      <div class="tagrow sheet-tags" id="s-tags"></div>
      <div class="sheet-stats" id="s-stats"></div>
      <div class="sheet-actions">
        <button class="copy big" id="s-copy" type="button">复制</button>
        <a class="sheet-open" id="s-open" target="_blank" rel="noreferrer">在小红书打开 ↗</a>
        <a class="sheet-open vid" id="s-video" target="_blank" rel="noreferrer" style="display:none">播放视频 ↗</a>
      </div>
    </div>
  </div>
</div>
"""

    script_body = """
<script>
const NOTES = JSON.parse(document.getElementById('notes-data').textContent);
const TAGS = JSON.parse(document.getElementById('tag-data').textContent);
const fmt = n => n >= 10000 ? (n/10000).toFixed(1)+'w'
  : (n >= 1000 ? (n/1000).toFixed(1)+'k' : String(n));
function noteText(n){
  const L = [];
  L.push('标题：' + (n.title || ''));
  L.push('作者：@' + (n.author || '未知') + (n.fans ? '（粉丝 ' + n.fans + '）' : '（粉丝 —）'));
  if(n.cat) L.push('分类：' + n.cat);
  if(n.type) L.push('类型：' + (n.type === 'video' ? '视频' + (n.dur ? '（时长 ' + n.dur + '）' : '') : '图文'));
  if(n.video_url) L.push('视频直链：' + n.video_url);
  if(n.pub) L.push('发布：' + n.pub);
  if(n.fetch) L.push('获取时间：' + n.fetch);
  L.push('互动：赞 ' + n.like + ' / 藏 ' + n.collect + ' / 评 ' + n.comment + ' / 转 ' + n.share);
  if((n.tags || []).length) L.push('标签：' + n.tags.join('、'));
  L.push('正文：');
  L.push(n.desc || '（无正文）');
  L.push('链接：' + n.url);
  return L.join(String.fromCharCode(10));
}
function copyFallback(text, resolve, reject){
  try{
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.top = '-9999px'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(ta);
    ok ? resolve() : reject(new Error('execCommand failed'));
  }catch(e){ reject(e); }
}
function copyText(text){
  return new Promise((resolve, reject) => {
    if(navigator.clipboard && window.isSecureContext){
      navigator.clipboard.writeText(text).then(resolve)
        .catch(() => copyFallback(text, resolve, reject));
    } else { copyFallback(text, resolve, reject); }
  });
}
function flash(btn, ok){
  if(!btn) return;
  if(!btn.dataset.label) btn.dataset.label = btn.textContent.trim();
  btn.textContent = ok ? '已复制 ✓' : '复制失败';
  btn.classList.toggle('done', ok);
  clearTimeout(btn._t);
  btn._t = setTimeout(() => {
    btn.textContent = btn.dataset.label;
    btn.classList.remove('done');
  }, 1500);
}
function copyNote(i, btn){
  const n = NOTES[i];
  if(!n) return;
  copyText(noteText(n)).then(() => flash(btn, true)).catch(() => flash(btn, false));
}
const FS = {type: 'all', tags: [], mode: 'any', time: 'today'};
const SO = {key: 'none', dir: 'desc'};
const SORT_LABEL = {like: '点赞', collect: '收藏', comment: '评论', share: '转发'};
function allCards(){
  return Array.prototype.slice.call(document.querySelectorAll('.card'));
}
function cardTags(c){
  const n = NOTES[Number(c.dataset.idx)];
  return (n && n.tags) ? n.tags : [];
}
function noteHay(i){
  const n = NOTES[i]; if(!n) return '';
  return ((n.title || '') + ' ' + (n.desc || '') + ' '
          + (n.tags || []).join(' ')).toLowerCase();
}
function findItem(id){
  for(let i = 0; i < TAGS.length; i++){ if(TAGS[i].id === id) return TAGS[i]; }
  return null;
}
/* 主题命中：组内任一词在「标签 / 标题 / 正文」里出现即算（v1.30 起不再只看 tags） */
function hitItem(i, id){
  const it = findItem(id); if(!it) return false;
  if(!it.tags.length) return !((NOTES[i] && NOTES[i].tags) || []).length;
  const hay = noteHay(i);
  for(let k = 0; k < it.tags.length; k++){
    if(hay.indexOf(String(it.tags[k]).toLowerCase()) !== -1) return true;
  }
  return false;
}
function tagOk(c){
  if(!FS.tags.length) return true;
  const idx = Number(c.dataset.idx);
  const hits = FS.tags.map(id => hitItem(idx, id));
  return FS.mode === 'all' ? hits.every(Boolean) : hits.some(Boolean);
}
const TIME_LABEL = {today: '今天', yesterday: '昨天', '7d': '近1周',
  '30d': '近1个月', '90d': '近3个月', custom: '自定义时间',
  all: '全部时间', cur: '本次'};
function fmtDate(d){
  const p = n => (n < 10 ? '0' : '') + n;
  return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}
function dayShift(n){
  const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + n);
  return fmtDate(d);
}
function rangeOk(c, key){
  const f = c.dataset.fetch || '';
  if(key === 'all') return true;
  if(key === 'cur') return c.dataset.cur === '1';
  if(!f) return false;
  if(key === 'today') return f === dayShift(0);
  if(key === 'yesterday') return f === dayShift(-1);
  if(key === '7d') return f >= dayShift(-6) && f <= dayShift(0);
  if(key === '30d') return f >= dayShift(-29) && f <= dayShift(0);
  if(key === '90d') return f >= dayShift(-89) && f <= dayShift(0);
  if(key === 'custom'){
    const a = (document.getElementById('tf-from') || {}).value || '';
    const b = (document.getElementById('tf-to') || {}).value || '';
    if(a && f < a) return false;
    if(b && f > b) return false;
    return true;
  }
  return false;
}
function timeOk(c){ return rangeOk(c, FS.time); }
function mayShow(c){
  const t = FS.type;
  const typeOk = (t === 'all') || ((c.dataset.type || '') === t);
  return typeOk && tagOk(c) && timeOk(c);
}
function ensureTagItem(tag){
  for(let i = 0; i < TAGS.length; i++){
    if(TAGS[i].tags.length === 1 && TAGS[i].tags[0] === tag) return TAGS[i].id;
  }
  const id = 't:' + tag;
  TAGS.push({id: id, label: tag, tags: [tag], count: 0});
  const wrap = document.getElementById('tag-chips');
  if(wrap){
    const b = document.createElement('button');
    b.className = 'tab'; b.type = 'button'; b.dataset.id = id; b.title = tag;
    b.innerHTML = '<span class="lbl"></span> <span class="n">0</span>';
    b.querySelector('.lbl').textContent = tag;
    b.onclick = function(){ toggleTag(this); };
    wrap.appendChild(b);
    layoutTagChips();
  }
  return id;
}
function pickTag(tag){
  const id = ensureTagItem(tag);
  const at = FS.tags.indexOf(id);
  if(at >= 0) FS.tags.splice(at, 1); else FS.tags.push(id);
  applyFilter(true);
}
function toggleTag(btn){
  const id = btn.dataset.id;
  const at = FS.tags.indexOf(id);
  if(at >= 0) FS.tags.splice(at, 1); else FS.tags.push(id);
  applyFilter(true);
}
function clearTags(){
  FS.tags = [];
  applyFilter(false);
}
function toggleTagMode(){
  FS.mode = (FS.mode === 'all') ? 'any' : 'all';
  const b = document.getElementById('tag-mode');
  if(b){
    b.textContent = FS.mode === 'all' ? '匹配：全部' : '匹配：任一';
    b.classList.toggle('on', FS.mode === 'all');
  }
  applyFilter(false);
}
function labelOf(id){
  const it = findItem(id);
  return it ? it.label : id;
}
function applyFilter(scroll){
  let shown = 0;
  const cards = allCards();
  cards.forEach(c => {
    const ok = mayShow(c);
    c.style.display = ok ? '' : 'none';
    if(ok) shown++;
  });
  refreshFacets();
  const txt = document.getElementById('fstate-txt');
  if(txt){
    const bits = [];
    if(FS.time !== 'today'){
      let tl = TIME_LABEL[FS.time] || FS.time;
      if(FS.time === 'custom'){
        const a = (document.getElementById('tf-from') || {}).value || '';
        const b = (document.getElementById('tf-to') || {}).value || '';
        tl = '自定义 ' + (a || '…') + ' ~ ' + (b || '…');
      }
      bits.push('获取时间 ' + tl);
    }
    if(FS.type !== 'all') bits.push(FS.type === 'video' ? '视频' : '图文');
    if(FS.tags.length){
      bits.push('标签「' + FS.tags.map(labelOf).join('、') + '」'
                + (FS.tags.length > 1
                   ? (FS.mode === 'all' ? '＋' : '｜') + '匹配'
                   : ''));
    }
    if(SO.key !== 'none'){
      bits.push('按' + (SORT_LABEL[SO.key] || SO.key)
                + (SO.dir === 'desc' ? '降序' : '升序'));
    }
    txt.textContent = (bits.length ? '当前：' + bits.join(' · ')
                                    : '当前：全部内容 · 本次数据 · 无主题筛选')
                   + ' · 命中 ' + shown + ' / ' + cards.length + ' 条';
  }
  const tip = document.getElementById('tab-empty');
  if(tip){
    tip.style.display = (shown === 0 && (FS.type !== 'all' || FS.tags.length))
                        ? 'block' : 'none';
  }
  if(scroll){
    const anchor = document.getElementById('type-tabs');
    if(anchor){
      const y = anchor.getBoundingClientRect().top + window.pageYOffset - 16;
      window.scrollTo({top: y, behavior: 'smooth'});
    }
  }
}
function refreshFacets(){
  const cards = allCards();
  // 类型胶囊：在当前时间 / 主题选择下重算可用条数
  document.querySelectorAll('#type-tabs .tab').forEach(b => {
    const k = b.dataset.t || 'all';
    let n = 0;
    cards.forEach(c => {
      if((k === 'all' || (c.dataset.type || '') === k)
         && timeOk(c) && tagOk(c)) n++;
    });
    const s = b.querySelector('span'); if(s) s.textContent = n;
    b.classList.toggle('on', k === FS.type);
    b.classList.toggle('dim', n === 0 && k !== FS.type);
  });
  // 标签胶囊：在当前类型 / 时间下重算可用条数（多选互不影响各自计数）
  document.querySelectorAll('#tag-chips .tab').forEach(b => {
    const id = b.dataset.id;
    let n = 0;
    cards.forEach(c => {
      if((FS.type === 'all' || (c.dataset.type || '') === FS.type)
         && timeOk(c) && hitItem(Number(c.dataset.idx), id)) n++;
    });
    const s = b.querySelector('span.n') || b.querySelector('span');
    if(s) s.textContent = n;
    b.classList.toggle('on', FS.tags.indexOf(id) !== -1);
    b.classList.toggle('dim', n === 0 && FS.tags.indexOf(id) === -1);
  });
  // 时间胶囊：高亮当前选中的时间窗口，并按当前窗口重算各段可用条数
  recountTimeChips();
  document.querySelectorAll('#time-filter .tab').forEach(b => {
    b.classList.toggle('on', b.dataset.t === FS.time);
  });
  // 标签热度条：命中任一已选标签即高亮
  document.querySelectorAll('.bar').forEach(b => {
    let hit = false;
    FS.tags.forEach(id => {
      const it = findItem(id);
      if(it && it.tags.indexOf(b.dataset.tag) !== -1) hit = true;
    });
    b.classList.toggle('on', hit);
  });
  layoutTagChips();
}
function recountTimeChips(){
  const cards = allCards();
  document.querySelectorAll('#time-filter .tab').forEach(b => {
    const k = b.dataset.t;
    if(!k) return;
    let n = 0;
    cards.forEach(c => { if(rangeOk(c, k)) n++; });
    const s = b.querySelector('span.n');
    if(s) s.textContent = n;
    b.classList.toggle('dim', n === 0 && k !== FS.time);
  });
}
function filterType(t, btn){
  FS.type = t;
  applyFilter(true);
}
function filterTime(btn){
  const t = btn.dataset.t || 'today';
  if(t === 'custom'){
    const a = document.getElementById('tf-from');
    const b = document.getElementById('tf-to');
    if(a && b && a.value && b.value && a.value > b.value){
      const tmp = a.value; a.value = b.value; b.value = tmp;   // 起止颠倒自动纠正
    }
    if((!a || !a.value) && b && b.value){ if(a) a.value = b.value; }
  }
  FS.time = t;
  applyFilter(true);
}
function onCustomDate(){
  FS.time = 'custom';
  applyFilter(false);
}
/* ---------- 主题胶囊：超过 3 行折叠，可展开/收起（v1.31） ---------- */
const TE = {open: false};
function tagRowStats(){
  const wrap = document.getElementById('tag-chips');
  if(!wrap) return null;
  const tabs = Array.from(wrap.querySelectorAll('.tab'))
                    .filter(b => b.style.display !== 'none');
  if(!tabs.length) return null;
  const tops = [];
  tabs.forEach(b => { if(tops.indexOf(b.offsetTop) < 0) tops.push(b.offsetTop); });
  tops.sort((x, y) => x - y);
  let rh = tabs[0].offsetHeight + 8;
  if(tops.length > 1) rh = tops[1] - tops[0];
  return {rows: tops.length, rh: rh, wrap: wrap};
}
function layoutTagChips(){
  const more = document.getElementById('tag-more');
  const st = tagRowStats();
  if(!st || !more) return;
  st.wrap.style.maxHeight = 'none';       // 先放开，量真实行数
  const s2 = tagRowStats() || st;
  if(s2.rows > 3){
    more.classList.add('show');
    if(TE.open){
      s2.wrap.style.maxHeight = (s2.rows * s2.rh) + 'px';
      s2.wrap.classList.remove('cut');
      more.textContent = '收起主题';
    } else {
      s2.wrap.style.maxHeight = (3 * s2.rh - 8) + 'px';
      s2.wrap.classList.add('cut');
      more.textContent = '展开全部（共 ' + s2.rows + ' 行）';
    }
  } else {
    s2.wrap.style.maxHeight = 'none';
    s2.wrap.classList.remove('cut');
    more.classList.remove('show');
    more.textContent = '展开全部';
  }
}
function toggleTagExpand(){ TE.open = !TE.open; layoutTagChips(); }
window.addEventListener('resize', layoutTagChips);
window.addEventListener('load', layoutTagChips);
function clearFilter(){
  FS.type = 'all'; FS.tags = []; FS.mode = 'any'; FS.time = 'today';
  TE.open = false;
  const b = document.getElementById('tag-mode');
  if(b){ b.textContent = '匹配：任一'; b.classList.remove('on'); }
  ['tf-from', 'tf-to'].forEach(id => {
    const el = document.getElementById(id);
    if(el && el.dataset.def) el.value = el.dataset.def;
  });
  applyFilter(true);
}
/* ---------- 排序（v1.29）：点赞 / 收藏 / 评论 / 转发，升降序可切 ---------- */
function applySort(){
  const grid = document.querySelector('.grid');
  if(!grid) return;
  const cards = allCards();
  const dir = SO.dir === 'asc' ? 1 : -1;
  cards.sort((a, b) => {
    if(SO.key === 'none') return Number(a.dataset.seq) - Number(b.dataset.seq);
    const va = Number(a.dataset[SO.key] || 0);
    const vb = Number(b.dataset[SO.key] || 0);
    if(va !== vb) return (va - vb) * dir;
    const ra = Number(a.dataset.rank || 1e9) || 1e9;   // 同值回落到榜内名次
    const rb = Number(b.dataset.rank || 1e9) || 1e9;
    return ra - rb;
  });
  cards.forEach(c => grid.appendChild(c));   // 只重排 DOM，不重建卡片、不动筛选状态
  updateSortUI();
}
function setSort(k){
  SO.key = k;
  SO.dir = 'desc';        // 点指标即「多→少」，再点右侧按钮切升序
  applySort();
}
function toggleSortDir(){
  if(SO.key === 'none') return;   // 原始顺序没有方向可切
  SO.dir = SO.dir === 'desc' ? 'asc' : 'desc';
  applySort();
}
function updateSortUI(){
  document.querySelectorAll('#sort-bar .tab[data-k]').forEach(b => {
    b.classList.toggle('on', b.dataset.k === SO.key);
  });
  const d = document.getElementById('sort-dir');
  if(d){
    d.textContent = SO.key === 'none' ? '—'
      : (SO.dir === 'desc' ? '降序 ↓' : '升序 ↑');
    d.classList.toggle('dim', SO.key === 'none');
  }
  const note = document.getElementById('sort-note');
  if(note){
    note.textContent = SO.key === 'none' ? '当前：榜单原始顺序'
      : '当前：按' + (SORT_LABEL[SO.key] || SO.key) + (SO.dir === 'desc'
          ? '数降序（多 → 少）' : '数升序（少 → 多）');
  }
}
function openNote(i){
  const n = NOTES[i]; if(!n) return;
  const cover = document.getElementById('s-cover');
  const miss = document.getElementById('s-miss');
  const vp = document.getElementById('s-vplayer');
  resetVideo();
  const poster = n.cover ? n.cover.replace('/w/360', '/w/720') : '';
  if(n.type === 'video' && n.video_url){
    cover.style.display='none'; miss.style.display='none';
    vp.poster = poster; vp.src = n.video_url; vp.style.display='block';
    vp.onerror = () => {          // 直链失效/防盗链：退回封面，仍可点「播放视频 ↗」
      vp.style.display='none';
      try{ vp.pause(); }catch(e){}
      vp.removeAttribute('src'); vp.onerror = null;
      if(poster){ cover.style.display='block'; cover.src = poster;
                  cover.onerror = () => { cover.style.display='none';
                                          miss.style.display='flex'; }; }
      else { miss.style.display='flex'; }
    };
  } else if(n.cover){
    miss.style.display='none'; cover.style.display='block';
    cover.src = poster || n.cover;
    cover.onerror = () => { cover.style.display='none'; miss.style.display='flex'; };
  } else { cover.style.display='none'; miss.style.display='flex'; }
  document.getElementById('s-title').textContent = n.title || '（无标题）';
  document.getElementById('s-author').textContent = '@' + (n.author || '未知作者');
  const fans = document.getElementById('s-fans');
  fans.textContent = n.fans ? '粉丝 ' + fmt(n.fans) : '粉丝 —';
  fans.className = 'chip' + (n.fans > 0 && n.fans <= 1000 ? ' hot' : '');
  const cat = document.getElementById('s-cat');
  if(n.cat){ cat.style.display='inline-block'; cat.textContent = n.cat; }
  else { cat.style.display = 'none'; }
  const tp = document.getElementById('s-type');
  if(n.type === 'video'){ tp.style.display='inline-block'; tp.textContent = '▶ 视频笔记' + (n.dur ? ' · ' + n.dur : ''); }
  else if(n.type === 'normal'){ tp.style.display='inline-block'; tp.textContent = '图文笔记'; }
  else { tp.style.display = 'none'; }
  const vlink = document.getElementById('s-video');
  if(n.video_url){ vlink.style.display='inline-block'; vlink.href = n.video_url; }
  else { vlink.style.display = 'none'; vlink.removeAttribute('href'); }
  const desc = document.getElementById('s-desc');
  desc.textContent = n.desc || '（正文未采集）';
  desc.classList.add('clamp');
  const more = document.getElementById('s-more');
  more.style.display = (n.desc || '').length > 260 ? 'inline-block' : 'none';
  more.textContent = '展开全文 ↓';
  more.onclick = () => {
    if(desc.classList.contains('clamp')){
      desc.classList.remove('clamp'); more.textContent = '收起 ↑';
    } else { desc.classList.add('clamp'); more.textContent = '展开全文 ↓'; }
  };
  const tagEsc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/"/g,'&quot;');
  document.getElementById('s-tags').innerHTML = (n.tags || [])
    .map(t => '<span class="chip taglink" data-tag="' + tagEsc(t) + '"'
            + ' title="按该标签筛选"'
            + ' onclick="pickTag(this.dataset.tag);closeNote()">' + tagEsc(t) + '</span>')
    .join('') || '<span class="chip">无标签</span>';
  document.getElementById('s-stats').innerHTML =
    '<span>赞 <b>' + fmt(n.like) + '</b></span>' +
    '<span>藏 <b>' + fmt(n.collect) + '</b></span>' +
    '<span>评 <b>' + fmt(n.comment) + '</b></span>' +
    '<span>转 <b>' + fmt(n.share) + '</b></span>' +
    '<span style="color:#a8a29a">' + (n.pub || '') + '</span>' +
    (n.fetch ? '<span style="color:#a8a29a">获取 ' + n.fetch + '</span>' : '');
  document.getElementById('s-open').href = n.url;
  const copyBtn = document.getElementById('s-copy');
  copyBtn.dataset.label = '复制';
  copyBtn.textContent = '复制';
  copyBtn.classList.remove('done');
  copyBtn.onclick = function(){ copyNote(i, this); };
  document.getElementById('sheet').classList.add('on');
  document.body.style.overflow = 'hidden';
  document.querySelector('.sheet-body').scrollTop = 0;
}
function resetVideo(){
  const vp = document.getElementById('s-vplayer');
  if(!vp) return;
  vp.onerror = null;
  try{ vp.pause(); }catch(e){}
  vp.removeAttribute('src');
  try{ vp.load(); }catch(e){}
  vp.style.display='none';
}
function closeNote(){
  resetVideo();
  document.getElementById('sheet').classList.remove('on');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => { if(e.key === 'Escape') closeNote(); });
if(document.querySelector('.grid')){
  applySort();                                         // 初始化排序条状态（默认不重排）
  // 看板若隔天才打开，「今天」可能空：自动退到覆盖全部批次的「自定义时间」
  const cards0 = allCards();
  let hasToday = false;
  cards0.forEach(c => { if(rangeOk(c, 'today')) hasToday = true; });
  if(!hasToday && cards0.length){
    const ds = cards0.map(c => c.dataset.fetch).filter(Boolean).sort();
    FS.time = 'custom';
    const a = document.getElementById('tf-from'), b = document.getElementById('tf-to');
    if(a && ds.length) a.value = ds[0];
    if(b && ds.length) b.value = ds[ds.length - 1];
    applyFilter(false);
  }
}
layoutTagChips();                                      // 主题胶囊超过 3 行先折叠
recountTimeChips();
</script>
"""
    script_html = script_body
    data_html = ('<script type="application/json" id="notes-data">'
                 + notes_js + '</script>'
                 + '<script type="application/json" id="tag-data">'
                 + tag_data_js + '</script>')

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>低粉爆款 · {_esc(label)} · {tr}</title>
<style>{HTML_CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <div class="eyebrow">小红书 · 低粉爆款榜 · {tr} 维度</div>
      <h1><em>{_esc(label)}</em> 低粉爆款</h1>
      <div class="sub">数据更新 <b>{updated}</b> · 样本 <b>{pulled} 条</b> ·
        命中 <b>{matched} 条</b> · 来源 <b>{src}</b></div>
    </div>
    <div class="sub">粉丝 ≤1 万的低粉账号爆文<br>图文 + 视频 · 每日 1000 条配额样本</div>
  </header>

  {position_html}

  <section class="kpis">
    <div class="kpi"><div class="k">命中条数</div>
      <div class="v">{matched}<small>/ {pulled} 条</small></div>
      <div class="n">命中率 {int(matched * 100 / pulled) if pulled else 0}% · 视频 {n_video} / 图文 {n_normal}{f' / 未标注 {n_unknown}' if n_unknown else ''}</div></div>
    <div class="kpi"><div class="k">平均点赞</div>
      <div class="v">{_fmt_count(avg_like)}</div>
      <div class="n">命中内容的互动基线</div></div>
    <div class="kpi"><div class="k">粉丝中位数</div>
      <div class="v">{_fmt_count(med_fans)}</div>
      <div class="n">低粉起量的可复制性参考</div></div>
    <div class="kpi"><div class="k">最高点赞</div>
      <div class="v">{_fmt_count(top_like)}</div>
      <div class="n">{_esc((top.get('title') or '—')[:22])}</div></div>
  </section>

  {f'<section class="tagsbox"><h2>样本标签热度 Top {len(tags_top)}</h2><div class="bars">{bars}</div><div class="hintline">点任意标签格即把它加入标签筛选（再点一次移出）；标签可多选，和内容类型叠加生效</div></section>' if tags_top else ''}

  {type_tabs if items else ''}

  {time_filter}

  {tag_filter if items else ''}

  {sort_bar if items else ''}

  {body}

  <footer>
数据来源：流川数据服务（liuchuan-data）公网只读 API，本地采集端定时推送。<br>
口径说明：互动量（赞/藏/评/转）为抓取时刻快照，非实时。
<div class="service">定制服务：<b>guipi999</b></div>
</footer>
</div>
{sheet_html}
{data_html}
{script_html}
</body>
</html>
"""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    return out_path


def _safe_name(text: str) -> str:
    return re.sub(r'[\\/:*?"<>|\s]+', "_", text).strip("_") or "低粉爆款"


SERVE_PORT_BASE = 8777   # 本地预览服务起始端口（只绑 127.0.0.1，不对外）


def _serve_state_file() -> Path:
    return CACHE_DIR / "serve.json"


def _port_alive(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.4):
            return True
    except OSError:
        return False


def _free_port(start: int = SERVE_PORT_BASE, span: int = 24) -> int:
    for p in range(start, start + span):
        if not _port_alive(p):
            return p
    return 0


def _serve_ok(port: int) -> bool:
    """端口上跑的是不是能正常响应 HTTP 的服务（比 TCP 连通更可靠）。"""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1.0) as r:
            return 200 <= r.status < 400
    except (OSError, urllib.error.URLError, ValueError):
        return False


def _start_server(dir_s: str, port: int) -> None:
    """在 127.0.0.1:port 起 detached 的 http.server，等端口活起来再返回。"""
    flags = 0
    if os.name == "nt":
        flags = 0x00000008 | 0x00000200   # DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP
    subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port),
         "--bind", "127.0.0.1", "--directory", dir_s],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, creationflags=flags, close_fds=True)
    for _ in range(25):
        time.sleep(0.15)
        if _port_alive(port):
            break


def ensure_server(directory: Path) -> int:
    """确保 `directory` 由本机 127.0.0.1 的 http.server 提供，返回端口。

    服务用独立进程跑（Windows 下 detached），脚本退出后仍可用；端口只绑
    本机，不暴露到局域网。**同目录优先沿用上次端口**（哪怕进程已退出），
    这样用户手里的预览地址不会每次取数都变。
    """
    dir_s = str(Path(directory).resolve())
    try:
        st = json.loads(_serve_state_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        st = {}
    port = int(st.get("port") or 0)
    if st.get("dir") == dir_s and port:
        if _serve_ok(port):
            return port                       # 上次的服务还活着，直接复用
        if not _port_alive(port):
            _start_server(dir_s, port)        # 端口空着：沿用原端口重启
            return port

    port = _free_port()
    if not port:
        raise OSError("no free port for local preview server")
    _start_server(dir_s, port)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _serve_state_file().write_text(
            json.dumps({"dir": dir_s, "port": port}, ensure_ascii=False),
            encoding="utf-8")
    except OSError:
        pass
    return port


def preview_url(html_path: Path, force_port: int = 0) -> str:
    """给 HTML 生成可直接点开的 http 地址；失败则回 file:// 兜底。
    文件名保留中文（浏览器会自动转义），方便用户复制粘贴。"""
    try:
        port = force_port or ensure_server(html_path.parent)
        name = html_path.name.replace(" ", "%20").replace("#", "%23")
        return f"http://127.0.0.1:{port}/{name}"
    except Exception:
        return "file:///" + urllib.parse.quote(str(html_path.resolve()))


def _pid_on_port(port: int) -> int:
    """Windows: netstat -ano；类 Unix: lsof。取占端口的 pid，找不到返回 0。"""
    try:
        if os.name == "nt":
            out = subprocess.run(["netstat", "-ano"], capture_output=True,
                                 text=True, timeout=8).stdout
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 5 and parts[1].endswith(f":{port}"):
                    return int(parts[-1])
        else:
            out = subprocess.run(["lsof", "-ti", f"tcp:{port}"],
                                 capture_output=True, text=True,
                                 timeout=8).stdout.strip()
            return int(out.splitlines()[0]) if out else 0
    except (OSError, ValueError, subprocess.SubprocessError):
        return 0
    return 0


def stop_server() -> str:
    """停掉本技能起的预览服务（只杀占着记录端口的那个进程）。"""
    try:
        st = json.loads(_serve_state_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "没有记录到预览服务"
    port = int(st.get("port") or 0)
    if not port:
        return "没有记录到预览服务"
    pid = _pid_on_port(port)
    if not pid:
        return f"端口 {port} 上没有服务在跑"
    try:
        os.kill(pid, 15)          # SIGTERM / TerminateProcess
    except OSError as e:
        return f"停止失败：{e}"
    try:
        _serve_state_file().unlink()
    except OSError:
        pass
    return f"已停止 127.0.0.1:{port} 的预览服务（pid {pid}）"


def print_conclusion(items: list, meta: dict, from_cache: bool,
                     url: str = "") -> None:
    """对话结论块：只给三条——条数 / 类型 / 剩余额度。
    agent 直接把它贴给用户，不再复述过程、改动或建议。"""
    pulled = meta.get("pulled") or 0
    cur_items = [i for i in items if i.get("_cur")] or []
    if not cur_items and items:
        cur_items = items            # 历史池场景兜底（--json 等）
    matched = meta.get("matched") if "matched" in meta else len(cur_items)
    n_video = sum(1 for i in cur_items if i.get("note_type") == "video")
    n_normal = sum(1 for i in cur_items if i.get("note_type") == "normal")
    n_unknown = matched - n_video - n_normal

    if matched == 0:
        count = f"0 条（样本 {pulled} 条，服务端过滤后无命中）"
    else:
        rate = int(matched * 100 / pulled) if pulled else 0
        count = f"{matched} 条（样本 {pulled} 条，命中率 {rate}%）"

    if matched == 0:
        types = "—"
    elif n_video and n_normal:
        types = f"图文 + 视频（视频 {n_video} · 图文 {n_normal}）"
    elif n_video:
        types = f"视频 {n_video} 条"
    elif n_normal:
        types = f"图文 {n_normal} 条"
    else:
        types = f"类型未标注 {n_unknown} 条（历史条目）"
    if n_unknown and matched:
        types += f"（另有 {n_unknown} 条未标注）"

    rem = meta.get("quota_remaining")
    if rem is None:
        quota = "未知（本次未拿到服务端额度头）"
    elif from_cache:
        at = meta.get("quota_at") or ""
        quota = f"{rem} 条" + (f"（上次已知 {at}，本次未消耗）" if at
                              else "（缓存时点，本次未消耗）")
    else:
        quota = f"{rem} 条"

    print("\n【结论】")
    print(f"抓取条数：{count}")
    print(f"内容类型：{types}")
    print(f"剩余额度：{quota}")
    if url:
        print(f"预览地址：{url}")


def resolve_api_key(cli_key: str = "") -> str:
    """--key > LIUCHUAN_API_KEY > 旧 YAUNDIAN_API_KEY（兜底，并提示改名）。"""
    if (cli_key or "").strip():
        return cli_key.strip()
    for name in ("LIUCHUAN_API_KEY", "YAUNDIAN_API_KEY"):
        v = (os.environ.get(name) or "").strip()
        if v:
            if name == "YAUNDIAN_API_KEY":
                print("NOTE: 读到旧变量 YAUNDIAN_API_KEY。服务已改名，"
                      "请改为 LIUCHUAN_API_KEY（旧变量暂仍兼容）。",
                      file=sys.stderr)
            return v
    return ""


SELFCHECK_SAMPLE = [
    {"note_id": "sc1", "title": "selfcheck sample note",
     "desc": "离线自检样本正文，不来自任何真实接口。",
     "like_count": 12, "collect_count": 3, "comment_count": 1,
     "share_count": 0, "fans_count": 800, "tags": ["自我检查"],
     "category": "样本", "nickname": "sample",
     "published_at": "2026-11-26", "video_url": "", "note_type": "normal"},
]

ENDPOINT_HINT = """未配置数据服务端点：环境变量 LIUCHUAN_BASE_URL 未设置（当前为占位符，不会发请求）。
取数前先配置（二选一）：
  1) 环境变量（推荐，永久生效）：
     Linux/macOS:  export LIUCHUAN_BASE_URL=https://<你的服务域名>/liuchuan/api/v1
     Windows:      [Environment]::SetEnvironmentVariable("LIUCHUAN_BASE_URL","https://<你的服务域名>/liuchuan/api/v1","User")
  2) 单次指定：    --base-url https://<你的服务域名>/liuchuan/api/v1
API Key（可选但推荐）：export LIUCHUAN_API_KEY=<你的 key>
不依赖端点的离线能力：--menu / --selfcheck / --show-paths / --show-profile / --tag-report"""


def run_selfcheck() -> int:
    """离线自检：不联网、不要 Key。任一项失败即 exit 1。"""
    checks = []

    def ok(name, detail=""):
        checks.append((True, name, detail))

    def bad(name, detail=""):
        checks.append((False, name, detail))

    ok("python", f"{sys.version_info.major}.{sys.version_info.minor}."
                 f"{sys.version_info.micro}")
    ok("requests", "已安装" if requests is not None else
       "未安装（取数需 pip install requests；离线能力不受影响）")
    try:
        assert parse_time_range("1") == "12h"
        assert parse_time_range("3") == "yesterday"
        assert parse_type("2") == "video"
        assert parse_type("图文") == "normal"
        ok("参数解析", "time-range 编号映射 / type 编号与中文映射均正确")
    except AssertionError as exc:
        bad("参数解析", repr(exc))
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        probe = CACHE_DIR / ".selfcheck.tmp"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        ok("缓存目录可写", str(CACHE_DIR))
    except OSError as exc:
        bad("缓存目录可写", str(exc))
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_menu()
        text = buf.getvalue()
        if "问题 1" in text and "问题 6" in text:
            ok("问卷打印", f"--menu 输出 {len(text)} 字符，六题齐全")
        else:
            bad("问卷打印", "输出缺少问卷结构")
    except Exception as exc:
        bad("问卷打印", repr(exc))
    try:
        with tempfile.TemporaryDirectory() as td:
            out = render_html(
                SELFCHECK_SAMPLE,
                {"time_range": "12h", "data_updated_at": "2026-11-26 12:00",
                 "pulled": 1, "from_cache": True},
                "selfcheck", Path(td) / "selfcheck.html")
            size = out.stat().st_size
            if size > 1000:
                ok("HTML 看板渲染", f"离线样本 {size} 字节")
            else:
                bad("HTML 看板渲染", f"输出过小（{size} 字节）")
    except Exception as exc:
        bad("HTML 看板渲染", repr(exc))

    width = max(len(n) for _, n, _ in checks)
    for passed, name, detail in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {name.ljust(width)}  {detail}")
    failed = [c for c in checks if not c[0]]
    print(f"\nselfcheck: {len(checks) - len(failed)}/{len(checks)} 通过"
          + ("，全部通过" if not failed else f"，{len(failed)} 项失败"))
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query xiaohongshu low-fans-hot notes from the "
                    "liuchuan-data public API (generic client: endpoint via "
                    "LIUCHUAN_BASE_URL, key via LIUCHUAN_API_KEY)")
    parser.add_argument("--time-range", default="12h",
                        type=parse_time_range, choices=TIME_RANGES,
                        help="time window (default: 12h); accepts 1-5 as "
                             "menu numbers: 1=12h 2=24h 3=yesterday 4=3d 5=7d")
    parser.add_argument("--sort", default="like", choices=SORTS,
                        help="sort (default like = highest engagement first; "
                             "rank = board head first after local re-sort)")
    parser.add_argument("--rows", type=int, default=None,
                        help=f"rows to hold in the cache, pulled page by page "
                             f"(default {DEFAULT_ROWS}; 5 for anonymous tier; "
                             f"max {MAX_ROWS} = the daily quota)")
    parser.add_argument("--mix", default=None,
                        help="sort orders to sample from, split across the "
                             "quota; default like,collect (wider content mix; "
                             "single sort like for anonymous tier). "
                             "Single order narrows the sample, e.g. --mix like")
    parser.add_argument("--page-size", type=int, default=0,
                        help="deprecated alias of --rows")
    parser.add_argument("--position", default="",
                        help="account positioning words, matched against the "
                             "official category tree (see --plan); "
                             "comma/space separated, e.g. 职场 / 美妆,母婴育儿")
    parser.add_argument("--category", default="",
                        help="official huitun category name or id, filtered "
                             "SERVER-side, e.g. 美食饮品 / 861 / 表情包; "
                             "comma-separated for multi-category OR; a "
                             "parent covers its whole subtree. ~74%% of 12h "
                             "rows carry a category. See --list-categories")
    parser.add_argument("--body-keyword", default="",
                        help="body keywords, filtered SERVER-side on note "
                             "body (desc_text); comma-separated words OR'd, "
                             "literal match (no wildcards), e.g. 咖啡 / 咖啡,瑞幸")
    parser.add_argument("--type", default="all", type=parse_type,
                        choices=("all", "video", "normal"),
                        help="content type: all (default) / video only / "
                             "normal (image-text) only; accepts menu numbers "
                             "1=all 2=video 3=normal. SERVER-side filter, "
                             "quota charged on returned rows. Legacy rows "
                             "with unknown type only show under all")
    parser.add_argument("--list-categories", action="store_true",
                        help="print the official category tree and exit")
    parser.add_argument("--plan", action="store_true",
                        help="match --position against the official category "
                             "tree and print the numbered confirmation list; "
                             "zero row quota, no data pulled")
    parser.add_argument("--menu", action="store_true",
                        help="print the one-shot questionnaire (all 6 questions: "
                             "category / time range / mix / rows / filters / "
                             "note_type, with 其他 options where applicable) and "
                             "exit; zero quota, paste the whole list to the user "
                             "so they answer in a single reply")
    parser.add_argument("--save-profile", action="store_true",
                        help="fix the current persona (category / position / "
                             "body keyword + defaults) into "
                             "~/.liuchuan_cache/profile.json; zero quota")
    parser.add_argument("--show-profile", action="store_true",
                        help="print the fixed persona; zero quota")
    parser.add_argument("--forget-profile", action="store_true",
                        help="remove the fixed persona; zero quota")
    parser.add_argument("--cache-dir", default="",
                        help="override the sample cache directory for this run")
    parser.add_argument("--config-dir", default="",
                        help="override the config directory (profile.json) "
                             "for this run")
    parser.add_argument("--set-cache-dir", default="",
                        help="move the sample cache to this path: copy existing "
                             "files, write a pointer file, zero quota")
    parser.add_argument("--show-paths", action="store_true",
                        help="print the resolved cache/config paths and counts; "
                             "zero quota")
    parser.add_argument("--min-like", type=int, default=0,
                        help="minimum like_count")
    parser.add_argument("--tag-groups", default="",
                        help="curated tag groups for the HTML filter, "
                             "'名称=标签a,标签b;名称2=标签c' — agent judges "
                             "the tag distribution of the fetched sample and "
                             "passes it in; omitted = raw tags by frequency")
    parser.add_argument("--tag-report", action="store_true",
                        help="print the tag frequency of the fetched sample "
                             "and exit (so the agent can curate --tag-groups); "
                             "hits cache, costs no row quota")
    parser.add_argument("--max-fans", type=int, default=0,
                        help="maximum fans_count, e.g. 10000; fans_count=0 "
                             "always passes")
    parser.add_argument("--refresh", action="store_true",
                        help="ignore the local cache and pull again "
                             "(costs quota)")
    parser.add_argument("--no-history", action="store_true",
                        help="only show the notes fetched in this run; default "
                             "also loads every cached batch into the board so "
                             "the 获取时间 filter can replay historical data")
    parser.add_argument("--clear-cache", action="store_true",
                        help="delete every local notes_*.json cache file "
                             "(zero quota); quota snapshot and preview-server "
                             "state are kept")
    parser.add_argument("--key", default="",
                        help="api key (default: $LIUCHUAN_API_KEY)")
    parser.add_argument("--allow-anon", action="store_true",
                        help="keyless mode is blocked by the server's UA guard "
                             "since v1.25; pass this only to see the 429 yourself "
                             "(single 5 rows, 10 rows/day, 1 req/3 min)")
    parser.add_argument("--base-url", default=BASE_URL,
                        help="override api base url")
    parser.add_argument("--html", default="",
                        help="write an HTML board to this path "
                             "(default: ./低粉爆款_<类目>_<range>.html)")
    parser.add_argument("--no-serve", action="store_true",
                        help="skip the local preview server and only hand over "
                             "the file path (no http address)")
    parser.add_argument("--serve-port", type=int, default=0,
                        help=f"port for the local preview server; default reuses "
                             f"the running one or takes {SERVE_PORT_BASE}+; "
                             f"bound to 127.0.0.1 only")
    parser.add_argument("--stop-serve", action="store_true",
                        help="stop the local preview server started earlier "
                             "(zero quota)")
    parser.add_argument("--no-html", action="store_true",
                        help="skip HTML generation, print the table only")
    parser.add_argument("--json", action="store_true",
                        help="print raw JSON instead of a table")
    parser.add_argument("--selfcheck", action="store_true",
                        help="offline self-check (no network, no key): "
                             "imports, arg parsing, cache dir, questionnaire "
                             "and the HTML board with a bundled sample")
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()

    # 通用客户端版：端点未配置（占位符）时不发注定失败的请求
    if (args.base_url == PLACEHOLDER_BASE_URL
            and "--base-url" not in sys.argv
            and not (args.menu or args.show_paths or args.set_cache_dir
                     or args.show_profile or args.forget_profile
                     or args.save_profile or args.clear_cache
                     or args.stop_serve or args.tag_report)):
        print(ENDPOINT_HINT, file=sys.stderr)
        return 0 if len(sys.argv) == 1 else 2

    # v1.34：路径先定下来（命令行 > 环境变量 > 指针文件 > 平台默认），
    # 首次启动把旧的家目录缓存复制过来（只复制、不删除）
    configure_paths(getattr(args, "cache_dir", "") or "",
                    getattr(args, "config_dir", "") or "")
    note = migrate_legacy_paths()
    if note:
        print(note, file=sys.stderr)

    if args.show_paths or args.set_cache_dir:
        if args.set_cache_dir:
            print(set_cache_dir(args.set_cache_dir))
        notes = list(CACHE_DIR.glob("notes_*.json")) if CACHE_DIR.exists() else []
        hist = list(HISTORY_DIR.glob("*.json")) if HISTORY_DIR.exists() else []
        print(f"缓存目录：{CACHE_DIR}")
        print(f"配置目录：{CONFIG_DIR}")
        print(f"指针文件：{PATHS_FILE}"
              f"{'（未设置，走默认）' if not PATHS_FILE.exists() else ''}")
        print(f"样本缓存：{len(notes)} 个文件 · 历史快照：{len(hist)} 个")
        return 0

    if args.menu:
        print_menu()
        return 0

    if args.show_profile:
        prof = load_profile()
        if not prof:
            print("尚未固定人设。取数完成后可用 --save-profile 固定"
                  "（category / position / 默认参数）。")
        else:
            print("人设已固定：" + profile_label(prof))
            print(f"  保存时间：{prof.get('saved_at', '')}")
            flt = []
            if prof.get("min_like"):
                flt.append("点赞≥" + str(prof["min_like"]))
            if prof.get("max_fans"):
                flt.append("粉丝≤" + str(prof["max_fans"]))
            print(f"  默认参数：时间 {prof.get('time_range', '')} · 采样 "
                  f"{'/'.join(prof.get('mix') or [])} · 规模 "
                  f"{prof.get('rows', '')} 条 · 过滤 "
                  f"{('、'.join(flt) if flt else '不加过滤')} · 类型 "
                  f"{prof.get('note_type') or 'all'}")
            print(f"  文件：{PROFILE_FILE}")
        return 0

    if args.forget_profile:
        print("已清除固定人设，下次取数照常问卷。"
              if clear_profile() else "本来就没有固定人设。")
        return 0

    if args.save_profile:
        pos = [t.strip() for t in
               (args.position or "").replace("，", ",").replace(" ", ",")
               .split(",") if t.strip()]
        if not (args.category or pos or args.body_keyword):
            print("ERROR: --save-profile 至少要有 --category / --position / "
                  "--body-keyword 之一", file=sys.stderr)
            return 1
        mix = [s.strip() for s in (args.mix or "like,collect")
               .replace("，", ",").split(",") if s.strip()]
        prof = {
            "category": args.category or "",
            "position": pos,
            "body_keyword": args.body_keyword or "",
            "note_type": "" if args.type == "all" else args.type,
            "time_range": parse_time_range(args.time_range),
            "mix": mix,
            "rows": args.rows or DEFAULT_ROWS,
            "min_like": args.min_like or 0,
            "max_fans": args.max_fans or 0,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        save_profile(prof)
        print("已固定人设：" + profile_label(prof))
        print(f"  存到 {PROFILE_FILE}；以后 --menu 第 1 题回 0 即沿用，"
              "不想用了随时 --forget-profile。")
        return 0

    key = resolve_api_key(args.key)

    # /v1/categories 是公开端点：免 Key、免配额，必须排在 Key 检查之前
    if args.list_categories or args.plan:
        try:
            cat_items = fetch_categories(args.base_url, key)
        except FetchError as e:
            print(f"ERROR: {e.message}", file=sys.stderr)
            return 3
        if args.plan:
            pos_tokens = [t.strip() for t in
                          args.position.replace("，", ",").replace(" ", ",")
                          .split(",") if t.strip()]
            print_position_plan(pos_tokens, cat_items)
            return 0
        print_categories(cat_items)
        return 0

    # 无 Key：服务端 v1.25 起匿名档对脚本 UA 一律 429（风控设计，非故障）。
    # 所以这里前置拦截，不发那次注定失败的请求；--allow-anon 是知情逃生口。
    anon = not key
    migrate_legacy_cache()   # 改名后首次运行：旧缓存一次性铺到新目录
    load_quota()   # 先读上次落盘的剩余额度，缓存命中时也能报
    if args.clear_cache:
        print(clear_local_cache())
        return 0
    seed_history_from_cache()   # v1.30：老缓存补历史快照，时间筛选立刻可用
    if args.stop_serve:
        print(stop_server())
        return 0
    probe = probe_meta(args.base_url)     # 公开端点探活，零配额
    if anon and not args.allow_anon:
        print(f"未配置 API Key → 无法取数。服务端 v1.25 起匿名档对脚本 UA "
              f"一律返回 429（user-agent blocked），这是风控设计，重试无用。",
              file=sys.stderr)
        if probe:
            print(f"（服务端可达：{probe.get('service', '')} · 最近入库 "
                  f"{(probe.get('last_ingest_at') or '—')[:16]}）",
                  file=sys.stderr)
        print("→ 领 Key 后写环境变量即可正常取数（设完重开终端）：\n"
              '   [Environment]::SetEnvironmentVariable('
              '"LIUCHUAN_API_KEY","<你的 key>","User")\n'
              "→ 已知情仍要试匿名档（单次 5 条、每天 10 条、3 分钟 1 次，"
              "且必然被拦）：加 --allow-anon\n"
              "→ 只想看分类/菜单（免 Key、零配额）：--menu / "
              "--list-categories / --plan", file=sys.stderr)
        stale = stale_note(probe)
        if stale:
            print("WARN: " + stale, file=sys.stderr)
        return 1
    if anon:
        print("NOTE: 已按 --allow-anon 走【匿名体验档】：单次最多 "
              f"{ANON_ROWS} 条、每天 {ANON_DAILY} 条、默认单排序；"
              "trend/authors 端点不可用。脚本 UA 会被服务端风控 429。",
              file=sys.stderr)
    stale = stale_note(probe)
    if stale:
        print("WARN: " + stale, file=sys.stderr)

    rows = args.page_size or args.rows or (ANON_ROWS if anon else DEFAULT_ROWS)
    if rows < 1:
        print("ERROR: --rows must be >= 1", file=sys.stderr)
        return 1
    if rows > MAX_ROWS:
        print(f"NOTE: --rows={rows} 超过每日配额上限 {MAX_ROWS}，按 "
              f"{MAX_ROWS} 取。", file=sys.stderr)
        rows = MAX_ROWS
    target_rows = rows          # 记下目标条数，别被后面循环里的同名变量覆盖

    # 两通道：--category（官方类目，服务端子树过滤）+ --body-keyword
    # （正文词，服务端 LIKE 收窄）。账号定位词只走 --plan 候选确认，
    # 不再有话题词自动映射通道。--type 是叠加其上的内容类型收窄。
    category = args.category
    keyword = args.body_keyword
    note_type = "" if args.type == "all" else args.type

    mix_raw = args.mix or ("like" if anon else "like,collect")
    mix = tuple(s.strip() for s in mix_raw.replace("，", ",").split(",")
                if s.strip())
    bad = [s for s in mix if s not in SORTS]
    if bad or not mix:
        print(f"ERROR: --mix 只能是 {', '.join(SORTS)} 的组合",
              file=sys.stderr)
        return 1

    per_sort = max(PAGE_SIZE, rows // max(1, len(mix)))
    req_count = -(-per_sort // PAGE_SIZE) * len(mix)

    items, meta, from_cache = collect(args.base_url, key, args.time_range,
                                      mix, rows, args.refresh,
                                      category, keyword, note_type)
    if not from_cache:
        if anon:
            print(f"将发 {req_count} 次请求（{'/'.join(mix)}）；匿名档单次最多回 "
                  f"{ANON_ROWS} 条、每天共 {ANON_DAILY} 条，本次实际最多 "
                  f"{ANON_ROWS} 条。", file=sys.stderr)
        else:
            print(f"将发 {req_count} 次请求（{'/'.join(mix)}）；类目/正文词"
                  "均为服务端过滤，按实际返回条数扣配额。", file=sys.stderr)
    items = filter_items(items, args.min_like, args.max_fans)
    items = sort_items(items, args.sort)

    # 本期取到的数据 + 本地已缓存的历史数据（v1.30）
    # 每条都记下「获取时间」：本期=本次缓存快照时间，历史=该缓存文件的保存时间；
    # 同一篇笔记多批次出现时取最早的获取时间（第一次被我们拿到）。
    cur_at = meta.get("cached_at") or ""
    for it in items:
        it["_cur"] = True
        it["_fetch_at"] = cur_at
    cur_n = len(items)
    hist_n = 0
    if not args.no_history:
        cur_files = [cache_file(args.time_range, s, category, keyword, note_type)
                     for s in mix]
        earliest = {}
        cur_ids = {it.get("note_id") for it in items}
        scope = _safe_name(category) if category else cache_slug(
            category, keyword, note_type)
        for ts, hist_batch in load_cache_history(scope, cur_files):
            lab = fmt_fetch(ts)
            for it in hist_batch:
                nid = it.get("note_id")
                if not nid or nid in cur_ids:
                    continue
                prev = earliest.get(nid)
                if prev and prev[0] <= ts:
                    continue
                earliest[nid] = (ts, it, lab)
        hist_rows = []
        for nid, (ts, it, lab) in earliest.items():
            it = dict(it)
            it["_cur"] = False
            it["_fetch_at"] = lab
            hist_rows.append(it)
        if hist_rows:
            hist_rows = sort_items(
                filter_items(hist_rows, args.min_like, args.max_fans), args.sort)
        hist_n = len(hist_rows)
        items = items + hist_rows

    position = [t.strip() for t in
                args.position.replace("，", ",").replace(" ", ",")
                .split(",") if t.strip()]
    meta.update({
        "sort": args.sort,
        "mix": list(mix),
        "rows_target": target_rows,
        "position": position or None,
        "category": category or None,
        "body_keyword": keyword or None,
        "note_type": note_type or None,
        "matched": cur_n,
        "history_n": hist_n,
        "from_cache": from_cache,
        "tag_groups": parse_tag_groups(args.tag_groups) or None,
        "category": category or "",
    })
    # 最近一次成功取数的参数（v1.32）：只用于下次问卷的 ★ 推荐，不算固定人设
    record_last_run({
        "category": category or "",
        "position": position,
        "body_keyword": keyword or "",
        "note_type": note_type,
        "time_range": args.time_range,
        "mix": list(mix),
        "rows": meta.get("rows_target") or DEFAULT_ROWS,
        "min_like": args.min_like,
        "max_fans": args.max_fans,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    # 主题筛选缓存（v1.33）：本批主题组 / 标签并进本地，下一批只做增量补充
    merge_theme_cache(
        category,
        parse_tag_groups(args.tag_groups),
        [i for i in items if i.get("_cur")],
        meta.get("cached_at") or "",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    if args.tag_report:
        cur_items = [it for it in items if it.get("_cur")]
        tc = Counter(t for it in cur_items for t in (it.get("tags") or []) if t)
        print(f"topic_report: 本期 {len(cur_items)} 条样本 / {len(tc)} 个标签"
              f"（缺 tags 的条目 {sum(1 for it in cur_items if not it.get('tags'))} 条）")
        for t, n in tc.most_common(80):
            print(f"  {n:>2}  {t}")
        print("\n--- 逐条标题 / 正文字眼 / 标签（提炼主题用）---")
        for it in cur_items[:80]:
            ttl = (it.get("title") or "").replace("\n", " ")
            desc = (it.get("desc_text") or "").replace("\n", " ")
            tags = "、".join((it.get("tags") or [])[:8])
            print(f"#{str(it.get('rank_no') or '-').rjust(3)} "
                  f"{ttl[:42]} ｜ 标签: {tags or '无'} ｜ 正文: {desc[:70]}")
        print("\n归组：主题词可以来自标题/正文字眼，不限于 tags；用 "
              "--tag-groups \"主题=词a,词b;主题2=词c\" 重跑（命中缓存，零配额）。"
              "组内任一「标签或标题/正文包含该词」即算命中，选项数量不设上限。")
        return 0

    if args.json:
        print(json.dumps({"meta": meta, "items": items},
                         ensure_ascii=False, indent=2))
        return 0

    scope_parts = []
    if category:
        scope_parts.append(f"类目={category}")
    if keyword:
        scope_parts.append(f"正文词={keyword}")
    if note_type:
        scope_parts.append(f"类型={TYPE_LABEL[note_type]}")
    scope = " + ".join(scope_parts) if scope_parts else "全部领域"
    src = f"缓存@{meta.get('cached_at')}" if from_cache else "实时"
    by_sort = "/".join(f"{k}:{v}" for k, v in
                       (meta.get("pulled_by_sort") or {}).items())
    rem_txt = (f" 剩余={meta['quota_remaining']} 条"
               if meta.get("quota_remaining") is not None else "")
    print(f"time_range={meta.get('time_range')} total={meta.get('total')} "
          f"pulled={meta.get('pulled')}({by_sort or 'n/a'}) "
          f"matched={len(items)} {scope} "
          f"updated={meta.get('data_updated_at')} 来源={src}{rem_txt}")
    if scope_parts and (meta.get("total") or 0) == 0:
        print("NOTE: 该组合条件下库内 0 命中——类目在该时间窗可能没数据"
              "（官方类目覆盖率约 74%，老维度与历史条目可能缺类目），"
              "可换 12h/yesterday 维度、去掉 --category 用 --body-keyword "
              "检索，或用 --plan 重新确认类目。", file=sys.stderr)
    elif (meta.get("pulled") or 0) > 0 and (meta.get("total") or 0) < 5:
        print("NOTE: 该时间维度库内数据异常偏少（疑似采集/入库不全），"
              "建议换 12h 或 yesterday 维度。", file=sys.stderr)

    label = (category if category else
             (keyword if keyword else "全部领域"))
    # 类型过滤时文件名带类型后缀，避免 视频版/图文版 互相覆盖
    type_suffix = ("" if not note_type
                   else f"_{TYPE_LABEL.get(note_type, note_type)}")
    default_html = f"低粉爆款_{_safe_name(label)}{type_suffix}_{meta.get('time_range')}.html"

    if not items:
        if meta.get("pulled") == 0:
            print("ERROR: 没取到任何数据，且本地无缓存。配额可能已用完。",
                  file=sys.stderr)
            return EXIT_QUOTA
        print("no notes matched —— 服务端过滤后 0 命中（total="
              f"{meta.get('total')}）。类目没数据时可去掉 --category 用 "
              "--body-keyword 按正文词检索，或换时间维度重试。")

    if not items:
        if not args.no_html:
            path = (Path(args.html) if args.html else
                    Path(default_html))
            out = render_html(items, meta, label, path)
            print(f"HTML 报告已生成：{out.resolve()}")
            url = "" if args.no_serve else preview_url(out, args.serve_port)
            print_conclusion(items, meta, from_cache, url)
        else:
            print_conclusion(items, meta, from_cache)
        return 0

    print_table(items)

    url = ""
    if not args.no_html:
        path = (Path(args.html) if args.html else
                Path(default_html))
        out = render_html(items, meta, label, path)
        print(f"HTML 报告已生成：{out.resolve()}")
        url = "" if args.no_serve else preview_url(out, args.serve_port)
    print_conclusion(items, meta, from_cache, url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
