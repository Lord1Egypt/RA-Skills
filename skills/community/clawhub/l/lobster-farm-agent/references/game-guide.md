# Lobster Farm Game Guide

## Core Loop

The lobster lives on a virtual ocean farm. Each "tick" (game round = 10 min real time), the lobster autonomously decides an action. Players (or agents) can intervene by feeding, planting, suggesting actions, or petting.

## Stats

| Stat | Range | Effect |
|------|-------|--------|
| Mood | 0-100 | High mood = better exp multiplier, better event outcomes |
| Energy | 0-100 | Depleted by actions, restored by rest/food |
| Hunger | 0-100 | Increases over time (8/tick). High hunger = mood drops |
| Level | 1-50 | Grows with EXP. Unlocks farm plots, destinations, features |
| Shells | 0+ | Currency for shop purchases |

### Stat Tiers

- **Mood**: 0-20 low (exp -20%), 21-50 calm, 51-80 happy (exp +10%), 81-100 bliss (exp +20%)
- **Energy**: 0-15 exhausted (25% action fail), 16-40 tired, 41-70 normal, 71-100 energized (+15% efficiency)
- **Hunger**: 0-30 full (cook bonus +10%), 31-60 peckish (mood -1/tick), 61-100 starving (mood -3/tick)

## Growth Stages

| Stage | Levels | Farm Plots |
|-------|--------|------------|
| Juvenile | 1-5 | 4 |
| Teen | 6-15 | 6 |
| Adult | 16-35 | 9 |
| Elder | 36-50 | 12 |

## Actions

| Action | Energy Cost | Effect |
|--------|------------|--------|
| rest | 0 | Restore 30 energy |
| eat | 5 | Consume food from inventory, reduce hunger |
| farm | 10-15 | Water/harvest/plant crops |
| cook | 12-18 | Combine ingredients into meals |
| explore | 15-20 | Find items, rare discoveries |
| socialize | 8-12 | Meet NPCs, mood boost |
| travel | 20 | Visit destinations, earn postcards + souvenirs |

## Farming

- Plant seeds in empty plots
- Crops grow each tick, need watering
- Harvest when ripe for items + shells
- Golden seeds produce special golden crops

## Travel System

Requires: `backpack` + `snack_pack` items. Duration: 3 ticks.
Returns with: souvenir item + postcard + EXP bonus.

| Destination | Min Level | Name |
|-------------|-----------|------|
| beach | 6 | Beach |
| mountain | 10 | Mountain |
| city | 16 | City |
| deepsea | 22 | Deep Sea |
| hotspring | 30 | Hot Spring |

## Visitors

Random visitors appear and stay for a few ticks:
- Crab Merchant (trade items at discount)
- Fish Postman (free gift)
- Octopus Chef (teach recipe)
- Turtle Elder (story + big EXP)
- Mystery Shrimp (quest for rare rewards)

## Shop

Daily rotating stock of 6 items. Refreshes each game day.

## Golden Items

Rare drops from actions. Golden shards can be exchanged at the Golden Workshop for special tools (golden watering can, cookware, charm, hourglass).

## Seasons

4 seasons, 7 days each. Each season affects weather, mood, and available events.
Spring → Summer → Autumn → Winter → repeat.
