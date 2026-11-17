# Normalized Choices

For an unresolved material shopping preference among two to eight observed
merchant options, use `request_choice` instead of asking an independent
plain-chat question. Include accurate product-variant photos when the merchant
supplies them, resolving their observed URLs to absolute HTTPS URLs. Preserve
the observed price and exact detail link for each option. Ask color and delivery
as separate requests; one selection must not silently decide both preferences.
Skip a redundant choice when the user already specified or authorized the
option, and continue with it.

For other tasks, a MagicPay choice remains an optional human-in-the-loop aid
when concrete, closed-world options materially change the next step. Do not
create one for a single obvious result, a factual lookup, an open-ended
question, or to replace payment, Memory, login, or other protected approval.

## Normalize messy sources

Fetch or observe the current source first. Turn comparable results into the
small stable `request_choice` shape:

- `prompt`: a short question plus only the shared context needed to choose.
- `notes`: optional concrete limitations shared by the options that change the
  user's decision, rendered after the options. Omit them when no such limitation
  is observed. Keep routine explanations out of both notes and the prompt.
- `id`: opaque and unique within this request; never derive authority from it.
- `type`: a lower-case semantic hint such as `flight`, `hotel`, `product`,
  `plan`, or `service`; unknown content uses a useful generic key.
- `title`: short, unique human label.
- `subtitle` and `description`: product/seller context and the tradeoff that matters.
- `attributes`: ordered `{key,label,value}` facts that compare across options.
  Keep zero and false values. Include units and qualification in the value.
- `price`: display text with currency, billing interval, per-unit/total, and tax
  qualification where the source supplies them.
- `images`: objects with `url`, explicit `kind: image` or `kind: logo`, and
  optional `alt`. Preserve source order; a text-only option may omit images.
- `url`: the exact source/detail page. Opening it never selects the option.

Use actual current source facts. Do not convert payment-network alternatives
for one endpoint into duplicate products, claim travel availability without
dates/occupancy, or invent a missing price, baggage allowance, stock state, or
commercial term. Narrow a larger result set by relevance before asking.
Keep option-specific terms in that option's description or attributes, not in
shared notes. For flights, include observed date, route and departure/arrival
times on each option so its selected receipt is self-contained. Preserve the
currency, total/per-person basis and supplied fare qualifications in `price`.
Send these fields as plain text; the host owns bold titles/prices and note
formatting. Never add HTML or Markdown decorations to the stored choice fields.

Keep retrieval-provider attribution (such as "from Google Flights"), API/tool
names and "official"/"unofficial" implementation labels out of customer-facing
choice text. Preserve observed airline, seller and service identities and all
material product terms; never turn an unknown fact into a reassuring claim.
Keep concrete baggage or fare restrictions in the affected option. Do not add
generic disclaimers such as "Local times shown", "All options are nonstop
economy", "recheck fare availability and baggage before purchase", or "selection
does not book or pay". Show the actual itinerary and fare facts once on each
option; verify current availability and terms internally before checkout. If
the user explicitly asks about the source or implementation, answer truthfully
without adding routine attribution to choice notes.

For Memory options, use the saved item name as `title`, its entity as `subtitle`,
and only the requested field labels in `description`. Keep the entity/item
descriptions when needed to distinguish otherwise identical names. For a
multi-item option, identify each item and the fields requested from it. Never
put saved field values in choice metadata.

Memory resolver choices have their own decision contract in [memory.md](memory.md).
Keep a declared **Provide different details** alternative, including on a
single-item approval, and submit its exact stored ID with `choose_candidate`.
It is not the generic “none of these” denial described below. Never synthesize
this option or hide it to fit a native control; use a faithful fallback when
needed. Do not create `request_choice` to replace an existing Memory request.

## One durable request, one conversation control

If no relevant MagicPay session already exists, call `begin_request_session`
once with a plain description, then use its exact `sessionId`. Call
`request_choice` once with a stable idempotency key and the normalized options.

For a new `waiting_user` result:

1. Prefer one faithful host-native single-select control with the exact stored
   prompt, option order, titles, and decision-relevant descriptions. When that
   native control is available, show only it: do not paste `chatMessage`, open
   a MagicPay widget, or display `request_url` in this conversation.
   Preserve shared notes beneath the options when the control supports them;
   otherwise use the faithful widget/chat fallback rather than dropping a
   qualification that changes the user's decision.
