# HeartbeatKit — Plug-and-Play Agent Heartbeat Configs

Your OpenClaw agent has a heartbeat system — periodic check-ins where it can do background work. But writing a good HEARTBEAT.md from scratch is tedious. HeartbeatKit gives you battle-tested templates.

## Quick Start

```bash
# Copy a template
cp templates/combined-lite.md /path/to/workspace/HEARTBEAT.md

# Edit variables
# That's it. Your agent picks it up automatically.
```

## Templates

### email-check.md
Checks for unread emails and surfaces anything urgent. Configurable urgency keywords and sender priority list.

### calendar-watch.md
Scans upcoming events (24-48h window). Alerts for conflicts, prep time needed, or travel requirements.

### weather-brief.md
Quick weather check for your location. Includes "should I bring an umbrella?" logic and severe weather alerts.

### system-health.md
Monitors disk space, memory usage, CPU load, and critical service status. Alerts on thresholds you set.

### news-digest.md
Pulls headlines from your configured topics. Summarizes top 5 stories. Rotates topics across heartbeats to save tokens.

### social-monitor.md
Checks mentions and notifications across configured platforms (Twitter, Discord, etc). Surfaces anything that needs a response.

### project-status.md
Git status for configured repos. Open PRs, failed builds, stale branches. Developer-focused.

### combined-lite.md
Email + calendar + weather in one heartbeat. The "daily driver" for most users. Rotates checks to stay under token budget.

### combined-full.md
Everything above, intelligently rotated. Checks 2-3 categories per heartbeat, cycles through all of them over the day. Includes quiet hours (no alerts 11 PM - 7 AM unless critical).

## Customization

Every template starts with a variables block:

```markdown
<!-- HEARTBEAT CONFIG -->
<!-- EMAIL_ACCOUNT: your@email.com -->
<!-- LOCATION: Denver, CO -->
<!-- QUIET_HOURS: 23:00-07:00 -->
<!-- CHECK_INTERVAL: 30m -->
```

Edit these to match your setup. The agent reads them as configuration.

## Writing Your Own

Use any template as a starting point. The pattern is:

1. **Check condition** (is there new email? is disk > 80%?)
2. **If yes:** alert with context
3. **If no:** move to next check or reply HEARTBEAT_OK
4. **Respect quiet hours** — unless it's critical

## Token Budget Tips

- Combined templates rotate checks to avoid burning tokens on every heartbeat
- News and social checks are the most expensive — schedule them 2-3x daily, not every heartbeat
- System health checks are cheap — run every time
- Set heartbeat interval to 30-60 minutes for balanced coverage
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
