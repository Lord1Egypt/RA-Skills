# -*- coding: utf-8 -*-
"""会话落盘加速层：本地先落地，后台单写者回写网络盘（**不改语义**）。

## 为什么需要（2026-09-20 实测）

技能目录（`<用户主目录>/.workbuddy/skills/meta-analysis`）是软链接 →
指向内网文件盘（`\\\\<内网文件服务器>\\c$\\...`，SMB）。
同一份 2.4MB 会话 JSON 的写入成本实测：

    | 位置            | 写 1 MB   | 写 2.4 MB（一次 save） |
    | skill 目录(网络) | 185.5 ms  | 272.3 ms               |
    | 本机 C:          |   2.5 ms  |   2.6 ms               |
    | 倍数             |   ×74     |   ×105                 |

而 `fullflow.py` 有 16 处 `save()` 调用点，一次打回/回退连续触发 3~5 次
（rewind → invalidate → 各阶段推进 → 审计留痕）→ 纯 I/O 吃掉 8~13 秒。

## 做法

* **写**：本地镜像（原子写，几毫秒）+ 把「网络盘那份」丢给单写者后台线程。
  同一路径**合并**（后写覆盖前写），主流程不再等网络 I/O。
* **读**：本进程写过的会话直接内存命中（`_DOC`）；内存里没有（别的进程写的 /
  进程重启过）则**照旧读网络盘**——读只要 33 ms，不值得为它引入歧义。
* **兜底**：镜像只在「有修订还没回写到网络」时被读取（见 `_read_mirror`），
  以及 `flush()` 时重试；`atexit` 冲刷队列（带超时），正常退出不留未回写改动。

## 安全边界（刻意约束）

* 网络盘那份文件始终是**同一份字节**：镜像标记只写在本地镜像文件的头部，
  会话 JSON 本体不含任何额外字段 → 审计日志格式与人工可读性完全不变。
* 回写失败**不清 pending**，改为退避重试；本地副本仍是权威，读不会拿到旧数据。
* `_DOC` 命中前会比对网络盘 mtime/size 是否仍是「上次回写成功后观测到的值」；
  变了说明**别的进程改过**→ 丢弃内存副本，回落到读网络盘（不覆盖别人的写入）。
* 镜像目录默认 `%LOCALAPPDATA%\\meta-analysis-wb`，可用环境变量
  `META_WB_LOCAL_DIR` 覆盖；该目录可随时手工删除，删掉只是回到「读网络盘」。
"""

import atexit
import hashlib
import json
import os
import struct
import threading
import time

_MAGIC = b"MWB1"
_HDR_LEN = struct.Struct("<I")

_APP_DIRNAME = "meta-analysis-wb"
_KEEP_DOC = 8            # 内存中保留的会话正文本数（LRU 上限）
_FLUSH_TIMEOUT = 30.0    # atexit 冲刷超时（秒）
_RETRY_BACKOFF = 1.5     # 回写失败退避（秒）
_WRITE_RETRIES = 3       # 单次回写重试次数（之后交回后台循环退避重试）


# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
def local_root():
    """本机落盘根目录（可由 META_WB_LOCAL_DIR 覆盖）。"""
    base = os.environ.get("META_WB_LOCAL_DIR")
    if base:
        return os.path.abspath(base)
    la = (os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP")
          or os.path.expanduser("~"))
    return os.path.join(la, _APP_DIRNAME)


def mirror_dir():
    return os.path.join(local_root(), "sessions")


_CANON_MEMO = {}


def _canon(path):
    """把路径规范化成唯一键。

    关键：技能目录是软链接，同一个文件可能以本地盘（`C:\\Users\\...\\skills\\...`）或
    UNC（`\\\\<内网文件服务器>\\c$\\...`）两种写法出现。`realpath` 消解链接后再 normcase，
    两种写法才会落到同一个键上（否则缓存与镜像会各存一份、互相看不见）。

    记忆化（2026-09-20）：`realpath` 对路径**每一段**都要 stat，在网络盘上单次
    实测 ~50 ms（`/api/session` 的命中路径里它占了大头）。而映射在进程内不会变
    （软链接不会运行期改写），故按原文路径缓存结果。
    """
    hit = _CANON_MEMO.get(path)
    if hit is not None:
        return hit
    try:
        p = os.path.realpath(path)
    except OSError:
        p = os.path.abspath(path)
    cp = os.path.normcase(os.path.abspath(p))
    if len(_CANON_MEMO) > 512:
        _CANON_MEMO.clear()
    _CANON_MEMO[path] = cp
    return cp


def mirror_paths(path):
    cp = _canon(path)
    k = hashlib.sha1(cp.encode("utf-8", "surrogatepass")).hexdigest()[:20]
    d = mirror_dir()
    return (os.path.join(d, k + ".mirror"),   # 正文镜像（头部带元信息）
            os.path.join(d, k + ".synced"))   # 已回写进度（seq / 网络盘状态）


