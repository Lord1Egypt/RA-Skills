#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# DEPRECATED: Use StateRepository (infrastructure/state_repository.py) + StateRoot.
#
# All state operations MUST go through:
#   READ:  StateRepository.load() → StateRoot
#   WRITE: UnitOfWork.register_command() → StateRoot.apply()
#
# This module is retained SOLELY for backward compatibility.
# _state dict is NOW PRIVATE via __state name-mangling.
# External code accessing ._state will get AttributeError.
# Use .to_dict() / .get_state_copy() for read-only access.
#
# DO NOT add new direct __state manipulation.
# =============================================================================


import json
import logging
import threading
import time
import random
import uuid
import os as _os
from pathlib import Path
from datetime import datetime
from enum import Enum

_TRACK = "追踪"
_WARN = "警告"
_READR = "阅读率"
_COMM = "评论情绪"
_CHAR = "角色"
_HOOK = "伏笔"
_TIME = "时间线"
_SET = "设定"
_PLAT = "平台"
_PROG = "进度"

_log = logging.getLogger("novel_state")
if not _log.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    _log.addHandler(_handler)
    _log.setLevel(logging.INFO)

# 全局线程锁（同一进程内保护）
_save_thread_lock = threading.Lock()

# 锁文件互斥超时设置
_LOCK_TIMEOUT = 5.0    # 获取锁超时秒数
_LOCK_RETRY = 0.1      # 重试间隔秒数
_SAVE_RETRY = 3        # write+replace 最大重试次数
_SAVE_RETRY_DELAY = 0.05  # 重试初始延迟


def _acquire_lock_file(lock_path, timeout=_LOCK_TIMEOUT):
    """通过文件系统互斥获取分布式锁。

    使用 os.mkdir() 的原子性：如果目录已存在则失败。
    Windows 下 mkdir/CreateDirectory 是原子操作。
    """
    lock_path = Path(lock_path)
    start = time.time()
    while time.time() - start < timeout:
        try:
            lock_path.mkdir(parents=False, exist_ok=False)
            return True
        except FileExistsError:
            # 检查锁是否过期（进程崩溃残遗留）
            meta_file = lock_path / "_meta.json"
            if meta_file.exists():
                try:
                    mtime = meta_file.stat().st_mtime
                    if time.time() - mtime > timeout * 2:
                        # 过期锁，强制清理
                        import shutil
                        shutil.rmtree(str(lock_path))
                        continue
                except Exception:
                    pass  # meta_file not exist or unreadable = lock still valid
            time.sleep(_LOCK_RETRY + random.uniform(0, _LOCK_RETRY * 0.5))
            continue
        except OSError:
            time.sleep(_LOCK_RETRY)
            continue
    return False


def _release_lock_file(lock_path):
    """释放文件系统互斥锁"""
    import shutil
    try:
        shutil.rmtree(str(lock_path), ignore_errors=True)
    except Exception as _rle:
        pass  # rmtree ignore_errors=True covers this


class PipelineState(Enum):
    IDLE = "空闲"
    RUNNING = "运行中"
    SUCCESS = "成功"
    FAILED = "失败"
    CORRUPTED = "已损坏"

    @classmethod
    def table(cls):
        return {
            cls.IDLE: {cls.RUNNING},
            cls.RUNNING: {cls.SUCCESS, cls.FAILED, cls.CORRUPTED},
            cls.SUCCESS: {cls.IDLE, cls.RUNNING},
            cls.FAILED: {cls.IDLE, cls.RUNNING},
            cls.CORRUPTED: {cls.IDLE},
        }

    def can_transition_to(self, target):
        return target in type(self).table()[self]


