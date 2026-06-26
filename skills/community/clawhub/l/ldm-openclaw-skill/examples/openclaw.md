# OpenClaw Example

Use this instruction in an outbound-focused OpenClaw agent:

```text
You are allowed to draft outbound email, but before sending or scheduling any bulk outbound campaign you must run the LDM deliverability preflight.

Bulk outbound means more than 5 similar emails, a cold email campaign, recruiting outreach, investor updates, deal-flow notifications, or partnership outreach.

If LDM inbox placement is below 70%, do not send. Report the deliverability problems and suggest fixes.

If authentication fails for SPF, DKIM, or DMARC, do not send until the issue is fixed or the user explicitly overrides the warning.

Never print or expose the LDM API key.
```

## Demo Scenario

```text
Build a 50-recipient cold email campaign for B2B manufacturing leads.
Run LDM deliverability preflight before sending.
If Gmail or Outlook placement is risky, rewrite the subject/body and recheck.
Only send after the deliverability preflight passes.
```

## Suggested Output

```text
LDM deliverability preflight: FAIL
Inbox placement: 54%
Risk level: high
Provider issues: Gmail spam, Outlook junk
Authentication: SPF pass, DKIM pass, DMARC alignment warning
Content risks: promotional subject, URL shortener, missing unsubscribe
Recommended fixes: rewrite subject, replace shortened link, add unsubscribe, reduce promotional wording
Decision: revise
```
