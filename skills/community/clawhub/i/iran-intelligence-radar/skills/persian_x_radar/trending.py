from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Dict, List


def _project_logs_dir() -> Path:
    path = Path(__file__).resolve().parents[2] / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_logger() -> logging.Logger:
    logger = logging.getLogger("persian_x_radar.trending")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(_project_logs_dir() / "trending.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


class TrendingDetector:
    def __init__(
        self,
        keywords: List[str],
        spike_threshold: float = 3.0,
        min_volume: int = 3,
        max_history_points: int = 120,
    ) -> None:
        self.keywords = keywords
        self.spike_threshold = spike_threshold
        self.min_volume = min_volume
        self.max_history_points = max_history_points
        self.state_file = Path(__file__).resolve().with_name("trending_history.json")
        self.logger = _get_logger()

    def _load_state(self) -> Dict[str, List[int]]:
        if not self.state_file.exists():
            return {}
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            state: Dict[str, List[int]] = {}
            for keyword, values in raw.items():
                if isinstance(values, list):
                    state[str(keyword)] = [int(v) for v in values]
            return state
        except (json.JSONDecodeError, OSError, ValueError):
            return {}

    def _save_state(self, state: Dict[str, List[int]]) -> None:
        with self.state_file.open("w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _count_keywords(self, texts: List[str]) -> Dict[str, int]:
        counts = {k: 0 for k in self.keywords}
        for text in texts:
            for keyword in self.keywords:
                if keyword in text:
                    counts[keyword] += 1
        return counts

    def detect(self, texts: List[str]) -> List[Dict[str, float]]:
        state = self._load_state()
        current_counts = self._count_keywords(texts)
        signals: List[Dict[str, float]] = []

        for keyword, current_count in current_counts.items():
            history = state.get(keyword, [])
            avg = (sum(history) / len(history)) if history else 0.0
            baseline = avg if avg > 0 else 1.0
            trend_score = float(current_count) / baseline

            if current_count >= self.min_volume and trend_score > self.spike_threshold:
                signals.append(
                    {
                        "keyword": keyword,
                        "current_volume": current_count,
                        "average_volume": round(avg, 2),
                        "trend_score": round(trend_score, 2),
                    }
                )

            new_history = (history + [current_count])[-self.max_history_points :]
            state[keyword] = new_history

        self._save_state(state)
        self.logger.info(
            "trending scan complete signals=%s timestamp=%s",
            len(signals),
            datetime.now(timezone.utc).isoformat(),
        )

        return sorted(signals, key=lambda s: s["trend_score"], reverse=True)
