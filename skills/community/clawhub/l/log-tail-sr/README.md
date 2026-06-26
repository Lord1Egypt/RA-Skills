# LogTail — Smart Log Monitor & Analyzer

Logs are noisy. LogTail finds the signal.

## Usage

```javascript
const { LogTail } = require('./src/log-tail');
const tail = new LogTail({
  files: ['./logs/app.log', './logs/error.log'],
  filters: {
    ignore: ['DEBUG', 'health_check'],
    highlight: ['ERROR', 'FATAL', 'timeout']
  }
});

tail.watch((entry) => {
  if (entry.severity === 'error') console.log('🔴', entry.message);
});

const summary = await tail.summarize({ period: '1h' });
```

## Summary Output

```
📋 Log Summary — Last Hour

Total: 12,847 entries
Errors: 23 (0.18%)
Warnings: 156 (1.2%)

Top errors:
  1. "Connection timeout" — 12x (clustered 2:15-2:20 PM)
  2. "Rate limit exceeded" — 8x (spread)
  3. "File not found" — 3x

Pattern: Timeout spike correlates with backup job at 2:15 PM
```

## Features

- **Real-time tailing** with smart filtering
- **Pattern detection** — recurring errors, time correlations
- **Noise reduction** — configurable ignore patterns
- **Anomaly detection** — "Error rate 3x normal"
- **Multi-file** — multiple log files simultaneously
- **Format agnostic** — JSON, plaintext, syslog, custom
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
