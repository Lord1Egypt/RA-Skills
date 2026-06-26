"""WuXing (五行) - Five Elements statistics with proper hidden stem weights."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import TIANGAN_WUXING, CANGGAN_WEIGHT
from .paipan import SiZhu


@dataclass
class WuxingStats:
    wood: float
    fire: float
    earth: float
    metal: float
    water: float
    dominant: str
    weakest: str


def _largest_remainder_round(values: dict[str, float]) -> dict[str, int]:
    """Round percentages so they sum to exactly 100."""
    total = sum(values.values())
    raw = {k: v / total * 100 for k, v in values.items()}
    floored = {k: int(v) for k, v in raw.items()}
    remainders = {k: raw[k] - floored[k] for k in raw}
    diff = 100 - sum(floored.values())
    for k in sorted(remainders, key=remainders.get, reverse=True)[:diff]:
        floored[k] += 1
    return floored


def calculate_wuxing(sizhu: SiZhu) -> WuxingStats:
    """Calculate five-element distribution."""
    counts = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}

    for pillar in [sizhu.year, sizhu.month, sizhu.day, sizhu.time]:
        counts[TIANGAN_WUXING[pillar.gan]] += 1.0

    for pillar in [sizhu.year, sizhu.month, sizhu.day, sizhu.time]:
        for i, hg in enumerate(pillar.hide_gan):
            w = CANGGAN_WEIGHT[i] if i < len(CANGGAN_WEIGHT) else 0.1
            counts[TIANGAN_WUXING[hg]] += w

    pct = _largest_remainder_round(counts)
    dominant = max(counts, key=counts.get)
    weakest = min(counts, key=counts.get)

    return WuxingStats(
        wood=pct["木"], fire=pct["火"], earth=pct["土"],
        metal=pct["金"], water=pct["水"],
        dominant=dominant, weakest=weakest,
    )
