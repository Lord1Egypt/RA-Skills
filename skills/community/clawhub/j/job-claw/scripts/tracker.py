#!/usr/bin/env python3
"""
JobClaw Tracker - CSV-based job database management.

Usage:
    from tracker import JobTracker
    t = JobTracker()
    t.add_jobs([{...}])
    jobs = t.load()
    t.print_summary()
"""

import csv
import os
import json
from datetime import date, datetime
from pathlib import Path

# ── Column definitions ─────────────────────────────────────────────────────────
COLUMNS = [
    "company", "role", "location", "work_mode", "salary",
    "job_url", "date_posted", "date_found", "source",
    "match_score", "ml_direction", "seniority", "interview_type",
    "status", "date_applied", "referral", "recruiter_contact",
    "followup_date", "priority", "notes", "job_category",
]

VALID_STATUSES = [
    "New", "Interested", "Applied", "Phone Screen",
    "Technical Interview", "Final Round", "Offer", "Accepted", "Rejected", "Passed"
]

VALID_INTERVIEW_TYPES = [
    "No Leetcode", "Case Study", "Research Talk", "Fair Coding",
    "Standard Coding", "Heavy Leetcode", "Take-Home", "Unknown"
]

VALID_PRIORITIES = ["High", "Medium", "Low"]
VALID_CATEGORIES = ["coding", "noncoding", "unknown"]


def get_config_dir() -> Path:
    """Find the JobClaw config directory (workspace root or ~/Documents/JobClaw)."""
    # Check env var first (set by run_daily.sh)
    env_dir = os.environ.get("JOBCLAW_DIR")
    if env_dir and Path(env_dir).exists():
        return Path(env_dir)
    # Default: ~/Documents/JobClaw
    return Path.home() / "Documents" / "JobClaw"


def load_config() -> dict:
    """Load config.json from JOBCLAW_DIR."""
    config_path = get_config_dir() / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found at {config_path}. Run setup.py first."
        )
    with open(config_path) as f:
        return json.load(f)


