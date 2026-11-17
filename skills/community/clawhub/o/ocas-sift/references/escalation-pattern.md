# Anti-bot Escalation Pattern

When to read: when auto-escalation triggers mid-fetch, when debugging why a
site returns a challenge page, or before tuning tier behavior.

## The chain

```
Tier 1: sift.fetch (Scrapling → Jina Reader fallback)
  ↓ blocked / empty / challenge page detected
Tier 2: sift.webwright (Playwright Firefox, standard mode)
  ↓ still blocked / challenge not passing
Tier 3: sift.webwright with stealth=true
  ↓ still blocked on a CONFIRMED HARD-BLOCK (404/410/451 or bot/auth wall)
Tier 4: Wayback fallback (scripts/wayback_fallback.py) — closest archive.org
        snapshot; marked source='archive.org', is_stale=True
  ↓ no usable snapshot
Mark as unreachable — report to user with evidence.
```

**Why this order:** Scrapling is near-instant and handles ~90% of sites.
Webwright Firefox handles JS-heavy sites Scrapling can't parse. Stealth mode is
the nuclear option — slower and more expensive, but covers the ~10% of sites
that actively block automation. Wayback is recovery-only: it never fires on
soft failures (429/5xx) where a retry helps, and its output is always marked
stale so synthesis cannot mistake an old snapshot for live content.

## Detection signals (auto-escalate when observed)

- HTTP 403 response from Scrapling
- Page title contains "Just a moment…" / "Attention Required" / "Access denied"
- Body text < 200 chars but page loads (challenge page)
- Scrapling returns a Cloudflare/Akamai challenge HTML pattern

## Tier 3 stealth mode (`sift.webwright` with `stealth: true`)

- Randomize user-agent, viewport, WebGL vendor, canvas fingerprint
- Enable stealth plugins (puppeteer-extra-plugin-stealth equivalent)
- Auto-detect challenge pages and wait for resolution (up to 15s)
- Retry up to 3 times with exponential backoff
- If behind proxy, rotate to a residential exit node if available

## Hard-block vs soft-failure decision table

| Failure | Class | Action |
|---|---|---|
| 403 / challenge HTML | hard-ish | escalate tiers |
| 404 / 410 / 451, bot wall, auth wall | confirmed hard-block | wayback fallback |
| 429 / 5xx | soft — retry helps | back off and retry same tier; do NOT escalate |
| Empty body <200 chars | challenge | escalate tiers |
