#!/usr/bin/env python3
"""
Prediction Market Arbiter — Cross-platform divergence scanner.

Compares Kalshi and Polymarket prices on identical events.
Detects arbitrage opportunities via price divergences.

Usage:
    python arbiter.py                          # Single run
    python arbiter.py --config config.yaml     # Custom config
    python arbiter.py --dry-run                # Display matches, no alerts
    python arbiter.py --force                  # Force run regardless of interval
"""

import json
import time
import urllib.request
import urllib.parse
import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

try:
    import yaml
except ImportError:
    yaml = None

try:
    from kalshi_python_sync import Configuration as KalshiConfiguration, KalshiClient
except ImportError:
    try:
        from kalshi_python import Configuration as KalshiConfiguration, KalshiClient
    except ImportError:
        KalshiConfiguration = None
        KalshiClient = None


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


# ============================================================================
# Configuration
# ============================================================================

DEFAULT_CONFIG = {
    "kalshi": {
        "enabled": True,
        "api_key_id": None,
        "private_key_file": None,
    },
    "prediction_market_arbiter": {
        "enabled": True,
        "check_interval_minutes": 240,
        "divergence_threshold_pct": 8.0,
        "fuzzy_match_threshold": 0.6,
        "min_volume": 1000,
        "kalshi_max_pages": 5,
        "polymarket_limit": 200,
    }
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file or use defaults."""
    candidate_paths = []
    if config_path:
        candidate_paths.append(Path(config_path).expanduser())
    else:
        candidate_paths.append(Path.home() / ".openclaw" / "config.yaml")

    user_cfg = {}
    for candidate in candidate_paths:
        if candidate.exists():
            if yaml is None:
                logging.warning("PyYAML not installed; using defaults")
                return DEFAULT_CONFIG
            with open(candidate) as f:
                user_cfg = yaml.safe_load(f) or {}
            break

    # Merge with defaults
    cfg = {
        **DEFAULT_CONFIG,
        **user_cfg,
        "kalshi": {
            **DEFAULT_CONFIG["kalshi"],
            **user_cfg.get("kalshi", {}),
        },
        "prediction_market_arbiter": {
            **DEFAULT_CONFIG["prediction_market_arbiter"],
            **user_cfg.get("prediction_market_arbiter", {}),
        },
    }

    # Backward compatibility for older setup templates.
    if "arbiter" in user_cfg and "prediction_market_arbiter" not in user_cfg:
        cfg["prediction_market_arbiter"] = {
            **DEFAULT_CONFIG["prediction_market_arbiter"],
            **user_cfg.get("arbiter", {}),
        }

    return cfg


# ============================================================================
# Kalshi Market Fetching
# ============================================================================

def fetch_kalshi_markets(cfg: Dict[str, Any], logger: logging.Logger) -> List[Dict[str, Any]]:
    """Fetch active Kalshi markets. Returns list of dicts with title, yes_price, volume."""
    kalshi_cfg = cfg.get("kalshi", {})
    if not kalshi_cfg.get("enabled"):
        logger.info("Kalshi disabled in config")
        return []

    if KalshiClient is None:
        logger.error("kalshi-python not installed. Install with: pip install kalshi-python")
        return []

    key_id = kalshi_cfg.get("api_key_id")
    key_file = kalshi_cfg.get("private_key_file")

    if not key_id or not key_file:
        logger.error("Kalshi API credentials missing (api_key_id, private_key_file)")
        return []

    try:
        base_url = "https://api.elections.kalshi.com/trade-api/v2"
        sdk_config = KalshiConfiguration(host=base_url)
        with open(key_file, "r") as f:
            sdk_config.private_key_pem = f.read()
        sdk_config.api_key_id = key_id
        client = KalshiClient(sdk_config)
        sdk_config.private_key_pem = None  # clear PEM from memory

        max_pages = cfg.get("prediction_market_arbiter", {}).get("kalshi_max_pages", 5)
        all_markets = []
        cursor = None

        for page in range(max_pages):
            url = (
                "https://api.elections.kalshi.com/trade-api/v2/markets"
                "?limit=200&status=open"
            )
            if cursor:
                url += f"&cursor={cursor}"

            resp = client.call_api("GET", url)
            data = json.loads(resp.read())
            batch = data.get("markets", [])

            if not batch:
                logger.debug(f"Kalshi page {page + 1}: no more markets")
                break

            for m in batch:
                price = m.get("last_price", 0) or m.get("yes_ask", 0)
                vol = m.get("volume", 0)
                oi = m.get("open_interest", 0)

                if price > 0 and (vol > 0 or oi > 0):
                    all_markets.append({
                        "title": m.get("title", ""),
                        "ticker": m.get("ticker", ""),
                        "yes_price": price,
                        "volume": vol,
                        "source": "kalshi",
                    })

            cursor = data.get("cursor")
            if not cursor:
                break

            logger.debug(f"Kalshi page {page + 1}: {len(batch)} markets (cursor: {cursor})")

        logger.info(f"Fetched {len(all_markets)} Kalshi markets across {page + 1} pages")
        return all_markets

    except Exception as e:
        logger.error(f"Kalshi fetch error: {e}")
        return []


# ============================================================================
# Polymarket Market Fetching
# ============================================================================

def fetch_polymarket_markets(cfg: Dict[str, Any], logger: logging.Logger) -> List[Dict[str, Any]]:
    """Fetch active Polymarket markets. Returns list of dicts with title, yes_price, volume."""
    try:
        url = "https://gamma-api.polymarket.com/markets?closed=false&limit=200&order=volume&ascending=false"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-Arbiter/1.0",
        })

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        markets = []
        for m in data if isinstance(data, list) else []:
            prices = m.get("outcomePrices", "[]")
            if isinstance(prices, str):
                try:
                    prices = json.loads(prices)
                except Exception:
                    continue

            if not prices:
                continue

            yes_price = int(float(prices[0]) * 100) if prices else 0
            vol = float(m.get("volume", 0) or 0)

            if yes_price > 0 and vol > 0:
                markets.append({
                    "title": m.get("question", m.get("title", "")),
                    "slug": m.get("slug", ""),
                    "yes_price": yes_price,
                    "volume": vol,
                    "source": "polymarket",
                })

        logger.info(f"Fetched {len(markets)} Polymarket markets")
        return markets

    except Exception as e:
        logger.error(f"Polymarket fetch error: {e}")
        return []


# ============================================================================
# Fuzzy Title Matching
# ============================================================================

def fuzzy_match_title(a: str, b: str) -> float:
    """
    Simple word-overlap similarity score (Jaccard similarity).

    Scores:
        1.0 = identical (after stopword removal)
        0.6 = fairly similar
        0.0 = no overlap
    """
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())

    # Remove common stopwords
    stopwords = {
        "will", "the", "a", "an", "in", "on", "by", "of", "to",
        "for", "be", "is", "at", "?", "and", "or", "with", "from"
    }
    a_words -= stopwords
    b_words -= stopwords

    if not a_words or not b_words:
        return 0.0

    intersection = a_words & b_words
    union = a_words | b_words
    return len(intersection) / len(union) if union else 0.0


# ============================================================================
# Core Comparison Logic
# ============================================================================

def check_cross_platform(
    state: Dict[str, Any],
    cfg: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
    force: bool = False,
    logger: Optional[logging.Logger] = None,
) -> bool:
    """
    Compare Kalshi vs Polymarket prices, alert on significant divergences.

    Args:
        state: Persistent state dict (tracks last_cross_platform_check)
        cfg: Configuration dict
        dry_run: If True, print matches instead of returning True
        force: If True, ignore check_interval_minutes
        logger: Logger instance

    Returns:
        True if divergences found and action taken, False otherwise
    """
    if logger is None:
        logger = setup_logging()

    if cfg is None:
        cfg = DEFAULT_CONFIG

    arbiter_cfg = cfg.get("prediction_market_arbiter", {})
    if not arbiter_cfg.get("enabled", True):
        logger.info("Cross-platform arbiter disabled")
        return False

    # Check interval
    interval_minutes = arbiter_cfg.get("check_interval_minutes", 240)
    last_check = state.get("last_cross_platform_check", 0)
    if not force and time.time() - last_check < interval_minutes * 60:
        logger.debug(f"Skipping: last check {(time.time() - last_check) / 60:.1f}m ago")
        return False

    state["last_cross_platform_check"] = time.time()

    # Extract thresholds
    threshold = arbiter_cfg.get("divergence_threshold_pct", 8.0)
    match_threshold = arbiter_cfg.get("fuzzy_match_threshold", 0.6)
    min_vol = arbiter_cfg.get("min_volume", 1000)

    logger.info("Cross-platform comparator starting...")

    # Fetch markets
    kalshi_markets = fetch_kalshi_markets(cfg, logger)
    pm_markets = fetch_polymarket_markets(cfg, logger)

    if not kalshi_markets or not pm_markets:
        logger.warning(
            f"Comparator: K={len(kalshi_markets)}, PM={len(pm_markets)} — "
            "skipping (need both)"
        )
        return False

    logger.info(f"Comparator: {len(kalshi_markets)} Kalshi, {len(pm_markets)} Polymarket markets")

    # Find matches and compare prices
    divergences = []
    for km in kalshi_markets:
        for pm in pm_markets:
            score = fuzzy_match_title(km["title"], pm["title"])
            if score < match_threshold:
                continue

            combined_vol = km["volume"] + pm["volume"]
            if combined_vol < min_vol:
                continue

            delta = abs(km["yes_price"] - pm["yes_price"])
            midpoint = (km["yes_price"] + pm["yes_price"]) / 2
            delta_pct = (delta / midpoint * 100) if midpoint > 0 else 0

            if delta_pct >= threshold:
                divergences.append({
                    "kalshi_title": km["title"][:60],
                    "pm_title": pm["title"][:60],
                    "kalshi_price": km["yes_price"],
                    "pm_price": pm["yes_price"],
                    "delta": delta,
                    "delta_pct": round(delta_pct, 1),
                    "match_score": round(score, 2),
                })

    # Save to cache — standardized schema for morning-brief consumption
    cache_dir = Path.home() / ".openclaw" / "state"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "arbiter_cache.json"
    try:
        # Convert divergences to morning-brief compatible format:
        # - key: "divergences" (not "matches")
        # - prices as 0-1 floats (not integer cents)
        # - "cached_at" as ISO timestamp (not unix epoch)
        # - include "ticker", "polymarket_price", "spread_cents" keys
        normalized = []
        for d in divergences[:20]:
            normalized.append({
                "ticker": d.get("kalshi_title", "?")[:40],
                "kalshi_title": d["kalshi_title"],
                "pm_title": d["pm_title"],
                "kalshi_price": d["kalshi_price"] / 100.0,  # cents → 0-1 float
                "polymarket_price": d["pm_price"] / 100.0,  # cents → 0-1 float
                "pm_price": d["pm_price"] / 100.0,
                "delta": d["delta"],
                "delta_pct": d["delta_pct"],
                "spread_cents": d["delta"],
                "match_score": d["match_score"],
            })

        with open(cache_path, "w") as f:
            json.dump({
                "divergences": normalized,
                "kalshi_count": len(kalshi_markets),
                "pm_count": len(pm_markets),
                "cached_at": datetime.now().astimezone().isoformat(),
                "timestamp": time.time(),
            }, f, indent=2)
        logger.debug(f"Cached results to {cache_path}")
    except OSError as e:
        logger.warning(f"Could not write cache: {e}")

    # Also write legacy path for backward compat
    legacy_cache = Path.home() / ".arbiter_cache.json"
    try:
        with open(legacy_cache, "w") as f:
            json.dump({
                "matches": divergences[:20],
                "kalshi_count": len(kalshi_markets),
                "pm_count": len(pm_markets),
                "timestamp": time.time(),
            }, f, indent=2)
    except OSError:
        pass

    logger.info(f"Comparator: {len(divergences)} divergences >= {threshold}%")

    if not divergences:
        return False

    # Sort by largest divergence
    divergences.sort(key=lambda x: x["delta"], reverse=True)

    # Format alert message
    parts = [f"📊 Cross-platform divergences (>={int(threshold)}%):"]
    for d in divergences[:5]:
        arrow = "↑" if d["kalshi_price"] > d["pm_price"] else "↓"
        parts.append(
            f"  {d['kalshi_title'][:40]}\n"
            f"    Kalshi {d['kalshi_price']}¢ vs PM {d['pm_price']}¢ ({arrow}{d['delta_pct']}%)"
        )

    message = "\n".join(parts)

    if dry_run:
        print(message)
        print(f"\n[DRY RUN] Found {len(divergences)} divergences")
        return True

    # In production, user agent would handle delivery
    logger.info(f"Cross-platform alert: {len(divergences)} divergences found")
    print(message)

    return True


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Prediction Market Arbiter — Cross-platform divergence scanner"
    )
    parser.add_argument(
        "--config",
        help="Path to config.yaml",
        default=None
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display results without sending alerts"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force run even if interval hasn't elapsed"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose logging"
    )

    args = parser.parse_args()

    logger = setup_logging(verbose=args.verbose)
    cfg = load_config(args.config)

    try:
        check_cross_platform(
            state={},
            cfg=cfg,
            dry_run=args.dry_run,
            force=args.force,
            logger=logger,
        )
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
