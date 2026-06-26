# Example: Natural Language Query

**User:** How much did I spend on meals last month?

**Agent:** 
<think>
1. User wants to know their spending on meals for February 2026.
2. I need to read `expenses/expense-log.json`.
3. Filter expenses where `date` starts with "2026-02".
4. Filter by category "Meals & Entertainment".
5. Sum the `total` fields.
</think>

[Agent runs tool:]
```bash
jq '[.[] | select(.date | startswith("2026-02")) | select(.category == "Meals & Entertainment")] | map(.total) | add' expenses/expense-log.json
```

[Tool output:]
```
145.50
```

**Agent:** 
You spent **$145.50** on Meals & Entertainment in February 2026. 

Would you like me to generate a PDF report for those specific expenses?
