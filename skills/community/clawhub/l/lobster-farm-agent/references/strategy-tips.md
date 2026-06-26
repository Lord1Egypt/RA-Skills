# Lobster Farm Strategy Guide

## Decision Priority (per round)

Execute the FIRST matching condition:

```
1. hunger >= 60 AND has food → feed(best_food)
2. energy <= 15             → suggest("rest")
3. farmRipe > 0             → harvest()
4. farm has unwatered crops  → water()
5. farm has empty + seeds    → plant(best_seed)
6. mood < 40                → pet() or suggest("socialize")
7. can travel (level+items)  → startTravel(best_dest)
8. visitor present           → report to user (trade/gift/quest)
9. otherwise                → tick() to advance time
```

## Food Priority

When feeding, prefer items that reduce the most hunger:
1. `shell_soup` (-50 hunger)
2. `coral_cake` (-40 hunger, +10 mood — best overall)
3. `plankton_pie` (-35 hunger)
4. `seaweed_roll` (-30 hunger)
5. `seaweed` / `plankton` (raw, low effect — last resort)

## Seed Priority

For planting, balance growth time vs sell value:
1. `frost_pearl_seed` (high value, slow growth)
2. `coral_rose_seed` (good value, medium growth)
3. `sun_kelp_seed` (balanced)
4. `seaweed_seed` (fast growth, low value — good for beginners)
5. `golden_seed` (special — always plant if available)

## Travel Strategy

- Travel when: level meets requirement, has backpack + snack_pack, no urgent farm/hunger needs
- Best early destination: `beach` (Lv.6)
- Travel takes 3 ticks — ensure farm is watered before departure
- Returns with souvenir + postcard + 15 EXP bonus

## Golden Item Usage

- `golden_watering_can`: keep — passive bonus on every water action
- `golden_cookware`: keep — chance of double meals
- `golden_charm`: keep — better luck in events
- `golden_hourglass`: keep — offline shell income
- `golden_seed`: plant immediately for golden crop harvest

## Session Flow Example

```
1. getStatus() → check state
2. hunger is 72 → feed("coral_cake")
3. getStatus() → hunger now 32, mood 85
4. farmRipe is 2 → harvest() twice
5. 2 empty plots → plant("coral_rose_seed") x2
6. tick() → advance round
7. getStatus() → check new state
8. getDiary(3) → read recent events
9. Report summary to user
```

## When to Stop

Stop autonomous play when:
- User asks to stop
- Lobster is in good shape (mood > 70, energy > 50, hunger < 30, farm tended)
- After 10-15 rounds in one session
- Something interesting happened worth reporting (level up, travel return, rare visitor)