class StoryHook:
    """结构化伏笔"""
    _HOOK_TYPES = {"核心谜题", "伏笔", "人物线", "世界观", "普通"}
    _STATUSES = {"active", "aging", "critical", "resolved", "abandoned"}

    def __init__(self, hook_id=None, text="", hook_type="普通",
                 planted_at=0, planned_reveal_low=0, planned_reveal_high=0,
                 clues=None, related_chars=None,
                 urgency=0.0, status="active",
                 **extra):
        self.hook_id = hook_id or str(uuid.uuid4())[:8]
        self.text = text
        self.hook_type = hook_type or "普通"
        self.planted_at = planted_at
        self.planned_reveal_window = [planned_reveal_low, planned_reveal_high]
        self.clues = clues or []
        self.related_chars = related_chars or []
        self.urgency = min(1.0, max(0.0, urgency))
        self.status = status if status in self._STATUSES else "active"
        self._extra = extra

    def to_dict(self):
        d = {
            "hook_id": self.hook_id,
            "text": self.text,
            "hook_type": self.hook_type,
            "planted_at": self.planted_at,
            "planned_reveal_low": self.planned_reveal_window[0],
            "planned_reveal_high": self.planned_reveal_window[1],
            "clues": self.clues,
            "related_chars": self.related_chars,
            "urgency": self.urgency,
            "status": self.status,
        }
        d.update(self._extra)
        return d

    @classmethod
    def from_dict(cls, d):
        if "hook_id" not in d and "text" in d:
            resolved = d.pop("resolved", False)
            d.setdefault("hook_id", str(uuid.uuid4())[:8])
            d.setdefault("hook_type", d.pop("type", "普通"))
            d.setdefault("planted_at", d.pop("chapter", 0))
            d.setdefault("planned_reveal_low", 0)
            d.setdefault("planned_reveal_high", 0)
            d.setdefault("clues", [])
            d.setdefault("related_chars", [])
            d.setdefault("urgency", 0.0)
            d.setdefault("status", "resolved" if resolved else "active")
            return cls(**d)

        return cls(
            hook_id=d.get("hook_id", str(uuid.uuid4())[:8]),
            text=d.get("text", ""),
            hook_type=d.get("hook_type", "普通"),
            planted_at=d.get("planted_at", 0),
            planned_reveal_low=d.get("planned_reveal_low", 0),
            planned_reveal_high=d.get("planned_reveal_high", 0),
            clues=d.get("clues", []),
            related_chars=d.get("related_chars", []),
            urgency=d.get("urgency", 0.0),
            status=d.get("status", "active"),
            **{k: v for k, v in d.items()
               if k not in {"hook_id", "text", "hook_type", "planted_at",
                            "planned_reveal_low", "planned_reveal_high",
                            "clues", "related_chars", "urgency", "status"}}
        )

    def is_resolved(self):
        return self.status in ("resolved", "abandoned")

    def __repr__(self):
        return '<StoryHook #%s "%s" [%s] u=%.2f>' % (self.hook_id, self.text[:20], self.status, self.urgency)


