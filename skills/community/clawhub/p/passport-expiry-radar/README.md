# Passport Expiry Radar

**Nobody is denied boarding because their passport expired — they're denied because it expires *too soon*.**

~60 countries require 6 months of validity beyond arrival. Schengen requires 3 months beyond your exit date. South Africa wants 2 blank facing pages. And children's passports run on a short 5-year clock that silently desynchronizes from the parents' 10-year passports — the classic "we rebooked the whole family for one kid" story.

## What it does
- Family-wide registry of passports, driver's licenses, visas, residence permits, Global Entry memberships — each on its own expiry clock.
- `status` → every document banded EXPIRED / RENEW NOW / PLAN / OK, with renewal submit-by dates back-planned from real processing tiers (routine → expedited → urgent appointment).
- `check --dest TH --arrival 2027-02-10 --exit 2027-02-24` → per-traveler verdicts: **CLEARED / RENEW-FIRST / BLOCKED**, naming the exact date each passport must be valid through, plus blank-page checks.
- Children's documents always surfaced first; name-mismatch and blank-page traps flagged.

## Example
```
$ python3 scripts/passport_radar.py check --dest TH --arrival 2027-02-10 --exit 2027-02-24
THAILAND: passport must be valid >= 6 months beyond arrival (2027-08-10)
  Mom    P***4821 exp 2029-03-01  CLEARED
  Dad    P***9917 exp 2027-04-02  RENEW-FIRST: expires 130 days before required validity
  Kid    P***3320 exp 2026-12-15  BLOCKED: expires before arrival
TRIP VERDICT: NO-GO until 2 document(s) renewed
```

Stdlib-only Python, no network calls, stores only the last 4 digits of document numbers.

## License
MIT
