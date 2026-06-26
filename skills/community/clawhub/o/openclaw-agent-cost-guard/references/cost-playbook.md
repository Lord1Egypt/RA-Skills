# Cost Guard Playbook

## Objective
Keep OpenClaw useful without letting background automation, expensive defaults, or model drift create runaway bills.

## First-line controls
1. Set explicit monthly and daily budgets when supported.
2. Use the cheapest model that clears the task.
3. Reserve expensive models for escalation paths, not default paths.
4. Keep cron frequency intentional; always-on loops need stricter limits.
5. Prefer scripts and deterministic checks over repeated model calls.
6. Review browser-based or high-context tasks separately because they amplify cost quickly.

## Warning signs
- No budget fields or usage caps are visible.
- Default or override models are premium-tier everywhere.
- Large `maxTokens` / output limits are set globally.
- High-think or verbose modes are left on for routine jobs.
- Interactive/browser workflows are used where a script/API would work.
- Multiple recurring jobs exist with no cost owner.

## Operator questions
- What is the monthly budget ceiling?
- Which tasks deserve premium models?
- Which tasks can be downgraded to cheaper models or scripts?
- What cron jobs run frequently enough to matter financially?
- What is the kill switch if spend spikes?
