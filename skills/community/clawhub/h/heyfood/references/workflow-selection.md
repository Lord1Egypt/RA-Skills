# Workflow selection

Select by surface first. The local and remote surfaces share no tool names, so
a tool that is absent is absent — not renamed.

## Local surface

### Discovery

Run `heyfood agent describe` first. It is offline, credential-free, and
version-matched to the executable.

Use these surfaces in order:

1. A listed `heyfood_*` MCP tool with an input schema matching the task.
2. An exact manifest command whose audience is `agent_safe`.
3. A truthful user handoff.

Never treat MCP absence as permission to invoke a different audience.

### Supported read intents

Your tool list is authoritative — this inventory describes a release, not a
ceiling. A newer client may expose `heyfood_*` tools not named here; read their
schemas and use them. Never withhold a tool the client advertises because this
list predates it, and never assume one it does not.

When present, prefer:

- `heyfood_get_manifest` for installed contract discovery;
- `heyfood_get_status` for service, authorization, and local readiness;
- `heyfood_get_capabilities` for server-advertised support;
- `heyfood_get_grocery_list` for the active household-aware list;
- `heyfood_get_grocery_exclusions` for never-buy exclusions; and
- `heyfood_list_menu_watches` for recurring watch summaries.

Do not guess that a service failure means an empty result.

Collection tools return at most 100 records. When `page.next_cursor` is
present, pass it back unchanged with an optional `limit` from 1 through 100.
Do not parse, edit, or fabricate cursors. If the server returns
`mcp_cursor_stale`, restart at the first page and do not combine pages from
different snapshots.

## Remote surface

### Discovery

There is no manifest and no binary. Your tool list is the contract. Do not run
`heyfood agent describe`, and do not report its absence as a fault.

Use these in order:

1. A listed hello.food tool whose input schema matches the task.
2. A truthful user handoff.

There is no command fallback on this surface. If no tool matches, stop.

### Tool inventory

- `lookup_restaurant`, `search_restaurants` — identify a restaurant
- `get_menu_status` — polls a menu-fetch job. It requires a `job_id` issued by
  a fetch you started, so on a read-only deployment that never starts one there
  is nothing to poll. Do not call it to test whether a menu exists; that is not
  what it answers.
- `evaluate_menu`, `recommend_items` — dietary assessment against a captured menu
- `explain_item` — dietary assessment of an item *name*; reads no menu
- `draft_order_message` — phrase an order request
- `search_recipes`, `list_saved_recipes`, `suggest_recipes` — recipes
- `ask_dietary_question` — general dietary knowledge
- `describe_dietary_graph`, `get_food_preferences`, `get_meal_history` —
  profile-derived context

A hosted deployment may expose a subset. Absent tools are unavailable
capabilities, not tools to be reached another way.

### Restaurants and menus

**Resolve the restaurant before assessing anything.** Most assessment tools key
on `restaurant_id`, which you do not have from a user's words. Get it first:

- `lookup_restaurant(name)` when the user named a specific place.
- `search_restaurants(query, location_query, radius_miles, limit)` when they
  described one, or asked what is nearby.

If resolution is ambiguous, ask. Never assess a guess — two branches of a chain
can carry different menus, and a confident answer about the wrong location is
worse than a question.

**One asymmetry, and it is not a shortcut.**
`explain_item(item_name, restaurant_name)` takes plain names, while
`evaluate_menu`, `recommend_items`, and `draft_order_message` take
`restaurant_id`. That is not because it resolves the restaurant for you — it is
because **it never reads a menu at all.**

`explain_item` assesses the item *name* against the dietary profile.
`restaurant_name` is context, not evidence. Its verdict is not evidence that the
dish exists at that restaurant, that it is described the way the user described
it, or that the kitchen prepares it that way. It returns the same answer whether
or not that menu has ever been captured.

That makes it genuinely useful — a user can ask about a dish anywhere — and it
makes one specific move wrong:

> **After a `menu_not_captured` result, do not quietly retry with
> `explain_item` and present what comes back as though it came from the
> restaurant's menu.**

