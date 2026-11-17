# Document Retention Table & Filing System (Reference)

## 1. The clock rules (US household)

| Category | Keep | Clock starts | Disposition |
|---|---|---|---|
| Tax return (the return) | 7 yr min, forever if scanned | filing date | KEEP / SCAN+SHRED |
| Tax supporting docs (receipts, W-2, 1099) | 7 yr | filing date | SHRED after |
| Paystubs | until W-2 matches (then shred) | receipt | SHRED |
| W-2 / 1099 forms | with tax return 7 yr | filing date | KEEP w/ return |
| Bank statements | 1 yr (7 if tax-relevant) | statement date | SHRED |
| Credit card statements | 1 yr (7 if tax deductions) | statement date | SHRED |
| Utility bills | 1 yr (until next arrives) | bill date | SHRED |
| Phone/internet bills | 1 yr | bill date | SHRED |
| Medical bills & EOBs | 1–3 yr (until insurance dispute window closes; 7 if claiming) | payment date | SHRED |
| Immunization records | FOREVER | — | FOREVER |
| Medical records (major) | 5–7 yr adult; until age 18+ for kids | event | SCAN+KEEP |
| Insurance policy (active) | life of policy + claims | until replaced | KEEP current |
| Insurance policy (expired) | until claims impossible (~4 yr) | expiry | SHRED |
| Home purchase closing docs | as long as you own + 7 yr | sale date | KEEP / SAFE |
| Property deed | FOREVER (owning period) | — | SAFE-DEPOSIT |
| Mortgage statements | until annual statement matches | receipt | SHRED |
| Receipts (general) | until warranty/return window closes | purchase | SHRED |
| Receipts (tax-deductible) | with tax return 7 yr | filing date | KEEP w/ return |
| Receipts (big purchases) | as long as you own (insurance claim) | purchase | SCAN+KEEP |
| Warranties + manuals | until product gone or warranty expired | expiry | SHRED |
| Vehicle title | FOREVER while owned | — | SAFE-DEPOSIT |
| Vehicle maintenance records | while you own it (value at sale) | — | KEEP |
| Lease agreements | lease + deposit returned + 1 yr | move-out | SHRED |
| Birth/marriage/death certificates | FOREVER | — | SAFE-DEPOSIT |
| Divorce decree / custody orders | FOREVER | — | SAFE-DEPOSIT |
| Adoption papers | FOREVER | — | SAFE-DEPOSIT |
| Citizenship/immigration docs | FOREVER | — | SAFE-DEPOSIT |
| Passport (expired) | FOREVER | — | KEEP |
| Military discharge DD-214 | FOREVER | — | SAFE-DEPOSIT |
| Pension/401k plan docs | FOREVER (plan rules change) | — | KEEP |
| Social Security statements | until superseded | receipt | SHRED prior |
| Will / power of attorney / directives | FOREVER, current version only | — | KEEP (lawyer + home) |
| Education transcripts/diplomas | FOREVER | — | KEEP |
| Employment offer letters | while employed + 1 yr | end | SHRED |
| Retirement account statements | until annual matches, annual 7 yr | filing | SHRED/KEEP |
| Investment confirmations | until sold + cost basis needed (7 yr after sale) | sale | KEEP |
| Savings bonds | until redeemed | — | SAFE-DEPOSIT |
| Guarantees/contracts (service) | life of contract + 1 yr | end | SHRED |
| Funeral/prepaid documents | FOREVER | — | SAFE-DEPOSIT |
| Warranty deeds, liens released | FOREVER while owned | — | SAFE-DEPOSIT |

## 2. Why 7 years for tax

IRS audit window: generally 3 years from filing; **6 years** if income
was underreported by >25%; unlimited for fraud. States can run longer
(aging states like CA: 4). Seven years covers the practical ceiling.
The return itself: keep forever digitally (proves filing, basis
carry-forwards, AMT/loss carryforwards).

Special basis documents (home improvements for capital gains, stock
cost basis, IRA nondeductible contributions Form 8606) — keep until
7 years AFTER the asset is sold/account emptied, not 7 years after
purchase.

## 3. The filing blueprint

```
FILING CABINET
├── ACTIVE (this year, reachable in seconds)
│   ├── To-pay / to-file tray
│   ├── Current insurance policies
│   ├── Current year tax folder
│   └── Active warranties+receipts (stapled)
├── YEAR FOLDERS (time-limited items, one per year)
│   ├── 2026  2025  2024  2023  2022  2021  2020  2019
│   └── rule: after tax day, shred the folder older than 7 yr
├── TOPIC FOLDERS (no clock)
│   ├── Vehicles (title copy, maintenance)
│   ├── House (closing, improvements — basis!)
│   ├── Medical (immunizations forever; active conditions)
│   └── Manuals-current-appliances
└── FOREVER BOX (fireproof) / SAFE-DEPOSIT
    certificates, deeds, DD-214, will, passports-old, bonds
```

Purge ritual (30 min/year, tax day + 1 week): shred year-folder older
than 7, move last year's ACTIVE into its year folder, done.

## 4. Scan doctrine

Scan before shredding anything with >7-year value: returns, closing
docs, basis receipts, diplomas. Naming: `YYYY-MM-DD_type_entity.pdf`
in `Documents/Archive/<year>/`. Backups: 3-2-1 rule (see
backup-3-2-1-auditor). A scan on one device is a receipt for grief,
not an archive.

## 5. Shredding rules

- Cross-cut (not strip) for SSN, account numbers, medical IDs,
  signatures, anything pre-approved credit.
- If the shred pile is enormous: bank/shred-event days, office-store
  shredding services ($1/lb class) are fine for dead paper — remove
  the forever items FIRST.
- Recycling bin is for catalogs and pizza boxes, not statements.
- Kids' documents: the immunization record follows the kid to college;
  the crayon art does not need a retention schedule (photo it, keep 3
  favorites, box the rest by year, one box per kid total).

## 6. Incoming-mail firewall (stop the pile at the door)

1. Stand over recycling at the mailbox: junk, catalogs, envelopes —
   gone before they enter the house.
2. Shred-worthy junk (pre-approved offers) straight to shred bin by
   the door.
3. Two trays ONLY: to-pay (deadline visible) and to-file (weekly
   10-minute filing slot, calendar it).
4. Everything that can be paperless → paperless, except: legal
   notices, tax notices, anything you might dispute (paper trail).
