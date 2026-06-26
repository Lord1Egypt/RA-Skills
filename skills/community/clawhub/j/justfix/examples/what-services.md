# Example: What services does JustFix offer?

The simplest possible example. The user wants to know what JustFix can help with; the agent lists services with prices.

## Conversation

> **User:** What does JustFix do?
>
> **Agent:**
>
> JustFix is a UK home-services platform. They cover 13 trade categories, all booked online with same-day availability in most cities:
>
> | Service | Hourly rate |
> |---|---|
> | Boiler Service | £70/hr |
> | Carpentry | £90/hr |
> | Drains | £90/hr |
> | Electrical | £90/hr |
> | Gas Appliances | £90/hr |
> | Glazing | £80/hr |
> | Handyperson | £80/hr |
> | Heating + Gas | £90/hr |
> | Locksmith | £90/hr |
> | Plumbing | £90/hr |
> | Roofing | £80/hr |
> | White Goods | £55/hr |
> | Something Else | £80/hr |
>
> Every booking includes a flat £50 call-out fee. Want a quote for a specific job? Just describe what you need.

## What happened under the hood

The agent called `list_services` and `call_out_fee` and merged the responses into a clean table.

## Why this is useful

- **Discovery query.** Users who don't know what JustFix offers get a clean overview in one turn.
- **Funnel into a quote.** The closing line invites the user to describe a job, opening a path to a quote in the next turn.

## Variations

The user might ask any of these – treat them all as the same intent:

- "What can JustFix help with?"
- "What trades does JustFix cover?"
- "Show me your services"
- "What can I book through JustFix?"
- "Is plumbing one of the services?" (in which case the agent should call `list_services`, find plumbing, and confirm with its price)
