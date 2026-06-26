"""
Nex Vault - Alert management
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sqlite3
import datetime as dt
import urllib.request
import urllib.parse
import json
from storage import (
    get_expiring_documents, save_key_clause, get_upcoming_alerts,
    mark_alert_sent, _connect, get_document_stats
)
from config import (
    ALERT_DAYS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_PATH,
    API_MIN_INTERVAL, API_MAX_RETRIES, API_BACKOFF_BASE
)
from doc_parser import calculate_notice_deadline


def check_upcoming_alerts(days=90):
    """Check all active documents for upcoming deadlines."""
    documents = get_expiring_documents(days)
    all_alerts = []

    for doc in documents:
        alerts = generate_alerts(doc)
        all_alerts.extend(alerts)

    return all_alerts


def generate_alerts(document):
    """For a single document, generate all applicable alerts."""
    alerts = []
    doc_id = document['id']
    end_date_str = document['end_date']

    if not end_date_str:
        return alerts

    try:
        end_date = dt.datetime.fromisoformat(end_date_str).date()
    except (ValueError, TypeError):
        return alerts

    today = dt.date.today()

    # Check each alert threshold
    for threshold_days in ALERT_DAYS:
        alert_date = end_date - dt.timedelta(days=threshold_days)

        if today >= alert_date and today < end_date:
            # Check if alert already exists
            with _connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id FROM alerts
                    WHERE document_id = ? AND alert_type = 'expiry'
                    AND alert_date = ?
                """, (doc_id, alert_date.isoformat()))

                if cursor.fetchone():
                    continue  # Alert already exists

            # Create new alert
            days_remaining = (end_date - today).days
            message = (
                f"Document '{document['name']}' expires in {days_remaining} day(s) "
                f"({end_date.isoformat()})"
            )

            with _connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts (document_id, alert_date, alert_type, message)
                    VALUES (?, ?, ?, ?)
                """, (doc_id, alert_date.isoformat(), 'expiry', message))
                alert_id = cursor.lastrowid

            alerts.append({
                'id': alert_id,
                'type': 'expiry',
                'message': message,
                'days_remaining': days_remaining,
            })

    # Check termination notice deadline
    notice_days = document.get('termination_notice_days')
    if notice_days:
        notice_deadline = calculate_notice_deadline(end_date_str, notice_days)
        if notice_deadline:
            notice_date = dt.datetime.fromisoformat(notice_deadline).date()
            if today >= notice_date and today < end_date:
                with _connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id FROM alerts
                        WHERE document_id = ? AND alert_type = 'termination_notice'
                    """, (doc_id,))

                    if not cursor.fetchone():
                        days_until = (notice_date - today).days
                        message = (
                            f"Termination notice due for '{document['name']}' "
                            f"by {notice_date.isoformat()} ({days_until} day(s) remaining)"
                        )
                        cursor.execute("""
                            INSERT INTO alerts (document_id, alert_date, alert_type, message)
                            VALUES (?, ?, ?, ?)
                        """, (doc_id, notice_date.isoformat(), 'termination_notice', message))

                        alerts.append({
                            'id': cursor.lastrowid,
                            'type': 'termination_notice',
                            'message': message,
                            'days_remaining': days_until,
                        })

    return alerts


def send_telegram_alert(message):
    """Send alert via Telegram bot API using urllib (no requests dependency)."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
    }).encode('utf-8')

    retries = 0
    while retries < API_MAX_RETRIES:
        try:
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('ok', False)
        except urllib.error.URLError as e:
            retries += 1
            if retries >= API_MAX_RETRIES:
                return False
            # Exponential backoff
            import time
            time.sleep(API_BACKOFF_BASE ** retries)
        except Exception:
            return False

    return False


def format_alert_message(alert):
    """Format alert for display/sending."""
    alert_type = alert.get('alert_type', 'expiry')
    message = alert.get('message', '')

    if alert_type == 'expiry':
        return f"EXPIRY ALERT: {message}"
    elif alert_type == 'termination_notice':
        return f"NOTICE REQUIRED: {message}"
    elif alert_type == 'renewal':
        return f"RENEWAL: {message}"
    else:
        return f"ALERT: {message}"


def run_daily_check():
    """Main function called by scheduler. Checks all documents, generates new alerts, sends notifications."""
    alerts = check_upcoming_alerts(days=90)

    summary = {
        'timestamp': dt.datetime.now().isoformat(),
        'total_alerts': len(alerts),
        'sent_count': 0,
        'failed_count': 0,
        'alerts': [],
    }

    for alert in alerts:
        formatted = format_alert_message(alert)
        summary['alerts'].append(formatted)

        # Send Telegram if configured
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            if send_telegram_alert(formatted):
                mark_alert_sent(alert['id'])
                summary['sent_count'] += 1
            else:
                summary['failed_count'] += 1

    return summary


def get_vault_summary():
    """Get a summary of vault status for display."""
    stats = get_document_stats()
    upcoming = get_upcoming_alerts(days=30)

    return {
        'total_documents': stats['total_documents'],
        'upcoming_alerts': len(upcoming),
        'total_monthly_cost': stats['total_monthly_cost'],
        'total_yearly_cost': stats['total_yearly_cost'],
        'by_type': stats['by_type'],
    }