# ---------------------------------------------------------------------------
# 进程内状态
# ---------------------------------------------------------------------------
_LOCK = threading.RLock()
_COND = threading.Condition(_LOCK)
_DOC = {}          # canon -> 正文（本进程最近写入的内容）
_ORDER = []        # canon 的 LRU 顺序
_REV = {}          # canon -> 本进程写入的修订号（单调递增，从 1 起）
_PENDING = set()   # canon -> 有修订尚未成功回写网络盘
_QUEUE = {}        # canon -> (net_path, text)；合并：后写覆盖前写
_NET_STAT = {}     # canon -> (mtime_ns, size) 上次回写成功后观测到的网络盘状态
_ERR = {}          # canon -> 最近一次回写错误摘要
_WRITER = None
_STOP = False


# ---------------------------------------------------------------------------
# 原子写
# ---------------------------------------------------------------------------
def _atomic_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def _atomic_write_bytes(path, raw):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(raw)
    os.replace(tmp, path)


def _pack_mirror(header, body):
    hb = json.dumps(header, ensure_ascii=False).encode("utf-8")
    return _MAGIC + _HDR_LEN.pack(len(hb)) + hb + body.encode("utf-8")


def _parse_mirror(raw):
    """返回 (header, body_text)；格式不符返回 (None, None)。"""
    try:
        if not raw.startswith(_MAGIC):
            return None, None
        off = len(_MAGIC)
        (n,) = _HDR_LEN.unpack_from(raw, off)
        off += _HDR_LEN.size
        hdr = json.loads(raw[off:off + n].decode("utf-8"))
        body = raw[off + n:].decode("utf-8")
        return hdr, body
    except Exception:  # noqa: BLE001 — 镜像损坏一律当作不存在
        return None, None


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None


