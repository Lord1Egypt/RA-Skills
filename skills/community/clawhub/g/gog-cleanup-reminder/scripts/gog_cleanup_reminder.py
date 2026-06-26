#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_GOG_CONFIG = "config/gog_library.json"
DEFAULT_HIMALAYA_CONFIG = "config/himalaya.toml"
DEFAULT_REMINDERS_LIST = "Gaming"
DEFAULT_DAYS = 30
DEFAULT_ACCOUNT = "personal"


@dataclass
class StaleGame:
    id: Any
    name: str
    last_played_raw: Optional[str]
    last_played_dt: Optional[datetime]
    days_since_played: Optional[int]
    install_path: Optional[str]
    platforms: List[str]
    genres: List[str]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Find installed GOG games not played for N days, email the list, and add Apple Reminders."
    )
    p.add_argument("--gog-config", default=DEFAULT_GOG_CONFIG, help="Path to GOG library JSON")
    p.add_argument("--himalaya-config", default=DEFAULT_HIMALAYA_CONFIG, help="Path to himalaya.toml")
    p.add_argument("--email-account", default=DEFAULT_ACCOUNT, help="Himalaya account name to send from/to")
    p.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Minimum inactive days threshold")
    p.add_argument("--list", dest="reminders_list", default=DEFAULT_REMINDERS_LIST, help="Apple Reminders list name")
    p.add_argument("--dry-run", action="store_true", help="Do not send email or create reminders")
    p.add_argument("--print-json", action="store_true", help="Print result JSON to stdout")
    p.add_argument("--allow-no-play-history", action="store_true", help="Treat installed games with null last_played as stale")
    p.add_argument("--skip-email", action="store_true", help="Skip email sending")
    p.add_argument("--skip-reminders", action="store_true", help="Skip reminders creation")
    p.add_argument("--subject-prefix", default="[GOG Cleanup]", help="Prefix for email subject")
    return p.parse_args()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_iso_like(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    text = value.strip()
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        return datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
    return None


def extract_email_from_himalaya_config(path: Path, account: str) -> str:
    current = None
    target_header = f"[accounts.{account}]"
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current = line
                continue
            if current == target_header and line.startswith("email"):
                _, value = line.split("=", 1)
                return value.strip().strip('"').strip("'")
    raise RuntimeError(f"Could not find email for account '{account}' in {path}")


def collect_stale_games(data: Dict[str, Any], threshold_days: int, allow_no_play_history: bool) -> List[StaleGame]:
    now = datetime.now()
    out: List[StaleGame] = []
    for game in data.get("games", []):
        if not game.get("installed"):
            continue
        last_played_raw = game.get("last_played")
        last_played_dt = parse_iso_like(last_played_raw)
        if last_played_dt is None and not allow_no_play_history:
            continue
        if last_played_dt is None:
            days_since = None
            stale = True
        else:
            delta = now - last_played_dt
            days_since = delta.days
            stale = delta >= timedelta(days=threshold_days)
        if not stale:
            continue
        out.append(
            StaleGame(
                id=game.get("id"),
                name=game.get("name", "Unknown Game"),
                last_played_raw=last_played_raw,
                last_played_dt=last_played_dt,
                days_since_played=days_since,
                install_path=game.get("install_path"),
                platforms=list(game.get("platforms") or []),
                genres=list(game.get("genres") or []),
            )
        )
    out.sort(key=lambda g: (g.days_since_played is None, -(g.days_since_played or -1), g.name.lower()))
    return out


def build_email(stale_games: List[StaleGame], threshold_days: int) -> Tuple[str, str]:
    subject = f"Installed GOG games inactive for {threshold_days}+ days"
    lines = [
        f"Found {len(stale_games)} installed GOG game(s) inactive for at least {threshold_days} days.",
        "",
    ]
    for idx, game in enumerate(stale_games, 1):
        if game.last_played_dt is None:
            last_played = "Never / no play history"
            age = "unknown"
        else:
            last_played = game.last_played_dt.isoformat(sep=' ', timespec='seconds')
            age = f"{game.days_since_played} days"
        lines.extend(
            [
                f"{idx}. {game.name}",
                f"   - Last played: {last_played}",
                f"   - Inactive: {age}",
                f"   - Install path: {game.install_path or 'unknown'}",
                f"   - Platforms: {', '.join(game.platforms) if game.platforms else 'unknown'}",
                f"   - Genres: {', '.join(game.genres) if game.genres else 'unknown'}",
                "   - Action: Consider uninstalling if you are not planning to play soon.",
                "",
            ]
        )
    body = "\n".join(lines).rstrip() + "\n"
    return subject, body


def build_reminder_title(game: StaleGame, threshold_days: int) -> str:
    if game.days_since_played is None:
        inactivity = f"{threshold_days}+d inactive (no play history)"
    else:
        inactivity = f"{game.days_since_played}d inactive"
    return f"Consider uninstalling {game.name} ({inactivity})"


def run_command(cmd: List[str], input_text: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def send_email(himalaya_config: Path, account: str, to_addr: str, subject_prefix: str, subject: str, body: str) -> None:
    final_subject = f"{subject_prefix} {subject}".strip()
    mml = f"From: {to_addr}\nTo: {to_addr}\nSubject: {final_subject}\nContent-Type: text/plain; charset=utf-8\n\n{body}"
    cmd = [
        "himalaya",
        "--config",
        str(himalaya_config),
        "message",
        "send",
        "--account",
        account,
        "--read-from-stdin",
    ]
    result = run_command(cmd, input_text=mml)
    if result.returncode != 0:
        raise RuntimeError(
            "Email send failed via himalaya.\n"
            f"Command: {' '.join(shlex.quote(c) for c in cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def ensure_reminders_list_exists(list_name: str) -> None:
    cmd = ["remindctl", "list", list_name, "--create"]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(
            "Failed to ensure Apple Reminders list exists.\n"
            f"Command: {' '.join(shlex.quote(c) for c in cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def add_reminder(list_name: str, title: str) -> None:
    cmd = ["remindctl", "add", "--title", title, "--list", list_name]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(
            "Failed to add Apple Reminder.\n"
            f"Command: {' '.join(shlex.quote(c) for c in cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def main() -> int:
    args = parse_args()
    gog_config = Path(args.gog_config)
    himalaya_config = Path(args.himalaya_config)

    if not gog_config.exists():
        raise SystemExit(f"GOG config not found: {gog_config}")
    if not args.skip_email and not himalaya_config.exists():
        raise SystemExit(f"Himalaya config not found: {himalaya_config}")

    data = load_json(gog_config)
    stale_games = collect_stale_games(data, args.days, args.allow_no_play_history)
    email_subject, email_body = build_email(stale_games, args.days)

    result_payload = {
        "threshold_days": args.days,
        "total_stale_games": len(stale_games),
        "games": [
            {
                "id": g.id,
                "name": g.name,
                "last_played": g.last_played_raw,
                "days_since_played": g.days_since_played,
                "install_path": g.install_path,
                "platforms": g.platforms,
                "genres": g.genres,
                "reminder_title": build_reminder_title(g, args.days),
            }
            for g in stale_games
        ],
        "email_subject": f"{args.subject_prefix} {email_subject}".strip(),
    }

    if not stale_games:
        print("No installed GOG games exceed the inactivity threshold.")
        if args.print_json:
            print(json.dumps(result_payload, indent=2, ensure_ascii=False))
        return 0

    if args.dry_run:
        print(email_body)
        if args.print_json:
            print(json.dumps(result_payload, indent=2, ensure_ascii=False))
        return 0

    if not args.skip_email:
        to_addr = extract_email_from_himalaya_config(himalaya_config, args.email_account)
        send_email(himalaya_config, args.email_account, to_addr, args.subject_prefix, email_subject, email_body)

    if not args.skip_reminders:
        ensure_reminders_list_exists(args.reminders_list)
        for game in stale_games:
            add_reminder(args.reminders_list, build_reminder_title(game, args.days))

    print(f"Processed {len(stale_games)} stale installed GOG game(s).")
    if args.print_json:
        print(json.dumps(result_payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
