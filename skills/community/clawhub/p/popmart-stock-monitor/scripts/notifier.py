"""
Notification module for PopMart stock alerts
Supports multiple notification channels
"""

import requests
import json
import logging

logger = logging.getLogger(__name__)

def send_notification(alert_data: dict, config: dict):
    """
    Send stock alert notification via configured channel
    """
    channel = config.get('channel', 'console')
    
    if channel == 'feishu':
        _send_feishu_notification(alert_data, config)
    elif channel == 'email':
        _send_email_notification(alert_data, config)
    elif channel == 'console':
        _send_console_notification(alert_data)
    else:
        logger.warning(f"Unknown notification channel: {channel}")

def _send_feishu_notification(alert_data: dict, config: dict):
    """Send notification to Feishu webhook"""
    try:
        webhook_url = config.get('webhook_url')
        if not webhook_url:
            logger.error("Feishu webhook URL not configured")
            return
            
        message = {
            "msg_type": "text",
            "content": {
                "text": f"""🚨 POPMART RESTOCK ALERT 🚨
Product: {alert_data['product_name']}
Platform: {alert_data['platform'].upper()}
Status: Back in Stock!
Link: {alert_data['product_url']}
Price: {alert_data['price']}
Last Checked: {alert_data['timestamp']}"""
            }
        }
        
        response = requests.post(webhook_url, json=message, timeout=10)
        if response.status_code == 200:
            logger.info("Feishu notification sent successfully")
        else:
            logger.error(f"Feishu notification failed: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Feishu notification error: {e}")

def _send_email_notification(alert_data: dict, config: dict):
    """Send email notification (placeholder)"""
    # Email implementation would require SMTP configuration
    logger.info(f"Email notification would be sent for {alert_data['product_name']}")
    pass

def _send_console_notification(alert_data: dict):
    """Send console notification"""
    print(f"""
🚨 POPMART RESTOCK ALERT 🚨
Product: {alert_data['product_name']}
Platform: {alert_data['platform'].upper()}
Status: Back in Stock!
Link: {alert_data['product_url']}
Price: {alert_data['price']}
Last Checked: {alert_data['timestamp']}
""")

# Example usage
if __name__ == "__main__":
    test_alert = {
        'product_name': 'Molly Ocean Series',
        'platform': 'jd',
        'product_url': 'https://item.jd.com/123456.html',
        'price': '¥599',
        'timestamp': '2026-04-08 08:30:00'
    }
    
    test_config = {'channel': 'console'}
    send_notification(test_alert, test_config)