---
name: "NewsletterKit Email Newsletter Builder"
description: "Build and format email newsletters from agent-curated content. Sections, formatting, subscriber-friendly HTML output. Works with any email service."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["newsletter-kit"]
license: "MIT"
---

# NewsletterKit Email Newsletter Builder

Build and format email newsletters from agent-curated content. Sections, formatting, subscriber-friendly HTML output. Works with any email service.

---

Curate content through the week. Generate a formatted newsletter on publish day.

## Workflow

1. **Collect** — save links, notes, snippets during the week
2. **Curate** — agent organizes by section and relevance
3. **Draft** — generate newsletter copy with section intros
4. **Format** — output as HTML email, markdown, or plain text
5. **Review** — human approves final version
6. **Send** — export to your email service

## Usage

```javascript
const { NewsletterKit } = require('./src/newsletter-kit');
const kit = new NewsletterKit();

kit.addItem({ section: 'AI News', title: 'New model released', url: '...' });
kit.addItem({ section: 'Tools', title: 'Useful new library', url: '...' });

const newsletter = await kit.generate({
  name: 'Weekly AI Brief',
  intro: 'This week in AI...',
  format: 'html'
});
```

## Output Formats

- **HTML** — ready for Mailchimp, ConvertKit, or any ESP
- **Markdown** — for Substack, Ghost, or your own platform
- **Plain text** — for minimalist newsletters
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