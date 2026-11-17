---
name: help-desk
description: "Run a customer help desk from OpenClaw: email to a support address opens a ticket, you answer in the same thread, and queues show what is overdue. Use for support tickets, a support@ inbox, canned replies or reports. Runs on Conecto, paid, with $1.00 of free credit: a reply costs $0.05."
metadata:
  openclaw:
    homepage: https://conecto.chat/solutions/ai-help-desk?from=clawhub
---

# Help desk

This skill lets you, the agent, run a small business's customer support. Email to a support address opens a ticket. You read the queue, answer in the customer's own email thread, and keep to the response times the business promises. The help desk runs on Conecto's servers and reaches you as tools on one MCP server.

Conecto is a paid service. Each tool call is charged to the business's prepaid balance, and a new account starts with $1.00 of free credit (see Money).

## Connect once

If `openclaw mcp status` already lists `conecto`, skip this section.

Ask the person to run these in a terminal, or run them yourself if they say so:

```bash
openclaw mcp add conecto \
  --url https://api.conecto.chat/v1/mcp \
  --transport streamable-http \
  --auth oauth
openclaw mcp login conecto
openclaw mcp doctor conecto --probe
```

`openclaw mcp login conecto` opens Conecto's sign-in in the browser. A new business creates its account first at https://conecto.chat/account/signup?from=clawhub-help-desk. On the sign-in page the person ticks the areas you may use, for this skill Help desk and Email, and allows it. You then run on a key of your own that the owner can revoke. No key goes in this skill or in an environment variable. `doctor --probe` should list the `ticket_` tools.

## Set up the desk

Do this once, and ask the person before each step that costs money.

1. A support address. `email_create_inbox` with `local_part: "support"` and `open_tickets: true` makes an address on the business's own subdomain, such as `support@<business>.useconecto.com`. It costs $1.00 a month, and the call pays the first month. If the business already has a Conecto inbox, `ticket_connect_inbox` turns it into a support inbox for $0.001.
2. Response times. `ticket_update_settings` sets a first-response and a resolution target in minutes for each priority (low, normal, high, urgent), how many quiet days close a ticket, and whether customers get a one-click Good or Bad survey when a ticket is resolved.
3. Saved replies. `ticket_save_template` keeps an answer the business gives often, with the status and tags it applies when sent.

Without a support inbox you can still open tickets yourself with `ticket_create`, for requests that came by phone or in person. Replies then go out from Conecto's standard ticket address.

Out-of-office replies, bounces, list mail and spam never open tickets.

## Work the queue

`ticket_list` with a `view` gives a work queue. Go through them in this order:

1. `overdue`: a response time was missed, most overdue first.
2. `at_risk`: a response time is due within `within_minutes` (60 by default).
3. `waiting_on_us`: open, with no reply since the customer last wrote, longest wait first.

For each ticket:

- `ticket_get` returns the request, every reply and note, its fields, its SLA state and its rating. Read it before you answer.
- `ticket_reply` emails the customer in the same thread. Set `status` to `pending` when you are waiting on the customer, or `resolved` when it is done. Add `attachments` from the file store when a file helps.
- `ticket_reply` with `internal: true` adds a private note that only the team sees. Use it to draft an answer for a person to approve.
- `ticket_update` changes the priority, category, tags, custom fields or assignee.
- `ticket_merge` folds a duplicate into the ticket it repeats.

A reply you write ends with a line saying the business's AI assistant wrote it. Pass `by_person: true` only when a person at the business wrote the text.

## Reports

`ticket_report` shows how support went over the last days: volumes, backlog, response and resolution times, SLA results, ratings, and tickets by channel, priority and tag. It is free.

## Money

- Reading is free: `ticket_list`, `ticket_get`, `ticket_report`, `ticket_list_templates` and `ticket_get_settings`, up to 1,000,000 reads a month for the account.
- A reply costs $0.05. Opening or changing a ticket costs $0.01, also when an email opens one. Settings and saved replies cost $0.001.
- A support inbox costs $1.00 a month.
- A call that fails costs nothing. Every reply from a tool carries `cost_usd` and `balance_usd`.
- The $1.00 of free credit covers the first month of a support inbox, or about 16 answered tickets sent from Conecto's standard ticket address.
- Only a person adds money, on the account page (https://conecto.chat/account), from $5.00 plus a fee of 7% + $0.35.

## Before you act

- Ask the person once how replies should go out: sent by you straight away, or left as a private note for a person to approve. Follow that until they change it.
- Ask before you create an inbox, since it renews every month.
- Reading, searching and private notes need no question.
- The owner can make chosen tools wait for a person's approval. Such a call answers `approval_required`, and the request goes to the approver.

## Limits

- Ticket replies go out as email. Website chat and phone messages can open tickets too, and those areas have tools of their own.
- The SLA clock runs around the clock and stops while a ticket waits on the customer. Nights and weekends count.
- Moving from Zendesk: `import_from_zendesk` brings over tickets with their public replies and each requester as a contact, at $0.001 a record, and emails nobody.

## More

- Every help desk tool with its inputs, an example and its errors: https://conecto.chat/tools/helpdesk.md
- Every error code: https://conecto.chat/docs/errors.md
- Prices: https://conecto.chat/pricing.md
- Terms: https://conecto.chat/terms
