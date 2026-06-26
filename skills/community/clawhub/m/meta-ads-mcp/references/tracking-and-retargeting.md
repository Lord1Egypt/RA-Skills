# Pixel/CAPI Tracking & Retargeting

## 9. PIXEL & TRACKING SETUP

### The Recommended Setup: Pixel + CAPI Together

**Meta Pixel** (browser-side) and **Conversions API / CAPI** (server-side) must both be running. Never rely on Pixel alone — Safari/Firefox block third-party cookies by default, and iOS privacy changes cause 40–60% data loss in Pixel-only setups.

```
Browser Side:  User action → JavaScript Pixel fires → Meta receives event
Server Side:   User action → Your server → CAPI → Meta receives event
Deduplication: Both send same event_id → Meta counts it once
```

### Priority Events to Track (in order of importance)
1. `Purchase` / `Lead` — primary conversion event
2. `InitiateCheckout` / `ViewContent` — funnel signals
3. `AddToCart` — intent signals
4. `PageView` — top-of-funnel presence
5. `CompleteRegistration` — for lead-gen sites

### Pixel Installation (WordPress Sites)
- Install via **Meta for WordPress plugin** (official) or **PixelYourSite plugin**
- For CAPI on WordPress: use **PixelYourSite Pro** (has CAPI built in) or custom server-side integration
- Verify in **Events Manager → Test Events** tool after installation
- Check **Event Match Quality (EMQ)** score — target 7+/10

### Pixel Verification Checklist
- [ ] Pixel fires on all key pages
- [ ] Purchase / Lead event fires correctly on conversion page
- [ ] CAPI events are sending (check Events Manager → Aggregated Event Measurement)
- [ ] Deduplication is working (no doubled events in Events Manager)
- [ ] EMQ score is 7+/10 — improve by sending **hashed** email/phone in event parameters. **PII: requires a documented lawful basis, consent, and SHA‑256 hashing before transmission (see budget-and-audience.md → "Privacy & compliance").**
- [ ] Attribution window set to: 7-day click, 1-day view

---

## 10. RETARGETING CAMPAIGNS

### Retargeting Campaign Architecture

```
Campaign: [Site] | Sales/Leads | Retargeting | [Date]
  Ad Set 1: Hot — Checkout abandoners (7 days)
  Ad Set 2: Warm — Product page visitors (30 days, excl. purchasers)
  Ad Set 3: Warm — Video viewers 75% (60 days)
  Ad Set 4: Warm — Page engagers (90 days)
```

### Retargeting Creative Strategy
- Be specific — reference what they viewed or did ("Still thinking about [product]?")
- Show social proof — testimonials, reviews, trust signals
- Create urgency if truthful — limited stock, expiring offer
- Different creative from prospecting — they know you already
- Use BAB (Before → After → Bridge) framework

### Retargeting Exclusions (Critical)
- Always exclude purchasers/converters from all retargeting sets
- Set a **frequency cap** — max 3–5 impressions per person per week to avoid burnout
- Monitor frequency score — above 5 = audience is oversaturated, expand or refresh creative

---
