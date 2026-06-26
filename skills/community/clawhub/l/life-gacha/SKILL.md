---
name: life-gacha
description: A daily gacha skill — draw a random activity each morning, check in at night, and get a weekly summary. Adds a little surprise to every day.
---

# Life Gacha

This skill is invoked when the user types `/life-gacha`, or says anything related to drawing a card, evening check-in, or weekly review.

**Always respond in the same language the user is using.**

---

## On invocation

When this skill is invoked (e.g. `/life-gacha`), run the following onboarding flow:

1. Introduce the skill in the user's language: every morning a random activity is drawn from the card pool; in the evening the agent checks in on how it went; on Sunday a weekly summary is generated.
2. Read `config.yaml` and show the user the current card pool. Ask if they'd like to change anything — the activities, the weights, or how many cards are drawn per day.
3. Apply any changes the user requests to `config.yaml`. Skip this step if they're happy with the defaults.
4. Set up the three scheduled tasks (see **Scheduled tasks** below).
5. Confirm setup is done. Let the user know they can say things like "update my card pool" or "change the check-in time" at any time.

---

## Commands

All scripts are located in the same directory as this SKILL.md. Use that path when running them.

### Daily draw

```bash
python3 draw.py           # draw based on config
python3 draw.py -n 2      # draw exactly 2 cards
python3 draw.py --extra 1 # draw 1 more on top of today's existing cards
python3 draw.py --reroll  # redraw today (replaces existing entry)
```

Results are written to `data/YYYY-MM/week-NN.md` with the daily note left blank for the evening.

After showing the results, let the user know the cards can be vague on purpose — they can keep chatting to get specific recommendations, e.g. which movie to watch, which book fits their current mood.

### Evening check-in

```bash
python3 checkin.py "user's response here"
```

Ask the user how their day went, then pass their answer as an argument to the script. It fills in the blank note in today's entry. No interactive mode — the agent handles the conversation.

### Weekly review

```bash
python3 review.py
```

Reads the week's entries and appends an encouraging summary to the weekly file.

---

## Scheduled tasks

Set up the following three tasks using an appropriate scheduling tool:

- Every day at 7:00am — run `draw.py` and show the result to the user
- Every day at 11:00pm — read today's drawn cards from the weekly file, ask the user how it went, then call `checkin.py` with their answer
- Every Sunday at 11:55pm — run `review.py` and show the result to the user

---

## Config

`config.yaml` controls the card pool and draw rules:

```yaml
draw_rules:
  workday: 1   # cards drawn on weekdays
  holiday: 2   # cards drawn on weekends

# weight 1-5: higher weight = more likely to be drawn
workday_pool:
  - item: ...
    weight: 3

holiday_pool:
  - item: ...
    weight: 3
```

Weights only apply within each pool independently.

---

## Data format

```
data/
└── 2026-03/
    └── week-12.md
```

```markdown
## 2026-03-22 Sat

**Today's draw**

- Have a meal with a friend

**Daily note**

（待填写）

---

# Weekly review (week 12)
...
```
