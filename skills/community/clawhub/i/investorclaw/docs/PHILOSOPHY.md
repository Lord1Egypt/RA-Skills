# InvestorClaw: Software, Not Just a Skill

**Why Apache 2.0? Why not Clawhub?**

---

## The Distinction: Software vs Skill

InvestorClaw is **software**—not a skill you submit to Clawhub and let someone else distribute.

### Clawhub Skills (MIT-0)
- Owned by the hub operator
- Distributed through their infrastructure
- Your code runs in their environment
- You get discoverability, but lose control
- MIT-0: anyone can use, modify, resell without attribution
- Good for: prototype tools, niche utilities, demos

### InvestorClaw (Apache 2.0, Direct Install)
- You own the software
- Users install directly from your repo
- You control the release cycle, security, updates
- Commercial business model possible
- Apache 2.0: patent protection + attribution + dual-licensing capable
- Good for: serious software, commercial products, long-term projects

---

## Why This Matters

### For Developers
- **Full control**: Push updates whenever you want (no hub approval)
- **Security**: Respond to issues directly, no third-party delay
- **Commercialization**: Build premium features without hub restrictions
- **Licensing**: Apache 2.0 allows dual-licensing (open + proprietary tiers)

### For Users
- **Transparency**: Full source code, license, no surprise changes
- **Portability**: Can fork, self-host, run offline
- **Cost clarity**: Free tier is genuinely open-source; premium tier is optional paid service
- **Sustainability**: Supporting a real business model (not a hobbyist skill)

### For the Market
InvestorClaw competes with commercial tools (Bloomberg, Interactive Brokers, etc.), not hobby skills. Apache 2.0 + direct install signals:
- This is production software
- The authors stand behind it
- You can build a business with this
- Patent protection if needed

---

## The Free Tier + Premium Tier Model

**Free (Open Source, Apache 2.0)**
- Holdings analysis, portfolio tracking, news sentiment
- Self-hosted: Mac (OpenClaw) or Raspberry Pi (zeroclaw)
- Educational guardrails (single investor mode)
- No commercial licensing fees
- Community contributions welcome

**Premium (Proprietary, Paid)**
- Multi-portfolio management, tax optimization, advisor mode
- Cloud hosting + API access
- Compliance & audit trails
- Advanced consultation (tier-3 enrichment)
- Coming 2026

This model doesn't work on Clawhub (which requires MIT-0, no proprietary extensions). Direct installation enables it.

---

## Installation Path

```text
Without ClawHub: users had to fetch a shell installer from the project's
GitLab raw-file URL and pipe it to bash — an audit-flagged pattern that
distributors (zeroclaw skills audit, ClawHub static-analyzer) reasonably
block by default.

With ClawHub: users install the skill bundle through the hub CLI:
  clawhub install investorclaw
The bundle is signed, audited, and published with an immutable version
slug. The container image is pinned by sha256 digest. No raw shell-script
download is needed from the user's shell.
```

Direct install means:
- You control the distribution
- Users get the latest version immediately
- No approval process, no gating
- Security patches ship same-day

---

## Why Apache 2.0 Specifically?

| License | Patent Protection | Dual-License Capable | Commercial | Attribution | Free Software |
|---------|-------------------|----------------------|------------|-------------|---|
| MIT-0 | ❌ No | ❌ No | ✅ Yes | ❌ None | ✅ Yes |
| MIT | ❌ No | ❌ No | ✅ Yes | ✅ Required | ✅ Yes |
| Apache 2.0 | ✅ **Yes** | ✅ **Yes** | ✅ Yes | ✅ Required | ✅ Yes |
| GPL v3 | ✅ Yes | ❌ No | ❌ Restricted | ✅ Required | ✅ Yes (copyleft) |

Apache 2.0 is the sweet spot:
- **Patent protection**: If you have IP, your patents are granted to users (and they're safe using your code)
- **Dual-licensing**: You can license the same code as both open-source AND proprietary (premium tier)
- **Commercial viability**: Clear signal that you're building a business, not a hobby
- **Permissive**: Still allows commercial use, forks, modifications

---

## What This Means for Contributors

If you contribute to InvestorClaw:
- Your code is covered by Apache 2.0
- You retain ownership, but grant rights to the project
- You're contributing to both the open-source free tier AND enabling the commercial product
- See CONTRIBUTING.md for guidelines (coming soon)

---

## The Bottom Line

InvestorClaw is **enterprise-grade open-source software** with a **commercial business model**.

- **Not a hobby skill** — too much functionality, too many dependencies
- **Not trapped on Clawhub** — you need direct control
- **Not proprietary-first** — the core analysis/portfolio logic stays free and open
- **Not GPL-restricted** — you can build proprietary extensions

This is how serious software gets built and maintained long-term.

---

**Licensed under Apache 2.0.** See LICENSE for full terms.
