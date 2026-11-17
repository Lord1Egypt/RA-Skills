---
name: hipaa-check
description: |
  HIPAA Compliance Check — Health Insurance Portability and Accountability Act (HIPAA), 45 C.F.R. Parts 160 & 164 (Privacy, Security, Breach Notification Rules).

  Free to install; scoring runs on the CQDev cloud compliance engine.
  No Key? The skill auto-runs an anonymous trial (5 real cloud-scored
  runs, 7-day window) before asking you to register. Covers 12 core items.
  Use when: the user asks to run the hipaa-check skill, or requests a
  HIPAA 医疗隐私合规检查 / Health Insurance Portability and Accountability Act (HIPAA), 45 C.F.R. Parts 160 & 164 (Privacy, Security, Breach Notification Rules).
  Trigger: hipaa-check, run hipaa check, HIPAA compliance check, 医疗隐私检查, 健康数据合规, HIPAA 合规
  Pricing: Free skill; cloud scoring uses points (Check 1 / Audit 10 per run) from compliancehub.cn
  ⚠️ Cloud scoring sends your answers to compliancehub.cn. The free preview (--non-interactive) fetches the latest check items from the cloud rule library but transmits NO answers; if the network is unavailable it falls back to the bundled item set. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 Account & free API Key are created on the website (compliancehub.cn) — not in the terminal.
  Open https://compliancehub.cn/account.html?skill=hipaa-check to register and get a Key instantly, then
  provide it via env `COMPLIANCEHUB_API_KEY` or save to ~/.config/compliancehub/hipaa-check.key (mode 0600).
  🌐 Language: bilingual (中文/English). Guidance and recommendations default to Chinese for Chinese-speaking compliance teams;
  legal and regulatory terms keep English originals. Users may request English output at any time.

  💡 Free preview: --non-interactive lists the 12 items without a Key
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 HIPAA 医疗隐私合规检查 — Free 检查 (Cloud-Scored)

## Overview
HIPAA 医疗隐私合规检查 is a **free** 检查 based on 美国《健康保险流通与责任法案》（HIPAA）及隐私规则/安全规则/违约通知规则（45 C.F.R. 160 & 164）.
It covers 12 core items. Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* 检查, your responses are
> transmitted to the CQDev cloud at `compliancehub.cn` for scoring. The free `--non-interactive` preview
> fetches the latest check items from the cloud rule library but transmits NO answers; it falls back to the
> bundled item set if the network is unavailable.

- The skill is free to install.
- Check items are served from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (12 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | Covered Entity / Business Associate | §160.102-.103 |
| 2 | Notice of Privacy Practices | Privacy Rule §164.520 |
| 3 | Valid Authorizations | §164.508 |
| 4 | Administrative Safeguards | Security Rule §164.308 |
| 5 | Physical Safeguards | §164.310 |
| 6 | Technical Safeguards | §164.312 |
| 7 | Breach Notification | Breach Rule §164.400+ |
| 8 | Minimum Necessary | §164.502(b) |
| 9 | Business Associate Agreements | §164.504(e) |
| 10 | Ongoing Risk Analysis | §164.308(a)(1)(ii)(A) |
| 11 | Workforce Training | §164.308(a)(5) |
| 12 | Individual Rights | §164.524/.526 |

## Usage
### Free preview (no Key)
```bash
python3 scripts/hipaa-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full 检查 — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
Open https://compliancehub.cn/account.html?skill=hipaa-check in your browser to register and get a free Key instantly.
Then provide it to the skill via env or key file:
```bash
export COMPLIANCEHUB_API_KEY=<your-key>
# or save to ~/.config/compliancehub/hipaa-check.key (mode 0600)
```

### Full 检查 + report
```bash
python3 scripts/hipaa-check.py --format html -o hipaa-check-report.html
```

## Agent guide
When a user asks for a HIPAA 医疗隐私合规检查:
1. Run `--non-interactive` to preview the 12 items (no Key needed).
2. Run the full 检查. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No account in the terminal:** Account creation and free API Key issuance happen on the website
  (compliancehub.cn). This skill never prompts for or transmits your email/password.
- **No persistence by default:** In preview mode (`--non-interactive`) it only reads the public rule library and
  sends NO answers. Scored runs persist only a local random `anon_id` (`~/.config/compliancehub/<slug>.anon_id`,
  0600, carries no personal data) used to continue the anonymous trial; your answers are never stored locally.
- **Where data goes:** Check items are fetched from, and your answers are scored by, the CQDev cloud at
  `https://compliancehub.cn` (the operator's official endpoint). Scoring transmits only your item answers, plus
  either the free API Key (as a Bearer token) when registered, or the local random anon_id during the anonymous trial.
- **API Key storage:** provided via env `COMPLIANCEHUB_API_KEY`, or saved to
  `~/.config/compliancehub/hipaa-check.key` (0600), outside the skill folder.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Not a rogue/autonomous agent:** The stored file is an ordinary API-key (0600), not an auto-start,
  session, or background process. No state is kept beyond that single key file.
- **Preview mode:** `--non-interactive` fetches the public check items from the cloud rule library but
  sends NO answers; it falls back to the bundled item set if the network is unavailable.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.

## License
MIT.
