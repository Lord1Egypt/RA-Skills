from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import ConfigError, load_jobs, load_settings
from db import Database, utc_now
from deepseek_client import DeepSeekClient
from models import PaperMatchResult


PROMPT_VERSION = "paper-job-v1"


@dataclass(frozen=True)
class StoredMatch:
    match_id: str
    paper_id: str
    job_snapshot_id: str
    classification: str


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _job_snapshot(database: Database, job: dict[str, Any]) -> str:
    config_json = _canonical_json(job)
    config_hash = hashlib.sha256(config_json.encode("utf-8")).hexdigest()
    now = utc_now()
    database.execute(
        """
        INSERT INTO jobs (id, title, active, config_json, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            active = excluded.active,
            config_json = excluded.config_json,
            updated_at = excluded.updated_at
        """,
        (job["id"], job["title"], int(job.get("active", False)), config_json, now),
    )
    existing = database.fetch_one(
        """
        SELECT id FROM job_snapshots
        WHERE job_id = ? AND config_hash = ?
        ORDER BY created_at DESC LIMIT 1
        """,
        (job["id"], config_hash),
    )
    if existing:
        return str(existing["id"])
    snapshot_id = str(uuid.uuid4())
    database.execute(
        """
        INSERT INTO job_snapshots (id, job_id, config_json, config_hash, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (snapshot_id, job["id"], config_json, config_hash, now),
    )
    return snapshot_id


def _result_json(result: PaperMatchResult) -> str:
    return _canonical_json(
        {
            "classification": result.classification.value,
            "evidence": result.evidence,
            "matched_requirements": result.matched_requirements,
            "missing_requirements": result.missing_requirements,
            "uncertainties": result.uncertainties,
            "summary": result.summary,
            "usage": result.usage,
        }
    )


def match_pending_papers(
    database: Database,
    jobs: list[dict[str, Any]],
    client: DeepSeekClient,
) -> list[StoredMatch]:
    active_jobs = [job for job in jobs if job.get("active", False)]
    if not active_jobs:
        raise ConfigError("At least one complete active job is required for matching")
    papers = database.fetch_all(
        """
        SELECT id, title, abstract, original_keywords_json, generated_keywords_json
        FROM papers ORDER BY publication_date, id
        """
    )
    stored: list[StoredMatch] = []
    for job in active_jobs:
        snapshot_id = _job_snapshot(database, job)
        for paper in papers:
            existing = database.fetch_one(
                """
                SELECT id FROM paper_job_matches
                WHERE paper_id = ? AND job_snapshot_id = ?
                """,
                (paper["id"], snapshot_id),
            )
            if existing:
                continue
            original = json.loads(paper["original_keywords_json"])
            generated = json.loads(paper["generated_keywords_json"])
            result = client.match_paper(
                {
                    "paper": {
                        "title": paper["title"],
                        "abstract": paper["abstract"] or "",
                        "original_keywords": original,
                        "generated_keywords": generated,
                    },
                    "job": job,
                }
            )
            match_id = str(uuid.uuid4())
            database.execute(
                """
                INSERT INTO paper_job_matches (
                    id, paper_id, job_snapshot_id, classification, result_json,
                    model, prompt_version, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    match_id,
                    paper["id"],
                    snapshot_id,
                    result.classification.value,
                    _result_json(result),
                    result.model,
                    PROMPT_VERSION,
                    utc_now(),
                ),
            )
            stored.append(
                StoredMatch(
                    match_id=match_id,
                    paper_id=str(paper["id"]),
                    job_snapshot_id=snapshot_id,
                    classification=result.classification.value,
                )
            )
    return stored


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Match papers to active jobs.")
    parser.add_argument(
        "--settings-config", default=str(root / "config" / "settings.yaml")
    )
    parser.add_argument("--jobs-config", default=str(root / "config" / "jobs.yaml"))
    args = parser.parse_args()
    settings = load_settings(args.settings_config)
    database = Database(settings.database_path)
    database.initialize()
    matches = match_pending_papers(
        database, load_jobs(args.jobs_config), DeepSeekClient(settings)
    )
    print(
        json.dumps(
            {
                "matches": len(matches),
                "classifications": [item.classification for item in matches],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