2. Without a suitable native control, present the same request with
   `show_session_request` when the host renders its widget. If neither control
   is available, echo `structuredContent.chatMessage` unchanged and include
   `request_url` when available. Do not duplicate a rendered widget with a
   chat prompt. `request_choice` itself creates no widget.
3. Preserve `sessionId`, `requestId`, stored option order, and opaque IDs. Never
   create a sibling request because another channel is open.

Other enabled MagicPay channels may still carry this same request. The user
may answer in chat, the widget, web, mobile, or Telegram. Submit a chat
answer only when it maps unambiguously to an in-range ordinal, exact stored
title, or exact ID. Call `decide_request` with `decision: confirmed` and the
exact `selectedChoiceId`, then `wait_request` on the same IDs.

A follow-up that changes cabin, date, passenger count or another search fact
refines the same task. If the generic choice permits adjustments, submit
`decide_request` with `decision: confirmed` and `adjustmentPrompt` containing
the user's correction, with no selectedChoiceId, values or Save. Read its exact
adjustment_requested outcome with `wait_request`, then search and publish
updated options in the same task. Use one new stable choice idempotency key for
the revised result set in the same session; reuse that new key on retries and
keep the old adjustment outcome immutable. An active hosted turn that consumes the
adjustment owns this search; continue in that turn without creating a second
continuation. If the host instead resumes a saved adjustment after the source
turn ended, that continuation is its sole owner.
Do not use `denied` to clear an old choice. Status and side questions leave it
pending. When the scope is unclear, clarify it before making a decision.

A native picker is presentation only and follows the same decide/wait path:
an answered option submits `confirmed` with its stored ID; an explicit task
cancel or rejection without refinement submits `denied`; a skipped or dismissed control is not a decision, so present
the same stored options once more through the same control and never create a
sibling request.

All open views converge on the first durable decision. If submission is late,
ambiguous, or loses a race, read/wait on the exact request and use its recorded
outcome. Never overwrite the winner or report a local draft as selected. A
terminal replay omits a new prompt: do not present the options again.
When the displayed request already shows the selected state, skip another
“You chose…” acknowledgement. If work continues, describe the next meaningful
step from actual execution instead of repeating the selected option or price.

The selected option authorizes only which branch the agent may continue with.
It does not book, buy, subscribe, transfer funds, submit a form, or approve a
payment. Obtain the normal authority for any later consequential action.

Good uses: compare three current cloud plans; select one real itinerary after
dates are fixed; choose among normalized x402 search providers when a material
tradeoff remains; pick one product variant from current browser results.

Do not use a choice for a factual lookup, a single matching result, free-form
requirements, payment confirmation, or a saved Memory candidate conflict.

## Input example

Example `request_choice` input (synthetic data, not current commercial claims).
In a real call, use the returned session ID and observed source facts:

```json
{
  "sessionId": "11111111-1111-4111-8111-111111111111",
  "idempotencyKey": "compare-plans-01",
  "prompt": "Which plan fits your preference?",
  "options": [
    {
      "id": "plan-starter",
      "type": "plan",
      "title": "Starter",
      "subtitle": "Example provider",
      "description": "Lower cost, no included support",
      "price": "USD 5/month, taxes excluded",
      "attributes": [
        {"key": "setup_fee", "label": "Setup fee (USD)", "value": 0},
        {"key": "support", "label": "Included support", "value": false}
      ],
      "images": [
        {"url": "https://example.com/starter.png", "kind": "image", "alt": "Starter plan overview"},
        {"url": "https://example.com/logo.png", "kind": "logo", "alt": "Example provider"}
      ],
      "url": "https://example.com/starter"
    },
    {
      "id": "plan-assisted",
      "type": "plan",
      "title": "Assisted",
      "description": "Includes support; source does not list a price",
      "attributes": [{"key": "support", "label": "Included support", "value": true}],
      "url": "https://example.com/assisted"
    }
  ]
}
```

## Continuation examples

| Observation | Next action |
| --- | --- |
| One factual answer, no material tradeoff | Answer directly; do not create a choice. |
| Two useful plans differ in price or service | Create one choice; prefer only the native picker, otherwise one widget or the chat/link fallback. |
| Reply could mean two options | Ask which stored option the user means; do not decide or create a sibling. |
| Another channel selected a different option | Read/wait on the same request; use its recorded winner. |
| Request expired or was denied/canceled | Report that outcome; no fabricated selection or repeated pending prompt. |
| Browser is unavailable | Choices still work through MCP; a later browser payment needs the actual host capability. |