class JobTracker:
    """Manages job records in a CSV file with deduplication."""

    def __init__(self, csv_path: str | None = None):
        if csv_path:
            self.csv_path = Path(csv_path)
        else:
            config = load_config()
            data_dir = get_config_dir() / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.csv_path = data_dir / config.get("csv_filename", "jobs.csv")

        self._ensure_csv()

    def _ensure_csv(self):
        """Create CSV with headers if it doesn't exist."""
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=COLUMNS)
                writer.writeheader()
            print(f"[tracker] Created new CSV: {self.csv_path}")

    def load(self) -> list[dict]:
        """Load all jobs from CSV."""
        jobs = []
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(dict(row))
        return jobs

    def _build_seen_sets(self, jobs: list[dict]) -> tuple[set, set]:
        """Build dedup sets from existing jobs."""
        seen_keys = set()
        seen_urls = set()
        for j in jobs:
            company = (j.get("company") or "").strip().lower()
            role = (j.get("role") or "").strip().lower()
            url = (j.get("job_url") or "").strip().lower()
            if company and role:
                seen_keys.add((company, role))
            if url:
                seen_urls.add(url)
        return seen_keys, seen_urls

    def add_jobs(self, new_jobs: list[dict]) -> tuple[int, int]:
        """
        Add new jobs, skipping duplicates.

        Returns:
            (added_count, skipped_count)
        """
        existing = self.load()
        seen_keys, seen_urls = self._build_seen_sets(existing)

        to_add = []
        skipped = 0

        for job in new_jobs:
            company = (job.get("company") or "").strip()
            role = (job.get("role") or "").strip()
            url = (job.get("job_url") or "").strip()

            key = (company.lower(), role.lower())
            is_dup = key in seen_keys or (url and url.lower() in seen_urls)

            if is_dup:
                skipped += 1
                continue

            # Normalize and fill defaults
            normalized = _normalize_job(job)
            to_add.append(normalized)

            seen_keys.add(key)
            if url:
                seen_urls.add(url.lower())

        if to_add:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
                writer.writerows(to_add)

        print(f"[tracker] Added {len(to_add)} jobs, skipped {skipped} duplicates")
        return len(to_add), skipped

    def update_status(self, company: str, role: str, new_status: str) -> bool:
        """Update the status of a specific job."""
        jobs = self.load()
        updated = False
        for j in jobs:
            if (
                j.get("company", "").lower() == company.lower()
                and j.get("role", "").lower() == role.lower()
            ):
                j["status"] = new_status
                updated = True
                break

        if updated:
            self._write_all(jobs)
        return updated

    def _write_all(self, jobs: list[dict]):
        """Overwrite CSV with all jobs."""
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(jobs)

    def stats(self) -> dict:
        """Return summary statistics."""
        jobs = self.load()
        today = date.today().isoformat()

        new_today = sum(
            1 for j in jobs
            if (j.get("date_found") or "")[:10] == today
        )
        by_status = {}
        for j in jobs:
            s = j.get("status", "Unknown")
            by_status[s] = by_status.get(s, 0) + 1

        by_category = {}
        for j in jobs:
            c = j.get("job_category", "unknown")
            by_category[c] = by_category.get(c, 0) + 1

        return {
            "total": len(jobs),
            "new_today": new_today,
            "by_status": by_status,
            "by_category": by_category,
            "csv_path": str(self.csv_path),
        }

    def print_summary(self):
        """Print a human-readable summary."""
        s = self.stats()
        print(f"\n{'='*50}")
        print(f"  JobClaw Tracker — {s['csv_path']}")
        print(f"{'='*50}")
        print(f"  Total jobs:  {s['total']}")
        print(f"  New today:   {s['new_today']}")
        print(f"  By status:")
        for status, count in s["by_status"].items():
            print(f"    {status:<25} {count}")
        print(f"  By category:")
        for cat, count in s["by_category"].items():
            print(f"    {cat:<25} {count}")
        print(f"{'='*50}\n")

    def search(self, query: str = "", status: str = "", min_score: int = 0) -> list[dict]:
        """Simple search/filter over jobs."""
        jobs = self.load()
        results = []
        for j in jobs:
            if status and j.get("status", "").lower() != status.lower():
                continue
            score = int(j.get("match_score") or 0)
            if score < min_score:
                continue
            if query:
                text = f"{j.get('company','')} {j.get('role','')} {j.get('notes','')}".lower()
                if query.lower() not in text:
                    continue
            results.append(j)
        return results

    def top_jobs(self, n: int = 10, category: str = "") -> list[dict]:
        """Return top N jobs by match score."""
        jobs = self.load()
        if category:
            jobs = [j for j in jobs if j.get("job_category", "") == category]
        jobs.sort(key=lambda j: int(j.get("match_score") or 0), reverse=True)
        return jobs[:n]


def _normalize_job(job: dict) -> dict:
    """Fill in defaults and normalize field values."""
    today = date.today().isoformat()
    normalized = {col: "" for col in COLUMNS}
    normalized.update(job)

    # Fill defaults
    if not normalized.get("date_found"):
        normalized["date_found"] = today
    if not normalized.get("status"):
        normalized["status"] = "New"
    if not normalized.get("source"):
        normalized["source"] = "Daily Search"
    if not normalized.get("job_category"):
        normalized["job_category"] = "unknown"

    # Normalize score to int string
    score = normalized.get("match_score", 0)
    try:
        normalized["match_score"] = str(int(score))
    except (ValueError, TypeError):
        normalized["match_score"] = "0"

    # Truncate notes to 500 chars to keep CSV readable
    notes = normalized.get("notes", "")
    if notes and len(notes) > 500:
        normalized["notes"] = notes[:497] + "..."

    return normalized


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        t = JobTracker()
        t.print_summary()
    elif len(sys.argv) > 1 and sys.argv[1] == "top":
        t = JobTracker()
        top = t.top_jobs(10)
        for j in top:
            print(f"[{j['match_score']:>3}] {j['company']:<30} {j['role'][:40]:<40} {j['status']}")
    else:
        print("Usage: tracker.py stats | top")
