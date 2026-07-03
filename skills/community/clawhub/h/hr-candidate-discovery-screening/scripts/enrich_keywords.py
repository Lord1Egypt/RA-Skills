from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import load_settings
from db import Database, utc_now
from deepseek_client import DeepSeekClient


PROMPT_VERSION = "keywords-v1"


def enrich_missing_keywords(database: Database, client: DeepSeekClient) -> int:
    rows = database.fetch_all(
        """
        SELECT id, title, abstract, original_keywords_json, generated_keywords_json
        FROM papers
        ORDER BY publication_date, id
        """
    )
    enriched = 0
    for row in rows:
        original = json.loads(row["original_keywords_json"])
        generated = json.loads(row["generated_keywords_json"])
        if original or generated:
            continue
        result = client.generate_keywords(
            {"title": row["title"], "abstract": row["abstract"] or ""}
        )
        database.execute(
            """
            UPDATE papers
            SET generated_keywords_json = ?,
                keyword_model = ?,
                keyword_prompt_version = ?,
                keywords_generated_at = ?
            WHERE id = ?
            """,
            (
                json.dumps(result.keywords, ensure_ascii=False),
                result.model,
                PROMPT_VERSION,
                utc_now(),
                row["id"],
            ),
        )
        enriched += 1
    return enriched


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate missing paper keywords.")
    parser.add_argument(
        "--settings-config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "settings.yaml"),
    )
    args = parser.parse_args()
    settings = load_settings(args.settings_config)
    database = Database(settings.database_path)
    database.initialize()
    count = enrich_missing_keywords(database, DeepSeekClient(settings))
    print(json.dumps({"enriched": count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
