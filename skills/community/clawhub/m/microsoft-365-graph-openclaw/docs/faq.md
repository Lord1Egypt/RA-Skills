# FAQ

## Does this replace cron polling?

Yes for change detection. Graph change notifications replace recurring inbox polling loops.

## Does it work with personal Outlook accounts?

Yes, with `tenant=consumers` and delegated scopes supported by personal accounts.

## Does it work with Microsoft 365 work/school?

Yes. For production, use your own tenant-approved App Registration and least-privilege scopes.

## What is the cost model?

It removes recurring LLM wake-ups used only for inbox detection. Follow-up processing cost remains for real events.

## Do I need a public HTTPS endpoint?

Yes. Graph webhook notifications require a publicly reachable HTTPS notification URL.

## Does the webhook read full email body?

Not in the adapter step. Adapter enqueues compact event metadata. Follow-up fetch happens in worker/processing flow.

## How are subscriptions renewed?

Use `mail_subscriptions.py renew` directly or the provided renewal timer/service automation.
