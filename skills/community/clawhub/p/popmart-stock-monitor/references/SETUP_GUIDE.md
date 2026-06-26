# PopMart Stock Monitor Setup Guide

## Prerequisites

### 1. Python Environment
```bash
# Ensure Python 3.8+ is installed
python3 --version

# Create virtual environment (recommended)
python3 -m venv popmart-env
source popmart-env/bin/activate  # On Windows: popmart-env\Scripts\activate
```

### 2. Required Dependencies
```bash
pip install requests beautifulsoup4 selenium playwright
playwright install chromium
```

### 3. Platform API Access (Optional but Recommended)

#### Taobao Open Platform
1. Register as Taobao developer at [Taobao Open Platform](https://open.taobao.com/)
2. Create an application to get `app_key` and `app_secret`
3. Configure API permissions for product search

#### JD Open Platform  
1. Register at [JD Open Platform](https://jos.jd.com/)
2. Create application to get credentials
3. Enable product query APIs

### 4. Feishu Webhook (For Notifications)
1. In Feishu, create a bot in your desired chat/group
2. Copy the webhook URL
3. Update `notification.webhook_url` in config file

## Configuration

### 1. Create Configuration File
Copy the example config and customize:

```bash
cp references/example_config.json popmart_config.json
```

### 2. Edit Product List
Update the `products` array with your desired PopMart items:

```json
{
  "name": "Your Product Name",
  "sku": "Optional SKU", 
  "platforms": ["jd", "tmall", "taobao", "wechat"],
  "priority": ["jd", "tmall", "taobao", "wechat"]
}
```

### 3. Configure Notification
Set your preferred notification method:

```json
"notification": {
  "channel": "feishu",
  "webhook_url": "YOUR_FEISHU_WEBHOOK_URL"
}
```

## Usage

### Basic Usage
```bash
# Run with default config
python scripts/monitor_popmart.py

# Run with custom config
python scripts/monitor_popmart.py --config my_custom_config.json
```

### Integration with OpenClaw
To use this skill with OpenClaw:

1. **Install the skill**:
   ```bash
   # Move to OpenClaw skills directory
   cp -r popmart-stock-monitor ~/.npm-global/lib/node_modules/openclaw/skills/
   ```

2. **Use in conversation**:
   ```
   Monitor PopMart Molly Ocean series stock status
   Check if Labubu blind boxes are back in stock on JD
   Track Dimoo Space Adventure availability across all platforms
   ```

## Limitations & Troubleshooting

### Common Issues

#### 1. "Access Denied" Errors
- **Cause**: Platform anti-bot measures
- **Solution**: Use official APIs, implement delays between requests

#### 2. False Stock Alerts  
- **Cause**: Pre-order items showing as "in stock"
- **Solution**: Update stock detection logic in platform handlers

#### 3. Connection Timeouts
- **Cause**: Network restrictions or rate limiting
- **Solution**: Increase timeout values, use proxy servers

### Platform Reliability Ranking

1. **JD.com**: Most reliable (official API available)
2. **Tmall**: Good reliability (Taobao API)  
3. **Taobao**: Moderate reliability (API + scraping)
4. **WeChat**: Least reliable (frequent Mini Program changes)

## Maintenance

### Monthly Tasks
- Update CSS selectors (Chinese sites change frequently)
- Test with new PopMart product launches
- Rotate user agents to avoid detection
- Monitor API quota usage

### Security Considerations
- Store API keys securely (use environment variables)
- Implement reasonable request intervals (≥30 seconds)
- Respect platform terms of service
- Do not overload servers with excessive requests

## Advanced Features

### Custom Alert Conditions
Modify `send_stock_alert()` in `monitor_popmart.py` to add custom logic:
- Price thresholds
- Specific variant availability  
- Regional stock checks

### Multiple Notification Channels
Extend the notifier module to support:
- SMS alerts
- Email notifications  
- Desktop push notifications
- Discord/Slack webhooks

### Data Persistence
Add database logging to track:
- Historical stock patterns
- Price history
- Restock frequency analysis