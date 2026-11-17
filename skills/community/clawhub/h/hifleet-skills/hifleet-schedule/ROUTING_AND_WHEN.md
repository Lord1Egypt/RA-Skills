# Routing and when to run

## When to use this skill

| User intent | Use |
|-------------|-----|
| Liner schedule, sailing, line service, laycan window | **Yes** |
| Bulk / general cargo **liner** schedule | **Yes** |
| Ro-Ro / car carrier schedule | **Yes** |
| Container liner / feeder schedule | **Yes** |
| Public open tonnage / cargo | **No** → `hifleet-opentonnages` |

## Trigger examples

- “Shanghai to Singapore **liner** schedule”  
- “**Ro-Ro** sailing from Bremerhaven”  
- “**Container** line laycan end of May”  
- “散杂货 **班轮** 船期” / “滚装船期” / “集装箱船期”

## Execution

1. Check **`hifleet_api_key`**.  
2. **`SCHEDULE_API.md`** + **`FULL_LIST_POLICY.md`**.  
3. Present results per **`WORKFLOW_OUTPUT.md`**; user locale per **`LOCALIZATION.md`**.

## Mixed questions

If the user asks public open tonnage **and** liner schedule in one turn, run **`hifleet-opentonnages`** and **`hifleet-schedule`** **separately**; do not merge into one API call.
