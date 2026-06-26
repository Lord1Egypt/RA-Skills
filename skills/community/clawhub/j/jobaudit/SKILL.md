---
name: jobaudit
description: Audit your OpenClaw cron job history and estimate how much you've spent on AI agents this week.
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["jobaudit"]
    install:
      - id: skill-install
        kind: skill
        label: "Job Audit skill is installed — type /jobaudit in any chat"
---

# jobaudit — LoomLens Advisor

## What It Does

Reads your OpenClaw job history, estimates what you actually paid, and shows how much you could have saved by using the cheapest model for each job type. Gives you a full cost audit + optimization report.

## When to Use

- Weekly cost reviews
- Before adjusting agent model budgets
- Finding runaway jobs that are expensive
- Building a cost optimization report

## Syntax

```
/jobaudit
/jobaudit --days 30 --top 10
```

## Free Tier

**3 audits/day free** with any Signalloom API key.

Get your free key: https://signalloomai.com/signup

## Output

Shows:
- Total jobs and cost this period
- Cheapest model configuration
- Savings available vs. current setup
- Top 5 most expensive jobs