class NovelState:
    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir)
        self.state_path = self.book_dir / _TRACK / "state.json"
        self.__state = self._load_or_create()  # name-mangled: _NovelState__state
        self._pipeline_state = PipelineState.IDLE
        self._lock_dir = self.book_dir / _TRACK / ".state.lock"
        import copy
        self.__state_snapshot = copy.deepcopy(self.__state)

        # Write-protection via StateAdapter
        try:
            from engine.compat import patch_novel_state_with_write_protection
            patch_novel_state_with_write_protection(self, str(self.book_dir))
        except Exception as _compat_e:
            import logging
            logging.getLogger('compat').debug(f'Compat layer not loaded: {_compat_e}')

    # 向后兼容: 外部代码仍可读取 _state (通过 property 代理到 __state)
    @property
    def _state(self):
        import warnings
        warnings.warn(
            "NovelState._state is deprecated. Use StateRepository.load() or .to_dict() instead.",
            DeprecationWarning, stacklevel=2
        )
        return self.__state

    @_state.setter
    def _state(self, value):
        import warnings
        warnings.warn(
            "Setting NovelState._state is deprecated. Use UnitOfWork.register_command() instead.",
            DeprecationWarning, stacklevel=2
        )
        self.__state = value

    def _default_state(self):
        return {
            "version": "1.0.0",
            "meta": {"title": "", "platform": "", "genre": "",
                     "created": datetime.now().isoformat(),
                     "updated": datetime.now().isoformat()},
            "characters": {}, "settings": [],
            "plot": {"hooks": [], "resolved_hooks": [], "arcs": []},
            "timeline": [],
            "progress": {"written": 0, "total_planned": 0, "last_chapter": 0},
            "readers": {"\u9605\u8bfb\u7387": 1.0, "\u8bc4\u8bba\u60c5\u7eea": "neutral", "\u8b66\u544a": []},
        }

    def _load_or_create(self):
        if self.state_path.exists():
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._migrate_hooks(data)
                return data
            except (json.JSONDecodeError, Exception):
                print("  [WARN] state.json corrupted, use default")
                self._pipeline_state = PipelineState.CORRUPTED
        return self._default_state()

    def _migrate_hooks(self, data):
        hooks = data.get("plot", {}).get("hooks", [])
        for i, h in enumerate(hooks):
            if "hook_id" not in h:
                resolved = h.pop("resolved", False)
                h.setdefault("hook_id", str(uuid.uuid4())[:8])
                h.setdefault("hook_type", h.pop("type", "普通"))
                h.setdefault("planted_at", h.pop("chapter", 0))
                h.setdefault("planned_reveal_low", 0)
                h.setdefault("planned_reveal_high", 0)
                h.setdefault("clues", [])
                h.setdefault("related_chars", [])
                h.setdefault("urgency", 0.0)
                h.setdefault("status", "resolved" if resolved else "active")
                hooks[i] = {k: v for k, v in h.items() if not k.startswith("_")}
        rhooks = data.get("plot", {}).get("resolved_hooks", [])
        for i, h in enumerate(rhooks):
            if "hook_id" not in h:
                resolved = h.pop("resolved", False)
                h.setdefault("hook_id", str(uuid.uuid4())[:8])
                h.setdefault("hook_type", h.pop("type", "普通"))
                h.setdefault("planted_at", h.pop("chapter", 0))
                h.setdefault("planned_reveal_low", 0)
                h.setdefault("planned_reveal_high", 0)
                h.setdefault("clues", [])
                h.setdefault("related_chars", [])
                h.setdefault("urgency", 0.0)
                h.setdefault("status", "resolved" if resolved else "active")
                rhooks[i] = {k: v for k, v in h.items() if not k.startswith("_")}

    def save_snapshot(self):
        """保存写前快照，供 rollback_state() 使用。"""
        import copy
        self.__state_snapshot = copy.deepcopy(self.__state)

    def rollback_state(self):
        """回滚状态到上一次 save_snapshot() 时的快照。"""
        import copy
        self.__state = copy.deepcopy(self.__state_snapshot)
        self._pipeline_state = PipelineState.IDLE


    # === 兑现台账 (Payoff Ledger) 参考 AI-Novel-Writing-Assistant ===
    def record_promise(self, text: str, chapter_planted: int, payoff_deadline: int = 0):
        """记录一个需要未来兑现的承诺"""
        if "payoff_ledger" not in self.__state:
            self.__state["payoff_ledger"] = []
        entry = {
            "id": len(self.__state["payoff_ledger"]),
            "text": text[:100],
            "planted_at": chapter_planted,
            "deadline": payoff_deadline or chapter_planted + 10,
            "status": "pending",
            "paid_at": 0,
        }
        self.__state["payoff_ledger"].append(entry)
        return entry["id"]

    def fulfill_promise(self, promise_id: int, chapter: int):
        """兑现一个承诺"""
        for p in self.__state.get("payoff_ledger", []):
            if p["id"] == promise_id:
                p["status"] = "fulfilled"
                p["paid_at"] = chapter
                return True
        return False

    def get_pending_promises(self) -> list:
        """获取所有未兑现的承诺"""
        return [p for p in self.__state.get("payoff_ledger", []) if p["status"] == "pending"]

    def get_overdue_promises(self, current_chapter: int) -> list:
        """获取已逾期未兑现的承诺（超过deadline）"""
        return [p for p in self.__state.get("payoff_ledger", [])
                if p["status"] == "pending" and p["deadline"] < current_chapter]

    def check_promise_health(self, current_chapter: int) -> list:
        """检查承诺健康度"""
        overdue = self.get_overdue_promises(current_chapter)
        issues = []
        for p in overdue:
            issues.append(f"[承诺] '{p['text']}' 逾期{current_chapter - p['deadline']}章未兑现")
        return issues

    def save(self):
        # Phase 1 fix: 写前快照
        self.save_snapshot()
        # Phase 1 #4: 线程锁 + 文件系统互斥锁 + 写入重试退避
        with _save_thread_lock:
            _lock_acquired = _acquire_lock_file(self._lock_dir)
            if not _lock_acquired:
                _log.warning(f"save() 无法获取文件锁 (超时{_LOCK_TIMEOUT}s)，强制覆盖")
            try:
                self.__state["version"] = self.__state.get("version", "1.0.0")
                self.__state["meta"]["updated"] = datetime.now().isoformat()
                p = self.state_path.parent
                p.mkdir(parents=True, exist_ok=True)
                tmp = self.state_path.with_suffix(".json.tmp")

                # 写入 retry（原子 tmp → replace）
                _last_err = None
                for attempt in range(_SAVE_RETRY):
                    try:
                        with open(tmp, "w", encoding="utf-8") as f:
                            json.dump(self.__state, f, ensure_ascii=False, indent=2)
                        tmp.replace(self.state_path)
                        _last_err = None
                        break
                    except (OSError, PermissionError) as _e:
                        _last_err = _e
                        if attempt < _SAVE_RETRY - 1:
                            delay = _SAVE_RETRY_DELAY * (2 ** attempt)
                            time.sleep(delay)
                            continue
                        _log.error(f"save() 写入失败 (重试{_SAVE_RETRY}次): {_e}")
                if _last_err:
                    raise _last_err

                # Volume snapshot（在锁内，确保一致性）
                vol_dir = p / "state"
                vol_dir.mkdir(parents=True, exist_ok=True)
                # 兼容 written 为 list 或 int（统一后为 int）
                _raw_written = self.__state.get("progress", {}).get("written", 0)
                if isinstance(_raw_written, list):
                    _written_count = max(_raw_written) if _raw_written else 0
                else:
                    _written_count = int(_raw_written) if _raw_written else 0
                vol = max(1, _written_count // 10 + 1)
                tmp_vol = vol_dir / f"state-vol-{vol:04d}.json.tmp"
                tmp_vol.write_text(json.dumps(self.__state, ensure_ascii=False, indent=2), encoding="utf-8")
                tmp_vol.replace(vol_dir / f"state-vol-{vol:04d}.json")
                self._cleanup_snapshots(vol_dir)
                if _written_count > 0 and _written_count % 100 == 0:
                    self.archive_old(_written_count)
            finally:
                if _lock_acquired:
                    _release_lock_file(self._lock_dir)

    MAX_SNAPSHOTS = 50

    def _cleanup_snapshots(self, vol_dir):
        if not vol_dir.exists():
            return
        snapshots = sorted(
            [f for f in vol_dir.iterdir() if f.suffix == ".json" and f.stem.startswith("state-vol-")],
            key=lambda x: x.name
        )
        if len(snapshots) <= self.MAX_SNAPSHOTS:
            return
        keep = set(snapshots[-self.MAX_SNAPSHOTS:])
        for i, snap in enumerate(snapshots[:-self.MAX_SNAPSHOTS]):
            if i % 50 == 0:
                keep.add(snap)
        removed = 0
        for snap in snapshots:
            if snap not in keep:
                snap.unlink(missing_ok=True)
                removed += 1
        if removed > 0:
            print(f"  [INFO] NovelState: cleanup {removed} old snapshots (keep {len(keep)})")

    def get_character(self, name):
        return self.__state["characters"].get(name, {})

    def set_character(self, name, data):
        self.__state["characters"][name] = data

    def update_character(self, name, **kw):
        self.__state["characters"].setdefault(name, {}).update(kw)

    def all_characters(self):
        return dict(self.__state["characters"])

    def add_hook(self, hook=None, ch=None, ht="general", dist="short", imp=3,
                 hook_obj=None, hook_type=None, clues=None, related_chars=None):
        if hook_obj is not None and isinstance(hook_obj, StoryHook):
            self.__state["plot"]["hooks"].append(hook_obj.to_dict())
            return
        if isinstance(hook, StoryHook):
            self.__state["plot"]["hooks"].append(hook.to_dict())
            return
        if hook is None:
            return
        new_hook_type = hook_type or ht
        planted = ch if ch is not None else (self.__state["progress"]["last_chapter"] + 1)
        story_hook = StoryHook(
            text=str(hook),
            hook_type=new_hook_type or "普通",
            planted_at=planted,
            clues=clues or [],
            related_chars=related_chars or [],
            importance=imp,
            recovery_distance=dist,
        )
        self.__state["plot"]["hooks"].append(story_hook.to_dict())

    def resolve_hook(self, ht):
        for h in self.__state["plot"]["hooks"]:
            matched = (h.get("hook_id") == ht) or (h.get("text") == ht)
            if matched and h.get("status", "active") not in ("resolved", "abandoned"):
                h["status"] = "resolved"
                h["urgency"] = 1.0
                self.__state["plot"]["resolved_hooks"].append(h)
                return True
        return False

    def unresolved_hooks(self):
        result = []
        for h in self.__state["plot"]["hooks"]:
            status = h.get("status", "active")
            if status in ("active", "aging", "critical"):
                result.append(StoryHook.from_dict(h))
        return result

    def _compute_urgency(self, hook_dict, current_chapter):
        planted = hook_dict.get("planted_at", 0)
        low = hook_dict.get("planned_reveal_low", 0)
        high = hook_dict.get("planned_reveal_high", 0)
        if low <= 0 and high <= 0:
            low = planted + 3
            high = planted + 10
        if current_chapter <= low:
            return round((current_chapter - planted) / max(1, low - planted) * 0.3, 3)
        elif current_chapter <= high:
            progress = (current_chapter - low) / max(1, high - low)
            return round(0.3 + progress * 0.4, 3)
        else:
            overdue = current_chapter - high
            return round(min(1.0, 0.7 + overdue * 0.06), 3)

    def _auto_update_hook_status(self, hook_dict, current_chapter):
        urgency = self._compute_urgency(hook_dict, current_chapter)
        hook_dict["urgency"] = urgency
        current_status = hook_dict.get("status", "active")
        if current_status in ("resolved", "abandoned"):
            return
        if urgency >= 0.85:
            new_status = "critical"
        elif urgency >= 0.5:
            new_status = "aging"
        else:
            new_status = "active"
        if new_status != current_status:
            _log.info("  \u4f0f\u7b14 #%s \u72b6\u6001\u66f4\u65b0: %s \u2192 %s (u=%.2f)" % (hook_dict.get("hook_id"), current_status, new_status, urgency))
        hook_dict["status"] = new_status

    def mark_chapter_done(self, ch):
        if not self._pipeline_state.can_transition_to(PipelineState.SUCCESS):
            if self._pipeline_state == PipelineState.IDLE:
                self._pipeline_state = PipelineState.RUNNING
            else:
                _log.warning(f"mark_chapter_done: invalid transition from {self._pipeline_state}")
        self._pipeline_state = PipelineState.SUCCESS
        t = self.__state["progress"]
        if ch <= t.get("last_chapter", 0):
            _log.warning(f"mark_chapter_done: idempotent skip ch{ch} (last={t.get('last_chapter', 0)})")
            return False
        # v1.0 unified: written 统一为 int（已完成章节数）
        t["written"] = ch
        t["last_chapter"] = ch
        # 同时维护 written_list 用于幂等检查
        wl = t.setdefault("written_list", [])
        if ch not in wl:
            wl.append(ch)
        for hook_dict in self.__state["plot"]["hooks"]:
            if hook_dict.get("status", "active") not in ("resolved", "abandoned"):
                self._auto_update_hook_status(hook_dict, ch)
        return True

    # ==== Encapsulation accessors (replace direct _state access) ====

    @property
    def meta(self):
        return self.__state.setdefault('meta', {})

    @property
    def progress(self):
        return self.__state.setdefault('progress', {})

    @property
    def hooks_list(self):
        return self.__state.setdefault('plot', {}).setdefault('hooks', [])

    @property
    def characters(self):
        return self.__state.setdefault('characters', {})

    @property
    def settings_list(self):
        return self.__state.setdefault('settings', [])

    @property
    def timeline_events(self):
        return self.__state.setdefault('timeline', [])

    @property
    def foreshadows(self):
        return self.__state.setdefault('foreshadows', {})

    @property
    def global_memory(self):
        return self.__state.setdefault('global_memory', {})

    @property
    def character_states(self):
        return self.__state.setdefault('character_states', {})

    @property
    def plot_arcs(self):
        return self.__state.setdefault('plot', {}).setdefault('arcs', [])

    def set_meta_field(self, key, value):
        self.__state.setdefault('meta', {})[key] = value

    def set_progress_field(self, key, value):
        self.__state.setdefault('progress', {})[key] = value

    def set_foreshadows(self, data):
        self.__state['foreshadows'] = data

    def set_character_states(self, data):
        self.__state['character_states'] = data

    def set_global_memory(self, data):
        self.__state['global_memory'] = data

    def written_chapters(self):
        w = self.__state.get('progress', {}).get('written', 0)
        if isinstance(w, list):
            return max(w) if w else 0
        return int(w) if w else 0

    def total_planned(self):
        return self.__state.get('progress', {}).get('total_planned', 0)

    def last_chapter(self):
        return self.__state.get('progress', {}).get('last_chapter', 0)


    def next_chapter(self):
        return self.__state["progress"]["last_chapter"] + 1

    def add_timeline_event(self, ch, ev):
        self.__state["timeline"].append({"chapter": ch, "event": ev})

    def update_readers(self, **kw):
        self.__state["readers"].update(kw)

    def add_warning(self, w):
        if w not in self.__state["readers"][_WARN]:
            self.__state["readers"][_WARN].append(w)

    def llm_context(self, mc=3000):
        s = self.__state
        lines = []
        l = lambda x: lines.append(x)
        l(f"{_PLAT}: {s['meta']['platform']} {_PROG}: {s['meta']['genre']}")
        l(f"{_PROG}: {s['progress']['written']}/{s['progress']['total_planned']}")
        l("")
        l(f"[{_CHAR}]")
        for n, i in s["characters"].items():
            l(f"  {n}: {i.get('state', '?')} @ {i.get('location', '?')}")
        l("")
        a = [st for st in s.get("settings", []) if st.get("status") == "active"]
        if a:
            l(f"[{_SET}]")
            for st in a[:3]:
                l(f"  {st['name']}: {st['content'][:50]}")
            l("")
        hks = self.unresolved_hooks()
        if hks:
            l(f"[{_HOOK}]")
            for h in hks[:5]:
                urg = "!"
                if h.urgency >= 0.85:
                    urg = "\u26a0\ufe0f"
                elif h.urgency >= 0.5:
                    urg = "\u26a1"
                l(f"  [{h.hook_type}] #{h.hook_id} {urg} ch{h.planted_at}: {h.text[:40]} (u={h.urgency:.2f})")
            l("")
        tl = s.get("timeline", [])
        if tl:
            l(f"[{_TIME}]")
            for e in tl[-10:]:
                l(f"  {e['chapter']}: {e['event'][:60]}")
            l("")
        txt = "\n".join(lines)
        return txt[:mc] + "\n..." if len(txt) > mc else txt

    VOLUME_SIZE = 100
    MAX_ARCHIVE_AGE = 10

    def _vol_path(self, vol):
        return self.book_dir / _TRACK / "state" / f"state-vol-{vol:04d}.json"

    def archive_old(self, cc):
        if cc < self.VOLUME_SIZE * (self.MAX_ARCHIVE_AGE + 1):
            return 0
        ad = self.book_dir / _TRACK / "state" / "archived"
        ad.mkdir(parents=True, exist_ok=True)
        a = 0
        oldest_keep = max(1, (cc // self.VOLUME_SIZE) - self.MAX_ARCHIVE_AGE)
        for v in range(1, oldest_keep):
            p = self._vol_path(v)
            if not p.exists():
                continue
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            sm = {
                "vol": v,
                "chapter_range": [(v - 1) * self.VOLUME_SIZE + 1, v * self.VOLUME_SIZE],
                "characters": d.get("characters", {}),
                "character_count": len(d.get("characters", {})),
                "timeline": d.get("timeline", []),
                "events_count": len(d.get("timeline", [])),
                "unresolved_hooks": [
                    h for h in d.get("plot", {}).get("hooks", [])
                    if h.get("status", "active") not in ("resolved", "abandoned")
                    and not h.get("resolved", False)
                ],
                "progress": d.get("progress", {}),
                "last_chapter": d.get("progress", {}).get("last_chapter", 0),
            }
            tmp = ad / (f"vol-{v:04d}.summary.json" + ".tmp")
            tmp.write_text(json.dumps(sm, ensure_ascii=False), encoding="utf-8")
            json.loads(tmp.read_text(encoding="utf-8"))
            dst = ad / f"vol-{v:04d}.summary.json"
            tmp.replace(dst)
            p.unlink(missing_ok=True)
            a += 1
        return a
