#!/usr/bin/env python3
"""
JobClaw Archiver

Auto-archives expired jobs in jobs.csv → jobs_archive.csv.

Rules (same as the web app):
  1. expired_30d   — status New/Interested, no action for 30+ days
  2. auto_rejected — status Rejected/Passed for 60+ days
  3. url_dead      — non-LinkedIn URL returns 404/410 or contains dead phrases
     (LinkedIn URLs are skipped — always inconclusive)

Usage:
    python3 archiver.py                  # dry-run (shows what would be archived)
    python3 archiver.py --commit         # actually archive
    python3 archiver.py --restore <url>  # restore a job by URL
    python3 archiver.py --stats          # show archive stats
"""

import argparse
import csv
import os
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
EXPIRE_DAYS_NEW      = 30
EXPIRE_DAYS_REJECTED = 60

DEAD_PHRASES = [
    "no longer accepting", "job has expired", "this job is no longer available",
    "position has been filled", "listing has expired", "job is closed",
    "this listing has been removed", "application closed",
]

ARCHIVE_COLUMNS = [
    "company", "role", "location", "work_mode", "salary",
    "job_url", "date_posted", "date_found", "source",
    "match_score", "ml_direction", "seniority", "interview_type",
    "status", "date_applied", "referral", "recruiter_contact",
    "followup_date", "priority", "notes", "job_category",
    # Archive-specific columns appended here:
    "archived_at", "archived_reason",
]

# ── Path helpers ──────────────────────────────────────────────────────────────

def get_jobclaw_dir() -> Path:
    env_dir = os.environ.get("JOBCLAW_DIR")
    if env_dir and Path(env_dir).exists():
        return Path(env_dir)
    return Path.home() / "Documents" / "JobClaw"


def get_paths():
    data_dir = get_jobclaw_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return {
        "active":  data_dir / "jobs.csv",
        "archive": data_dir / "jobs_archive.csv",
    }


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ensure_archive_csv(path: Path):
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ARCHIVE_COLUMNS)
            writer.writeheader()

# ── URL check ─────────────────────────────────────────────────────────────────

def check_url_alive(url: str) -> bool | None:
    """
    Returns:
        True  — URL alive
        False — URL dead (404/410 or dead phrase in body)
        None  — inconclusive (timeout, network error, LinkedIn)
    """
    if not url or "linkedin.com" in url:
        return None  # can't reliably check LinkedIn

    try:
        # HEAD check for status code
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "8", "--location", url],
            capture_output=True, text=True, timeout=12
        )
        code = int(result.stdout.strip() or "0")
        if code in (404, 410):
            return False
        if 200 <= code < 400:
            # GET to check for dead phrases in body
            body_result = subprocess.run(
                ["curl", "-s", "--max-time", "8", "--location", url],
                capture_output=True, text=True, timeout=12
            )
            body = body_result.stdout.lower()
            if any(p in body for p in DEAD_PHRASES):
                return False
            return True
        return None  # 5xx or other = inconclusive
    except Exception:
        return None


# ── Archive logic ─────────────────────────────────────────────────────────────

def run_archive(commit: bool = False) -> dict:
    paths = get_paths()
    active_jobs = load_csv(paths["active"])
    ensure_archive_csv(paths["archive"])

    today = date.today()
    expire_threshold    = (today - timedelta(days=EXPIRE_DAYS_NEW)).isoformat()
    rejected_threshold  = (today - timedelta(days=EXPIRE_DAYS_REJECTED)).isoformat()
    now_str             = datetime.now().isoformat(timespec="seconds")

    to_archive: list[tuple[dict, str]] = []  # (job, reason)
    keep: list[dict] = []

    for job in active_jobs:
        status     = (job.get("status") or "").strip()
        date_found = (job.get("date_found") or "")[:10]
        job_url    = (job.get("job_url") or "").strip()
        reason     = None

        # Rule 1: New/Interested inactive 30+ days
        if status in ("New", "Interested") and date_found and date_found <= expire_threshold:
            reason = "expired_30d"

        # Rule 2: Rejected/Passed 60+ days
        elif status in ("Rejected", "Passed") and date_found and date_found <= rejected_threshold:
            reason = "auto_rejected"

        # Rule 3: URL check (non-LinkedIn only)
        elif status in ("New", "Interested") and job_url and "linkedin.com" not in job_url:
            alive = check_url_alive(job_url)
            if alive is False:
                reason = "url_dead"

        if reason:
            to_archive.append((job, reason))
        else:
            keep.append(job)

    details = []
    for job, reason in to_archive:
        details.append(f"[{reason}] {job.get('company','')} — {job.get('role','')} (found: {job.get('date_found','')})")

    if commit and to_archive:
        # Load existing archive and append
        existing_archive = load_csv(paths["archive"])
        new_archive_rows = []
        for job, reason in to_archive:
            row = dict(job)
            row["archived_at"]     = now_str
            row["archived_reason"] = reason
            new_archive_rows.append(row)

        # Determine fieldnames for active CSV (preserve original columns)
        active_fieldnames = list(active_jobs[0].keys()) if active_jobs else []

        write_csv(paths["active"], keep, active_fieldnames)
        write_csv(paths["archive"], existing_archive + new_archive_rows, ARCHIVE_COLUMNS)
        print(f"[archiver] Archived {len(to_archive)} jobs → {paths['archive']}")
    else:
        if not commit:
            print(f"[archiver] DRY RUN — would archive {len(to_archive)} jobs (pass --commit to apply)")

    return {
        "archived":   len(to_archive),
        "remaining":  len(keep),
        "details":    details,
    }


