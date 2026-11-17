# Home Office Tax Deduction Planner

Millions of remote workers and freelancers leave the home-office deduction on the table — or claim it wrong and invite an audit. The rules fork hard: in the US, **employees (W-2) cannot deduct a home office at all** since 2018, while **self-employed people** choose between the *regular method* (actual expenses × business-use percentage, carryover of excess) and the **simplified method** ($5/sq ft up to 300 sq ft, no depreciation, no records beyond a floor plan). Pick wrong by even 100 sq ft and you've cost yourself real money or created a depreciation-recapture headache you'll carry until you sell the house.

This skill is a **defensible-deduction instrument**: it computes both methods from your actual numbers, picks the legal maximum, tests the strict "regular and exclusive use" gate room-by-room, sizes the deduction against your business income cap (the deduction can't exceed gross income from the business use), and generates the audit-proofing paper trail — a dated floor-plan worksheet, expense log format, and photo checklist. It also prices the hidden tail: depreciation recapture (the simplified method never triggers it; the regular method does, at sale).

## Real problem it solves
- "Can I deduct my home office?" — the answer forks on employment status, room exclusivity, and method; most people guess and guess small.
- "Simplified or regular?" — needs side-by-side math with the same inputs; this does it in one pass and states the tie-breaking rules.
- "What if I'm audited?" — exclusive-use is the #1 disallowance reason; the skill produces the evidence format (floor plan, photos, expense log) before you need it.

## Quick start
```bash
# Self-employed, 140 sq ft dedicated room, $2,400 rent/yr, $180 electric, etc.
python3 scripts/home_office_deduction.py compute --status self-employed \
    --sqft 140 --rent-year 2400 --utilities-year 480 --internet-year 720 \
    --insurance-year 0 --repairs-year 200 --income 42000

# Renting a desk corner in a shared room? Exclusive-use gate first:
python3 scripts/home_office_deduction.py gate --exclusive-room yes --dual-use no

# Employee (W-2 remote) — checks what's still available
python3 scripts/home_office_deduction.py compute --status employee --sqft 140
```

## The two methods, plainly
| | Regular | Simplified |
|---|---|---|
| Rate | actual expenses × business % | $5 × sq ft (max 300) |
| Records | expense log + floor plan | floor plan only |
| Depreciation | yes (owners; 39-yr, recapture at sale) | none, ever |
| Carryover | excess carries to next year | lost |
| Renters | often wins big (rent is the biggest line) | caps at $1,500 |
| Best when | dedicated space + high housing cost | small space or thin records |

## The exclusive-use gate (read before computing anything)
The room must be used **regularly and exclusively** for the business. A guest bed that's slept on twice a year disqualifies the whole room. A desk corner in the living room fails — unless it's a *separately identifiable* area used only for business. Separate structures (studio, garage office) qualify even without exclusivity of the whole structure. Principal-place-of-business test: it must be where you do the substantive work, or where you meet clients — not just billing at night.

## Hidden traps this tool prices
1. **Income cap**: deduction ≤ gross income from business use of the home; regular-method excess carries forward, simplified excess just dies.
2. **Depreciation recapture**: regular-method owners pay tax on allowed/allowable depreciation at sale — the simplified method sidesteps it entirely. For a $400k home with 10% business use, that's a real future bill the $1,500 cap might not justify.
3. **Method switching** is allowed year to year (after a year of regular method, you can go simplified; depreciation taken is recaptured regardless).
4. **Roommates/family**: exclusive use is *yours* — a partner's Zoom calls from "your" office don't poison it, but a kids' play area does.

## Contents
- `SKILL.md` — decision tree, method comparison, gate tests, pitfalls
- `references/rules-and-audit-proofing.md` — IRS Pub 587 distillation, record formats, state add-ons (NY/CA employee allowances post-TCJA), non-US notes
- `scripts/home_office_deduction.py` — stdlib-only CLI (gate/compute/evidence)

## License
MIT
