"""
automation_guidance.py — Automation setup guidance

Responsibilities:
- Build platform-agnostic automation intent
- Choose auto-config, semi-auto-config, or guide mode based on platform capabilities
- Output next-step setup suggestions or pending confirmation configurations
- Reference stable artifact types from artifact_renderer as default output targets

Design Principles:
- Generate platform-agnostic intent first, then adapt to specific platform
- OpenClaw/Hermes as priority adaptation targets
- For unknown or unavailable platforms, output guides, script templates, or copyable workflow templates
- Do not build cross-platform daemon or unified notification system
"""

import json
from typing import Optional, Dict, Any, List

# Frequency types
FREQUENCY_OPTIONS = ["daily", "weekday", "weekly", "custom"]
FREQUENCY_LABELS = {
    "daily": "Daily",
    "weekday": "Weekdays only",
    "weekly": "Weekly",
    "custom": "Custom",
}

# Output formats
OUTPUT_FORMATS = ["brief", "standard", "deep", "team_report", "discord", "wechat"]
OUTPUT_FORMAT_LABELS = {
    "brief": "Brief summary",
    "standard": "Standard daily brief",
    "deep": "Deep analysis",
    "team_report": "Team daily report",
    "discord": "Discord format",
    "wechat": "WeChat group format",
}

# Delivery channels
DELIVERY_CHANNELS = ["current_chat", "discord", "wechat", "slack", "email", "webhook", "file", "knowledge_base"]
DELIVERY_CHANNEL_LABELS = {
    "current_chat": "Current chat",
    "discord": "Discord channel",
    "wechat": "WeChat group",
    "slack": "Slack channel",
    "email": "Email",
    "webhook": "Webhook",
    "file": "Save to file",
    "knowledge_base": "Knowledge base",
}


def build_automation_intent(
    inputs: Dict[str, Any],
    preferences: Optional[dict] = None,
) -> Dict[str, Any]:
    """
    Build platform-agnostic automation intent.

    Parameters:
        inputs: User configuration, e.g., frequency, time, timezone, content_scope, etc.
        preferences: Local preferences dict

    Returns:
        Standardized automation intent structure
    """
    intent = {
        "version": "v1",
        "task_name": "daily_ai_news_brief",
        "schedule": {
            "frequency": inputs.get("frequency", "daily"),
            "time": inputs.get("time", "09:00"),
            "timezone": inputs.get("timezone", "Asia/Shanghai"),
            "weekdays_only": inputs.get("frequency") == "weekday",
        },
        "content": {
            "source": "ai_daily_news",
            "mode": inputs.get("content_mode", "latest"),
            "use_preferences": bool(preferences),
            "topics": preferences.get("topics", []) if preferences else [],
            "strict_filtering": preferences.get("strict_filtering", False) if preferences else False,
        },
        "output": {
            "language": preferences.get("language", "zh-CN") if preferences else "zh-CN",
            "format": inputs.get("output_format", "standard"),
            "target_style": inputs.get("target_style", "standard"),
        },
        "delivery": {
            "channel": inputs.get("channel", "current_chat"),
            "target": inputs.get("target", ""),
            "requires_platform_setup": True,
        },
        "platform": {
            "name": inputs.get("platform_name", "unknown"),
            "adapter": inputs.get("platform_adapter", "generic"),
        },
    }

    return intent


def format_automation_intent(intent: Dict[str, Any]) -> str:
    """Format automation intent as user-readable summary"""
    schedule = intent.get("schedule", {})
    output = intent.get("output", {})
    delivery = intent.get("delivery", {})
    platform = intent.get("platform", {})

    lines = [
        "## Automation Configuration Summary",
        "",
        "### Execution Schedule",
        "",
        f"- Frequency: {FREQUENCY_LABELS.get(schedule.get('frequency', 'daily'), schedule.get('frequency'))}",
        f"- Time: {schedule.get('time', '09:00')}",
        f"- Timezone: {schedule.get('timezone', 'Asia/Shanghai')}",
        "",
        "### Content Settings",
        "",
        f"- Content Mode: {intent.get('content', {}).get('mode', 'latest')}",
        f"- Use Preferences: {'Yes' if intent.get('content', {}).get('use_preferences') else 'No'}",
        "",
        "### Output Format",
        "",
        f"- Language: {output.get('language', 'zh-CN')}",
        f"- Format: {OUTPUT_FORMAT_LABELS.get(output.get('format', 'standard'), output.get('format'))}",
        "",
        "### Delivery Method",
        "",
        f"- Channel: {DELIVERY_CHANNEL_LABELS.get(delivery.get('channel', 'current_chat'), delivery.get('channel'))}",
        f"- Platform: {platform.get('name', 'unknown')}",
        "",
    ]

    return "\n".join(lines)


def choose_automation_mode(
    intent: Dict[str, Any],
    host_capabilities: Optional[Dict[str, bool]] = None,
) -> str:
    """
    Choose automation configuration mode.

    Returns:
        "auto": Can auto-configure (host platform supports task scheduling API)
        "semi": Semi-auto (provide config scripts or wizard)
        "guide": Output setup guide only
    """
    if not host_capabilities:
        return "guide"

    platform = intent.get("platform", {}).get("name", "").lower()

    if platform in ("openclaw", "hermes"):
        if host_capabilities.get("can_create_scheduled_tasks"):
            return "auto"
        if host_capabilities.get("has_task_config_ui"):
            return "semi"

    return "guide"


