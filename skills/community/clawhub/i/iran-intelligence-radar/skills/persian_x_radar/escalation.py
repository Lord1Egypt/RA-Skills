from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List


def _project_logs_dir() -> Path:
    path = Path(__file__).resolve().parents[2] / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_logger() -> logging.Logger:
    logger = logging.getLogger("persian_x_radar.escalation")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(_project_logs_dir() / "escalation.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def _contains_any(text: str, needles: List[str]) -> bool:
    return any(n in text for n in needles)


def classify_escalation_level(score: int) -> str:
    if score <= 30:
        return "LOW"
    if score <= 60:
        return "MEDIUM"
    if score <= 80:
        return "HIGH"
    return "CRITICAL"


def calculate_escalation_score(rows: List[Dict], monitored_accounts: List[str]) -> Dict:
    logger = _get_logger()

    missile_keywords = ["موشک", "حمله موشکی", "missile", "rocket"]
    military_keywords = ["پدافند", "نظامی", "سپاه", "air defense", "military"]
    protest_keywords = ["اعتراض", "زن زندگی آزادی", "protest", "strike"]

    total = max(len(rows), 1)
    normalized_accounts = {a.lower().lstrip("@") for a in monitored_accounts}

    missile_hits = 0
    military_hits = 0
    protest_hits = 0
    verified_hits = 0
    total_engagement = 0

    for row in rows:
        combined_text = f"{row.get('persian', '')} {row.get('english', '')}".lower()
        if _contains_any(combined_text, missile_keywords):
            missile_hits += 1
        if _contains_any(combined_text, military_keywords):
            military_hits += 1
        if _contains_any(combined_text, protest_keywords):
            protest_hits += 1

        author = str(row.get("author", "")).lower().lstrip("@")
        if author in normalized_accounts:
            verified_hits += 1

        total_engagement += int(row.get("score", 0))

    avg_engagement = total_engagement / total

    missile_score = min(30.0, (missile_hits / total) * 30.0)
    military_score = min(25.0, (military_hits / total) * 25.0)
    protest_score = min(20.0, (protest_hits / total) * 20.0)
    engagement_score = min(15.0, (avg_engagement / 600.0) * 15.0)
    account_score = min(10.0, (verified_hits / total) * 10.0)

    components = {
        "missile discussion spike": missile_score,
        "military discussion spike": military_score,
        "protest discussion spike": protest_score,
        "engagement spike": engagement_score,
        "verified account activity": account_score,
    }

    final_score = int(round(min(100.0, sum(components.values()))))
    level = classify_escalation_level(final_score)
    top_signal = max(components, key=components.get)

    logger.info(
        "escalation computed score=%s level=%s top_signal=%s rows=%s",
        final_score,
        level,
        top_signal,
        len(rows),
    )

    return {
        "escalation_score": final_score,
        "level": level,
        "top_signal": top_signal,
        "components": {k: round(v, 2) for k, v in components.items()},
    }