def _write_synced(cp, seq, st):
    """记录「已成功回写到 seq，且网络盘此刻的状态是 st」。仅在 seq 仍是最新时写。"""
    with _LOCK:
        if _REV.get(cp) != seq:
            return                       # 已有更新的修订，交给它去记录
    _, sync_f = mirror_paths(cp)         # cp 已是 canon，可再次 canon（幂等）
    try:
        os.makedirs(os.path.dirname(sync_f), exist_ok=True)
        _atomic_write(sync_f, json.dumps({
            "seq": seq,
            "net_mtime_ns": None if st is None else st.st_mtime_ns,
            "net_size": None if st is None else st.st_size,
        }, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001 — 进度文件写失败不影响主流程
        with _LOCK:
            _ERR[cp] = f"synced: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 后台回写线程
# ---------------------------------------------------------------------------
def _write_net(net, text):
    """把正文写到网络盘（临时文件 + 原子替换），返回写后 stat。"""
    d = os.path.dirname(net)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    last = None
    for attempt in range(_WRITE_RETRIES):
        try:
            _atomic_write(net, text)
            return os.stat(net)
        except Exception as e:  # noqa: BLE001 — 网络抖动/占用，短暂退避后重试
            last = e
            time.sleep(0.25 * (attempt + 1))
    raise last


def _writer_loop():
    while True:
        with _COND:
            while not _QUEUE and not _STOP:
                _COND.wait(0.5)
            if _STOP and not _QUEUE:
                return
            if not _QUEUE:
                continue
            cp = next(iter(_QUEUE))
            net, text, seq = _QUEUE.pop(cp)
        try:
            st = _write_net(net, text)
        except Exception as e:  # noqa: BLE001 — 回写失败：不放行，退避重试
            with _COND:
                # setdefault：期间若已有更新的正文入队，保留更新的那份
                _QUEUE.setdefault(cp, (net, text, seq))
                _ERR[cp] = f"{type(e).__name__}: {e}"
            time.sleep(_RETRY_BACKOFF)
            continue
        with _COND:
            _NET_STAT[cp] = (st.st_mtime_ns, st.st_size)
            # 只有当本次回写的正是最新修订时，才认为 pending 清空
            if _REV.get(cp) == seq:
                _PENDING.discard(cp)
            _ERR.pop(cp, None)
        _write_synced(cp, seq, st)


def _ensure_writer_locked():
    """调用方须持 _LOCK。"""
    global _WRITER
    if _WRITER is None or not _WRITER.is_alive():
        _WRITER = threading.Thread(target=_writer_loop, name="session-sync",
                                   daemon=True)
        _WRITER.start()


# ---------------------------------------------------------------------------
# 公开接口
# ---------------------------------------------------------------------------
def read_text(path):
    """返回可信本地副本的正文；没有可信本地副本时返回 None（调用方读原文件）。

    可信 = 本进程写过、且（仍有未回写的修订 或 原文件仍是上次回写后的状态）。
    原文件状态变了 ⇒ 别的进程改过 ⇒ 主动放弃内存副本，回落到读原文件，
    避免用陈旧副本盖住别人刚写的审计记录。
    """
    net = os.path.abspath(path)
    cp = _canon(net)
    with _LOCK:
        doc = _DOC.get(cp)
        pending = cp in _PENDING
        rec = _NET_STAT.get(cp)
        if doc is not None:
            if pending or rec is None or _stat_eq(net, rec):
                _touch_lru(cp)
                return doc
            # 外进程改写：丢弃内存副本，并回落到原文件（镜像同样已过时，不再采信）
            _DOC.pop(cp, None)
            _NET_STAT.pop(cp, None)
            return None
    return _read_mirror(net, cp)


def _stat_eq(path, rec):
    try:
        st = os.stat(path)
    except OSError:
        return False
    return (st.st_mtime_ns, st.st_size) == tuple(rec)


def _read_mirror(net, cp):
    """镜像只在「有修订尚未回写到网络盘」时更权威 —— 即上次进程没能落盘成功
    （崩溃 / 网络中断）而本地副本更完整的情况。其余一律以原文件为准。
    """
    mir, sync_f = mirror_paths(net)
    if not os.path.exists(mir):
        return None
    try:
        with open(mir, "rb") as f:
            hdr, body = _parse_mirror(f.read())
    except Exception:  # noqa: BLE001
        return None
    if not hdr or hdr.get("src") != cp or not isinstance(body, str):
        return None
    seq = hdr.get("seq") or 0
    done = (_read_json(sync_f) or {}).get("seq") or 0
    if seq > done:                       # 有未回写的修订 → 镜像更新
        return body
    return None


def write_text(path, text, updated_at=None):
    """本地落地 + 排队回写网络盘。

    网络盘那份**首次**写入走同步（会话文件尚不存在时必须立刻可见，否则
    `/api/session` 会 404）；此后每次只写本地镜像 + 排队，主流程不再等网络 I/O。
    """
    net = os.path.abspath(path)
    cp = _canon(net)
    mir, _ = mirror_paths(net)
    with _LOCK:
        _REV[cp] = _REV.get(cp, 0) + 1
        seq = _REV[cp]
        _DOC[cp] = text
        _touch_lru(cp)
    try:
        first = not os.path.exists(net)
    except OSError:
        first = True

    if first:
        # 首写：同步落网络盘，保证「save() 返回后文件一定存在」
        try:
            st = _write_net(net, text)
            with _LOCK:
                _NET_STAT[cp] = (st.st_mtime_ns, st.st_size)
        except Exception as e:  # noqa: BLE001 — 同步失败退回后台重试
            with _LOCK:
                _QUEUE[cp] = (net, text, seq)
                _PENDING.add(cp)
                _ERR[cp] = f"first-write: {type(e).__name__}: {e}"
                _ensure_writer_locked()
                _COND.notify()
            st = None
        _write_synced(cp, seq, st)
    else:
        with _LOCK:
            _QUEUE[cp] = (net, text, seq)      # 合并：后写覆盖前写
            _PENDING.add(cp)
            _ensure_writer_locked()
            _COND.notify()

    # 镜像：正文 + 头部（seq / 来源），单文件原子写 → 不会出现「正文与进度不匹配」
    try:
        os.makedirs(os.path.dirname(mir), exist_ok=True)
        _atomic_write_bytes(mir, _pack_mirror(
            {"src": cp, "seq": seq, "net_path": net,
             "updated_at": updated_at or ""}, text))
    except Exception as e:  # noqa: BLE001 — 镜像失败不影响主流程（_DOC 仍在）
        with _LOCK:
            _ERR[cp] = f"mirror: {type(e).__name__}: {e}"


def _touch_lru(cp):
    """调用方须持 _LOCK。"""
    try:
        _ORDER.remove(cp)
    except ValueError:
        pass
    _ORDER.append(cp)
    while len(_ORDER) > _KEEP_DOC:
        old = _ORDER.pop(0)
        _DOC.pop(old, None)


def rev(path):
    """本进程对该路径的修订号（没写过返回 None）。用于上层缓存失效。"""
    return _REV.get(_canon(os.path.abspath(path)))


def pending_paths():
    with _LOCK:
        return sorted(_PENDING)


def last_error(path):
    return _ERR.get(_canon(os.path.abspath(path)))


def flush(timeout=_FLUSH_TIMEOUT):
    """等待所有未回写修订落到网络盘（进程退出 / 关键点调用）。返回是否已清空。"""
    deadline = time.time() + max(0.0, float(timeout))
    with _COND:
        _ensure_writer_locked()
        while _QUEUE or _PENDING:
            left = deadline - time.time()
            if left <= 0:
                return False
            _COND.wait(min(0.25, left))
    return True


def stats():
    with _LOCK:
        return {
            "mirror_dir": mirror_dir(),
            "cached_docs": len(_DOC),
            "pending": sorted(_PENDING),
            "queued": sorted(_QUEUE),
            "net_stat_tracked": len(_NET_STAT),
            "errors": dict(_ERR),
            "writer_alive": bool(_WRITER and _WRITER.is_alive()),
        }


@atexit.register
def _flush_on_exit():
    try:
        flush(10.0)
    except Exception:  # noqa: BLE001 — 退出路径绝不抛
        pass
