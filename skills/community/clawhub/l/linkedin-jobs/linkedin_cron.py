"""
LinkedIn Job Cron Runner for OpenClaw
Runs saved search profiles, deduplicates jobs, and returns only new unique listings.

Usage:
    python linkedin_cron.py run                    # Run all enabled profiles
    python linkedin_cron.py run --profile ai-noida # Run specific profile
    python linkedin_cron.py add --keywords "AI Engineer" --location "Noida, India"
    python linkedin_cron.py list                   # List all profiles
    python linkedin_cron.py disable --profile ai-noida
    python linkedin_cron.py enable --profile ai-noida
    python linkedin_cron.py remove --profile ai-noida
    python linkedin_cron.py clear-history          # Clear seen jobs
    python linkedin_cron.py stats                  # Show statistics
"""

import json
import sys
import os
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import asdict

# Import the scraper from the same directory
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from linkedin_scraper import LinkedInScraper, JobListing, load_config, CONFIG


# ─────────────────────────────────────────────
#  File Paths
# ─────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent
PROFILES_FILE = SKILL_DIR / "search_profiles.json"
SEEN_JOBS_FILE = SKILL_DIR / "seen_jobs.json"


# ─────────────────────────────────────────────
#  Profile Management
# ─────────────────────────────────────────────


def get_defaults() -> dict:
    """Get default filter values from config."""
    return CONFIG.get(
        "defaults",
        {
            "experience": "2",
            "remote": "1,3",
            "date_posted": "r86400",
            "max_pages": 2,
            "job_type": "",
        },
    )


def load_profiles() -> dict:
    """Load search profiles from JSON file."""
    defaults = get_defaults()

    if not PROFILES_FILE.exists():
        return {"profiles": [], "defaults": defaults}

    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update defaults from config if not present in file
    if "defaults" not in data:
        data["defaults"] = defaults
    else:
        # Merge config defaults with saved defaults
        for key, value in defaults.items():
            if key not in data["defaults"]:
                data["defaults"][key] = value

    return data


def save_profiles(data: dict):
    """Save search profiles to JSON file."""
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_profile_id(keywords: str, location: str) -> str:
    """Generate a unique profile ID from keywords and location."""
    # Clean and combine
    clean_kw = re.sub(r"[^a-z0-9]+", "-", keywords.lower()).strip("-")
    clean_loc = (
        re.sub(r"[^a-z0-9]+", "-", location.lower()).strip("-")
        if location
        else "worldwide"
    )
    return f"{clean_kw}-{clean_loc}"[:50]


def add_profile(
    keywords: str,
    location: str = "",
    experience: str = "",
    remote: str = "",
    job_type: str = "",
    date_posted: str = "",
    max_pages: int = None,
) -> dict:
    """Add a new search profile. Supports comma-separated keywords for multiple profiles."""

    # Check if keywords contain commas (multiple job titles)
    if "," in keywords:
        return add_multiple_profiles(
            keywords=keywords,
            location=location,
            experience=experience,
            remote=remote,
            job_type=job_type,
            date_posted=date_posted,
            max_pages=max_pages,
        )

    data = load_profiles()
    defaults = data.get("defaults", get_defaults())

    profile_id = generate_profile_id(keywords, location)

    # Check if profile already exists
    for p in data["profiles"]:
        if p["id"] == profile_id:
            return {
                "success": False,
                "error": f"Profile '{profile_id}' already exists",
                "profile_id": profile_id,
            }

    profile = {
        "id": profile_id,
        "keywords": keywords,
        "location": location,
        "experience": experience or defaults.get("experience", "2"),
        "remote": remote or defaults.get("remote", "1,3"),
        "job_type": job_type or defaults.get("job_type", ""),
        "date_posted": date_posted or defaults.get("date_posted", "r86400"),
        "max_pages": max_pages
        if max_pages is not None
        else defaults.get("max_pages", 2),
        "enabled": True,
        "created_at": datetime.utcnow().isoformat(),
        "last_run": None,
        "total_jobs_found": 0,
    }

    data["profiles"].append(profile)
    save_profiles(data)

    return {
        "success": True,
        "message": f"Added profile '{profile_id}'",
        "profile": profile,
    }


