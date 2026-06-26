from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List
from urllib import error, request


def _project_logs_dir() -> Path:
    path = Path(__file__).resolve().parents[2] / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_logger() -> logging.Logger:
    logger = logging.getLogger("persian_x_radar.alerts")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(_project_logs_dir() / "alerts.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def _build_message(escalation: Dict, trending: List[Dict], rows: List[Dict]) -> str:
    top_trend = trending[0]["keyword"] if trending else "N/A"
    tweet_count = len(rows)
    top_links = [row.get("link", "") for row in rows[:2] if row.get("link")]
    links_block = "\n".join(top_links) if top_links else "No links available"

    return (
        "IRAN SIGNAL ALERT\n\n"
        f"Escalation Level: {escalation.get('level', 'UNKNOWN')}\n"
        f"Score: {escalation.get('escalation_score', 0)}\n\n"
        f"Trending keyword: {top_trend}\n"
        f"Tweets detected: {tweet_count}\n\n"
        "Summary:\n"
        "Possible missile-related discussion spike detected on Persian X.\n\n"
        "Link examples:\n"
        f"{links_block}"
    )


def send_telegram_alert(escalation: Dict, trending: List[Dict], rows: List[Dict], config: Dict) -> bool:
    logger = _get_logger()
    tg_cfg = config.get("telegram", {})
    if not tg_cfg.get("enabled", False):
        return False
    if int(escalation.get("escalation_score", 0)) < 60:
        return False

    bot_token = str(tg_cfg.get("bot_token", "")).strip()
    chat_id = str(tg_cfg.get("chat_id", "")).strip()
    if not bot_token or not chat_id:
        logger.warning("telegram alert skipped due to missing bot_token/chat_id")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": _build_message(escalation, trending, rows),
        "disable_web_page_preview": True,
    }

    req = request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=10) as resp:
            if 200 <= resp.status < 300:
                logger.info(
                    "telegram alert sent escalation_score=%s level=%s",
                    escalation.get("escalation_score"),
                    escalation.get("level"),
                )
                return True
    except (error.HTTPError, error.URLError, TimeoutError) as exc:
        logger.error("telegram alert failed error=%s", exc)

    return False
