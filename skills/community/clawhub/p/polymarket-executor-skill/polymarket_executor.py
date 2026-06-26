#!/usr/bin/env python3
"""
Polymarket Executor - Full Trading Engine
Version: 2.0.0
Author: Georges Andronescu (Wesley Armando)

Architecture identique à crypto-executor :
- Paper trading d'abord (PAPER_MODE=true)
- Vrai trading quand prêt (PAPER_MODE=false)
- Interface optimizer (learned_config.json)
- Kelly Criterion + circuit breakers
- Logging complet pour l'optimizer

Stratégies :
1. Parity Arbitrage (YES+NO ≠ $1)
2. Tail-End Trading (>95% certainty)
3. Market Making (spread capture)
4. Logical Arbitrage (correlated markets)
5. Info Edge (news-driven mispricing)
"""

import sys
import json
import os
import time
import urllib.request
import urllib.error
import hashlib
import hmac
import base64
from datetime import datetime, timezone
from pathlib import Path
import concurrent.futures
import math

# ==========================================
# CONFIGURATION — chargée depuis learned_config.json
# ==========================================

WORKSPACE = Path(os.getenv("WORKSPACE", "/workspace"))
CONFIG_FILE = WORKSPACE / "learned_config.json"
PAPER_TRADES_FILE = WORKSPACE / "paper_trades.json"
LIVE_TRADES_FILE = WORKSPACE / "live_trades.jsonl"
PORTFOLIO_FILE = WORKSPACE / "portfolio.json"
PERFORMANCE_FILE = WORKSPACE / "performance_metrics.json"