def add_multiple_profiles(
    keywords: str,
    location: str = "",
    experience: str = "",
    remote: str = "",
    job_type: str = "",
    date_posted: str = "",
    max_pages: int = None,
) -> dict:
    """Add multiple search profiles from comma-separated keywords."""

    # Parse comma-separated keywords
    keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]

    if not keyword_list:
        return {
            "success": False,
            "error": "No valid keywords provided",
            "profiles_added": [],
        }

    data = load_profiles()
    defaults = data.get("defaults", get_defaults())

    added_profiles = []
    skipped_profiles = []

    for kw in keyword_list:
        profile_id = generate_profile_id(kw, location)

        # Check if profile already exists
        exists = any(p["id"] == profile_id for p in data["profiles"])
        if exists:
            skipped_profiles.append(
                {"keywords": kw, "profile_id": profile_id, "reason": "already exists"}
            )
            continue

        profile = {
            "id": profile_id,
            "keywords": kw,
            "location": location,
            "experience": experience or defaults.get("experience", "2"),
            "remote": remote or defaults.get("remote", "1,3"),
            "job_type": job_type or defaults.get("job_type", ""),
            "date_posted": date_posted or defaults.get("date_posted", "r86400"),
            "max_pages": max_pages
            if max_pages is not None
            else defaults.get("max_pages", 2),
            "enabled": True,
            "created_at": datetime.utcnow().isoformat(),
            "last_run": None,
            "total_jobs_found": 0,
        }

        data["profiles"].append(profile)
        added_profiles.append(profile)

    # Save all profiles at once
    if added_profiles:
        save_profiles(data)

    return {
        "success": True,
        "message": f"Added {len(added_profiles)} profile(s), skipped {len(skipped_profiles)}",
        "profiles_added": added_profiles,
        "profiles_skipped": skipped_profiles,
        "total_added": len(added_profiles),
        "total_skipped": len(skipped_profiles),
    }


def remove_profile(profile_id: str) -> dict:
    """Remove a search profile."""
    data = load_profiles()
    original_count = len(data["profiles"])
    data["profiles"] = [p for p in data["profiles"] if p["id"] != profile_id]

    if len(data["profiles"]) == original_count:
        return {"success": False, "error": f"Profile '{profile_id}' not found"}

    save_profiles(data)
    return {"success": True, "message": f"Removed profile '{profile_id}'"}


def enable_profile(profile_id: str, enabled: bool = True) -> dict:
    """Enable or disable a search profile."""
    data = load_profiles()

    for p in data["profiles"]:
        if p["id"] == profile_id:
            p["enabled"] = enabled
            save_profiles(data)
            status = "enabled" if enabled else "disabled"
            return {"success": True, "message": f"Profile '{profile_id}' {status}"}

    return {"success": False, "error": f"Profile '{profile_id}' not found"}


def update_profile(profile_id: str, **kwargs) -> dict:
    """Update an existing search profile."""
    data = load_profiles()

    for p in data["profiles"]:
        if p["id"] == profile_id:
            for key, value in kwargs.items():
                if value is not None and key in p:
                    p[key] = value
            save_profiles(data)
            return {
                "success": True,
                "message": f"Updated profile '{profile_id}'",
                "profile": p,
            }

    return {"success": False, "error": f"Profile '{profile_id}' not found"}


def list_profiles() -> dict:
    """List all search profiles."""
    data = load_profiles()
    return {
        "success": True,
        "total": len(data["profiles"]),
        "enabled": len([p for p in data["profiles"] if p.get("enabled", True)]),
        "profiles": data["profiles"],
        "defaults": data.get("defaults", get_defaults()),
    }


# ─────────────────────────────────────────────
#  Seen Jobs Management
# ─────────────────────────────────────────────


