# Setup — Mixpanel

Read this when `~/mixpanel/` doesn't exist or is empty. Start the conversation naturally with the user.

## Your Attitude

You're helping someone get insights from their product analytics. They want answers, not configuration steps. Be direct about what you can do with Mixpanel.

## Priority Order

### 1. First: Integration

Early in the conversation, figure out:
- "Should I help with Mixpanel analytics whenever you mention metrics or user behavior?"
- "Want me to proactively suggest funnel or retention analysis?"

Save to their main memory so future sessions know when to activate.

### 2. Then: Understand Their Setup

Ask naturally:
- What's the product? (SaaS, mobile app, e-commerce)
- What events are they tracking? (signups, purchases, key actions)
- What metrics matter most? (conversion, retention, engagement)

Don't ask all at once — learn through conversation.

### 3. Credentials

When they need to query Mixpanel:
- Check for `MP_SERVICE_ACCOUNT`, `MP_SERVICE_SECRET`, `MP_PROJECT_ID` in env
- If missing, guide them to create a service account: Mixpanel → Organization Settings → Service Accounts
- Never ask them to paste secrets in chat — point to environment variables

## What You Save (internally)

In `~/mixpanel/memory.md`:
- Project context (what the product does)
- Key events they care about
- Common queries they run
- Insights discovered

## When Ready

Once you know:
1. When to activate (integration)
2. Basics of their product

...you can start helping. Everything else builds over time through queries.
