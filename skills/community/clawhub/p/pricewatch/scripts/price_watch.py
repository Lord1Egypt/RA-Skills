#!/usr/bin/env python3
"""
PriceWatch - Cross-Platform Competitive Price Monitor
Core monitoring engine for the PriceWatch OpenClaw skill.

Usage:
    python price_watch.py --scan
    python price_watch.py --add --url <product_url> --target <price>
    python price_watch.py --history --product <product_name>
    python price_watch.py --report
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)

# --- Configuration ---
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"
CONFIG_PATH = SCRIPT_DIR / "config.yaml"
DB_PATH = DATA_DIR / "price_history.db"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


# --- Database Layer ---
class PriceDatabase:
    """SQLite-backed price history storage."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                target_price REAL,
                currency TEXT DEFAULT 'USD',
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS price_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                shipping REAL DEFAULT 0.0,
                in_stock INTEGER DEFAULT 1,
                captured_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (product_id) REFERENCES watchlist(id)
            );

            CREATE INDEX IF NOT EXISTS idx_snapshots_product
                ON price_snapshots(product_id, captured_at);

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                old_price REAL,
                new_price REAL,
                change_percent REAL,
                alert_type TEXT DEFAULT 'price_drop',
                sent INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (product_id) REFERENCES watchlist(id)
            );
        """)
        self.conn.commit()

    def add_product(self, name: str, platform: str, url: str,
                    target_price: Optional[float] = None,
                    currency: str = "USD") -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO watchlist (name, platform, url, target_price, currency)
            VALUES (?, ?, ?, ?, ?)
        """, (name, platform, url, target_price, currency))
        self.conn.commit()
        # Return the product ID (whether newly inserted or existing)
        cursor.execute("SELECT id FROM watchlist WHERE url = ?", (url,))
        return cursor.fetchone()[0]

    def record_price(self, product_id: int, price: float, currency: str = "USD",
                     shipping: float = 0.0, in_stock: bool = True) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO price_snapshots (product_id, price, currency, shipping, in_stock)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, price, currency, shipping, 1 if in_stock else 0))
        self.conn.commit()
        return cursor.lastrowid

    def get_latest_price(self, product_id: int) -> Optional[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT price, currency, shipping, in_stock, captured_at
            FROM price_snapshots
            WHERE product_id = ?
            ORDER BY captured_at DESC
            LIMIT 1
        """, (product_id,))
        row = cursor.fetchone()
        if row:
            return {
                "price": row[0],
                "currency": row[1],
                "shipping": row[2],
                "in_stock": bool(row[3]),
                "captured_at": row[4]
            }
        return None

    def get_previous_price(self, product_id: int) -> Optional[dict]:
        """Get the second-to-last price for comparison."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT price, currency, shipping, captured_at
            FROM price_snapshots
            WHERE product_id = ?
            ORDER BY captured_at DESC
            LIMIT 1 OFFSET 1
        """, (product_id,))
        row = cursor.fetchone()
        if row:
            return {
                "price": row[0],
                "currency": row[1],
                "shipping": row[2],
                "captured_at": row[4]
            }
        return None

    def get_price_history(self, product_id: int, days: int = 30) -> list:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT price, currency, captured_at
            FROM price_snapshots
            WHERE product_id = ? AND captured_at >= datetime('now', ?)
            ORDER BY captured_at ASC
        """, (product_id, f'-{days} days'))
        return [
            {"price": row[0], "currency": row[1], "captured_at": row[2]}
            for row in cursor.fetchall()
        ]

    def get_all_active_products(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, platform, url, target_price, currency
            FROM watchlist
            WHERE active = 1
        """)
        return [
            {
                "id": row[0],
                "name": row[1],
                "platform": row[2],
                "url": row[3],
                "target_price": row[4],
                "currency": row[5]
            }
            for row in cursor.fetchall()
        ]

    def create_alert(self, product_id: int, old_price: float,
                     new_price: float, change_percent: float,
                     alert_type: str = "price_drop") -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (product_id, old_price, new_price, change_percent, alert_type)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, old_price, new_price, change_percent, alert_type))
        self.conn.commit()
        return cursor.lastrowid

    def close(self):
        self.conn.close()


# --- Platform Scrapers (Simplified for MVP) ---

class PriceScraper:
    """Base scraper for extracting prices from e-commerce platforms."""

    HEADERS = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36"),
        "Accept-Language": "en-US,en;q=0.9",
    }

    @staticmethod
    def extract_amazon_price(url: str) -> Optional[dict]:
        """
        Extract price from an Amazon product page.
        Uses the Amazon Product API if configured, otherwise parses HTML.
        """
        try:
            resp = requests.get(url, headers=PriceScraper.HEADERS, timeout=15)
            resp.raise_for_status()
            text = resp.text

            # Try to find price in the page
            # Note: Amazon uses dynamic loading; this is a simplified approach
            price_selectors = [
                'class="a-price-whole"',  # Standard price
                'id="priceblock_ourprice"',  # Legacy price block
                'id="priceblock_dealprice"',  # Deal price
                'class="a-offscreen"',  # Screen-reader price
            ]

            price = None
            for selector in price_selectors:
                idx = text.find(selector)
                if idx != -1:
                    # Find the actual price value nearby
                    # This is a simplified extraction — real MVP would use BS4
                    snippet = text[idx:idx + 200]
                    import re
                    price_match = re.search(r'\$?([0-9]+,[0-9]+\.\d{2}|\$?[0-9]+\.\d{2})', snippet)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '')
                        price = float(price_str)
                        break

            if price is None:
                # Fallback: search entire page for price pattern
                import re
                all_prices = re.findall(r'\$?([0-9]+\.[0-9]{2})', text)
                # Filter to reasonable product prices
                all_prices = [float(p) for p in all_prices if 0.99 < float(p) < 99999]
                if all_prices:
                    price = min(all_prices)  # Most likely the product price

            in_stock = "out of stock" not in text.lower()

            if price:
                return {
                    "price": price,
                    "currency": "USD",
                    "in_stock": in_stock,
                    "platform": "amazon"
                }
            return None

        except Exception as e:
            print(f"Error scraping Amazon URL {url}: {e}")
            return None

    @staticmethod
    def extract_walmart_price(url: str) -> Optional[dict]:
        """Extract price from a Walmart product page."""
        try:
            resp = requests.get(url, headers=PriceScraper.HEADERS, timeout=15)
            resp.raise_for_status()
            text = resp.text

            import re
            price_match = re.search(r'"price":\s*"?([0-9]+\.[0-9]{2})"?', text)
            if not price_match:
                price_match = re.search(r'\$?([0-9]+\.[0-9]{2})', text)

            if price_match:
                return {
                    "price": float(price_match.group(1)),
                    "currency": "USD",
                    "in_stock": "out of stock" not in text.lower(),
                    "platform": "walmart"
                }
            return None

        except Exception as e:
            print(f"Error scraping Walmart URL {url}: {e}")
            return None

    @staticmethod
    def extract_generic_price(url: str, platform: str = "shopify") -> Optional[dict]:
        """Generic price extractor for Shopify, Etsy, and other sites."""
        try:
            resp = requests.get(url, headers=PriceScraper.HEADERS, timeout=15)
            resp.raise_for_status()
            text = resp.text

            import re
            # Look for common price patterns in product pages
            price_patterns = [
                r'"price":\s*"([0-9]+\.[0-9]{2})"',
                r'"price":\s*([0-9]+\.[0-9]{2})',
                r'\$([0-9]+\.[0-9]{2})',
                r'€([0-9]+\.[0-9]{2})',
                r'£([0-9]+\.[0-9]{2})',
                r'CN¥([0-9]+\.[0-9]{2})',
            ]

            for pattern in price_patterns:
                match = re.search(pattern, text)
                if match:
                    price = float(match.group(1))
                    if 0.99 < price < 99999:
                        return {
                            "price": price,
                            "currency": "USD",
                            "in_stock": "out of stock" not in text.lower(),
                            "platform": platform
                        }

            return None

        except Exception as e:
            print(f"Error scraping {platform} URL {url}: {e}")
            return None

    @classmethod
    def extract_price(cls, url: str, platform: str) -> Optional[dict]:
        """Route to the appropriate platform extractor."""
        platform_map = {
            "amazon": cls.extract_amazon_price,
            "walmart": cls.extract_walmart_price,
            "shopify": cls.extract_generic_price,
            "etsy": cls.extract_generic_price,
        }
        extractor = platform_map.get(platform.lower(), cls.extract_generic_price)
        if platform.lower() in ("shopify", "etsy", "generic"):
            return extractor(url, platform)
        return extractor(url)


# --- Alert Engine ---

class AlertEngine:
    """Manages alert generation and delivery."""

    def __init__(self, config: dict):
        self.config = config.get("alerts", {})

    def check_and_alert(self, db: PriceDatabase, product: dict,
                        old_price: Optional[float], new_price: float) -> Optional[dict]:
        """Check if a price change warrants an alert and send it."""
        if old_price is None or old_price == 0:
            return None  # First scan, no comparison yet

        change_percent = ((new_price - old_price) / old_price) * 100
        threshold = abs(self.config.get("threshold_percent", 5.0))

        # Check if change exceeds threshold
        if abs(change_percent) < threshold:
            return None

        # Create alert in database
        alert_type = "price_drop" if change_percent < 0 else "price_increase"
        alert_id = db.create_alert(
            product["id"], old_price, new_price, change_percent, alert_type
        )

        alert_data = {
            "id": alert_id,
            "product": product["name"],
            "platform": product["platform"],
            "old_price": old_price,
            "new_price": new_price,
            "change_percent": round(change_percent, 2),
            "alert_type": alert_type,
            "detected_at": datetime.now(timezone.utc).isoformat(),
            "recommendation": self._generate_recommendation(alert_type, change_percent)
        }

        # Send notifications
        self._send_slack(alert_data)
        self._send_telegram(alert_data)

        return alert_data

    def _generate_recommendation(self, alert_type: str,
                                  change_percent: float) -> str:
        """Generate AI-contextualized recommendation."""
        if alert_type == "price_drop":
            if abs(change_percent) > 15:
                return ("Significant price drop detected. Consider matching or "
                        "investigating if this is a clearance sale or permanent "
                        "price change.")
            elif abs(change_percent) > 10:
                return ("Moderate price drop. Evaluate if you should adjust "
                        "your pricing to remain competitive.")
            else:
                return ("Minor price adjustment. Monitor for further changes.")
        else:
            if change_percent > 15:
                return ("Large price increase. This may indicate supply issues "
                        "or market shift — consider this an opportunity to gain "
                        "market share.")
            elif change_percent > 10:
                return ("Notable price increase. Your price advantage has "
                        "improved — consider capitalizing on this in your marketing.")
            else:
                return ("Minor price increase. No immediate action needed, "
                        "but continue monitoring.")

    def _send_slack(self, alert: dict) -> bool:
        """Send alert to Slack webhook."""
        webhook = self.config.get("slack_webhook")
        if not webhook:
            return False

        # Rate limiting / cooldown check
        cooldown = self.config.get("cooldown_minutes", 30)

        try:
            message = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"📊 Price Alert: {alert['product']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Platform:* {alert['platform']}"},
                            {"type": "mrkdwn", "text": f"*Change:* {alert['change_percent']:+.2f}%"},
                            {"type": "mrkdwn", "text": f"*Old Price:* ${alert['old_price']:.2f}"},
                            {"type": "mrkdwn", "text": f"*New Price:* ${alert['new_price']:.2f}"},
                        ]
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"💡 *Recommendation:* {alert['recommendation']}"}
                    }
                ]
            }
            resp = requests.post(webhook, json=message, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"Slack notification failed: {e}")
            return False

    def _send_telegram(self, alert: dict) -> bool:
        """Send alert to Telegram bot."""
        bot_token = self.config.get("telegram_bot_token")
        chat_id = self.config.get("telegram_chat_id")
        if not bot_token or not chat_id:
            return False

        try:
            text = (
                f"📊 *Price Alert: {alert['product']}*\n"
                f"Platform: {alert['platform']}\n"
                f"Change: {alert['change_percent']:+.2f}%\n"
                f"Old: ${alert['old_price']:.2f} → New: ${alert['new_price']:.2f}\n\n"
                f"💡 {alert['recommendation']}"
            )
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            resp = requests.post(url, json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"Telegram notification failed: {e}")
            return False


# --- Main Application ---

class PriceWatchApp:
    """Main application controller."""

    def __init__(self):
        self.db = PriceDatabase()
        self.config = self._load_config()
        self.alert_engine = AlertEngine(self.config)

    def _load_config(self) -> dict:
        """Load configuration from YAML file or return defaults."""
        try:
            import yaml
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
        except ImportError:
            # Fallback: try to parse as JSON
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    content = f.read()
                    try:
                        import json
                        return json.loads(content)
                    except json.JSONDecodeError:
                        pass
        return {}

    def scan(self) -> dict:
        """Run a full scan of all active products."""
        products = self.db.get_all_active_products()
        results = {
            "status": "success",
            "scan_id": f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "products_scanned": 0,
            "alerts_triggered": 0,
            "alerts": [],
            "errors": []
        }

        for product in products:
            try:
                print(f"Scanning: {product['name']} ({product['platform']})...")
                price_data = PriceScraper.extract_price(
                    product["url"], product["platform"]
                )

                if price_data is None:
                    results["errors"].append({
                        "product": product["name"],
                        "error": "Failed to extract price"
                    })
                    continue

                # Record the price
                self.db.record_price(
                    product["id"],
                    price_data["price"],
                    price_data.get("currency", "USD"),
                    price_data.get("shipping", 0.0),
                    price_data.get("in_stock", True)
                )
                results["products_scanned"] += 1

                # Check for price change alert
                prev = self.db.get_previous_price(product["id"])
                old_price = prev["price"] if prev else None

                print(f"  Current: ${price_data['price']:.2f} | "
                      f"Previous: ${old_price:.2f if old_price else 'N/A'}")

                alert = self.alert_engine.check_and_alert(
                    self.db, product, old_price, price_data["price"]
                )
                if alert:
                    results["alerts_triggered"] += 1
                    results["alerts"].append(alert)
                    print(f"  ⚠ Alert triggered: {alert['change_percent']:+.2f}%")

            except Exception as e:
                results["errors"].append({
                    "product": product.get("name", "unknown"),
                    "error": str(e)
                })
                print(f"  ✗ Error: {e}")

        # Calculate next scan time
        interval = self.config.get("schedule", {}).get("interval_minutes", 60)
        next_scan = datetime.now(timezone.utc).timestamp() + (interval * 60)
        results["next_scheduled_scan"] = datetime.fromtimestamp(
            next_scan, tz=timezone.utc
        ).isoformat()

        return results

    def add_product(self, url: str, target_price: Optional[float] = None,
                    platform: Optional[str] = None, name: Optional[str] = None):
        """Add a new product to the watchlist."""
        if platform is None:
            # Auto-detect platform from URL
            url_lower = url.lower()
            if "amazon" in url_lower:
                platform = "amazon"
            elif "walmart" in url_lower:
                platform = "walmart"
            elif "shopify" in url_lower or "myshopify" in url_lower:
                platform = "shopify"
            elif "etsy" in url_lower:
                platform = "etsy"
            else:
                platform = "generic"

        if name is None:
            name = url.split("/")[-1].replace("-", " ").title()[:50]

        product_id = self.db.add_product(name, platform, url, target_price)
        return {
            "status": "success",
            "product_id": product_id,
            "name": name,
            "platform": platform,
            "url": url,
            "target_price": target_price
        }

    def get_history(self, product_name: str, days: int = 30) -> dict:
        """Get price history for a product."""
        products = self.db.get_all_active_products()
        product = next(
            (p for p in products if product_name.lower() in p["name"].lower()),
            None
        )
        if not product:
            return {"status": "error", "message": f"Product '{product_name}' not found"}

        history = self.db.get_price_history(product["id"], days)
        return {
            "status": "success",
            "product": product,
            "history": history,
            "summary": {
                "current_price": history[-1]["price"] if history else None,
                "lowest_price": min(h["price"] for h in history) if history else None,
                "highest_price": max(h["price"] for h in history) if history else None,
                "average_price": (
                    sum(h["price"] for h in history) / len(history) if history else None
                ),
                "data_points": len(history)
            }
        }

    def generate_report(self) -> dict:
        """Generate a competitive market position report."""
        products = self.db.get_all_active_products()
        report_data = []

        for product in products:
            history = self.db.get_price_history(product["id"], 30)
            latest = self.db.get_latest_price(product["id"])

            if not history or not latest:
                continue

            prices = [h["price"] for h in history]
            report_data.append({
                "name": product["name"],
                "platform": product["platform"],
                "current_price": latest["price"],
                "lowest_30d": min(prices),
                "highest_30d": max(prices),
                "average_30d": sum(prices) / len(prices),
                "volatility": round(
                    (max(prices) - min(prices)) / sum(prices) * len(prices) * 100, 2
                ) if prices else 0,
                "trend": self._calculate_trend(prices),
                "target_price": product.get("target_price"),
                "below_target": (
                    latest["price"] <= product["target_price"]
                    if product.get("target_price") else None
                )
            })

        return {
            "status": "success",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "products_monitored": len(report_data),
            "products": report_data
        }

    def _calculate_trend(self, prices: list) -> str:
        """Calculate price trend from historical data."""
        if len(prices) < 3:
            return "insufficient_data"

        recent = prices[-3:]
        if recent[2] < recent[0]:
            return "downward"
        elif recent[2] > recent[0]:
            return "upward"
        return "stable"

    def close(self):
        self.db.close()


# --- CLI Entry Point ---

def main():
    parser = argparse.ArgumentParser(
        description="PriceWatch - Cross-Platform Competitive Price Monitor"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Run a full price scan on all watchlisted products"
    )
    parser.add_argument(
        "--add", action="store_true",
        help="Add a product to the watchlist (requires --url)"
    )
    parser.add_argument("--url", type=str, help="Product URL to monitor")
    parser.add_argument("--target", type=float,
                        help="Target price for alert threshold")
    parser.add_argument("--platform", type=str,
                        choices=["amazon", "walmart", "shopify", "etsy"],
                        help="Platform of the product")
    parser.add_argument("--name", type=str, help="Product display name")
    parser.add_argument("--history", action="store_true",
                        help="Show price history for a product")
    parser.add_argument("--product", type=str,
                        help="Product name for history lookup")
    parser.add_argument("--days", type=int, default=30,
                        help="Days of history to show")
    parser.add_argument("--report", action="store_true",
                        help="Generate competitive market report")
    parser.add_argument("--output", type=str,
                        choices=["json", "text"], default="text",
                        help="Output format")

    args = parser.parse_args()

    app = PriceWatchApp()

    try:
        if args.scan:
            result = app.scan()
        elif args.add:
            if not args.url:
                print("Error: --url is required when adding a product")
                sys.exit(1)
            result = app.add_product(args.url, args.target,
                                     args.platform, args.name)
        elif args.history:
            if not args.product:
                print("Error: --product is required for history lookup")
                sys.exit(1)
            result = app.get_history(args.product, args.days)
        elif args.report:
            result = app.generate_report()
        else:
            parser.print_help()
            sys.exit(0)

        if args.output == "json":
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_output(result))

    finally:
        app.close()


def format_output(result: dict) -> str:
    """Format output for human-readable display."""
    lines = []
    status = result.get("status", "unknown")

    if "scan_id" in result:
        lines.append("=" * 60)
        lines.append(f"  PriceWatch Scan Report")
        lines.append(f"  Scan ID: {result['scan_id']}")
        lines.append("=" * 60)
        lines.append(f"  Products scanned: {result['products_scanned']}")
        lines.append(f"  Alerts triggered: {result['alerts_triggered']}")
        lines.append("")

        if result["alerts"]:
            lines.append("  -- ALERTS --")
            for alert in result["alerts"]:
                direction = "DOWN" if alert["change_percent"] < 0 else "UP"
                lines.append(
                    f"  [{direction}] {alert['product']} on {alert['platform']}: "
                    f"${alert['old_price']:.2f} -> ${alert['new_price']:.2f} "
                    f"({alert['change_percent']:+.2f}%)"
                )
                lines.append(f"     > {alert['recommendation']}")
            lines.append("")

        if result.get("errors"):
            lines.append(f"  Errors: {len(result['errors'])}")
            for err in result["errors"]:
                lines.append(f"    ✗ {err.get('product', '?')}: {err.get('error', '?')}")

        lines.append(f"  Next scan: {result.get('next_scheduled_scan', 'N/A')}")

    elif "product_id" in result:
        lines.append(f"  ✓ Added to watchlist:")
        lines.append(f"    Product: {result.get('name', '?')}")
        lines.append(f"    Platform: {result.get('platform', '?')}")
        lines.append(f"    Target price: ${result.get('target_price', 0):.2f}")
        lines.append(f"    Product ID: {result.get('product_id', '?')}")

    elif "summary" in result:
        prod = result.get("product", {})
        summary = result.get("summary", {})
        lines.append(f"  Price History: {prod.get('name', '?')}")
        lines.append(f"  Platform: {prod.get('platform', '?')}")
        lines.append("-" * 40)
        lines.append(f"  Current: ${summary.get('current_price', 0):.2f}")
        lines.append(f"  30-day low: ${summary.get('lowest_price', 0):.2f}")
        lines.append(f"  30-day high: ${summary.get('highest_price', 0):.2f}")
        lines.append(f"  30-day avg: ${summary.get('average_price', 0):.2f}")
        lines.append(f"  Data points: {summary.get('data_points', 0)}")

        history = result.get("history", [])
        if history:
            lines.append("")
            lines.append("  Recent prices:")
            for h in history[-10:]:
                lines.append(f"    {h['captured_at'][:16]}  ${h['price']:.2f}")

    elif "products" in result:
        lines.append("=" * 60)
        lines.append("  Competitive Market Report")
        lines.append("=" * 60)
        lines.append(f"  Products monitored: {result.get('products_monitored', 0)}")
        lines.append(f"  Generated: {result.get('generated_at', '?')[:16]}")
        lines.append("")
        for p in result.get("products", []):
            lines.append(f"  {p['name']} ({p['platform']})")
            lines.append(f"    Current: ${p['current_price']:.2f}")
            lines.append(f"    30d range: ${p['lowest_30d']:.2f} - ${p['highest_30d']:.2f}")
            lines.append(f"    Trend: {p.get('trend', 'N/A')}")
            if p.get('below_target') is not None:
                status = "✓ Below target" if p['below_target'] else "✗ Above target"
                lines.append(f"    Target: ${p.get('target_price', 0):.2f} ({status})")
            lines.append("")

    elif status == "error":
        lines.append(f"  ✗ Error: {result.get('message', 'Unknown error')}")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
