#!/usr/bin/env python3
import argparse
import os
import pathlib
import subprocess
import sys
import time


def run_applescript(script: str, timeout: int = 15) -> str:
    proc = subprocess.run(
        ["/usr/bin/osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "AppleScript failed")
    return proc.stdout.strip()


def activate_app(app_name: str) -> None:
    subprocess.run(["/usr/bin/open", "-a", app_name], check=True)


def set_large_window(app_name: str) -> None:
    script = f'''
    tell application "System Events"
      tell process "{app_name}"
        set frontmost to true
        tell application "Finder"
          set desktopBounds to bounds of window of desktop
        end tell
        set screenW to item 3 of desktopBounds
        set screenH to item 4 of desktopBounds
        try
          set position of front window to {{60, 60}}
          set size of front window to {{screenW - 120, screenH - 140}}
        end try
      end tell
    end tell
    '''
    run_applescript(script)


def toggle_fullscreen() -> None:
    script = 'tell application "System Events" to keystroke "f" using {command down, control down}'
    run_applescript(script)


def get_window_bounds(app_name: str) -> str:
    script = f'''
    tell application "System Events"
      tell process "{app_name}"
        set frontmost to true
        set winPos to position of front window
        set winSize to size of front window
        set x1 to item 1 of winPos
        set y1 to item 2 of winPos
        set w1 to item 1 of winSize
        set h1 to item 2 of winSize
        return (x1 as text) & "," & (y1 as text) & "," & (w1 as text) & "," & (h1 as text)
      end tell
    end tell
    '''
    return run_applescript(script)


def screenshot_window(bounds: str, output_path: str) -> None:
    subprocess.run(["/usr/sbin/screencapture", "-x", f"-R{bounds}", output_path], check=True)


def screenshot_screen(output_path: str) -> None:
    subprocess.run(["/usr/sbin/screencapture", "-x", output_path], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open a camera app, enlarge or fullscreen it, then save a screenshot."
    )
    parser.add_argument("--app", default="Photo Booth")
    parser.add_argument("--capture", choices=["window", "screen"], default="window")
    parser.add_argument("--layout", choices=["large", "fullscreen", "none"], default="large")
    parser.add_argument("--output", required=True)
    parser.add_argument("--activate-delay", type=float, default=2.0)
    parser.add_argument("--layout-delay", type=float, default=1.0)
    parser.add_argument("--retries", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = pathlib.Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    activate_app(args.app)
    time.sleep(args.activate_delay)

    if args.layout == "large":
        set_large_window(args.app)
        time.sleep(args.layout_delay)
    elif args.layout == "fullscreen":
        toggle_fullscreen()
        time.sleep(args.layout_delay + 1)

    if args.capture == "screen":
        screenshot_screen(str(output_path))
        print(output_path)
        return 0

    last_error = None
    for _ in range(max(args.retries, 1)):
        try:
            bounds = get_window_bounds(args.app)
            screenshot_window(bounds, str(output_path))
            print(output_path)
            return 0
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(0.5)

    print(
        "Failed to capture app window. Check Screen Recording, Accessibility, and Automation permissions.",
        file=sys.stderr,
    )
    if last_error:
        print(str(last_error), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
