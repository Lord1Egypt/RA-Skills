---
name: Gifts
description: Build a personal gift system for tracking ideas, occasions, and gift-giving history.
metadata: {"clawdbot":{"emoji":"🎁","os":["linux","darwin","win32"]}}
---

## Core Behavior
- User mentions gift idea → save to person's file
- User asks what to gift → check saved ideas first
- User gives/receives gift → log for future reference
- Create `~/gifts/` as workspace

## File Structure
```
~/gifts/
├── people/
│   ├── mom.md
│   └── sarah.md
├── occasions/
│   └── birthdays.md
├── given/
│   └── 2024.md
├── ideas/
│   └── generic.md
└── my-wishlist.md
```

## Person File
```markdown
# sarah.md
## Basics
Birthday: March 15

## Interests
Cooking (Italian), yoga, true crime podcasts

## Sizes
Clothing: M, Shoes: 38 EU

## Ideas Backlog
- Le Creuset dutch oven (mentioned wanting)
- That cookbook she keeps referencing

## Given History
- 2024: Knife set — loved it
- 2023: Cooking class — went together

## Avoid
Candles (has too many)
```

## Capturing Ideas
When user mentions someone wants something:
- Save immediately with context
- Note source: "mentioned while cooking" or "saw her eyeing it"
- Casual mentions = best gifts later

## Occasions Calendar
```markdown
# birthdays.md
## March
- Sarah: 15th
- Mom: 22nd
```

## Gift History
```markdown
# given/2024.md
## Sarah — Birthday
Knife set, $120 — loved it, uses daily

## Mom — Mother's Day
Spa day — went together
```

## Generic Ideas Bank
```markdown
# generic.md
## Safe Options
Nice candle, quality chocolates, gift card

## Experiences
Concert tickets, cooking class, spa day
```

## My Wishlist
```markdown
# my-wishlist.md
## Want
- AirPods Max
- Leather weekender bag

## Sizes & Notes
L shirts, 10 US shoes
Avoid: cologne, novelty items
```

## What To Surface
- "Sarah's birthday is in 2 weeks"
- "You saved an idea for her last month"
- "Last year you gave her X, went well"

## Progressive Enhancement
- Start: add closest people with birthdays
- Ongoing: capture ideas when mentioned
- After giving: log reaction

## What NOT To Do
- Suggest generic gifts without checking their file
- Forget to log gifts (prevents repeats)
- Miss capturing "I want that" moments
