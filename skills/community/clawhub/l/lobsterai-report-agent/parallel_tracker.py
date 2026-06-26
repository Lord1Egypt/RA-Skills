"""
parallel_tracker.py
===================
多子Agent并行撰写可视化追踪模块

工作原理：
1. 主Agent使用 sessions_spawn 并行启动多个子Agent
2. 每个子Agent启动后向 TRACKER_FILE 写入自己的状态
3. 主Agent周期性地读取 TRACKER_FILE 并渲染可视化表格

使用方式：
  from parallel_tracker import Tracker, update_chapter_status

  # 子Agent端：启动时注册
  tracker = Tracker()
  tracker.register(seq="04", title="系统架构设计", batch="B")
  tracker.update(seq="04", phase="writing", progress=50, note="撰写功能模块...")

  # 子Agent端：完成后标记
  tracker.update(seq="04", phase="done", progress=100)
"""

import json, os, time, sys, threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ============ 路径配置（与 integrate_report.py 共用同一配置源）============

def _get_chapters_dir():
    env_val = os.environ.get('LOBAI_CHAPTERS_DIR')
    if env_val:
        return env_val
    return os.path.join(os.path.expanduser("~"), ".config", "lobsterai-report-agent", "chapters")

def _get_tracker_file():
    return os.path.join(_get_chapters_dir(), 'writing_tracker.json')

# 惰性属性（支持 from parallel_tracker import CHAPTERS_DIR 写法）
_tracker_cache = None

def _load_tracker_paths():
    global _tracker_cache
    if _tracker_cache is None:
        cd = _get_chapters_dir()
        _tracker_cache = {
            'CHAPTERS_DIR': cd,
            'TRACKER_FILE': os.path.join(cd, 'writing_tracker.json'),
        }
    return _tracker_cache

def __getattr__(name):
    _paths = _load_tracker_paths()
    if name in _paths:
        return _paths[name]
    raise AttributeError(f"module has no attribute '{name}'")

# ============ 追踪器 ============

_GLOBAL_TRACKER: Optional['Tracker'] = None
_GLOBAL_LOCK = threading.Lock()


class Tracker:
    """多子Agent并行撰写状态追踪器（线程安全单例）"""

    def __init__(self, tracker_file: str = None):
        if tracker_file is None:
            tracker_file = _get_tracker_file()
        self.tracker_file = tracker_file
        self._ensure_file()

    @staticmethod
    def get_instance(tracker_file: str = None) -> 'Tracker':
        """获取单例实例（线程安全）"""
        global _GLOBAL_TRACKER
        if _GLOBAL_TRACKER is None:
            with _GLOBAL_LOCK:
                if _GLOBAL_TRACKER is None:
                    _GLOBAL_TRACKER = Tracker(tracker_file)
        return _GLOBAL_TRACKER

    def _ensure_file(self):
        if not os.path.exists(self.tracker_file):
            self._write({})

    def _read(self) -> Dict[str, Any]:
        with _GLOBAL_LOCK:
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}

    def _write(self, data: Dict[str, Any]):
        with _GLOBAL_LOCK:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def register(self, seq: str, title: str, batch: str = "", agent_id: str = ""):
        """子Agent启动时注册"""
        data = self._read()
        data[seq] = {
            "seq": seq,
            "title": title,
            "batch": batch,
            "agent_id": agent_id,
            "phase": "registered",  # registered | outline | writing | reviewing | done | error
            "progress": 0,
            "note": "已注册，等待启动...",
            "started_at": datetime.now().strftime('%H:%M:%S'),
            "updated_at": datetime.now().strftime('%H:%M:%S'),
        }
        self._write(data)
        return self

    def update(self, seq: str, phase: str, progress: int = None,
                note: str = "", error: str = ""):
        """
        更新子Agent撰写状态
        phase: registered | outline | writing | reviewing | done | error
        progress: 0-100
        """
        data = self._read()
        if seq not in data:
            # 未注册，自动注册
            data[seq] = {"seq": seq, "title": seq, "batch": ""}
        entry = data[seq]
        entry["phase"] = phase
        if progress is not None:
            entry["progress"] = progress
        if note:
            entry["note"] = note
        if error:
            entry["error"] = error
        entry["updated_at"] = datetime.now().strftime('%H:%M:%S')
        self._write(data)
        return self

    def mark_done(self, seq: str, note: str = "已完成"):
        return self.update(seq, phase="done", progress=100, note=note)

    def mark_error(self, seq: str, error: str):
        return self.update(seq, phase="error", note="出错", error=error)

    def get_status(self) -> Dict[str, Any]:
        return self._read()

    def clear(self):
        """清空追踪状态（每批次开始前调用）"""
        self._write({})

    def get_summary(self) -> Dict[str, int]:
        data = self._read()
        phases = {}
        for entry in data.values():
            p = entry.get("phase", "unknown")
            phases[p] = phases.get(p, 0) + 1
        return phases