def load_seen_jobs() -> dict:
    """Load seen job IDs from JSON file."""
    if not SEEN_JOBS_FILE.exists():
        return {"job_ids": [], "last_updated": None, "total_seen": 0}
    with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_seen_jobs(data: dict):
    """Save seen job IDs to JSON file."""
    data["last_updated"] = datetime.utcnow().isoformat()
    data["total_seen"] = len(data.get("job_ids", []))
    with open(SEEN_JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def mark_jobs_seen(job_ids: list[str]):
    """Add job IDs to the seen list."""
    data = load_seen_jobs()
    existing = set(data.get("job_ids", []))
    existing.update(job_ids)
    data["job_ids"] = list(existing)
    save_seen_jobs(data)


def filter_new_jobs(jobs: list[dict]) -> list[dict]:
    """Filter out jobs that have already been seen."""
    seen_data = load_seen_jobs()
    seen_ids = set(seen_data.get("job_ids", []))
    return [j for j in jobs if j.get("job_id") not in seen_ids]


def clear_seen_jobs() -> dict:
    """Clear all seen job history."""
    data = {
        "job_ids": [],
        "last_updated": datetime.utcnow().isoformat(),
        "total_seen": 0,
    }
    save_seen_jobs(data)
    return {"success": True, "message": "Cleared all seen job history"}


def get_stats() -> dict:
    """Get statistics about profiles and seen jobs."""
    profiles_data = load_profiles()
    seen_data = load_seen_jobs()

    return {
        "success": True,
        "profiles": {
            "total": len(profiles_data["profiles"]),
            "enabled": len(
                [p for p in profiles_data["profiles"] if p.get("enabled", True)]
            ),
        },
        "seen_jobs": {
            "total": len(seen_data.get("job_ids", [])),
            "last_updated": seen_data.get("last_updated"),
        },
        "config": {
            "defaults": profiles_data.get("defaults", get_defaults()),
        },
    }


# ─────────────────────────────────────────────
#  Run Profiles
# ─────────────────────────────────────────────


def run_profiles(profile_id: Optional[str] = None, mark_seen: bool = True) -> dict:
    """Run search profiles and return only new jobs."""
    data = load_profiles()
    notifications_config = CONFIG.get("notifications", {})

    # Filter profiles
    if profile_id:
        profiles = [p for p in data["profiles"] if p["id"] == profile_id]
        if not profiles:
            return {
                "success": False,
                "error": f"Profile '{profile_id}' not found",
                "new_jobs": [],
                "total_new": 0,
            }
    else:
        profiles = [p for p in data["profiles"] if p.get("enabled", True)]

    if not profiles:
        if notifications_config.get("notify_on_empty", False):
            return {
                "success": True,
                "message": "No enabled profiles to run",
                "new_jobs": [],
                "total_new": 0,
            }
        return {
            "success": True,
            "message": "No enabled profiles to run",
            "new_jobs": [],
            "total_new": 0,
        }

    all_jobs = []
    profile_results = []

    scraper_config = CONFIG.get("scraper", {})
    scraper = LinkedInScraper(
        delay_min=scraper_config.get("delay_min", 1.5),
        delay_max=scraper_config.get("delay_max", 3.5),
        fetch_details=scraper_config.get("fetch_details", True),
    )

    for profile in profiles:
        print(f"[Cron] Running profile: {profile['id']}", file=sys.stderr)

        try:
            jobs = scraper.search_jobs(
                keywords=profile["keywords"],
                location=profile.get("location", ""),
                date_posted=profile.get("date_posted", "r86400"),
                experience=profile.get("experience", ""),
                job_type=profile.get("job_type", ""),
                remote=profile.get("remote", ""),
                max_pages=profile.get("max_pages", 2),
            )

            jobs_dict = [asdict(j) for j in jobs]

            # Add profile info to each job
            for j in jobs_dict:
                j["search_profile"] = profile["id"]
                j["search_keywords"] = profile["keywords"]
                j["search_location"] = profile.get("location", "Worldwide")

            all_jobs.extend(jobs_dict)

            # Update profile stats
            profile["last_run"] = datetime.utcnow().isoformat()
            profile["total_jobs_found"] = profile.get("total_jobs_found", 0) + len(jobs)

            profile_results.append(
                {
                    "profile_id": profile["id"],
                    "jobs_found": len(jobs),
                    "status": "success",
                }
            )

        except Exception as e:
            print(f"[Cron] Error running profile {profile['id']}: {e}", file=sys.stderr)
            profile_results.append(
                {
                    "profile_id": profile["id"],
                    "jobs_found": 0,
                    "status": "error",
                    "error": str(e),
                }
            )

    # Save updated profile stats
    save_profiles(data)

    # Deduplicate by job_id (in case same job appears in multiple profiles)
    seen_in_batch = set()
    unique_jobs = []
    for job in all_jobs:
        if job["job_id"] not in seen_in_batch:
            seen_in_batch.add(job["job_id"])
            unique_jobs.append(job)

    # Filter out previously seen jobs
    new_jobs = filter_new_jobs(unique_jobs)

    # Mark new jobs as seen
    if mark_seen and new_jobs:
        new_ids = [j["job_id"] for j in new_jobs]
        mark_jobs_seen(new_ids)

    # Group new jobs by search location for better display
    jobs_by_location = {}
    if notifications_config.get("group_by_location", True):
        for job in new_jobs:
            loc = job.get("search_location", "Unknown")
            if loc not in jobs_by_location:
                jobs_by_location[loc] = []
            jobs_by_location[loc].append(job)

    # Limit jobs per notification if configured
    max_jobs = notifications_config.get("max_jobs_per_notification", 20)
    truncated = len(new_jobs) > max_jobs
    display_jobs = new_jobs[:max_jobs] if truncated else new_jobs

    return {
        "success": True,
        "profiles_run": len(profiles),
        "profile_results": profile_results,
        "total_scraped": len(all_jobs),
        "total_unique": len(unique_jobs),
        "total_new": len(new_jobs),
        "truncated": truncated,
        "showing": len(display_jobs),
        "new_jobs": display_jobs,
        "jobs_by_location": jobs_by_location,
    }


# ─────────────────────────────────────────────
#  CLI Interface
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Job Cron Runner for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_cron.py add --keywords "AI Engineer" --location "Bengaluru"
  python linkedin_cron.py add --keywords "Python Developer" --location "San Francisco" --remote "2,3"
  python linkedin_cron.py list
  python linkedin_cron.py run
  python linkedin_cron.py run --profile ai-engineer-bengaluru

Configuration:
  Copy config.example.json to config.json to customize defaults, scraper settings,
  and notification preferences.
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Run search profiles")
    run_parser.add_argument("--profile", "-p", help="Run specific profile only")
    run_parser.add_argument(
        "--no-mark-seen", action="store_true", help="Don't mark jobs as seen"
    )

    # add command
    defaults = get_defaults()
    add_parser = subparsers.add_parser("add", help="Add a new search profile")
    add_parser.add_argument(
        "--keywords", "-k", required=True, help="Job search keywords"
    )
    add_parser.add_argument("--location", "-l", default="", help="Location")
    add_parser.add_argument(
        "--experience",
        "-e",
        default="",
        help=f"Experience levels (default: {defaults.get('experience', '2')})",
    )
    add_parser.add_argument(
        "--remote",
        "-r",
        default="",
        help=f"Remote options (default: {defaults.get('remote', '1,3')})",
    )
    add_parser.add_argument("--job-type", "-j", default="", help="Job types")
    add_parser.add_argument(
        "--date-posted",
        "-d",
        default="",
        help=f"Date posted filter (default: {defaults.get('date_posted', 'r86400')})",
    )
    add_parser.add_argument(
        "--max-pages",
        "-m",
        type=int,
        default=None,
        help=f"Max pages (default: {defaults.get('max_pages', 2)})",
    )

    # list command
    subparsers.add_parser("list", help="List all search profiles")

    # enable command
    enable_parser = subparsers.add_parser("enable", help="Enable a search profile")
    enable_parser.add_argument("--profile", "-p", required=True, help="Profile ID")

    # disable command
    disable_parser = subparsers.add_parser("disable", help="Disable a search profile")
    disable_parser.add_argument("--profile", "-p", required=True, help="Profile ID")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a search profile")
    remove_parser.add_argument("--profile", "-p", required=True, help="Profile ID")

    # update command
    update_parser = subparsers.add_parser("update", help="Update a search profile")
    update_parser.add_argument("--profile", "-p", required=True, help="Profile ID")
    update_parser.add_argument("--keywords", "-k", help="New keywords")
    update_parser.add_argument("--location", "-l", help="New location")
    update_parser.add_argument("--experience", "-e", help="New experience levels")
    update_parser.add_argument("--remote", "-r", help="New remote options")
    update_parser.add_argument("--max-pages", "-m", type=int, help="New max pages")

    # clear-history command
    subparsers.add_parser("clear-history", help="Clear seen job history")

    # stats command
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    result = {}

    if args.command == "run":
        result = run_profiles(
            profile_id=args.profile,
            mark_seen=not args.no_mark_seen,
        )
    elif args.command == "add":
        result = add_profile(
            keywords=args.keywords,
            location=args.location,
            experience=args.experience,
            remote=args.remote,
            job_type=args.job_type,
            date_posted=args.date_posted,
            max_pages=args.max_pages,
        )
    elif args.command == "list":
        result = list_profiles()
    elif args.command == "enable":
        result = enable_profile(args.profile, enabled=True)
    elif args.command == "disable":
        result = enable_profile(args.profile, enabled=False)
    elif args.command == "remove":
        result = remove_profile(args.profile)
    elif args.command == "update":
        result = update_profile(
            args.profile,
            keywords=args.keywords,
            location=args.location,
            experience=args.experience,
            remote=args.remote,
            max_pages=args.max_pages,
        )
    elif args.command == "clear-history":
        result = clear_seen_jobs()
    elif args.command == "stats":
        result = get_stats()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
