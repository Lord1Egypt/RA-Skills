#!/usr/bin/env python3
"""
karaoke_player.py — 卡拉 OK 播放器
即時逐字卡拉 OK 顯示、速度控制、段落反覆、Music.app 同步
"""

import sys
import json
import re
import argparse
import time
import subprocess
import threading
import readline
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Callable

DATA_DIR = Path.home() / ".karaoke-companion"
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = DATA_DIR / "player_state.json"


# ── Types ────────────────────────────────────────────────────────────────────

@dataclass
class LyricLine:
    time: float
    text: str
    line_num: int = 0


# ── LRC Parser ───────────────────────────────────────────────────────────────

def parse_lrc(raw: str) -> list[LyricLine]:
    lines_out = []
    line_num = 0
    for raw_line in raw.splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        # Remove tags like [ti:Title], [ar:Artist], etc.
        if raw_line.startswith("["):
            tag_match = re.match(r'\[(ti|ar|al|by|offset|re|ve|la):(.+)\]', raw_line)
            if tag_match:
                continue
        matches = re.findall(r'\[(\d{1,2}):(\d{2})[.:](\d{1,3})\]', raw_line)
        text = re.sub(r'\[\d{1,2}:\d{2}[.:]\d{1,3}\]', '', raw_line).strip()
        if not text:
            continue
        line_num += 1
        for m in matches:
            minutes, seconds, centis = m
            t = int(minutes) * 60 + int(seconds) + int(centis.ljust(3, '0')) / 1000
            lines_out.append(LyricLine(time=t, text=text, line_num=line_num))

    lines_out.sort(key=lambda x: x.time)
    return lines_out


def parse_plain(plain: str, interval: float = 3.5) -> list[LyricLine]:
    """純文字自動對時"""
    lines_out = []
    t = 0.0
    for i, text in enumerate(plain.splitlines(), 1):
        text = text.strip()
        if not text:
            continue
        lines_out.append(LyricLine(time=t, text=text, line_num=i))
        t += interval
    return lines_out


# ── Music.app integration ────────────────────────────────────────────────────

def music_get_position() -> float:
    try:
        script = '''tell application "Music"
            if player state is playing then
                return player position as string
            else
                return "0"
            end if
        end tell'''
        out = subprocess.run(["osascript", "-e", script],
                           capture_output=True, text=True, timeout=5)
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def music_is_playing() -> bool:
    try:
        script = 'tell application "Music" to player state as string'
        out = subprocess.run(["osascript", "-e", script],
                           capture_output=True, text=True, timeout=5)
        return "playing" in out.stdout.strip().lower()
    except Exception:
        return False


def music_get_track() -> dict:
    try:
        script = '''tell application "Music"
            set t to current track
            set n to name of t
            set a to artist of t
            set d to duration of t
            return n & "||" & a & "||" & (d as string)
        end tell'''
        out = subprocess.run(["osascript", "-e", script],
                           capture_output=True, text=True, timeout=5)
        parts = out.stdout.strip().split("||")
        if len(parts) >= 3:
            return {"name": parts[0], "artist": parts[1],
                    "duration": float(parts[2])}
    except Exception:
        pass
    return {"name": "未知", "artist": "未知", "duration": 0}


# ── Terminal karaoke display ──────────────────────────────────────────────────