# ============ 可视化渲染 ============

TRACKER_FILE_FOR_PRINT = _get_tracker_file()  # 模块级引用（惰性）


def _progress_bar(progress: int, width: int = 12) -> str:
    """渲染进度条：▓░░░░░░░░░░"""
    filled = int(width * progress / 100)
    return '▓' * filled + '░' * (width - filled)


def _phase_emoji(phase: str) -> str:
    emoji_map = {
        "registered": "⏳",
        "outline": "📋",
        "writing": "✍️",
        "reviewing": "🔍",
        "done": "✅",
        "error": "❌",
    }
    return emoji_map.get(phase, "⚪")


def render_progress_table(tracker_file: str = None) -> str:
    if tracker_file is None:
        tracker_file = _get_tracker_file()
    """
    渲染当前并行撰写状态表格

    返回格式：
    ╔══════════════════════════════════════════════════════════════╗
    ║  📊 多子Agent并行撰写进度监控                                ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  04 系统架构设计   ✍️  writing  ▓▓▓▓▓▓░░░░  50%  撰写功能模块... ║
    ║  05 技术路线       ✍️  writing  ▓▓▓░░░░░░░  25%  撰写技术选型... ║
    ║  06 功能模块设计   ⏳  registered  ─────────  0%   等待启动...   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    try:
        with open(tracker_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return "（追踪文件暂不可用）"

    if not data:
        return "（暂无并行撰写任务）"

    # 按 seq 排序
    sorted_entries = sorted(data.values(), key=lambda x: x.get('seq', '0'))

    # 计算全局进度
    total = len(sorted_entries)
    done = sum(1 for e in sorted_entries if e.get('phase') == 'done')
    errors = sum(1 for e in sorted_entries if e.get('phase') == 'error')
    overall_pct = int((done / total * 100)) if total > 0 else 0

    header = (
        f"╔══════════════════════════════════════════════════════════════╗\n"
        f"║  📊 多子Agent并行撰写进度监控  [{done}/{total} 完成"
        f"{' ❌' + str(errors) if errors > 0 else ''}]  总体 {overall_pct}%        ║\n"
        f"╠══════════════════════════════════════════════════════════════╣"
    )
    footer = "╚══════════════════════════════════════════════════════════════╝"

    rows = []
    for entry in sorted_entries:
        seq = entry.get('seq', '??').rjust(2)
        title = entry.get('title', '')[:14].ljust(14)
        phase_icon = _phase_emoji(entry.get('phase', ''))
        phase_name = entry.get('phase', '').rjust(10)
        progress = entry.get('progress', 0)
        bar = _progress_bar(progress)
        pct = str(progress).rjust(3) + '%'
        note = (entry.get('note', '') or '').strip()[:20].ljust(20)
        batch = entry.get('batch', '')
        batch_str = f"[{batch}] " if batch else "        "
        row = f"║  {seq} {batch_str}{title} {phase_icon} {phase_name} {bar} {pct}  {note} ║"
        rows.append(row)

    return '\n'.join([header] + rows + [footer])


def print_progress(tracker_file: str = None):
    """打印进度表格到标准输出（供 exec 调用）"""
    if tracker_file is None:
        tracker_file = _get_tracker_file()
    print(render_progress_table(tracker_file), flush=True)


# ============ 轮询监控器 ============

class ProgressMonitor:
    """
    定期轮询 tracker 文件并打印进度的监控器
    用于在子Agent并行撰写时，主session展示实时进度
    """

    def __init__(self, tracker_file: str = None, interval_sec: float = 8.0):
        if tracker_file is None:
            tracker_file = _get_tracker_file()
        self.tracker_file = tracker_file
        self.interval_sec = interval_sec
        self._running = False

    def start(self, duration_sec: float = None):
        """
        启动监控循环
        duration_sec: 监控持续秒数，None表示直到所有任务完成
        """
        self._running = True
        import time
        start = time.time()
        last_seen_done = set()

        print(f"[MONITOR] 启动进度监控（间隔{self.interval_sec}秒）", flush=True)

        while self._running:
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                entries = list(data.values())
                if not entries:
                    time.sleep(self.interval_sec)
                    continue

                # 检查是否全部完成
                done_seqs = {e['seq'] for e in entries if e.get('phase') == 'done'}
                error_seqs = {e['seq'] for e in entries if e.get('phase') == 'error'}

                # 打印进度
                os.system('cls' if os.name == 'nt' else 'clear')
                print(render_progress_table(self.tracker_file), flush=True)

                # 新完成任务时提示
                new_done = done_seqs - last_seen_done
                if new_done:
                    print(f"\n✅ 新完成：第 {[e['seq'] for e in entries if e['seq'] in new_done]} 章", flush=True)
                last_seen_done = done_seqs

                # 检查是否全部结束
                all_done = len(done_seqs) + len(error_seqs) == len(entries)
                if all_done:
                    print(f"\n[MONITOR] 所有章节撰写完成！", flush=True)
                    break

                # 检查超时
                if duration_sec and (time.time() - start) >= duration_sec:
                    print(f"\n[MONITOR] 监控超时（{duration_sec}秒）", flush=True)
                    break

                time.sleep(self.interval_sec)

            except Exception as e:
                print(f"[MONITOR] 轮询异常: {e}", flush=True)
                time.sleep(self.interval_sec)

    def stop(self):
        self._running = False


# ============ 子Agent端辅助函数 ============

def get_tracker() -> Tracker:
    """获取Tracker单例（子Agent端推荐使用）"""
    return Tracker.get_instance()


def chapter_register(seq: str, title: str, batch: str = ""):
    """子Agent启动时调用：注册章节撰写任务"""
    Tracker().register(seq=seq, title=title, batch=batch)


def chapter_update(seq: str, phase: str, progress: int = None, note: str = ""):
    """子Agent撰写过程中调用：更新进度"""
    Tracker().update(seq=seq, phase=phase, progress=progress, note=note)


def chapter_done(seq: str, note: str = "已完成"):
    """子Agent完成时调用：标记完成"""
    Tracker().mark_done(seq=seq, note=note)


def chapter_error(seq: str, error: str):
    """子Agent出错时调用：标记错误"""
    Tracker().mark_error(seq=seq, error=error)


# ============ CLI 入口 ============

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        tracker = Tracker()

        if cmd == 'show' or len(sys.argv) == 2:
            print(render_progress_table())

        elif cmd == 'clear':
            tracker.clear()
            print("追踪状态已清空")

        elif cmd == 'status':
            summary = tracker.get_summary()
            print(f"当前状态: {summary}")
            total = sum(summary.values())
            done = summary.get('done', 0)
            print(f"进度: {done}/{total} 完成")

        elif cmd == 'wait':
            # 阻塞监控模式
            import time
            print("开始监控... Ctrl+C 停止")
            try:
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(render_progress_table())
                    time.sleep(8)
            except KeyboardInterrupt:
                print("\n监控已停止")

        elif cmd == 'register' and len(sys.argv) >= 4:
            _, _, seq, title, *rest = sys.argv
            batch = rest[0] if rest else ""
            tracker.register(seq, title, batch)
            print(f"已注册：第{seq}章 {title} [{batch}]")

        elif cmd == 'update' and len(sys.argv) >= 4:
            _, _, seq, phase, *rest = sys.argv
            progress = int(restr[0]) if rest and rest[0].isdigit() else None
            note = rest[1] if len(restr := rest) > 1 else ""
            tracker.update(seq, phase, progress, note)
            print(f"已更新：第{seq}章 {phase} {progress or ''}% {note}")

        elif cmd == 'done' and len(sys.argv) >= 3:
            seq = sys.argv[2]
            tracker.mark_done(seq)
            print(f"已标记完成：第{seq}章")

    else:
        print(render_progress_table())