That is the failure this product exists to prevent. The user asked what is on
*that* menu; answering from the profile alone, in the same voice, tells them the
kitchen was checked when it was not. You may still use it — say what it is: an
assessment of the dish as described, not of that restaurant's version of it.

**Then choose by the shape of the question:**

| The user asks | Use |
|---|---|
| "Can I eat X here?" | `explain_item` — one dish, with reasons and conflicts. Not menu-grounded: see above |
| "What's safe on this menu?" | `evaluate_menu(restaurant_id, item_names)` |
| "What should I order?" | `recommend_items(restaurant_id, query, …)` |
| "Ask them to leave out the X" | `draft_order_message` |

`evaluate_menu` takes explicit `item_names`. It assesses what you give it — it
does not fetch a menu for you to browse. If the user has not named items, either
ask which dishes they are considering, or use `recommend_items` instead.

**Preserve the verdict.** Carry the service's own safety wording, reasons,
conflicts, allergen detail, alternatives, and any freshness or provenance
markers through to the user unchanged. Do not re-rank, re-summarize, soften, or
convert a status into your own phrasing. Never state that a food is "safe".

**Cold menus** are covered below. Treat them as coverage, not safety.

### Households — read this before answering for anyone

hello.food is built for people who decide what someone *else* eats. Getting the
scope wrong does not produce a vague answer; it produces a confident answer
about the wrong person.

**The default is household-wide, not you.** On an account with synced members,
a call that passes no scope is evaluated for the WHOLE household. Do not assume
an unscoped call means the account owner.

`household_scope` accepts exactly three things:

| Value | Means |
|---|---|
| `"_self"` | the account owner alone |
| `"everyone"` | all members |
| a member id | that member alone |

**`member_id="_self"` does NOT mean "just me".** It is the argument's default
and carries no scope at all, so it falls through to default resolution — which
on a member-having account is household-wide. To mean the owner alone you must
send `household_scope="_self"` explicitly. `member_id` is a legacy alias kept
for deployed clients: an explicit `household_scope` always wins, and any
`member_id` other than `_self` means that member.

**Never infer scope from phrasing.** "Can my daughter eat this" does not
license guessing a member. Resolve the member, or ask. The service honours the
scope you send authoritatively and never reads intent from wording — so an
unscoped call for a named person is a wrong answer, not an approximate one.

**Read the aggregate correctly.** In `evaluate_menu`, each item is assessed
once per member in scope. **The headline status on an item is the household
AGGREGATE — worst status wins** — and the additive `member_annotations` say
WHO. Reporting the headline alone tells a caregiver "avoid" without saying it
is avoid *for one member*, or lets them read a household verdict as being about
themselves. Always carry the per-member annotations through with the headline.

Flags on an item are informational; these tools never drop an item from the
result. Absence of a warning is not a clearance.

**Scope rejections are answers, not retry conditions:**

- **422** — the scope was malformed, or needs an account capability this one
  does not have.
- **404** — a well-formed member id that is not a synced member of THIS
  account.

Neither is ever degraded into a different evaluation set, and you must not
degrade it either. Do not retry unscoped, do not substitute `_self`, and do not
fall back to the owner. Report which member was not found and stop.

### Recipes

Three tools, three different jobs — picking the wrong one gives the user
something that looks like an answer and is not:

- `search_recipes(query, cuisine, meal_type, max_ready_time, limit)` — find
  existing recipes matching a request.
- `suggest_recipes(recipe_title, ingredients, constraints, servings)` — adapt a
  specific recipe the user already has in mind, for their constraints. Pass
  their actual constraints; do not restate them into your own words.
- `list_saved_recipes(limit)` — what the user already saved. Use it before
  suggesting something new when they refer to "my" recipes.

Recipe results carry dietary reasoning for the same reason menu results do.
Preserve it. A substitution offered by the service is part of the answer, not a
detail to compress away.

**Saving is a mutation** and is not available here. If a user asks to save a
recipe, say so plainly rather than implying it was kept.

### Households on the local surface — discover the exact boundary

Local household support varies by installed contract. Do not branch on the
binary version or on remembered tool counts. After accepting a supported
manifest schema, inspect the household capability rows and the current MCP tool
list.

