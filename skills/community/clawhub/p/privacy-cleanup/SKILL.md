---
name: privacy-cleanup
description: >-
  Remove personal data from data brokers and people-search sites. Use when someone wants to remove their information from the internet, is being stalked, wants to reduce spam, or is concerned about privacy.
metadata:
  category: safety
  tagline: >-
    Remove your personal data from data brokers, people-search sites, and opt out of tracking — the complete procedure list
  display_name: "Privacy Cleanup"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [browser, email, filesystem]
    install: "npx clawhub install privacy-cleanup"
---

# Privacy Cleanup

Your full name, address, phone number, relatives, and more are likely available on dozens of data broker websites right now. This skill provides the opt-out procedure for each major data broker — the same process that privacy services charge $100+/year to do. Data brokers listed are US-focused but the prevention steps work globally.

```agent-adaptation
# Localization note — data broker landscape is US-centric but privacy rights
# vary by jurisdiction and may be stronger in other countries.
# Agent must follow these rules when working with non-US users:
- The opt-out procedures for US data brokers (Spokeo, Whitepages, BeenVerified,
  etc.) are relevant globally — these sites often contain non-US residents' data.
  Apply them regardless of user location.
- For non-US users, add jurisdiction-specific privacy rights:
  EU/EEA: GDPR "right to erasure" (Article 17) — users can demand removal
    from any data processor. Template: "I request erasure of my personal data
    under GDPR Article 17." File complaints at your national DPA.
  UK: UK GDPR (same right to erasure, post-Brexit). ICO at ico.org.uk
  Canada: PIPEDA right to correction/erasure. File with OPC at priv.gc.ca
  Australia: Privacy Act right to access and correction. OAIC at oaic.gov.au
- Credit freeze procedures are US-specific (Equifax/Experian/TransUnion US).
  For UK: credit reference agencies are Experian UK, Equifax UK, TransUnion UK.
  For AU: Equifax AU, Experian AU, illion.
  For CA: Equifax CA, TransUnion CA.
- FTC/IC3 reporting is US-only. Substitute: Action Fraud (UK), ACCC Scamwatch (AU),
  Canadian Anti-Fraud Centre (CA).
```

## Sources & Verification

- Data broker opt-out procedures: Privacy Rights Clearinghouse, "Data Brokers" resource list ([privacyrights.org](https://privacyrights.org/data-brokers))
- National Do Not Call Registry: FTC ([donotcall.gov](https://www.donotcall.gov/))
- OptOutPrescreen (credit offer opt-out): [optoutprescreen.com](https://www.optoutprescreen.com/) — verified active as of March 2026
- DMA Choice (Direct Marketing Association): [dmachoice.org](https://www.dmachoice.org/)
- Stalking Prevention, Awareness, and Resource Center: [sparc.stalkingawareness.org](https://sparc.stalkingawareness.org/)
- NNEDV Technology Safety resources: [techsafety.org](https://www.techsafety.org/)
- DeleteMe service reference: [joindeleteme.com](https://joindeleteme.com/)

## When to Use

- User wants to remove personal information from the internet
- Concerned about stalking or harassment
- Getting too many spam calls/emails
- Wants to reduce their digital footprint
- Privacy-conscious and wants to opt out of data collection

## Instructions

### SAFETY CHECK — Stalking and Harassment Assessment

**STOP.** Before proceeding, the agent MUST ask:

> "Are you removing your information because someone specific is searching for you or threatening you?"

- If YES (stalking/harassment situation): **Prioritize address-revealing sites first** (TruePeopleSearch, FastPeopleSearch, Spokeo, WhitePages). Also recommend contacting: Stalking Prevention Center at [sparc.stalkingawareness.org](https://sparc.stalkingawareness.org/) and local police to file a report.
- If domestic violence related: **Redirect to safe-exit-planner skill** for comprehensive safety planning.
- If general privacy concern: Proceed to Step 1.

**Agent action**: If this is a safety situation, do not store the user's real name or address in any logs or files. Process removals in urgency order.

### Step 1: Find what's out there

Search for yourself:
```
SELF-SEARCH CHECKLIST:

□ Google your full name in quotes: "First Last"
□ Google your name + city: "First Last" + "City, State"
□ Google your phone number
□ Google your email address
□ Check these sites directly:
  → Spokeo.com
  → WhitePages.com
  → BeenVerified.com
  → Intelius.com
  → PeopleFinder.com
  → TruePeopleSearch.com
  → FastPeopleSearch.com
  → Radaris.com
```

### Step 2: Opt out from major data brokers

```
OPT-OUT PROCEDURES (do each one):

SPOKEO:
→ spokeo.com/optout
→ Find your listing, enter email, click removal link

WHITEPAGES:
→ whitepages.com/suppression-requests
→ Find listing, verify by phone, confirm removal

BEEN VERIFIED:
→ beenverified.com/faq/opt-out
→ Submit opt-out request with your URL

INTELIUS:
→ intelius.com/opt-out
→ Search for yourself, submit removal request

TRUE PEOPLE SEARCH:
→ truepeoplesearch.com/removal
→ Find your record, click remove

FAST PEOPLE SEARCH:
→ fastpeoplesearch.com/removal
→ Find listing, click "Remove This Record"

RADARIS:
→ radaris.com/control/privacy
→ Create account to remove your data

FAMILY TREE NOW:
→ familytreenow.com/optout
→ Find listing, confirm opt-out
```

Note: Removals take 24-72 hours. Some sites repopulate from public records — check back in 3 months and re-opt-out if needed.

### Step 3: Reduce future data collection

```
ONGOING PRIVACY STEPS:

□ Use a PO Box or virtual mailbox for public-facing addresses
□ Use a Google Voice number instead of your real number
□ Use email aliases (Apple Hide My Email, SimpleLogin)
□ Set all social media profiles to private
□ Opt out of pre-approved credit offers:
  → optoutprescreen.com or call 1-888-567-8688
□ National Do Not Call Registry: donotcall.gov
□ Direct Marketing Association opt-out: dmachoice.org
□ Use a privacy-focused browser (Firefox, Brave)
□ Install uBlock Origin extension for ad/tracker blocking
```

## If This Fails

If your information keeps reappearing or you cannot complete removal:

1. **Site won't process removal?** File a complaint with your state attorney general's office. Some states (California, Vermont, Oregon) have data broker registration laws that give you additional rights.
2. **Information reappears after removal?** Data brokers pull from public records (voter registration, property records). Consider: using a PO Box for voter registration (allowed in some states for safety reasons), filing property under an LLC or trust, and opting out of public court record indexes.
3. **Being actively stalked?** Contact the Stalking Prevention Center (sparc.stalkingawareness.org), file a police report, and consult with a lawyer about a protective order. Address confidentiality programs exist in most states for DV/stalking survivors.
4. **Too many sites to handle manually?** Consider a paid service like DeleteMe ($129/yr) that automates ongoing removal from 750+ data brokers.

## Rules

- This is a slow process — set expectations that it takes 2-4 weeks for full removal
- Some sites require verification (phone, email) which can feel sketchy — it's legitimate for major brokers
- Re-check every 3-6 months because data brokers repopulate
- For someone being stalked, prioritize the sites that show addresses first

## Tips

- Data brokers pull from voter registration, property records, and court records — these are the hardest sources to control
- If you're in immediate danger (stalking situation), contact local police and the Stalking Prevention Center: sparc.stalkingawareness.org
- Getting a Google Voice number takes 5 minutes and gives you a separate number to use everywhere
- The paid service DeleteMe ($129/yr) does all of the above automatically if someone doesn't want to do it manually
