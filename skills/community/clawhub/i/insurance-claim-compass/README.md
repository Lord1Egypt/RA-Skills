# Insurance Claim Compass

**After the loss, before the phone call.** A burst pipe floods the
kitchen, a break-in empties the office, hail trashes the roof — what
you do in the first 24 hours and how you document it moves the payout
by 30-50%. Most people clean up too early, notify by phone only, accept
the first depreciated check, and never learn the word "appraisal."

This toolkit gives you:

- **Loss-type evidence playbooks** (water/theft/wind/fire/auto/
  liability): first-24h actions, photo shot-lists, document checklists.
- **First-notice-of-loss letter generator** — same-day written notice
  that starts the paper trail and the clock.
- **ACV/RCV depreciation calculator** — item-class life tables, the
  same shape adjusters' software uses, with the recoverable-holdback
  gap on RCV policies.
- **Claim timeline** with typical milestones and where to verify the
  exact statutory bounds for your state/country.
- **Appeal ladder** for lowballs/denials: itemization demand →
  independent estimate → appraisal clause → DOI complaint, with a
  drafted objection letter.

## The real-world problem
Insurance exists for exactly these days, yet the moment of loss is the
worst possible moment to learn claims procedure. Adjusters work from
files; whatever isn't photographed, receipted, or written didn't
happen. And the system prices in passivity: first offers assume you
won't itemize, won't get an independent estimate, and won't complain
to the regulator.

## Quick start
```bash
python3 scripts/claim_navigator.py document --type water
python3 scripts/claim_navigator.py letter --type home \
    --loss "burst supply pipe, kitchen" --policy HP-2026-118 --amount 3800 > notice.txt
python3 scripts/claim_navigator.py value --item "55in TV" --purchase 2021 --price 1200 --rcv
python3 scripts/claim_navigator.py appeal --reason lowball --offer 2100 --estimate 3800
```

Pure Python stdlib. Offline. No accounts, no data leaves the machine.

**Not legal advice** — policies and deadlines vary; verify with your
carrier and insurance department. Companion skill: **insurance-gap-auditor**
(before loss: what's covered).

## License
MIT © Denis Voronin
