"""
decision_engine.py — Multi-factor decision engine.

Combines strategy signals, news sentiment, risk conditions, and volatility
into a single final decision with a confidence score. No trade fires without
passing through here.

Decision outputs:
  BUY | SELL | HOLD | REDUCE_RISK | NO_TRADE

Confidence: 0.0 – 1.0
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from loguru import logger

from strategy_engine import Signal

ROOT = Path(__file__).parent.parent
STRATEGIES_PATH = ROOT / "memory" / "strategies.json"


# ── Data Models ────────────────────────────────────────────────────────────────

@dataclass
class Decision:
    action: str                     # BUY | SELL | HOLD | REDUCE_RISK | NO_TRADE
    symbol: str
    confidence: float               # 0.0 – 1.0
    signal: Optional[Signal]        # Original technical signal (None if NO_TRADE)
    technical_score: float
    news_score: float
    risk_score: float
    volatility_score: float
    reason: str
    position_size_modifier: float = 1.0   # Multiplier on base position size
    stop_modifier: float = 1.0            # Multiplier on ATR stop distance


# ── Default Weights ────────────────────────────────────────────────────────────

DEFAULT_WEIGHTS = {
    "technical": 0.50,
    "news":      0.25,
    "risk":      0.15,
    "volatility": 0.10,
}


# ── DecisionEngine ─────────────────────────────────────────────────────────────

class DecisionEngine:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.weights = self._load_weights()
        self.risk_cfg = cfg.get("risk", {})
        self.news_cfg = cfg.get("news", {})
        logger.info(f"DecisionEngine initialized with weights: {self.weights}")

    def _load_weights(self) -> dict:
        """Load learned weights from strategies.json if available."""
        try:
            with open(STRATEGIES_PATH) as f:
                data = json.load(f)
            version = data["versions"][-1]
            return version.get("decision_weights", DEFAULT_WEIGHTS)
        except Exception:
            return DEFAULT_WEIGHTS.copy()

    # ── Core Decision Logic ────────────────────────────────────────────────────

    def decide(
        self,
        signal: Signal,
        market_sentiment: dict,
        symbol_sentiment: float,
        volatility_regime: str,     # "low" | "normal" | "high" | "extreme"
        portfolio_state: dict,      # {"positions": int, "daily_pnl_pct": float}
    ) -> Decision:
        """
        Combine all factors into a final Decision.

        Decision formula:
            final_confidence = Σ(factor_score × weight)

        Factors:
            technical_score  — signal confidence from strategy_engine (0–1)
            news_score       — normalized news sentiment for symbol (-1 to +1 → 0 to 1)
            risk_score       — inverse of current portfolio risk exposure (0–1)
            volatility_score — penalty for high volatility environments (0–1)
        """
        # ── 1. Technical score ─────────────────────────────────────────────────
        technical_score = signal.confidence  # Already 0–1

        # ── 2. News score ──────────────────────────────────────────────────────
        # Convert sentiment (-1 to +1) to directional alignment (0 to 1)
        agg_score = market_sentiment.get("aggregate_score", 0.0)
        combined_news = (symbol_sentiment * 0.6) + (agg_score * 0.4)

        if signal.direction == "LONG":
            news_score = (combined_news + 1) / 2          # Map -1→0.0, 0→0.5, +1→1.0
        else:  # SHORT
            news_score = (-combined_news + 1) / 2         # Inverted: negative news helps shorts

        news_score = max(0.0, min(1.0, news_score))

        # ── 3. Risk score ──────────────────────────────────────────────────────
        max_pos = self.risk_cfg.get("max_positions", 5)
        current_pos = portfolio_state.get("positions", 0)
        daily_pnl_pct = portfolio_state.get("daily_pnl_pct", 0.0)

        # Penalize as we approach position limit and daily loss limit
        pos_utilization = current_pos / max_pos
        loss_utilization = max(0, -daily_pnl_pct) / self.risk_cfg.get("max_daily_loss_pct", 3.0)
        risk_score = max(0.0, 1.0 - (pos_utilization * 0.5) - (loss_utilization * 0.5))

        # ── 4. Volatility score ────────────────────────────────────────────────
        vol_map = {"low": 1.0, "normal": 0.85, "high": 0.60, "extreme": 0.20}
        volatility_score = vol_map.get(volatility_regime, 0.85)

        # ── 5. Weighted composite ──────────────────────────────────────────────
        w = self.weights
        final_confidence = (
            technical_score  * w["technical"]  +
            news_score       * w["news"]        +
            risk_score       * w["risk"]        +
            volatility_score * w["volatility"]
        )
        final_confidence = round(max(0.0, min(1.0, final_confidence)), 4)

        # ── 6. Risk event override ─────────────────────────────────────────────
        risk_event = market_sentiment.get("risk_event", False)
        high_impact = market_sentiment.get("high_impact", False)

        position_size_modifier = 1.0
        stop_modifier = 1.0
        action = signal.direction  # "LONG" → "BUY", "SHORT" → "SELL"
        action = "BUY" if signal.direction == "LONG" else "SELL"

        if risk_event:
            logger.warning(f"⚠️ Risk event detected — defensive mode for {signal.symbol}")
            return Decision(
                action="REDUCE_RISK",
                symbol=signal.symbol,
                confidence=final_confidence,
                signal=None,
                technical_score=technical_score,
                news_score=news_score,
                risk_score=risk_score,
                volatility_score=volatility_score,
                reason="Risk event detected in news — no new entries",
                position_size_modifier=0.0,
                stop_modifier=0.8,
            )

        if high_impact:
            position_size_modifier *= 0.6
            stop_modifier *= 0.85
            logger.info(f"High-impact news: reducing size to 60%, tightening stops for {signal.symbol}")

        # ── 7. Conflict check: strong tech signal vs opposing news ────────────
        news_opposes_signal = (
            (signal.direction == "LONG" and combined_news < -0.4) or
            (signal.direction == "SHORT" and combined_news > 0.4)
        )
        if news_opposes_signal and technical_score < 0.8:
            logger.info(
                f"News conflicts with technical signal for {signal.symbol} "
                f"(news={combined_news:.2f}, tech={technical_score:.2f}) — skipping"
            )
            return Decision(
                action="NO_TRADE",
                symbol=signal.symbol,
                confidence=final_confidence,
                signal=None,
                technical_score=technical_score,
                news_score=news_score,
                risk_score=risk_score,
                volatility_score=volatility_score,
                reason=f"News sentiment conflicts with {signal.direction} signal",
            )

        # ── 8. Confidence threshold ────────────────────────────────────────────
        min_confidence = self.news_cfg.get("min_combined_confidence", 0.45)
        if final_confidence < min_confidence:
            return Decision(
                action="NO_TRADE",
                symbol=signal.symbol,
                confidence=final_confidence,
                signal=signal,
                technical_score=technical_score,
                news_score=news_score,
                risk_score=risk_score,
                volatility_score=volatility_score,
                reason=f"Combined confidence {final_confidence:.2f} below threshold {min_confidence}",
            )

        # ── 9. Size and stop modifiers based on confidence ─────────────────────
        if final_confidence >= 0.75:
            position_size_modifier = min(position_size_modifier * 1.2, 1.5)  # Up to 150%
        elif final_confidence < 0.55:
            position_size_modifier *= 0.75

        reason_parts = [
            f"tech={technical_score:.2f}",
            f"news={news_score:.2f}",
            f"risk={risk_score:.2f}",
            f"vol={volatility_score:.2f}",
            f"→ conf={final_confidence:.2f}",
        ]

        logger.info(
            f"Decision [{action}] {signal.symbol} | "
            + " | ".join(reason_parts)
            + f" | size_mod={position_size_modifier:.2f}"
        )

        return Decision(
            action=action,
            symbol=signal.symbol,
            confidence=final_confidence,
            signal=signal,
            technical_score=technical_score,
            news_score=news_score,
            risk_score=risk_score,
            volatility_score=volatility_score,
            reason=" | ".join(reason_parts),
            position_size_modifier=round(position_size_modifier, 2),
            stop_modifier=round(stop_modifier, 2),
        )

    # ── Volatility Helper ──────────────────────────────────────────────────────

    @staticmethod
    def classify_volatility(atr: float, price: float) -> str:
        """Classify volatility regime by ATR/price ratio."""
        atr_pct = (atr / price) * 100 if price > 0 else 0
        if atr_pct < 0.5:
            return "low"
        elif atr_pct < 1.5:
            return "normal"
        elif atr_pct < 3.0:
            return "high"
        else:
            return "extreme"

    # ── Weight Learning ────────────────────────────────────────────────────────

    def update_weights(self, new_weights: dict) -> None:
        """
        Update factor weights (called by performance tracker after sufficient data).
        Total weights must sum to 1.0.
        """
        total = sum(new_weights.values())
        if abs(total - 1.0) > 0.01:
            logger.warning(f"Weight sum {total:.3f} ≠ 1.0 — normalizing")
            new_weights = {k: v / total for k, v in new_weights.items()}

        self.weights = new_weights
        logger.info(f"Decision weights updated: {self.weights}")

        # Persist to strategies.json
        try:
            with open(STRATEGIES_PATH) as f:
                data = json.load(f)
            data["versions"][-1]["decision_weights"] = self.weights
            with open(STRATEGIES_PATH, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to persist weights: {e}")