def select_platform_guide(platform: str) -> str:
    """
    Select corresponding setup guide based on platform.
    """
    platform = platform.lower()

    if platform == "openclaw":
        return get_openclaw_guide()
    elif platform == "hermes":
        return get_hermes_guide()
    else:
        return get_generic_guide()


def get_openclaw_guide() -> str:
    """OpenClaw platform automation setup guide"""
    return """
## OpenClaw Automation Setup Guide

### Method 1: Use Task Scheduler (Recommended)

1. Open OpenClaw Settings
2. Go to "Tasks" page
3. Create new task:
   - Name: Daily AI News Briefing
   - Schedule: Daily at 09:00 (Asia/Shanghai)
   - Command: `python /path/to/ai-daily-news/scripts/get_latest_news.py`
   - Output: Send to current chat or specified channel

### Method 2: Use Quick Commands

Add to OpenClaw Quick Commands:
```
When: Every day at 09:00
Do: Run ai-daily-news skill with latest
Send result to: #ai-news-channel
```
"""


def get_hermes_guide() -> str:
    """Hermes Agent platform automation setup guide"""
    return """
## Hermes Agent Automation Setup Guide

### Using Hermes Workflow

1. Create new Workflow in Hermes
2. Add Trigger: Schedule (daily at 09:00)
3. Add Action: Call AI Daily News Skill
4. Configure parameters:
   ```json
   {
     "skill": "ai-daily-news",
     "command": "get_latest_news",
     "args": ["--tier", "guest"]
   }
   ```
5. Configure output target: Specify channel or user

### Using Hermes Cron
Add to `~/.hermes/crontab`:
```
0 9 * * * hermes skill ai-daily-news get_latest_news | hermes send @channel
```
"""


def get_generic_guide() -> str:
    """Generic platform setup guide"""
    return """
## Generic Automation Setup Guide

### Method 1: Use System Cron (Linux/macOS)

Add to crontab:
```bash
# Edit crontab
crontab -e

# Add the following line (every day at 9 AM)
0 9 * * * cd /path/to/ai-daily-news && python scripts/get_latest_news.py >> /var/log/ai-news.log 2>&1
```

### Method 2: Use GitHub Actions

Create `.github/workflows/daily-ai-news.yml`:
```yaml
name: Daily AI News Briefing
on:
  schedule:
    - cron: '0 1 * * *'  # UTC time = 9 AM Beijing time
jobs:
  briefing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: python scripts/get_latest_news.py
        env:
          AINEWS_ACCESS_TOKEN: ${{ secrets.AINEWS_ACCESS_TOKEN }}
```

### Method 3: Use Launchd (macOS)
Create `~/Library/LaunchAgents/com.ai-daily-news.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.ai-daily-news.daily</string>
  <key>ProgramArguments</key>
  <array>
    <string>python3</string>
    <string>/path/to/scripts/get_latest_news.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
</dict>
</plist>
```
Then run: `launchctl load ~/Library/LaunchAgents/com.ai-daily-news.plist`

### Method 4: n8n / Zapier / Make

1. Create Schedule Trigger
2. Add HTTP Request to call AI Daily News API
3. Send results to target channels (Discord/Slack/Email, etc.)
"""


def get_configuration_wizard_steps() -> List[Dict[str, str]]:
    """Get configuration wizard step list"""
    return [
        {
            "step": "1",
            "title": "Choose frequency",
            "options": "daily, weekday, weekly, custom",
            "default": "daily",
        },
        {
            "step": "2",
            "title": "Choose time",
            "options": "HH:MM format, e.g., 09:00",
            "default": "09:00",
        },
        {
            "step": "3",
            "title": "Choose timezone",
            "options": "IANA format, e.g., Asia/Shanghai",
            "default": "Asia/Shanghai",
        },
        {
            "step": "4",
            "title": "Content scope",
            "options": "latest, topic_filtered, preference_based, weekly_summary",
            "default": "latest",
        },
        {
            "step": "5",
            "title": "Output format",
            "options": "brief, standard, deep, team_report, discord, wechat",
            "default": "standard",
        },
        {
            "step": "6",
            "title": "Notification channel",
            "options": "current_chat, discord, wechat, slack, email, webhook, file, knowledge_base",
            "default": "current_chat",
        },
        {
            "step": "7",
            "title": "Host platform",
            "options": "openclaw, hermes, other, unknown",
            "default": "unknown",
        },
    ]


def render_cron_script(intent: Dict[str, Any]) -> str:
    """Generate cron script from intent"""
    schedule = intent.get("schedule", {})
    frequency = schedule.get("frequency", "daily")
    time = schedule.get("time", "09:00")

    hour, minute = time.split(":")

    if frequency == "daily":
        cron_expr = f"{minute} {hour} * * *"
    elif frequency == "weekday":
        cron_expr = f"{minute} {hour} * * 1-5"
    elif frequency == "weekly":
        cron_expr = f"{minute} {hour} * * 1"  # Every Monday
    else:
        cron_expr = f"{minute} {hour} * * *"

    script = f"""#!/bin/bash
# AI Daily News Automation Script
# Generated for: {frequency} at {time}

# Cron expression: {cron_expr}
# Install with: crontab -e
# Add line: {cron_expr} /path/to/this/script.sh

cd "$(dirname "$0")"
python3 scripts/get_latest_news.py --timezone {schedule.get('timezone', 'Asia/Shanghai')}
"""
    return script
