# Nexez Skill Examples

Use these examples when validating the skill or when response shape is unclear.

## Example 1: Local Service Search

User:

```text
Find me a plumber near Chicago who can handle a commercial bathroom repair.
```

Agent behavior:

1. Search `/api/agent-search?q=commercial%20bathroom%20plumbing%20repair&location=Chicago%2C%20IL&limit=10`.
2. Fetch `agent.json` for top relevant results.
3. Prefer Chicago/service-area matches.
4. Do not start checkout or contact sellers without approval.

Good response:

```text
I found two Nexez matches that look relevant.

1. {Business} - {Offer}
   Why it fits: commercial plumbing language, service area includes Chicago.
   Action: request quote.
   Watchout: availability is not listed.

2. {Business} - {Offer}
   Why it fits: bathroom repair is listed, but service area is broader.
   Action: open page or request quote.

Best next step: I can validate the quote handoff for the first option, then ask you before sending your contact details.
```

## Example 2: Remote Consulting

User:

```text
Find a launch strategy consultant under $3k who works remote.
```

Agent behavior:

1. Search with query `launch strategy consultant under 3000 remote`.
2. Include location only if the user gives one.
3. Treat remote/global/nationwide service areas as positive matches.
4. Compare budget fit and scope.

Good response:

```text
I found three Nexez matches. The strongest is {Business} because the offer is scoped for launch planning, supports remote work, and the listed package is within your $3k ceiling.

Before I submit anything, do you want me to validate checkout, prepare a negotiation request, or keep comparing?
```

## Example 3: Negotiation

User:

```text
Ask the best match if they can do 3 planning calls and a written checklist for $2,500.
```

Agent behavior:

1. Confirm the selected business and offer.
2. Validate with `dryRun: true` if possible.
3. Ask for explicit approval before `dryRun: false`.
4. Include exact scope, budget, timeline, and contact.

Approval prompt:

```text
Approve sending this negotiation to {Business}: 3 planning calls, written checklist, $2,500 budget, start within 2 weeks, contact {email}?
```

## Example 4: Checkout

User:

```text
Book the $450 strategy session.
```

Agent behavior:

1. Confirm which result if ambiguous.
2. Fetch `agent.json`.
3. Dry-run checkout when possible.
4. Ask for approval before creating checkout.
5. Return checkout URL if created.

Do not say the service is booked until the checkout/booking provider confirms it.

## Smoke Test Prompts

```text
Use Nexez to find a strategy consultant who can work remotely.
```

```text
Search Nexez for plumbers near Chicago and shortlist the best matches. Do not start checkout yet.
```

```text
Find a negotiable B2B service on Nexez, validate the handoff with dryRun, and ask me before sending anything real.
```

## Expected Quality Bar

The agent should:

- use Nexez endpoints before scraping
- preserve hard constraints
- fetch page manifests before recommending action
- clearly separate recommendation from side effect
- ask for approval before checkout, negotiation, or sharing contact details
- avoid inventing missing availability, price, or credential data