def restore_job(url_fragment: str) -> bool:
    """Move a job back from archive to active by URL fragment match."""
    paths = get_paths()
    archive = load_csv(paths["archive"])
    active  = load_csv(paths["active"])

    match = [j for j in archive if url_fragment.lower() in (j.get("job_url") or "").lower()
             or url_fragment.lower() in (j.get("company") or "").lower()
             or url_fragment.lower() in (j.get("role") or "").lower()]

    if not match:
        print(f"[archiver] No archived job found matching: {url_fragment}")
        return False

    if len(match) > 1:
        print(f"[archiver] Multiple matches — be more specific:")
        for j in match:
            print(f"  {j.get('company','')} — {j.get('role','')} ({j.get('job_url','')})")
        return False

    job = match[0]
    # Remove archive-specific columns before restoring
    restored = {k: v for k, v in job.items() if k not in ("archived_at", "archived_reason")}
    active.append(restored)

    remaining_archive = [j for j in archive if j is not job]

    active_fieldnames = list(active[0].keys()) if active else list(restored.keys())
    write_csv(paths["active"], active, active_fieldnames)
    write_csv(paths["archive"], remaining_archive, ARCHIVE_COLUMNS)

    print(f"[archiver] Restored: {job.get('company','')} — {job.get('role','')}")
    return True


def show_stats():
    paths = get_paths()
    active  = load_csv(paths["active"])
    archive = load_csv(paths["archive"])

    by_reason: dict[str, int] = {}
    for j in archive:
        r = j.get("archived_reason") or "unknown"
        by_reason[r] = by_reason.get(r, 0) + 1

    print(f"\n{'='*50}")
    print(f"  JobClaw Archive Stats")
    print(f"{'='*50}")
    print(f"  Active jobs:   {len(active)}")
    print(f"  Archived jobs: {len(archive)}")
    if by_reason:
        print(f"  By reason:")
        for reason, count in sorted(by_reason.items()):
            label = {
                "expired_30d":   "30-day inactivity",
                "auto_rejected": "Auto (rejected/passed)",
                "url_dead":      "Job listing removed",
                "manual":        "Manually archived",
            }.get(reason, reason)
            print(f"    {label:<30} {count}")
    print(f"{'='*50}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JobClaw archiver")
    parser.add_argument("--commit",  action="store_true", help="Actually archive (default is dry-run)")
    parser.add_argument("--restore", metavar="QUERY",     help="Restore job by URL/company/role fragment")
    parser.add_argument("--stats",   action="store_true", help="Show archive statistics")
    args = parser.parse_args()

    if args.stats:
        show_stats()
    elif args.restore:
        restore_job(args.restore)
    else:
        result = run_archive(commit=args.commit)
        print(f"\n{'='*50}")
        print(f"  {'Would archive' if not args.commit else 'Archived'}: {result['archived']} jobs")
        print(f"  Remaining active: {result['remaining']}")
        if result["details"]:
            print(f"\n  Details:")
            for d in result["details"][:20]:
                print(f"    {d}")
            if len(result["details"]) > 20:
                print(f"    ... and {len(result['details']) - 20} more")
        print(f"{'='*50}")
        if not args.commit and result["archived"] > 0:
            print(f"\n  Run with --commit to apply changes.")