CLEAR = "\033[2J\033[H"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[36m"
GREEN = "\033[32m"
YELLOW= "\033[33m"
RED   = "\033[31m"
RESET = "\033[0m"
SLOW  = "\033[3m"
INVERT= "\033[7m"


def _fmt_time(t: float) -> str:
    m = int(t // 60)
    s = int(t % 60)
    return f"{m:02d}:{s:02d}"


def clear_screen():
    sys.stdout.write(CLEAR + RESET)
    sys.stdout.flush()


def render_karaoke(lines: list[LyricLine], current_idx: int,
                   speed: float, total: float,
                   track: dict, show_prev: bool = True) -> str:
    """渲染 karaoke 畫面"""
    buf = []
    buf.append(CLEAR)
    buf.append(f"{BOLD}{CYAN}🎤 KARAOKE MODE  │  {RESET}"
               f"{BOLD}{track.get('name','?')}{RESET}")
    buf.append(f"{DIM}  👤 {track.get('artist','?')}  │  速度：{speed:.2f}x{RESET}")
    buf.append("─" * 56)

    # Which lines to show
    total_lines = len(lines)
    # current + 2 upcoming + 1 previous
    if total_lines == 0:
        buf.append(f"{YELLOW}  沒有歌詞{RESET}")
        return "\n".join(buf)

    # Show 3 upcoming lines
    start = max(0, current_idx)
    end   = min(total_lines, start + 3)

    # Previous if any
    if show_prev and current_idx > 0:
        prev_line = lines[current_idx - 1]
        buf.append(f"{DIM}  {prev_line.text}{RESET}")
        buf.append("")

    # Current (highlighted)
    if current_idx < total_lines:
        curr = lines[current_idx]
        buf.append(f"{BOLD}{GREEN}  ▶ {curr.text}{RESET}")
        buf.append(f"{DIM}    {_fmt_time(curr.time)}  |  行 {curr.line_num}/{total_lines}{RESET}")
        buf.append("")

    # Next lines
    for i in range(current_idx + 1, end):
        l = lines[i]
        buf.append(f"{DIM}    {l.text}{RESET}")

    # Progress bar
    if total > 0 and current_idx < total_lines:
        elapsed = lines[current_idx].time
        bar_len = 40
        filled = int(bar_len * elapsed / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        buf.append("")
        buf.append(f"  {CYAN}[{bar}]{RESET}  {BOLD}{_fmt_time(elapsed)}{RESET} / {_fmt_time(total)}")
    elif total > 0:
        buf.append(f"\n  {GREEN}{BOLD}✅ 歌詞結束！{RESET}")

    # Controls hint
    buf.append("")
    buf.append(f"{DIM}  🔰 控制：Space 暫停 │ ←/→ 段落 │ +/— 速度 │ r 重來 │ q 退出{RESET}")
    return "\n".join(buf)


def render_idle(lines: list[LyricLine], track: dict) -> str:
    """靜止狀態（未開始播放）"""
    buf = []
    buf.append(CLEAR)
    buf.append(f"{BOLD}{CYAN}🎤 KARAOKE MODE  │  {RESET}"
               f"{BOLD}{track.get('name','?')}{RESET}")
    buf.append(f"{DIM}  👤 {track.get('artist','?')}{RESET}")
    buf.append("─" * 56)
    buf.append("")

    if not lines:
        buf.append(f"  {YELLOW}等待 Music.app 開始播放...{RESET}")
    else:
        buf.append(f"  {GREEN}▶ 播放音樂即可開始卡拉 OK！{RESET}")
        buf.append(f"  {DIM}  共 {len(lines)} 行歌詞{RESET}")
        buf.append("")
        # Show first few lines
        for l in lines[:5]:
            buf.append(f"  {DIM}{l.text}{RESET}")
        if len(lines) > 5:
            buf.append(f"  {DIM}  ...（共 {len(lines)} 行）{RESET}")
    buf.append("")
    buf.append(f"{DIM}  🔰 Space 開始 │ q 退出{RESET}")
    return "\n".join(buf)


# ── Repeat section ────────────────────────────────────────────────────────────

def select_section(lines: list[LyricLine]) -> tuple[int, int]:
    """讓使用者選取要反覆的段落"""
    print(CLEAR)
    print(f"{BOLD}{YELLOW}📍 選擇反覆段落{RESET}")
    print("─" * 56)
    for i, l in enumerate(lines[:20]):
        print(f"  {i+1:2d}. [{_fmt_time(l.time)}] {l.text}")
    if len(lines) > 20:
        print(f"  ...（共 {len(lines)} 行）")
    print()
    try:
        start = int(input("  起始行號 [1]: ").strip() or "1") - 1
        end   = int(input("  結束行號: ").strip() or str(start + 4)) - 1
        start = max(0, min(start, len(lines)-1))
        end   = max(start, min(end, len(lines)-1))
        return start, end
    except (ValueError, KeyboardInterrupt):
        return 0, 0


# ── Player ───────────────────────────────────────────────────────────────────

class KaraokePlayer:
    def __init__(self, lines: list[LyricLine], track: dict,
                 sync_music: bool = False,
                 speed: float = 1.0,
                 start_offset: float = 0.0):
        self.lines        = lines
        self.track        = track
        self.sync_music   = sync_music
        self.speed        = speed
        self.offset       = start_offset  # manual time offset
        self.current_idx   = 0
        self.running       = False
        self.paused       = False
        self.repeat_start = None
        self.repeat_end   = None
        self._thread      = None

    @property
    def total(self) -> float:
        return self.lines[-1].time if self.lines else 0.0

    def current_time(self) -> float:
        if self.sync_music:
            return music_get_position() + self.offset
        return self._manual_time

    def _manual_tick(self):
        """手動模式的時間前進"""
        if not self.paused:
            self._manual_time += 0.1 * self.speed

    def start(self):
        self.running   = True
        self.paused    = False
        self._manual_time = 0.0
        if self.sync_music:
            self._thread = threading.Thread(target=self._music_watcher, daemon=True)
            self._thread.start()
        else:
            self._thread = threading.Thread(target=self._manual_timer, daemon=True)
            self._thread.start()

    def _music_watcher(self):
        while self.running:
            time.sleep(0.1)
            if self.paused:
                continue
            # Auto-sync with music
            pass  # current_time() reads Music.app each call

    def _manual_timer(self):
        while self.running:
            time.sleep(0.1)
            self._manual_tick()

    def pause(self):
        self.paused = not self.paused

    def stop(self):
        self.running = False

    def seek_to(self, idx: int):
        self.current_idx = max(0, min(idx, len(self.lines)-1))
        if not self.sync_music:
            self._manual_time = self.lines[self.current_idx].time

    def next_line(self):
        self.seek_to(self.current_idx + 1)

    def prev_line(self):
        self.seek_to(self.current_idx - 1)

    def set_speed(self, s: float):
        self.speed = max(0.25, min(3.0, s))

    def adjust_offset(self, delta: float):
        self.offset += delta


def run_player(player: KaraokePlayer):
    """主循環"""
    clear_screen()
    player.start()

    def get_key() -> str | None:
        import select
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None

    while player.running:
        t = player.current_time()
        # Find current line
        idx = player.current_idx
        for i, line in enumerate(player.lines):
            if line.time <= t:
                idx = i

        # Update display
        if player.sync_music:
            track = music_get_track()
            player.track.update(track)
        out = render_karaoke(player.lines, idx, player.speed,
                              player.total, player.track)
        print(out)
        player.current_idx = idx

        # Wait a bit (non-blocking)
        time.sleep(0.05)

        # Check if song ended
        if player.sync_music and not music_is_playing():
            # Song ended
            break

    player.stop()
    print(f"\n{GREEN}✅ 卡拉 OK 結束！唱得真好！🎤{RESET}")


def interactive_player(lines: list[LyricLine], track: dict,
                       sync_music: bool = False):
    """互動式播放器"""
    player = KaraokePlayer(lines, track, sync_music=sync_music)
    player.start()
    t = 0.0

    while player.running:
        if not player.paused:
            t = player.current_time()

        # Find current line index
        idx = player.current_idx
        for i, line in enumerate(lines):
            if line.time <= t:
                idx = i

        player.current_idx = idx

        # Render
        out = render_karaoke(lines, idx, player.speed, player.total, track)
        print(out)

        # Check if ended
        if player.sync_music and not music_is_playing():
            break
        if not player.sync_music and t >= player.total and player.total > 0:
            time.sleep(2)
            break

        time.sleep(0.05)


# ── Practice mode ─────────────────────────────────────────────────────────────

def practice_mode(lines: list[LyricLine], track: dict,
                  speed: float = 0.75,
                  start_line: int = 0):
    """練歌模式：減速 + 自動前進"""
    player = KaraokePlayer(lines, track, speed=speed)
    player.seek_to(start_line)
    player.start()
    t = 0.0

    print(CLEAR)
    print(f"{BOLD}{CYAN}🎤 練歌模式  │  速度：{speed}x{RESET}")
    print(f"  👤 {track.get('name','?')} — {track.get('artist','?')}")
    print("─" * 56)
    print()
    print("  跟著唱！唱完一句按 Enter 繼續，q 退出")
    input()
    player.paused = False

    while player.running and player.current_idx < len(lines):
        t = player.current_time()
        idx = player.current_idx
        for i, line in enumerate(lines):
            if line.time <= t:
                idx = i

        player.current_idx = idx
        curr = lines[idx]
        next_l = lines[idx+1]["text"] if idx+1 < len(lines) else "🎉 結束！"

        print(CLEAR)
        print(f"{GREEN}{BOLD}  ▶ {curr.text}{RESET}")
        print(f"{DIM}    下一句：{next_l}{RESET}")
        print(f"{DIM}    行 {idx+1}/{len(lines)}{RESET}")
        print()

        try:
            inp = input(f"{DIM}[Enter]下一句 [r]重來 [q]退出：{RESET} ").strip()
            if inp == "q":
                player.stop()
                break
            elif inp == "r":
                player.seek_to(idx)  # repeat same line
            else:
                player.next_line()
        except (KeyboardInterrupt, EOFError):
            player.stop()
            break

    player.stop()
    print(f"\n{GREEN}🎤 練習完成！太棒了！⭐{RESET}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎤 卡拉 OK 播放器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("play", help="卡拉 OK 播放")
    p.add_argument("lrc_file", type=Path, nargs="?")
    p.add_argument("-t", "--text", help="歌詞文字")
    p.add_argument("-i", "--interval", type=float, default=3.5,
                   help="純文字每行秒數")
    p.add_argument("--speed",  type=float, default=1.0)
    p.add_argument("--sync",   action="store_true",
                   help="與 Music.app 同步（需 Music.app 播放中）")
    p.add_argument("--offset", type=float, default=0.0,
                   help="時間偏移（秒）")

    p = sub.add_parser("practice", help="練歌模式")
    p.add_argument("lrc_file", type=Path, nargs="?")
    p.add_argument("-t", "--text")
    p.add_argument("-i", "--interval", type=float, default=3.5)
    p.add_argument("--speed",  type=float, default=0.75)
    p.add_argument("--start",  type=int, default=0)

    p = sub.add_parser("section", help="選擇反覆段落")
    p.add_argument("lrc_file", type=Path)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    # Load lyrics
    lines = []
    track = {"name": "未知", "artist": "未知", "duration": 0}

    if args.cmd in ("play", "practice"):
        if args.lrc_file and args.lrc_file.exists():
            raw = args.lrc_file.read_text(encoding="utf-8", errors="replace")
            if re.search(r'\[\d{2}:\d{2}', raw):
                lines = parse_lrc(raw)
            else:
                lines = parse_plain(raw, args.interval)
        elif args.text:
            lines = parse_plain(args.text, args.interval)
        else:
            print("❌ 請提供 LRC 檔案或 -t 歌詞文字"); return

        track = music_get_track() if args.sync else track

    elif args.cmd == "section":
        if args.lrc_file and args.lrc_file.exists():
            raw = args.lrc_file.read_text(encoding="utf-8", errors="replace")
            if re.search(r'\[\d{2}:\d{2}', raw):
                lines = parse_lrc(raw)
            else:
                lines = parse_plain(raw)
        start, end = select_section(lines)
        print(f"\n✅ 已選取：行 {start+1}–{end+1}")
        print(f"  「{lines[start].text}」")
        return

    if not lines:
        print("❌ 沒有解析到歌詞"); return

    if args.cmd == "play":
        try:
            interactive_player(lines, track, sync_music=args.sync)
        except KeyboardInterrupt:
            pass

    elif args.cmd == "practice":
        try:
            practice_mode(lines, track, speed=args.speed, start_line=args.start)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
