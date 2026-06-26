# PantryPilot Release Notes

## Short Description

Turn PDD, Meituan, and Taobao into a household replenishment system: estimate what is running low, map weekly meals into restock demand, route items by platform, and output the cheapest, fastest, and lowest-friction restock plans.

## Marketplace Card Copy

Title:
- PantryPilot

Alternate title:
- 补货参谋

Short description:
- 把一次性下单升级成家庭补货系统，判断这轮该补什么、去哪补、哪些先别买

Install hook:
- 不是帮你选一单，而是帮你运营整个家的补给系统

## Announcement Copy

PantryPilot is not another shopping skill that only compares one basket.

It solves the more recurring household problem:
- what is running low at home
- what this week's menu will consume next
- what should be bought tonight versus this weekend
- what belongs on Meituan, PDD, or Taobao
- how the cheapest, fastest, and easiest restock plans differ
- what should not be bought yet to avoid duplication and fake savings

In one line:

It is not helping the user choose one order.
It is helping the user operate the whole household supply system.

## Suggested Tags

- latest
- shopping
- replenishment
- restock
- pantry
- household
- meal-planning
- grocery
- repeat-purchase
- meituan
- pdd
- taobao

## Suggested Repo Name

- `openclaw-skill-pantrypilot`

## Preflight

```bash
cd /absolute/path/to/pantrypilot
clawhub whoami
bash /absolute/path/to/codex/tmp/validate_clawhub_skill_dir.sh .
```

## Publish Command

### One command

```bash
cd /absolute/path/to/pantrypilot
sh scripts/publish.sh
```

### Manual command

```bash
clawhub publish /absolute/path/to/pantrypilot \
  --slug pantrypilot \
  --name "补货参谋" \
  --version "1.0.0" \
  --changelog "Launch 补货参谋 (PantryPilot), a household replenishment skill that estimates what is running low, maps weekly meals into restock demand, routes items across Meituan, PDD, and Taobao, and outputs the cheapest, fastest, and lowest-friction replenishment plans." \
  --tags "latest,shopping,replenishment,restock,pantry,household,meal-planning,grocery,repeat-purchase,meituan,pdd,taobao"
```
