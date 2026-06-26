---
name: popmart-stock-monitor
description: Monitor PopMart product restock status across multiple channels including WeChat Mini Programs, Taobao, JD.com, and Tmall. Use when user wants to track availability of specific PopMart products and receive notifications when items are back in stock.
---

# PopMart Stock Monitor

## Overview
This skill monitors PopMart product availability across major Chinese e-commerce platforms:
- WeChat Mini Programs (official PopMart store)
- Taobao 
- JD.com
- Tmall

## Setup Requirements

### API Keys & Authentication
- **Taobao/Tmall**: Requires Taobao Open Platform API access
- **JD.com**: Requires JD Open Platform API access  
- **WeChat**: Requires official Mini Program access or web scraping (limited)
- **Proxy/VPN**: May be needed for reliable access to Chinese platforms

### Installation
```bash
# Install required dependencies
pip install requests beautifulsoup4 selenium playwright
```

## Usage Examples

### Basic Product Monitoring
```
Monitor PopMart "Molly Ocean" series on all platforms
Check PopMart Labubu blind box stock status
Track availability of PopMart Dimoo Space series
```

### Advanced Configuration
```
Monitor PopMart product ID 12345 every 30 minutes
Check PopMart stock with priority: JD > Tmall > Taobao
Alert me via Feishu when PopMart Molly is back in stock
```

## Implementation Details

### Platform-Specific Handlers

#### WeChat Mini Program
- **Method**: Web scraping (requires mobile user-agent)
- **Limitations**: Rate limiting, requires session cookies
- **Reliability**: Medium (depends on Mini Program updates)

#### Taobao/Tmall  
- **Method**: Official API preferred, fallback to web scraping
- **Authentication**: OAuth 2.0 with Taobao developer account
- **Rate Limits**: 100 requests/minute per app

#### JD.com
- **Method**: Official JD Open Platform API
- **Authentication**: App key + secret authentication  
- **Rate Limits**: 50 requests/minute per app

### Stock Detection Logic
1. **Product Identification**: Match by product name, SKU, or official product ID
2. **Availability Check**: 
   - "In Stock" / "有货" status
   - Add-to-cart button enabled
   - Price displayed (not "sold out")
3. **False Positive Filtering**: 
   - Exclude pre-order items
   - Verify actual inventory vs display status

## Notification System

### Supported Channels
- **Feishu**: Webhook integration (recommended)
- **Email**: SMTP configuration required  
- **SMS**: Requires telecom API integration
- **Local**: Desktop notifications

### Alert Templates
```
🚨 POPMART RESTOCK ALERT 🚨
Product: {product_name}
Platform: {platform}
Status: Back in Stock! 
Link: {product_url}
Price: {price}
Last Checked: {timestamp}
```

## Configuration File
Create `popmart_config.json` in your workspace:

```json
{
  "products": [
    {
      "name": "Molly Ocean Series",
      "sku": "PM-MLY-OCEAN-2026",
      "platforms": ["wechat", "taobao", "jd", "tmall"],
      "priority": ["jd", "tmall", "taobao", "wechat"]
    }
  ],
  "check_interval_minutes": 30,
  "notification": {
    "channel": "feishu",
    "webhook_url": "YOUR_FEISHU_WEBHOOK_URL"
  },
  "api_keys": {
    "taobao_app_key": "YOUR_TAOBAO_APP_KEY",
    "taobao_app_secret": "YOUR_TAOBAO_APP_SECRET",
    "jd_app_key": "YOUR_JD_APP_KEY",
    "jd_app_secret": "YOUR_JD_APP_SECRET"
  }
}
```

## Limitations & Considerations

### Technical Challenges
- **Anti-bot measures**: Chinese platforms have aggressive bot detection
- **Session management**: WeChat Mini Programs require valid sessions
- **Rate limiting**: All platforms enforce strict rate limits
- **Dynamic content**: Heavy JavaScript rendering on some platforms

### Legal Compliance
- Respect robots.txt and terms of service
- Implement reasonable request intervals (≥30 seconds)
- Do not overload platform servers
- Use official APIs when available

### Reliability Notes
- **WeChat**: Most unreliable due to frequent Mini Program updates
- **Taobao/Tmall**: Moderate reliability with proper API access  
- **JD.com**: Most reliable with official API integration

## Troubleshooting

### Common Issues
1. **"Access Denied" errors**: Check API credentials and rate limits
2. **False stock alerts**: Adjust detection logic in `stock_detection.py`
3. **Connection timeouts**: Increase timeout values or use proxy
4. **Missing products**: Verify product identifiers and platform availability

### Debug Mode
Enable debug logging by setting `DEBUG=true` in environment:
```bash
DEBUG=true python popmart_monitor.py
```

## Maintenance
- Update selectors monthly (Chinese sites change frequently)
- Rotate user agents to avoid detection
- Monitor API quota usage
- Test with new PopMart product launches