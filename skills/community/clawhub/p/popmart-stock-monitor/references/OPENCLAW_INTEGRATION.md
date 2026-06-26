# OpenClaw Integration Guide

## Using PopMart Stock Monitor with OpenClaw

### Method 1: Direct Command Execution

You can run the monitor directly through OpenClaw's exec tool:

```
/exec python /Users/panda/.openclaw/workspace/popmart-stock-monitor/scripts/monitor_stars_series.py
```

### Method 2: Create a Cron Job for Automated Monitoring

Set up automatic monitoring with OpenClaw's cron system:

```bash
# Check every 30 minutes during business hours (9 AM - 9 PM)
openclaw cron add --name "popmart-stars-monitor" --cron "*/30 9-21 * * *" --message "Check PopMart stars series stock status"
```

### Method 3: Interactive Monitoring Commands

Create custom commands for specific actions:

#### Check Current Status
```
Check current stock status for 星星人怦然星动系列
```

#### Set Up Monitoring
```
Start monitoring PopMart stars series for restock alerts
```

#### Stop Monitoring  
```
Stop PopMart stock monitoring
```

## Configuration for OpenClaw

### Feishu Notification Setup

Since you're using Feishu, update your config:

```json
{
  "notification": {
    "channel": "feishu",
    "webhook_url": "YOUR_FEISHU_BOT_WEBHOOK"
  }
}
```

To get your Feishu webhook:
1. Create a bot in your Feishu chat/group
2. Copy the webhook URL from bot settings
3. Update the config file

### Simplified Usage Prompts

You can use these natural language prompts:

- "Monitor PopMart stars series stock"
- "Check if 星星人怦然星动系列 is back in stock"  
- "Alert me when PopMart 899元 stars series is available"
- "Track availability of PopMart 搪胶毛绒公仔礼盒"

## Example Workflow

### Step 1: Initial Setup
```
I want to monitor the PopMart stars series product
```

### Step 2: Configuration
OpenClaw will:
- Load the popmart-stock-monitor skill
- Create default configuration for your product
- Ask for notification preferences

### Step 3: Monitoring
- Automatic checks every 30 minutes
- Instant alerts when product is back in stock
- Status updates on demand

## Limitations in OpenClaw Context

### Network Restrictions
- If external network access is blocked (as in your current environment), monitoring will be limited
- Consider running monitoring on a machine with internet access

### Persistent Monitoring
- Background processes may be limited in some OpenClaw deployments
- Cron jobs are more reliable for persistent monitoring

## Recommended Approach for Your Setup

Given your current network restrictions:

1. **Use Offline Mode**: Configure the monitor to run when you have internet access
2. **Manual Checks**: Use OpenClaw to manually trigger stock checks when needed
3. **External Server**: Consider running the monitor on a cloud server with full internet access

### Manual Check Command Template
```
/exec timeout 30 python /Users/panda/.openclaw/workspace/popmart-stock-monitor/scripts/monitor_stars_series.py --check-once
```

This approach gives you flexibility while working within your network constraints.