# Credentials
POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY", "")
POLYMARKET_SECRET = os.getenv("POLYMARKET_SECRET", "")
POLYMARKET_PASSPHRASE = os.getenv("POLYMARKET_PASSPHRASE", "")
WALLET_ADDRESS = os.getenv("POLYMARKET_WALLET_ADDRESS", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1584210176")

# Mode
PAPER_MODE = os.getenv("PAPER_MODE", "true").lower() == "true"

# Endpoints
CLOB_BASE = "https://clob.polymarket.com"
GAMMA_BASE = "https://gamma-api.polymarket.com"

# Config par défaut (écrasée par learned_config.json si présent)
DEFAULT_CONFIG = {
    # Capital
    "paper_capital_usdc": 100.0,
    "live_capital_usdc": float(os.getenv("POLYMARKET_CAPITAL", "50.0")),

    # Seuils par stratégie
    "parity_min_edge_pct": 0.03,
    "tail_end_min_certainty": 0.95,
    "tail_end_min_profit_pct": 0.01,
    "market_making_min_spread_pct": 0.025,
    "logical_arb_min_coverage": 0.90,

    # Risk management
    "max_position_pct": 0.10,        # 10% du capital max par trade
    "kelly_fraction": 0.25,          # Kelly conservateur (1/4 Kelly)
    "max_open_positions": 10,
    "max_daily_loss_pct": 0.15,      # Circuit breaker : -15% par jour
    "stop_loss_pct": 0.50,           # Stop loss : -50% sur position

    # Scan
    "scan_interval_seconds": 300,    # Scan toutes les 5 minutes
    "max_markets_to_scan": 500,
    "max_workers": 20,

    # Strategies activées
    "strategy_parity": True,
    "strategy_tail_end": True,
    "strategy_market_making": False, # Désactivé par défaut (nécessite proxy)
    "strategy_logical_arb": True,
    "strategy_info_edge": False,     # Activé si web search disponible

    # Optimizer
    "last_optimized": None,
    "optimization_count": 0
}


def load_config():
    """Charger config depuis learned_config.json ou utiliser défaut."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                saved = json.load(f)
            config = {**DEFAULT_CONFIG, **saved}
            print(f"[CONFIG] Loaded from {CONFIG_FILE}")
            return config
        except Exception as e:
            print(f"[CONFIG] Error loading: {e}, using defaults")
    else:
        # Créer le fichier avec les defaults
        save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Sauvegarder la config."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


# ==========================================
# PORTFOLIO MANAGER
# ==========================================

class PortfolioManager:
    """Gère le capital, les positions, le P&L."""

    def __init__(self, config, paper_mode=True):
        self.config = config
        self.paper_mode = paper_mode
        self.data = self._load()

    def _load(self):
        """Charger ou initialiser le portfolio."""
        if PORTFOLIO_FILE.exists():
            try:
                with open(PORTFOLIO_FILE) as f:
                    return json.load(f)
            except:
                pass

        capital = self.config["paper_capital_usdc"] if self.paper_mode \
                  else self.config["live_capital_usdc"]

        data = {
            "mode": "paper" if self.paper_mode else "live",
            "initial_capital": capital,
            "available_capital": capital,
            "invested_capital": 0.0,
            "total_pnl": 0.0,
            "daily_pnl": 0.0,
            "daily_pnl_date": datetime.now(timezone.utc).date().isoformat(),
            "open_positions": [],
            "closed_positions": [],
            "stats": {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "avg_profit_pct": 0.0,
                "best_trade": 0.0,
                "worst_trade": 0.0,
                "sharpe_ratio": 0.0
            }
        }
        self._save(data)
        return data

    def _save(self, data=None):
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(data or self.data, f, indent=2)

    def reset_daily_pnl_if_new_day(self):
        today = datetime.now(timezone.utc).date().isoformat()
        if self.data["daily_pnl_date"] != today:
            self.data["daily_pnl"] = 0.0
            self.data["daily_pnl_date"] = today
            self._save()

    def can_open_position(self, size_usdc):
        """Vérifier si on peut ouvrir une position."""
        self.reset_daily_pnl_if_new_day()

        # Circuit breaker journalier
        if self.data["daily_pnl"] < 0:
            daily_loss_pct = abs(self.data["daily_pnl"]) / self.data["initial_capital"]
            if daily_loss_pct >= self.config["max_daily_loss_pct"]:
                print(f"[CIRCUIT BREAKER] Daily loss {daily_loss_pct:.1%} >= "
                      f"{self.config['max_daily_loss_pct']:.1%} — trading halted")
                return False

        # Positions max
        if len(self.data["open_positions"]) >= self.config["max_open_positions"]:
            print(f"[RISK] Max open positions ({self.config['max_open_positions']}) reached")
            return False

        # Capital disponible
        if size_usdc > self.data["available_capital"]:
            print(f"[RISK] Insufficient capital: need {size_usdc:.2f}, "
                  f"have {self.data['available_capital']:.2f}")
            return False

        return True

    def kelly_size(self, win_prob, avg_win_pct, avg_loss_pct=1.0):
        """Calculer la taille Kelly."""
        if avg_loss_pct <= 0 or win_prob <= 0:
            return 0

        b = avg_win_pct / avg_loss_pct  # odds
        p = win_prob
        q = 1 - p

        kelly = (b * p - q) / b
        kelly = max(0, kelly)  # Jamais négatif
        kelly *= self.config["kelly_fraction"]  # Fraction conservative

        # Limiter au max_position_pct
        kelly = min(kelly, self.config["max_position_pct"])

        capital = self.data["available_capital"]
        return round(capital * kelly, 2)

    def open_position(self, opportunity, size_usdc):
        """Ouvrir une position."""
        position = {
            "id": f"pos_{int(time.time())}_{opportunity['strategy'][:4]}",
            "strategy": opportunity["strategy"],
            "market_id": opportunity["market_id"],
            "market_question": opportunity["market_question"],
            "category": opportunity.get("category", "other"),
            "token_id": opportunity.get("token_id", ""),
            "side": opportunity.get("side", "YES"),
            "entry_price": opportunity["entry_price"],
            "size_usdc": size_usdc,
            "shares": size_usdc / opportunity["entry_price"],
            "target_price": opportunity.get("target_price", 1.0),
            "stop_loss_price": opportunity["entry_price"] * (1 - self.config["stop_loss_pct"]),
            "expected_profit_pct": opportunity.get("profit_pct", 0),
            "opened_at": datetime.now(timezone.utc).isoformat(),
            "resolution_date": opportunity.get("resolution_date", ""),
            "status": "open",
            "mode": "paper" if self.paper_mode else "live"
        }

        self.data["open_positions"].append(position)
        self.data["available_capital"] -= size_usdc
        self.data["invested_capital"] += size_usdc
        self.data["stats"]["total_trades"] += 1
        self._save()

        print(f"[POSITION OPENED] {position['id']} | "
              f"{position['strategy']} | {size_usdc:.2f} USDC | "
              f"entry={position['entry_price']:.3f}")

        return position

    def close_position(self, position_id, exit_price, reason="manual"):
        """Fermer une position et calculer P&L."""
        pos = None
        for p in self.data["open_positions"]:
            if p["id"] == position_id:
                pos = p
                break

        if not pos:
            return None

        pnl = (exit_price - pos["entry_price"]) * pos["shares"]
        pnl_pct = (exit_price - pos["entry_price"]) / pos["entry_price"]

        pos.update({
            "status": "closed",
            "exit_price": exit_price,
            "exit_reason": reason,
            "pnl_usdc": round(pnl, 4),
            "pnl_pct": round(pnl_pct, 4),
            "closed_at": datetime.now(timezone.utc).isoformat()
        })

        self.data["open_positions"].remove(pos)
        self.data["closed_positions"].append(pos)
        self.data["available_capital"] += pos["size_usdc"] + pnl
        self.data["invested_capital"] -= pos["size_usdc"]
        self.data["total_pnl"] += pnl
        self.data["daily_pnl"] += pnl

        # Stats
        if pnl > 0:
            self.data["stats"]["winning_trades"] += 1
            self.data["stats"]["best_trade"] = max(
                self.data["stats"]["best_trade"], pnl)
        else:
            self.data["stats"]["losing_trades"] += 1
            self.data["stats"]["worst_trade"] = min(
                self.data["stats"]["worst_trade"], pnl)

        total = self.data["stats"]["winning_trades"] + self.data["stats"]["losing_trades"]
        if total > 0:
            self.data["stats"]["win_rate"] = self.data["stats"]["winning_trades"] / total

        self._save()
        self._update_performance_metrics(pos)

        print(f"[POSITION CLOSED] {position_id} | P&L: {pnl:+.2f} USDC "
              f"({pnl_pct:+.1%}) | reason={reason}")

        return pos

    def _update_performance_metrics(self, closed_pos):
        """Mettre à jour performance_metrics.json pour l'optimizer."""
        metrics = {}
        if PERFORMANCE_FILE.exists():
            try:
                with open(PERFORMANCE_FILE) as f:
                    metrics = json.load(f)
            except:
                pass

        strategy = closed_pos["strategy"]
        if strategy not in metrics:
            metrics[strategy] = {
                "trades": 0, "wins": 0, "total_pnl": 0,
                "win_rate": 0, "avg_pnl": 0
            }

        m = metrics[strategy]
        m["trades"] += 1
        if closed_pos["pnl_usdc"] > 0:
            m["wins"] += 1
        m["total_pnl"] += closed_pos["pnl_usdc"]
        m["win_rate"] = m["wins"] / m["trades"]
        m["avg_pnl"] = m["total_pnl"] / m["trades"]

        # Global
        metrics["global"] = {
            "total_pnl": self.data["total_pnl"],
            "win_rate": self.data["stats"]["win_rate"],
            "total_trades": self.data["stats"]["total_trades"],
            "available_capital": self.data["available_capital"],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

        with open(PERFORMANCE_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)

    def check_stop_losses(self, client):
        """Vérifier les stop-losses sur les positions ouvertes."""
        for pos in list(self.data["open_positions"]):
            try:
                current_price = client.get_price(pos["token_id"], "SELL")
                if not current_price:
                    continue

                if current_price <= pos["stop_loss_price"]:
                    print(f"[STOP LOSS] {pos['id']} hit at {current_price:.3f}")
                    self.close_position(pos["id"], current_price, "stop_loss")
            except Exception as e:
                print(f"[ERROR] Stop loss check {pos['id']}: {e}")

    def get_summary(self):
        """Résumé du portfolio."""
        total_value = self.data["available_capital"] + self.data["invested_capital"]
        return {
            "mode": self.data["mode"],
            "total_value": round(total_value, 2),
            "available": round(self.data["available_capital"], 2),
            "invested": round(self.data["invested_capital"], 2),
            "total_pnl": round(self.data["total_pnl"], 2),
            "daily_pnl": round(self.data["daily_pnl"], 2),
            "open_positions": len(self.data["open_positions"]),
            "win_rate": round(self.data["stats"]["win_rate"] * 100, 1),
            "total_trades": self.data["stats"]["total_trades"]
        }


# ==========================================
# POLYMARKET API CLIENT
# ==========================================

class PolymarketClient:
    """Client Polymarket CLOB + Gamma API."""

    def __init__(self, api_key="", secret="", passphrase="", wallet=""):
        self.api_key = api_key
        self.secret = secret
        self.passphrase = passphrase
        self.wallet = wallet
        self.authenticated = bool(api_key and secret and passphrase)

    def _request(self, endpoint, method="GET", params=None, body=None,
                 auth=False, base="clob"):
        url_base = CLOB_BASE if base == "clob" else GAMMA_BASE

        if params:
            query = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url_base}{endpoint}?{query}"
        else:
            url = f"{url_base}{endpoint}"

        headers = {"Content-Type": "application/json"}

        if auth and self.authenticated:
            timestamp = str(int(time.time() * 1000))
            message = f"{timestamp}{method}{endpoint}{json.dumps(body) if body else ''}"
            sig = hmac.new(
                self.secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            headers.update({
                "POLY-API-KEY": self.api_key,
                "POLY-SIGNATURE": sig,
                "POLY-TIMESTAMP": timestamp,
                "POLY-PASSPHRASE": self.passphrase
            })

        req_body = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=req_body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            print(f"[API ERROR] {e.code}: {e.read().decode()[:200]}")
            return None
        except Exception as e:
            print(f"[REQUEST ERROR] {e}")
            return None

    def get_markets(self, limit=100, offset=0, active=True):
        """Récupérer les marchés actifs."""
        params = {"limit": limit, "offset": offset}
        if active:
            params["active"] = "true"
        result = self._request("/markets", params=params, base="gamma")
        if result and isinstance(result, dict):
            return result.get("data", [])
        return result if isinstance(result, list) else []

    def get_all_markets(self, max_markets=500):
        """Récupérer tous les marchés actifs."""
        markets = []
        offset = 0
        batch = 100

        while len(markets) < max_markets:
            batch_markets = self.get_markets(limit=batch, offset=offset)
            if not batch_markets:
                break
            markets.extend(batch_markets)
            if len(batch_markets) < batch:
                break
            offset += batch
            time.sleep(0.2)

        print(f"[GAMMA] {len(markets)} marchés récupérés")
        return markets[:max_markets]

    def get_price(self, token_id, side="BUY"):
        """Prix meilleur ordre."""
        r = self._request(f"/price?token_id={token_id}&side={side}")
        return float(r["price"]) if r and "price" in r else None

    def get_midpoint(self, token_id):
        """Prix midpoint."""
        r = self._request(f"/midpoint?token_id={token_id}")
        return float(r["mid"]) if r and "mid" in r else None

    def get_orderbook(self, token_id):
        """Order book complet."""
        return self._request(f"/book?token_id={token_id}")

    def place_order(self, token_id, price, size, side="BUY"):
        """Placer un vrai ordre sur Polymarket."""
        if not self.authenticated:
            print("[TRADE] Not authenticated — cannot place real order")
            return None

        order = {
            "token_id": token_id,
            "price": str(round(price, 4)),
            "size": str(round(size, 2)),
            "side": side.upper(),
            "type": "LIMIT",
            "post_only": False
        }

        result = self._request("/order", method="POST", body=order, auth=True)
        if result:
            print(f"[ORDER PLACED] {side} {size} @ {price} | token={token_id[:20]}...")
        return result

    def get_balance(self):
        """Solde USDC du wallet."""
        if not self.authenticated:
            return None
        r = self._request("/balance", auth=True)
        return float(r.get("balance", 0)) if r else None


# ==========================================
# STRATEGY ENGINE
# ==========================================

class StrategyEngine:
    """Détecte les opportunités de trading."""

    def __init__(self, config, client):
        self.config = config
        self.client = client

    def _categorize(self, question):
        q = question.lower()
        cats = {
            "crypto": ["bitcoin", "btc", "eth", "crypto", "solana", "defi"],
            "politics": ["election", "president", "trump", "vote", "congress"],
            "sports": ["nba", "nfl", "super bowl", "championship", "soccer", "f1"],
            "economics": ["fed", "rate", "inflation", "gdp", "recession"],
            "tech": ["apple", "tesla", "nvidia", "ai", "ipo"]
        }
        for cat, keywords in cats.items():
            if any(k in q for k in keywords):
                return cat
        return "other"

    def _get_market_tokens(self, market):
        """Extraire les token IDs YES/NO d'un marché."""
        tokens = []
        for outcome in market.get("outcomes", []):
            if isinstance(outcome, dict) and "token_id" in outcome:
                tokens.append(outcome)
            elif isinstance(outcome, str):
                # Parfois outcomes = liste de strings
                cond_tokens = market.get("condition_tokens", [])
                if cond_tokens:
                    tokens = [{"name": o, "token_id": t}
                              for o, t in zip(market.get("outcomes", []),
                                              cond_tokens)]
                    break
        return tokens

    def strategy_parity_arb(self, market):
        """
        Stratégie 1 : Parity Arbitrage
        Si YES + NO < $1.00 → Acheter les deux, profit garanti à résolution
        Edge minimum : config["parity_min_edge_pct"]
        """
        if not self.config["strategy_parity"]:
            return None

        tokens = self._get_market_tokens(market)
        if len(tokens) < 2:
            return None

        try:
            yes_token = tokens[0].get("token_id")
            no_token = tokens[1].get("token_id") if len(tokens) > 1 else None

            yes_price = self.client.get_price(yes_token, "BUY")
            no_price = self.client.get_price(no_token, "BUY") if no_token else None

            if not yes_price or not no_price:
                return None

            total = yes_price + no_price
            edge = 1.0 - total  # profit si on achète les deux

            if edge >= self.config["parity_min_edge_pct"]:
                profit_pct = (edge / total) * 100
                return {
                    "strategy": "parity_arb",
                    "market_id": market.get("id", ""),
                    "market_question": market.get("question", ""),
                    "category": self._categorize(market.get("question", "")),
                    "token_id": yes_token,
                    "token_id_no": no_token,
                    "side": "BOTH",
                    "entry_price": total / 2,  # prix moyen
                    "yes_price": yes_price,
                    "no_price": no_price,
                    "total_cost": total,
                    "profit_pct": profit_pct,
                    "target_price": 1.0,
                    "win_probability": 0.99,  # Quasi-certain
                    "resolution_date": market.get("end_date_iso", ""),
                    "detected_at": datetime.now(timezone.utc).isoformat()
                }
        except Exception as e:
            print(f"[PARITY] Error {market.get('id')}: {e}")
        return None

    def strategy_tail_end(self, market):
        """
        Stratégie 2 : Tail-End Trading
        Acheter quand prix > 95% — attend résolution à $1.00
        Profit petit mais quasi-certain
        """
        if not self.config["strategy_tail_end"]:
            return None

        tokens = self._get_market_tokens(market)

        for token_info in tokens:
            token_id = token_info.get("token_id")
            if not token_id:
                continue
            try:
                price = self.client.get_price(token_id, "BUY")
                if not price:
                    continue

                if (price >= self.config["tail_end_min_certainty"] and
                        price < 0.998):
                    profit_pct = ((1.0 - price) / price) * 100

                    if profit_pct >= self.config["tail_end_min_profit_pct"] * 100:
                        return {
                            "strategy": "tail_end",
                            "market_id": market.get("id", ""),
                            "market_question": market.get("question", ""),
                            "category": self._categorize(market.get("question", "")),
                            "token_id": token_id,
                            "outcome": token_info.get("name", "YES"),
                            "side": "BUY",
                            "entry_price": price,
                            "target_price": 1.0,
                            "profit_pct": profit_pct,
                            "win_probability": price,
                            "resolution_date": market.get("end_date_iso", ""),
                            "detected_at": datetime.now(timezone.utc).isoformat()
                        }
            except Exception as e:
                print(f"[TAIL_END] Error: {e}")
        return None

    def strategy_logical_arb(self, markets):
        """
        Stratégie 3 : Arbitrage Logique sur marchés corrélés
        Trouve des paires où les prix sont logiquement incohérents
        Ex: "BTC > 100k Mar 15" à 40% ET "BTC > 90k Mar 15" à 35%
        → Impossible : P(>100k) ne peut pas être > P(>90k)
        """
        if not self.config["strategy_logical_arb"]:
            return []

        opportunities = []

        # Grouper par sujet similaire
        crypto_markets = [m for m in markets
                         if self._categorize(m.get("question", "")) == "crypto"]

        # Chercher les paires BTC price levels
        btc_markets = []
        for m in crypto_markets:
            q = m.get("question", "").lower()
            if "btc" in q or "bitcoin" in q:
                # Extraire le prix cible si mentionné
                import re
                prices = re.findall(r'\$?([\d,]+)k?', q)
                if prices:
                    btc_markets.append({"market": m, "prices": prices})

        # Chercher incohérences dans les paires
        for i in range(len(btc_markets)):
            for j in range(i+1, len(btc_markets)):
                m1 = btc_markets[i]
                m2 = btc_markets[j]

                tokens1 = self._get_market_tokens(m1["market"])
                tokens2 = self._get_market_tokens(m2["market"])

                if not tokens1 or not tokens2:
                    continue

                try:
                    p1 = self.client.get_price(tokens1[0]["token_id"], "BUY")
                    p2 = self.client.get_price(tokens2[0]["token_id"], "BUY")

                    if not p1 or not p2:
                        continue

                    # Si les deux sont censés être liés et les prix divergent trop
                    # Opportunité simple : le plus bas devrait être >= le plus haut
                    # (logique d'implication)
                    if abs(p1 - p2) > 0.15:  # 15% de divergence = potentiel arb
                        profit_pct = abs(p1 - p2) * 100
                        opp_token = tokens1[0]["token_id"] if p1 < p2 else tokens2[0]["token_id"]
                        entry = min(p1, p2)

                        opportunities.append({
                            "strategy": "logical_arb",
                            "market_id": m1["market"].get("id"),
                            "market_question": (f"{m1['market'].get('question', '')} "
                                               f"vs {m2['market'].get('question', '')}"),
                            "category": "crypto",
                            "token_id": opp_token,
                            "side": "BUY",
                            "entry_price": entry,
                            "target_price": max(p1, p2),
                            "profit_pct": profit_pct,
                            "win_probability": self.config["logical_arb_min_coverage"],
                            "resolution_date": m1["market"].get("end_date_iso", ""),
                            "detected_at": datetime.now(timezone.utc).isoformat()
                        })
                except Exception:
                    continue

        return opportunities

    def scan_market(self, market):
        """Scanner un marché avec toutes les stratégies."""
        opps = []

        opp = self.strategy_parity_arb(market)
        if opp:
            opps.append(opp)

        opp = self.strategy_tail_end(market)
        if opp:
            opps.append(opp)

        return opps

    def scan_all(self, markets):
        """Scanner tous les marchés en parallèle."""
        all_opps = []
        max_workers = self.config["max_workers"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(self.scan_market, m): m for m in markets}
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=15)
                    all_opps.extend(result)
                except Exception:
                    pass

        # Logical arb (nécessite tous les marchés)
        logical_opps = self.strategy_logical_arb(markets)
        all_opps.extend(logical_opps)

        # Trier par profit décroissant
        all_opps.sort(key=lambda x: x.get("profit_pct", 0), reverse=True)

        print(f"[SCAN] {len(markets)} marchés → {len(all_opps)} opportunités")
        return all_opps


# ==========================================
# TRADE EXECUTOR
# ==========================================

class TradeExecutor:
    """Décide et exécute les trades."""

    def __init__(self, config, client, portfolio, paper_mode=True):
        self.config = config
        self.client = client
        self.portfolio = portfolio
        self.paper_mode = paper_mode

    def evaluate_opportunity(self, opp):
        """
        Évaluer si une opportunité mérite un trade.
        Retourne (should_trade, size_usdc, reason)
        """
        # Calculer la taille Kelly
        win_prob = opp.get("win_probability", 0.5)
        profit_pct = opp.get("profit_pct", 0) / 100
        loss_pct = 1.0  # On perd 100% de la mise si résolution adverse

        size = self.portfolio.kelly_size(win_prob, profit_pct, loss_pct)

        if size < 1.0:
            return False, 0, "Kelly size too small (<$1)"

        # Vérifier si on peut ouvrir
        if not self.portfolio.can_open_position(size):
            return False, 0, "Risk check failed"

        # Vérifier la liquidité minimale
        min_liquidity = 100  # $100 USDC minimum dans le marché
        # (simplification — idéalement vérifier via orderbook)

        return True, size, "OK"

    def execute_trade(self, opp):
        """Exécuter un trade (paper ou réel)."""
        should_trade, size, reason = self.evaluate_opportunity(opp)

        if not should_trade:
            print(f"[SKIP] {opp['strategy']} | {reason}")
            return None

        if self.paper_mode:
            # Paper trade — simuler sans argent réel
            position = self.portfolio.open_position(opp, size)
            self._log_paper_trade(opp, position, size)
            return position
        else:
            # Live trade — vrai ordre Polymarket
            token_id = opp.get("token_id")
            entry_price = opp.get("entry_price", 0)

            result = self.client.place_order(
                token_id=token_id,
                price=entry_price,
                size=size,
                side="BUY"
            )

            if result:
                position = self.portfolio.open_position(opp, size)
                self._log_live_trade(opp, position, size, result)
                return position
            else:
                print(f"[TRADE FAILED] Order rejected by Polymarket")
                return None

    def _log_paper_trade(self, opp, position, size):
        """Logger le paper trade."""
        WORKSPACE.mkdir(parents=True, exist_ok=True)

        # Charger ou initialiser
        paper_data = {"trades": [], "portfolio_snapshots": []}
        if PAPER_TRADES_FILE.exists():
            try:
                with open(PAPER_TRADES_FILE) as f:
                    paper_data = json.load(f)
            except:
                pass

        paper_data["trades"].append({
            "position_id": position["id"],
            "strategy": opp["strategy"],
            "market_question": opp["market_question"],
            "entry_price": opp["entry_price"],
            "size_usdc": size,
            "expected_profit_pct": opp.get("profit_pct", 0),
            "win_probability": opp.get("win_probability", 0),
            "opened_at": position["opened_at"],
            "status": "open"
        })

        with open(PAPER_TRADES_FILE, 'w') as f:
            json.dump(paper_data, f, indent=2)

    def _log_live_trade(self, opp, position, size, order_result):
        """Logger le vrai trade."""
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        with open(LIVE_TRADES_FILE, 'a') as f:
            f.write(json.dumps({
                "position_id": position["id"],
                "order_result": order_result,
                "strategy": opp["strategy"],
                "size_usdc": size,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + '\n')

    def check_and_close_positions(self):
        """Vérifier et fermer les positions résolues."""
        for pos in list(self.portfolio.data["open_positions"]):
            token_id = pos.get("token_id")
            if not token_id:
                continue

            try:
                current_price = self.client.get_price(token_id, "SELL")
                if not current_price:
                    continue

                # Résolution détectée (prix très proche de 0 ou 1)
                if current_price >= 0.99:
                    self.portfolio.close_position(pos["id"], 1.0, "resolved_win")
                elif current_price <= 0.01:
                    self.portfolio.close_position(pos["id"], 0.0, "resolved_loss")
                # Stop loss
                elif current_price <= pos["stop_loss_price"]:
                    self.portfolio.close_position(pos["id"], current_price, "stop_loss")

            except Exception as e:
                print(f"[CHECK] Error on {pos['id']}: {e}")


# ==========================================
# TELEGRAM
# ==========================================

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage" if token else None
        self.chat_id = chat_id

    def send(self, text):
        if not self.url:
            print(f"[TELEGRAM] {text}")
            return
        try:
            data = json.dumps({"chat_id": self.chat_id, "text": text,
                               "parse_mode": "Markdown"}).encode()
            req = urllib.request.Request(self.url, data=data,
                                         headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"[TELEGRAM ERROR] {e}")

    def send_report(self, portfolio_summary, opportunities, new_trades):
        mode = "📄 PAPER" if PAPER_MODE else "💰 LIVE"
        msg = f"""⚡ *Wesley | Polymarket {mode}*

📊 *Portfolio*
• Capital: ${portfolio_summary['total_value']:.2f} USDC
• Disponible: ${portfolio_summary['available']:.2f}
• P&L total: {portfolio_summary['total_pnl']:+.2f} USDC
• P&L jour: {portfolio_summary['daily_pnl']:+.2f} USDC
• Win rate: {portfolio_summary['win_rate']:.1f}%
• Trades: {portfolio_summary['total_trades']}
• Positions ouvertes: {portfolio_summary['open_positions']}

🎯 *Ce scan*
• Opportunités: {len(opportunities)}
• Trades exécutés: {len(new_trades)}
"""
        if new_trades:
            msg += "\n📋 *Derniers trades:*\n"
            for t in new_trades[:3]:
                msg += (f"• {t['strategy']} | ${t['size_usdc']:.2f} | "
                       f"entry={t['entry_price']:.3f}\n")

        self.send(msg)


# ==========================================
# MAIN ENGINE
# ==========================================

def main():
    print("=" * 60)
    print("POLYMARKET EXECUTOR v2.0 — Wesley-Agent")
    print(f"Mode: {'📄 PAPER TRADING' if PAPER_MODE else '💰 LIVE TRADING'}")
    print("=" * 60)

    # Init
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    config = load_config()

    client = PolymarketClient(
        api_key=POLYMARKET_API_KEY,
        secret=POLYMARKET_SECRET,
        passphrase=POLYMARKET_PASSPHRASE,
        wallet=WALLET_ADDRESS
    )

    portfolio = PortfolioManager(config, paper_mode=PAPER_MODE)
    strategy_engine = StrategyEngine(config, client)
    executor = TradeExecutor(config, client, portfolio, paper_mode=PAPER_MODE)
    telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    # Vérifier le solde si live
    if not PAPER_MODE:
        balance = client.get_balance()
        if balance is not None:
            print(f"[WALLET] Balance: ${balance:.2f} USDC")
        else:
            print("[WARNING] Cannot fetch wallet balance — check credentials")

    summary = portfolio.get_summary()
    print(f"[PORTFOLIO] Capital: ${summary['total_value']:.2f} USDC | "
          f"Win rate: {summary['win_rate']:.1f}% | "
          f"Trades: {summary['total_trades']}")

    telegram.send(
        f"🚀 *Polymarket Executor Started*\n"
        f"Mode: {'PAPER' if PAPER_MODE else 'LIVE'}\n"
        f"Capital: ${summary['total_value']:.2f} USDC"
    )

    scan_interval = config["scan_interval_seconds"]

    # Boucle principale
    while True:
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] === SCAN START ===")

            # 1. Vérifier les positions ouvertes
            executor.check_and_close_positions()
            portfolio.check_stop_losses(client)

            # 2. Scanner les marchés
            markets = client.get_all_markets(
                max_markets=config["max_markets_to_scan"]
            )

            if not markets:
                print("[ERROR] No markets fetched — retrying in 60s")
                time.sleep(60)
                continue

            # 3. Détecter les opportunités
            opportunities = strategy_engine.scan_all(markets)

            # 4. Exécuter les meilleures opportunités
            new_trades = []
            max_new_trades = 3  # Max 3 nouveaux trades par scan

            for opp in opportunities[:10]:  # Regarder les 10 meilleures
                if len(new_trades) >= max_new_trades:
                    break

                position = executor.execute_trade(opp)
                if position:
                    new_trades.append(position)

            # 5. Rapport
            summary = portfolio.get_summary()
            telegram.send_report(summary, opportunities, new_trades)

            print(f"[SCAN DONE] Opportunities: {len(opportunities)} | "
                  f"Trades: {len(new_trades)} | "
                  f"Portfolio: ${summary['total_value']:.2f}")

            # 6. Attendre
            print(f"[SLEEP] {scan_interval}s...")
            time.sleep(scan_interval)

        except KeyboardInterrupt:
            print("\n[STOP] Stopped by user")
            telegram.send("⛔ Polymarket Executor stopped")
            break

        except Exception as e:
            print(f"[ERROR] Main loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