| Discovered state | Required behavior |
|---|---|
| No active household capability and no household MCP tool | Household work is human-TUI-only. Tell the user to run bare `heyfood`; never drive it yourself. |
| Roster/profile capability with its matching read tool | Use only the exact advertised read schema. Preserve stable member references, active scope, disclosure state, readiness, revisions, restricted counts, and pagination. |
| Roster/profile capability but no matching MCP read tool | Use an exact `agent_safe` one-shot read only if the manifest advertises it; otherwise hand off. |
| Lifecycle capability with prepare/status/cancel/reconcile tools | Prepare the exact change, give the returned bare-heyfood handoff, observe status, cancel only before dispatch, and reconcile only when the result requires it. The agent never approves or commits. |
| Any capability/tool/schema disagreement | Do not use the partial surface. Run the binary-owned compatibility diagnostic described in `SKILL.md` and fail closed. |

Treat household capabilities independently:

- roster access does not grant profile access;
- roster/profile access does not grant local household-scoped food evaluation;
- lifecycle preparation does not grant approval or commit authority; and
- one advertised operation does not authorize another absent operation.

Use `heyfood_get_household_context` and `heyfood_get_household_member` only when
they are present and their manifest inventory rows are active. If MCP is
unavailable, `household show` and `household member` are eligible fallbacks only
when their exact command rows are `agent_safe` and their required
`--json --no-input` contract is present. Never parse `/household` or other TUI
output.

Household reads are disclosure-gated. Do not infer a member from a display name,
substitute self after a denial, reveal a restricted subject, or present a
partial result as Everyone. A missing, expired, or revoked grant is an
authoritative refusal and a handoff to the person's TUI controls, not a retry
condition.

For the first read, ask the person to run `/household agent-access MEMBER` in
the attached TUI and copy the exact `Agent handoff` command it prints after the
grant. That handoff is the authority for the stable member reference,
disclosure generation, and maximum projection. Never scrape or automate the
TUI, guess either value, broaden the projection, or reuse the command after a
revocation reports that the earlier handoff is stale.

For a discovered lifecycle, use only tools actually present:

- `heyfood_prepare_household_change` prepares but does not mutate the household;
- `heyfood_get_household_change` observes the exact proposal state;
- `heyfood_cancel_household_change` is valid only before commit dispatch; and
- `heyfood_reconcile_household_change` resolves an uncertain outcome without
  replaying the change.

There is no agent confirmation path unless a future supported manifest and tool
contract explicitly introduce one. Never infer one from natural-language
agreement, a host approval dialog, proposal data, stdin, or TUI access. In the
supported attached-review flow, the person opens bare `heyfood`, reviews the
exact local change, and chooses whether to save it.

Local household food evaluation is a separate capability. Do not use roster,
profile, Grocery, or lifecycle tools as evidence that an evaluation tool exists.
When it is absent locally but the hosted surface is also available,
household-scoped evaluation may be performed only with the hosted tool contract
described above.

### Not available remotely

**Grocery and Menu Watch have no remote tools and no corresponding
authorization scopes.** Do not describe them as temporarily unavailable, do not
retry, and do not offer to enable them. Tell the user they require the local
hey.food client.

### Cold menus

A restaurant may have no captured menu. Evaluation tools then return a typed
`menu_not_captured` result — a successful call reporting coverage, not a
failure. Report it as such. Never present it as a safety judgement, and never
infer that a dish is acceptable because no menu was found.

**Do not substitute a different tool to produce an answer anyway.**
`explain_item` will happily return a verdict for the same dish, because it reads
the item name and not the menu — so it is unaffected by the very thing the user
just hit. Reaching for it here converts "we have not captured this menu" into
what sounds like a checked answer. If you use it, say plainly that it assesses
the dish as described and not that restaurant's version of it.

## Human experience

Bare `heyfood` and `heyfood chat` are human terminal experiences. Tell the
user how to launch them when appropriate, but never control them. They exist
only where the local client is installed.

## Deferred capabilities

Health, default-build native voice, and public Windows distribution remain
deferred unless the exact installed manifest says otherwise. Do not infer
support from source files, hidden commands, plans, or marketing history. On the
remote surface, infer support only from the tool list you were given.
