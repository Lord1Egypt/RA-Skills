#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""project-organization 公共工具：JSON 输出、根目录标记定位、命名与时间戳。

跨机/跨系统（Windows / Linux / macOS）纯标准库实现，零本机绝对路径。
所有默认根目录一律取自环境变量（OPENCODE_THU_DIR / OPENCODE_TEMP_DIR /
OPENCODE_SCRATCH_DIR），与 AGENTS.md「路径根与环境变量」保持一致。
"""
import datetime
import io
import json
import os
import re
import shutil
import sys
import tarfile
import time
from pathlib import Path

# 大项目根标记文件：某目录含此文件即认定其为 project-organization 管理的大项目根
MARKER = ".bigproject.json"
TRASH_DIR = ".trash"
PROJECTS_DIR = "projects"
SHARED_DIR = "shared"
ARCHIVE_DIR = "archive"
TOOLS_DIR = ".tools"

# 缓冲区（人类 ⇄ AI 交换区），位于大项目根下
BUFFER_DIR = "buffer"
BUFFER_INBOX = "inbox"      # 人 → AI：用户投递文件
BUFFER_OUTBOX = "outbox"    # AI → 人：AI 放回执/产物
BUFFER_LOG = "_buffer_log.jsonl"  # 非大项目根（无 MARKER）时的本地日志
BUFFER_LOCAL_TRASH = ".replaced"  # 非大项目根时，被覆盖旧物的暂存

# 操作日志（append-only JSONL + 派生 Markdown）
JOURNAL_NAME = "journal.jsonl"
JOURNAL_MD = "_log.md"

# 软删除暂存（.trash）：一个条目 = 一个压缩包（tar+算法）；中央索引 _index.json
# 条目内藏 _manifest.json（路径一律 **相对大项目根**，可跨机精确还原）
TRASH_INDEX = "_index.json"
TRASH_MANIFEST = "_manifest.json"
TRASH_ALGO = "zst"                       # 默认 zstd（Python 3.14 tarfile 原生支持）
TRASH_ALGO_EXT = {"zst": ".tar.zst", "gz": ".tar.gz", "xz": ".tar.xz", "bz2": ".tar.bz2"}

# 大项目根允许出现的顶层文件/目录（其余视为散落物）
ROOT_ALLOWED_FILES = {MARKER, "README.md", "AGENTS.md", "MEMORY.md", ".gitignore", ".gitattributes"}
ROOT_ALLOWED_DIRS = {PROJECTS_DIR, SHARED_DIR, ARCHIVE_DIR, TOOLS_DIR, TRASH_DIR, BUFFER_DIR, ".git"}

SHARED_SUBDIRS = ["references", "models", "config", "templates", "pipeline"]
SUBPROJECT_SUBDIRS = ["scripts", "data", "results", "output"]

# 根级目录名（用于兼容「仓库被移动过」的旧绝对路径）
ROOT_LEVEL_DIRS = (PROJECTS_DIR, SHARED_DIR, ARCHIVE_DIR, BUFFER_DIR, TOOLS_DIR, TRASH_DIR)


def rel_to_root(root, path):
    """路径 → **相对大项目根**（正斜杠）。

    正常用 relative_to；**兼容「仓库被移动过」**：旧绝对路径里若仍含某个**根级目录名**
    （`projects/ shared/ archive/ buffer/ .tools/ .trash/`），就从那里截取 → `projects/...`，使旧条目也能还原。
    """
    try:
        return Path(str(path)).resolve().relative_to(Path(root).resolve()).as_posix()
    except Exception:
        pass
    parts = re.split(r"[\\/]+", str(path))
    for i, seg in enumerate(parts):
        if seg in ROOT_LEVEL_DIRS:
            return "/".join(parts[i:])
    return ""


def reconfigure_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def emit(data, code=0):
    """stdout 只输出 JSON；成功/失败用退出码区分。"""
    reconfigure_stdio()
    text = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    raise SystemExit(code)


def log(msg):
    """进度/日志写 stderr，不污染 stdout JSON。"""
    reconfigure_stdio()
    print(msg, file=sys.stderr, flush=True)


def slugify(name):
    s = (name or "").strip()
    s = re.sub(r"[\\/:*?\"<>|\s]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-.")
    return s or "project"


def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


def actor():
    """操作者标识：优先 OPENCODE_ACTOR，其次系统用户名。"""
    return (os.environ.get("OPENCODE_ACTOR")
            or os.environ.get("USERNAME")
            or os.environ.get("USER")
            or "unknown")


def journal_path(root, markdown=False):
    return Path(root) / TOOLS_DIR / (JOURNAL_MD if markdown else JOURNAL_NAME)


def journal(root, event, target=None, **extra):
    """向 <大项目根>/.tools/journal.jsonl 追加一条操作日志（append-only）。

    事件字段：ts / actor / event / target / <extra>。日志失败不阻断主流程（返回 None）。
    """
    try:
        root = Path(root)
        rec = {"ts": now_iso(), "actor": actor(), "event": event}
        if target is not None:
            rec["target"] = str(target)
        rec.update({k: v for k, v in extra.items() if v is not None})
        p = journal_path(root)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    except Exception:
        return None


def read_journal(root):
    """读取全部日志记录（坏行跳过）。"""
    p = journal_path(root)
    out = []
    if p.is_file():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def render_journal(records):
    """把日志记录渲染成 Markdown 表格（用于派生 _log.md）。"""
    lines = ["# 操作日志（_log.md）", "",
             "> 由 `scripts/journal.py --render` 生成；数据源 `.tools/journal.jsonl`（append-only）。", "",
             "| 时间 | 操作者 | 事件 | 对象 | 详情 |",
             "|------|--------|------|------|------|"]
    keys_exclude = {"ts", "actor", "event", "target"}
    for r in records:
        extra = {k: v for k, v in r.items() if k not in keys_exclude}
        detail = json.dumps(extra, ensure_ascii=False) if extra else ""
        detail = detail.replace("|", "\\|")
        lines.append("| %s | %s | %s | %s | %s |" % (
            r.get("ts", ""), r.get("actor", ""), r.get("event", ""),
            str(r.get("target", "")).replace("|", "\\|"), detail))
    return "\n".join(lines) + "\n"


def env_path(*names):
    """返回第一个已设置的环境变量对应的 Path；都未设置则 None。"""
    for n in names:
        v = os.environ.get(n)
        if v:
            return Path(v)
    return None


def resolve_base_root(kind, explicit=None):
    """按 AGENTS.md「本地项目目录规范」把任务类别映射到 base 根（全部走环境变量）。

    kind:
      thu      -> $OPENCODE_THU_DIR
      tencent  -> $OPENCODE_TEMP_DIR/tencentcloud-ops
      shared   -> $OPENCODE_TEMP_DIR
      scratch  -> $OPENCODE_SCRATCH_DIR（未设时 $OPENCODE_TEMP_DIR/scratch）
      custom   -> 必须显式 --root
    返回 base 根 Path；无法解析时返回 None（由调用方报错）。
    """
    if explicit:
        return Path(explicit)
    if kind == "thu":
        return env_path("OPENCODE_THU_DIR")
    if kind == "tencent":
        base = env_path("OPENCODE_TEMP_DIR")
        return (base / "tencentcloud-ops") if base else None
    if kind == "shared":
        return env_path("OPENCODE_TEMP_DIR")
    if kind == "scratch":
        base = env_path("OPENCODE_SCRATCH_DIR")
        if base:
            return base
        temp = env_path("OPENCODE_TEMP_DIR")
        return (temp / "scratch") if temp else None
    return None


def find_root(start):
    """从 start（文件或目录）向上逐级查找含 MARKER 的大项目根；找不到返回 None。"""
    p = Path(start).resolve()
    if p.is_file():
        p = p.parent
    for cand in [p, *p.parents]:
        if (cand / MARKER).is_file():
            return cand
    return None


def is_big_project(path):
    return (Path(path) / MARKER).is_file()


def root_allow_extensions(root):
    """读取项目在 .bigproject.json 中声明的根级「有意扩展」，并入默认允许集。

    结构（可选，向后兼容；缺省时行为不变）：
        "root_extensions": {"files": ["INDEX.md", "TODO.md"], "dirs": ["chats"]}
    用途：某些项目在通用约定之外确有合法根级文件/目录（如研究组沿用
    research-ops 的 INDEX.md / chats/）。声明后 audit_project.py 不再报为散落物。
    返回 (extra_files:set, extra_dirs:set)。
    """
    data = read_json(Path(root) / MARKER, default={}) or {}
    ext = data.get("root_extensions", {}) if isinstance(data, dict) else {}
    ext = ext if isinstance(ext, dict) else {}
    files = set(ext.get("files", []) or [])
    dirs = set(ext.get("dirs", []) or [])
    return files, dirs


# ------------------------------------------------------------------ buffer ---
# ★ 2026-10-08 改：buffer 改「扁平」（不再有 inbox/outbox）。下面两个函数保留为兼容别名，
#   一律返回 buffer/ 本身；新代码请直接用 buffer_dir()。
def buffer_dir(root):
    return Path(root) / BUFFER_DIR


def buffer_inbox(root):
    """[兼容] 旧 inbox → 现即 buffer/ 本身（扁平）。"""
    return buffer_dir(root)


def buffer_outbox(root):
    """[兼容] 旧 outbox → 现即 buffer/ 本身（扁平）。"""
    return buffer_dir(root)


def find_project_root(start):
    """定位「大项目根」：优先含 MARKER；否则回退到含 projects/ 与 README.md 的目录。

    返回 (root, is_big_project)；找不到返回 (None, False)。
    """
    p = Path(start).resolve()
    if p.is_file():
        p = p.parent
    for cand in [p, *p.parents]:
        if (cand / MARKER).is_file():
            return cand, True
    for cand in [p, *p.parents]:
        if (cand / PROJECTS_DIR).is_dir() and (cand / "README.md").is_file():
            return cand, False
    return None, False


def project_log(root, is_big, event, target=None, **extra):
    """记录一次操作：大项目根写标准 journal；否则写 buffer 本地日志。"""
    if is_big:
        return journal(root, event, target=target, **extra)
    try:
        rec = {"ts": now_iso(), "actor": actor(), "event": event}
        if target is not None:
            rec["target"] = str(target)
        rec.update({k: v for k, v in extra.items() if v is not None})
        p = buffer_dir(root) / BUFFER_LOG
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    except Exception:
        return None


# --------------------------------------------------- 软删除暂存（.trash，压缩）
def trash_base(root, is_big):
    """暂存区根：大项目 = `.trash/`；否则 = `buffer/.replaced/`。"""
    return (Path(root) / TRASH_DIR) if is_big else (buffer_dir(root) / BUFFER_LOCAL_TRASH)


def rmtree_robust(path):
    """稳健删除目录/文件。**Windows 长路径**（>260）时 `shutil.rmtree` 会失败 →
    先**把顶层改名到短名**（不动子项 → 路径瞬间变短）再删。删不掉则抛错（不假装成功）。"""
    p = Path(path)
    if not p.exists():
        return
    if p.is_file():
        p.unlink()
        return
    tmp = p.parent / ("_.del_%d" % os.getpid())
    try:
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)
        os.rename(str(p), str(tmp))
        p = tmp
    except Exception:
        p = Path(path)
    shutil.rmtree(p, ignore_errors=True)
    if Path(path).exists() or p.exists():
        raise RuntimeError("删除失败（可能是 Windows 长路径）: %s" % path)


def _tree_bytes(path):
    path = Path(path)
    if path.is_dir():
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return path.stat().st_size if path.exists() else 0


def trash_index_load(base):
    return read_json(Path(base) / TRASH_INDEX, default={}) or {}


def _tar_add_tree(t, src, arc_root, skipped):
    """把 src 加进 tar：**逐个成员**加；读不到的（如 Windows 长路径）**跳过并记录**，不中断打包。"""
    src = Path(src)

    def _add(real, arc):
        try:
            t.add(str(real), arcname=arc, recursive=False)
        except Exception as e:
            skipped.append({"path": str(real), "error": str(e)[:140]})

    _add(src, arc_root)
    if src.is_dir():
        for dp, dns, fns in os.walk(src):
            for name in list(dns) + list(fns):
                real = Path(dp) / name
                rel = os.path.relpath(str(real), str(src)).replace(os.sep, "/")
                _add(real, arc_root + "/" + rel)


def trash_entry(base, root, paths, reason="", algo=None, rels=None):
    """把若干 path **压缩**进 `<base>/<id><ext>`，并删除原 path（压缩成功后才删）。

    包内含 `TRASH_MANIFEST`（JSON；路径一律 **相对大项目根**，跨机可精确还原）；
    同时更新 `<base>/_index.json`。返回 `(archive Path, manifest dict)`。
    `algo` ∈ {zst,gz,xz,bz2}；默认 **zstd**（Python≥3.14 `tarfile` 原生）。
    """
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    paths = [Path(p) for p in paths]
    if not paths:
        raise ValueError("trash_entry: no paths")
    algo = algo or TRASH_ALGO
    ext = TRASH_ALGO_EXT.get(algo, ".tar.zst")
    stem = "%s__%s" % (timestamp(), slugify(paths[0].name))
    arc = base / (stem + ext)
    k = 1
    while arc.exists():
        k += 1
        arc = base / ("%s-%d%s" % (stem, k, ext))
    eid = arc.name[: -len(ext)]
    root_r = Path(root).resolve()
    items, orig_bytes = [], 0
    for i, p in enumerate(paths):
        if rels is not None and i < len(rels):
            rel = rels[i]
        else:
            rel = rel_to_root(root, p)   # ★ 正斜杠；兼容仓库被移动
        items.append({"name": p.name, "orig_rel": rel})
        orig_bytes += _tree_bytes(p)
    man = {"id": eid, "time": now_iso(), "root": str(root),
           "reason": reason, "algo": algo, "items": items}
    skipped_members = []
    with tarfile.open(arc, "w:" + algo) as t:
        blob = json.dumps(man, ensure_ascii=False, indent=2).encode("utf-8")
        ti = tarfile.TarInfo(TRASH_MANIFEST)
        ti.size = len(blob)
        ti.mtime = int(time.time())
        t.addfile(ti, io.BytesIO(blob))
        for p in paths:
            _tar_add_tree(t, p, p.name, skipped_members)
    if skipped_members:
        man["skipped_members"] = skipped_members
    for p in paths:                                  # 压缩成功后才删原件
        try:
            if p.is_dir():
                rmtree_robust(p)                     # 长路径稳健删除
            else:
                p.unlink()
        except Exception as e:                       # 实在删不掉原件 → **回滚**：删包、保原状
            try:
                arc.unlink()
            except Exception:
                pass
            raise RuntimeError("无法删除原件 %s（%s）；已回滚（不留重复包）" % (p, e))
    idx = trash_index_load(base)
    idx[eid] = {"file": arc.name, "time": man["time"], "reason": reason, "algo": algo,
                "items": items, "orig_bytes": orig_bytes, "packed_bytes": arc.stat().st_size}
    write_json(Path(base) / TRASH_INDEX, idx)
    return arc, man


def soft_remove(root, is_big, path, reason=""):
    """把被覆盖/待弃的 path **压缩**存进暂存区（大项目 `.trash/`，否则 `buffer/.replaced/`）。

    条目 = `<base>/<ts>__<名>.tar.<algo>`（内含 `TRASH_MANIFEST`，路径 **相对大项目根**），
    并 **删除原 path**。返回压缩包 Path（`trash.py restore --id <id>` 可还原）。
    """
    arc, _man = trash_entry(trash_base(root, is_big), root, [Path(path)], reason=reason)
    return arc


def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def render_template(template_text, mapping):
    out = template_text
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def load_template(name):
    """读取 skill 内 templates/<name>（相对 __file__ 定位，跨机可用）。"""
    tpl = Path(__file__).resolve().parent.parent / "templates" / name
    if tpl.is_file():
        return tpl.read_text(encoding="utf-8")
    return ""
