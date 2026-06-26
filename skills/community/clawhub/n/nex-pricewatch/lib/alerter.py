"""
Nex PriceWatch Alerter Module
Price change detection and notifications
Copyright 2026 Nex AI (Kevin Blancaflor)
MIT-0 License
"""

import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

from .config import (
    ALERT_INCREASE_PCT, ALERT_DECREASE_PCT,
    TELEGRAM_ENABLED, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    CURRENCY_SYMBOLS
)
from .storage import save_alert, get_target_by_id, mark_alert_sent


def detect_changes(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect price changes from scrape results and return alerts.
    """
    alerts = []

    for result in results:
        if not result.get('success'):
            continue

        change_info = result.get('change_info', {})
        if not change_info.get('change'):
            continue

        target_id = result['target_id']
        target = get_target_by_id(target_id)

        if change_info['type'] == 'increase':
            change_pct = change_info['change_pct']
            if change_pct >= ALERT_INCREASE_PCT:
                alert = {
                    'target_id': target_id,
                    'type': 'increase',
                    'old_price': change_info['old_price'],
                    'new_price': change_info['new_price'],
                    'change_pct': change_pct,
                    'target': target,
                    'result': result,
                    'message': format_price_alert(
                        target,
                        'increase',
                        change_info['old_price'],
                        change_info['new_price'],
                        change_pct
                    )
                }
                alerts.append(alert)
                save_alert(
                    target_id, 'increase',
                    change_info['old_price'],
                    change_info['new_price'],
                    change_pct,
                    alert['message']
                )

        elif change_info['type'] == 'decrease':
            change_pct = change_info['change_pct']
            if abs(change_pct) >= ALERT_DECREASE_PCT:
                alert = {
                    'target_id': target_id,
                    'type': 'decrease',
                    'old_price': change_info['old_price'],
                    'new_price': change_info['new_price'],
                    'change_pct': change_pct,
                    'target': target,
                    'result': result,
                    'message': format_price_alert(
                        target,
                        'decrease',
                        change_info['old_price'],
                        change_info['new_price'],
                        change_pct
                    )
                }
                alerts.append(alert)
                save_alert(
                    target_id, 'decrease',
                    change_info['old_price'],
                    change_info['new_price'],
                    change_pct,
                    alert['message']
                )

        elif change_info['type'] == 'new_price':
            alert = {
                'target_id': target_id,
                'type': 'new_price',
                'old_price': None,
                'new_price': change_info['new_price'],
                'change_pct': 0,
                'target': target,
                'result': result,
                'message': f"New price tracking started for {target['name']}: {_format_currency(change_info['new_price'], target.get('currency', 'EUR'))}"
            }
            alerts.append(alert)
            save_alert(
                target_id, 'new_price',
                None,
                change_info['new_price'],
                0,
                alert['message']
            )

    return alerts


def format_price_alert(target: Dict[str, Any], alert_type: str,
                       old_price: float, new_price: float,
                       change_pct: float) -> str:
    """Format a price alert message."""
    currency = target.get('currency', 'EUR')
    old_formatted = _format_currency(old_price, currency)
    new_formatted = _format_currency(new_price, currency)

    competitor_name = target.get('competitor_name', 'Competitor')
    target_name = target.get('name', 'Unknown')

    if alert_type == 'increase':
        return (
            f"{competitor_name} just RAISED their {target_name} "
            f"from {old_formatted} to {new_formatted} "
            f"(+{abs(change_pct):.1f}%) ⬆️"
        )
    elif alert_type == 'decrease':
        return (
            f"{competitor_name} just LOWERED their {target_name} "
            f"from {old_formatted} to {new_formatted} "
            f"({change_pct:.1f}%) ⬇️"
        )
    else:
        return f"Price update for {target_name}"


def format_price_dashboard(results: List[Dict[str, Any]]) -> str:
    """Format all prices as a dashboard overview."""
    lines = []
    lines.append("=" * 70)
    lines.append("PRICE WATCH DASHBOARD")
    lines.append("=" * 70)
    lines.append("")

    grouped = {}
    for result in results:
        if not result.get('success'):
            continue

        target = result.get('target')
        if not target:
            continue

        competitor = target.get('competitor_name', 'Unknown')
        if competitor not in grouped:
            grouped[competitor] = []

        grouped[competitor].append(result)

    for competitor, items in sorted(grouped.items()):
        lines.append(f"\n📊 {competitor}")
        lines.append("-" * 70)

        for item in items:
            target = item.get('target')
            price = item.get('price')
            currency = target.get('currency', 'EUR')
            price_str = _format_currency(price, currency) if price else "N/A"

            change_info = item.get('change_info', {})
            change_indicator = ""

            if change_info.get('change'):
                if change_info['type'] == 'increase':
                    change_pct = change_info['change_pct']
                    change_indicator = f" ⬆️ +{change_pct:.1f}%"
                elif change_info['type'] == 'decrease':
                    change_pct = change_info['change_pct']
                    change_indicator = f" ⬇️ {change_pct:.1f}%"

            name = target.get('name', 'Unknown')
            lines.append(f"  • {name}: {price_str}{change_indicator}")

    lines.append("\n" + "=" * 70)
    lines.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)

    return "\n".join(lines)


def send_telegram(message: str) -> bool:
    """Send message via Telegram."""
    if not TELEGRAM_ENABLED or not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return False


def send_alerts(alerts: List[Dict[str, Any]]) -> int:
    """Send all alerts and return count of sent."""
    sent_count = 0

    for alert in alerts:
        message = alert.get('message', '')

        if TELEGRAM_ENABLED:
            if send_telegram(message):
                mark_alert_sent(alert['target_id'])
                sent_count += 1
        else:
            # Just print if Telegram not enabled
            print(message)
            sent_count += 1

    return sent_count


def _format_currency(amount: float, currency: str = "EUR") -> str:
    """Format amount as currency string."""
    if amount is None:
        return "N/A"

    symbol = CURRENCY_SYMBOLS.get(currency, currency)

    # Format with 2 decimals
    if isinstance(amount, float):
        formatted = f"{amount:,.2f}"
    else:
        formatted = str(amount)

    return f"{symbol}{formatted}"
