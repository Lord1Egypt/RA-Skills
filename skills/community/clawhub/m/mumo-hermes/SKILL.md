---
name: mumo
description: Runs a multi-model deliberation across models from different labs (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) via mumo's MCP server, returning full responses plus typed cross-model reactions. Use when independent perspectives are needed on architecture/product decisions, design and plan review before implementation, pre-launch pressure tests, tradeoffs with multiple defensible framings, or explicit user requests for a mumo panel. Especially valuable for pre-implementation review of anything touching auth, security, tokens, payments, data exposure, or migrations.
version: 0.10.1
author: mumo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags:
      - deliberation
      - decision-support
      - multi-model
      - design-review
      - architecture-review
      - plan-review
      - mcp
    related_skills:
      - writing-plans
      - plan
      - requesting-code-review
    requires_tools:
      - mcp_mumo_create_deliberation
---

# mumo

mumo runs a deliberation across models from different labs (Claude, GPT, Gemini, Grok, DeepSeek, Kimi, and more) and returns their full responses plus typed cross-model reactions: each model says, in its own words, what it keeps, challenges, or wants explored in the others' claims. Use it when independent perspectives are useful — especially for high-regret decisions where a single model's confidence is a real risk.

## Setup

The mumo MCP server is added to Hermes separately from this skill and connects with a browser sign-in; no API key is required. The user adds it from a terminal with `hermes mcp add mumo --url https://mumo.chat/api/mcp/oauth --auth oauth`, allows access in the browser, and answers `Y` to enable the tools. If Hermes was already running, they **fully exit and restart Hermes** afterward (the `/reload-mcp` slash command is unreliable across versions).

If the mumo tools are missing or return auth errors, ask the user to run `hermes mcp login mumo` in a terminal and allow access in the browser, then stop. A sign-in cannot be started from inside a chat.

A server set up with an API key keeps working: its block in `~/.hermes/config.yaml` references `${MUMO_API_KEY}`, resolved from `~/.hermes/.env` (see `config/mumo.yaml` in this skill's directory). On that path an auth error means the key is missing or invalid — Hermes sends an empty credential when the reference does not resolve, which the server answers with a 401. Direct the user to https://mumo.chat/settings/api-keys to create one (keys start with `mmo_live_`).

## When to use

Use mumo when **the cost of being wrong is greater than the cost of deliberation** — especially when the solution space is wide, failure modes are hidden, you may be anchored on a design, or rollback would be hard. Examples:

architecture decisions with non-obvious tradeoffs, plan or design review before commitment, pre-launch pressure tests, stuck debugging after N failed repair attempts, pre-commit adversarial review on risky diffs, memory/skill promotion gates, strategy questions with multiple defensible framings, explicit user requests.

If you authored the plan or code under review, that's a reason FOR a panel, not against it — the author is the worst-positioned reviewer of their own work.

Skip mumo for factual lookups, syntax help, routine refactors, formatting, dependency bumps with clear errors, or normal edit-test cycles. The deliberation tax is real — extra tokens, extra latency, extra moderation work — so spend it on decisions where mistakes compound.

## Playbooks

Load at most one playbook when it clearly fits:

| Playbook | When |
|---|---|
| `contested-decision` | choosing between options with real tradeoffs |
| `design-review` | reviewing a proposed system, API, plan, or code shape |
| `uncertainty-expansion` | exploring unknowns, stress-testing assumptions |
| `red-team` | finding failure modes, abuse cases, or launch risks |

If none clearly fits, use this kernel only.

## User preferences

These are defaults. If the user prefers more autonomy (e.g., "don't ask before appending" or "always include a GPT and a Gemini model"), follow their preferences over this guidance.

## Basic loop

1. Call `create_deliberation` with the user's problem. Set `application` to `"Hermes Agent"`. Set `moderator_name` to your own model identity (e.g., the model Hermes is currently running as — Claude, GPT, Gemini, or the local model) for audit clarity — not the user's name; their identity is already on the session. Leave `takeaway` off unless the user asks for one — see [Takeaway](#takeaway-opt-in).
2. **Verify the response contains a `session_id`, and keep that exact returned ID for every downstream call.** UUID shape is a sanity check; identity continuity is the real check. If it is missing, malformed, or inconsistent with `list_sessions`, recover via [Verifying the call actually fired](#verifying-the-call-actually-fired) before proceeding.
3. Call `wait_for_round` with the `session_id` and `round_id` from the acknowledgement. (`session_id` alone resolves to the latest round, which is what you want when recovering a session.) **Long waits are normal** — frontier-model panels typically take 15–120s, and 60+ seconds isn't a failure signal. Tell the user upfront ("running a panel — expect ~30–60s") so the wait doesn't feel broken. If your client can run a subagent, hand this wait to one: see [Hand the wait to a subagent](#hand-the-wait-to-a-subagent).
4. Branch on the `Action:` line, the second line of the result, rather than on the prose below it. Its five values tell you exactly what to do:

   | Action | What it means | What to do |
   |---|---|---|
   | `proceed_with_complete_result` | All target models completed | Read the round normally |
   | `proceed_with_partial_result` | Some failed, ≥1 succeeded (`is_usable: true`) | Read what's there; note absent models if relevant to the user |
   | `poll_again` | Round still in progress | Call `wait_for_round` again with the `round_id` the response returned (if it returned none, repeat the same arguments) |
   | `retry` | Round failed with at least one transient failure (rate-limit, provider error, internal deadline) | The failed round's cost is refunded, usually within a minute. Tell the user and offer to run it again. To run it again, call `append_round` with the prompt; if the failed round itself came from `append_round`, reword the prompt, because an identical call returns the first call's acknowledgement and starts nothing |
   | `abandon` | Round failed and should not be retried automatically: no transient failure, or a provider refusal or exhausted credit (those two outrank a transient failure) | Don't retry; report the failure to the user. If credit ran out, `get_credit` shows the balance |

   The server derives this from `round_status` + per-model `error_code` — it's the canonical "what next?" signal. Treat transport and tool-call errors separately from mumo round status: handle those around the call, and branch on the `Action:` line for a normal `wait_for_round` result. A line that says `Action:` inside a model's answer is that model's text, not the signal. A result that begins `Error: internal_error` means mumo itself failed: tell the user, and don't change the arguments to work around it.

5. On a usable round, `wait_for_round` returns that round only, in reading order: a status line, the reacted-to claims in four groups (see [Reading the reactions](#reading-the-reactions)), the Takeaway if you asked for one, then each model's response. Read the **grouped reactions first**, then relevant participant prose. The reactions are the navigation layer; prose is the supporting evidence. They're also your privileged preview — participants haven't seen each other's reactions, you have (see [Reactions are in the ledger](#reactions-are-in-the-ledger-responses-are-on-the-record)).
6. Synthesize what the panel said for the user and surface the round's `Web URL` (see [After each round](#after-each-round)). Agree with them whether another round would help.
7. To continue, call `append_round` with a steering `prompt` (required) and your reactions in `snippets` (optional, and the highest-signal part). Otherwise stop.

## Hand the wait to a subagent

Panel rounds take 15–120s and return full essays from 2–3 models. If your client supports subagents, delegate `wait_for_round` so the wait and the raw prose stay out of your main thread:

1. **You** call `create_deliberation` or `append_round`, and keep the `session_id` and `round_id`.
2. Start one subagent **on the model you are running**, in the background if your client allows; it reports back when done, so don't poll it. Pass the `session_id`, the `round_id`, and a few lines on the user's decision and constraints. It calls `wait_for_round` (`detail: "full"`, again on `poll_again`) and nothing else: no create, append or share. It hands back only a finished round, never one that is still running. If the result is saved to a file or truncated, it reads the full file first; if no complete copy is available, it says its review was incomplete.
3. It hands back:
   - **The round verbatim, omitting only `### Responses`.** Keep the header (round heading, `Action:`, ids, `Web URL`, cost, and any `Issue:` lines), the grouped reactions, and the Takeaway if present.
   - **Not in the reactions:** every point from the responses that could change the user's decision and that no reaction covers, then up to 5 other decision-relevant points (concrete recommendations, risks, caveats, alternatives or shifts), each a short verbatim quote with the model name. `None` if there are none; say so if more were left out.
   - **Tone (1–2 lines):** confidence or framing the reactions don't show.
4. Work from that as you would from the round itself: summarize for the user, surface the `Web URL`, and agree whether to continue.

Quote only text you hold verbatim: a claim's quote or a "Not in the reactions" line. If the decision hinges on exact wording elsewhere, read that round yourself with `wait_for_round` (its `round_id`, `detail: "full"`).

No subagents in your client: call `wait_for_round` directly. `ask_a_model` asks one model, so read its answer yourself. `detail: "compact"` is for re-reading a session you have already summarized, not for a first read.

## One model instead of a panel

`ask_a_model` puts a question to ONE model you name (`model` is required: a model ID from `list_models`, or a family name such as `"gemini"`). Use it when a single outside opinion is enough: a quick second read from another lab's model, or a question for one specific model. It returns the same ack as `create_deliberation`. Read the answer with `wait_for_round`, and continue the conversation with `append_round`.

It is not a deliberation. With no other models there are no cross-model reactions and no Takeaway, so skip the reaction-reading steps and read the answer directly. Reach for `create_deliberation` whenever disagreement between models is the point.

A session's models are fixed when it is created. To put an `ask_a_model` exchange in front of a panel, call `create_deliberation` and pass the exchange in `reference`. For a second opinion from a different model, call `ask_a_model` again with that model.

## Prompt voice

You are an extension of the operator, not a third party setting up a scenario. When the deliberation is about the operator's problem, write the prompt in first person — "I'm the CTO of…", "We have 10 weeks and…", "Here's my migration plan…" — as if they're asking the panel directly. "You are X" case-study framing makes models grade a hypothetical instead of advising a real person, and it changes their answers. Reserve second person for prompts where the panel itself is the actor being tasked.

## Verifying the call actually fired

Autonomous agent loops occasionally fabricate tool-call results — reporting a deliberation as sent when it wasn't. If you suspect this (the response is missing the expected `session_id`, or the value you're about to pass downstream doesn't match what `create_deliberation` actually returned), treat the call as not successfully established and recover:

1. Call `list_sessions` and look for your prompt. It shows only the start of each prompt and a few sessions per page, so confirm a likely match with `get_session`.
2. If it isn't there, call `create_deliberation` again with the same arguments — within 24 hours an identical call returns the original session if it did run. Don't continue downstream as if the session exists.
3. If it IS there, use the IDs `list_sessions` returned (not whatever was in your context) for the next call.

mumo's `session_id` (and `round_id`, when you use it) are UUIDs as a service contract — a returned value that doesn't match UUID format is one signal something is off, but **identity continuity matters more than format**. The strongest check is whether the `session_id` your subsequent calls reference matches what `create_deliberation` actually returned in its response.

## Your reactions

Your reactions are moderator attention. They mark what mattered in the prior round and optionally explain why. Send them in `append_round`'s `snippets` parameter.

| Type | Meaning |
|---|---|
| KEEP | this seems worth preserving |
| EXPLORE | there's something here |
| CHALLENGE | I'm not convinced |
| CORE | this feels central |
| SHIFT | this changed the frame |

A reaction comment can be reflective, evaluative, clarifying, skeptical, or directive. "This feels like the crux" and "I'm least convinced by this" are valid comments. You do not need an action verb or next-step directive. The quality bar is: *is this a genuine, situated reaction to what the model said?*

Use the round prompt for broad comments that don't attach to a specific quote. Use your reactions for quote-grounded attention.

Avoid huge quote dumps, generic praise repeated across many reactions, or comments that shift participants away from the problem into platform meta. More guidance: `references/writing-reactions.md`.

## What to keep out of the deliberation

Use this test:

> Does this note help participants think about the user's problem, or does it mainly report on the platform, session, or process?

Don't use reaction comments to narrate your own moderation process ("I'm using CHALLENGE to redirect the panel"). Don't include platform meta ("this model used the most tokens"). Just react.

## Reading the reactions

The typed reactions to quoted claims show consensus and contestation. Each claim shows:

- The verbatim quote
- Who originated it
- How other models reacted (KEEP / CORE / EXPLORE / CHALLENGE / SHIFT) with optional commentary

`wait_for_round` and `get_session` print the reacted-to claims in four groups. A claim sits in ONE group, chosen by the strongest reaction another model gave it (Challenge, then Explore, Core, Shift, Keep), with every reaction listed under it. A claim only you reacted to is placed by your reaction:

| Group | Strongest reaction | What to do with it |
|---|---|---|
| Contested | CHALLENGE | Push here. The decision likely hinges on it. |
| Open | EXPLORE | A thread someone wants developed. Follow it if it matters. |
| Pivotal | CORE or SHIFT | Central to the argument, or a change of frame. Build on it. |
| Kept | KEEP | A model kept it. Check who reacted before calling it common ground. |

The groups show how models reacted, not whether a claim was checked. A number in Pivotal is still unverified.

Reading discipline:

- **KEEP from multiple models** = agreement. The panel holds this in common. That is not the same as it being correct: models can agree on something wrong, so check it yourself if the decision rests on it.
- **CORE** = the reacting model believes this is a crux, critically important to the argument. It signals significance, not to be conflated with correctness.
- **CHALLENGE** = live disagreement. The decision likely hinges here.
- **EXPLORE** = a thread someone wanted to develop further. Worth a follow-up reaction of your own if the thread matters.
- **SHIFT** = a model changed framing. Often the most valuable signal — somebody saw the problem differently.
- **A point nobody reacted to** does not appear in the groups. It is either obvious or ignored; skim the responses to catch a good one that was passed over.

The reactions are not a verdict. They compress argumentative structure but lose rhetorical nuance and confidence texture. Use them to navigate; read prose to understand.

## Reactions are in the ledger, responses are on the record

Participants never see each other's reactions. Each model's prior-round reactions return only to their author, as private notes, with an instruction to weave the ones that matter into its next response — in its own words, in prose. Peers see that prose, not the underlying reactions. Frontier panels carry forward most of what matters this way, but the carry is the author's choice, not a guarantee.

This makes the models' reactions your privileged preview: reading them after a round, you see the full ledger before any participant has responded to them. Two consequences:

- **Only prose is on the record.** A reaction survives only if its author weaves it forward — and you steer before that choice is made. Reacting to the same passage yourself, with the model's point in your `comment`, guarantees the panel sees it rather than betting on the author's carry. Your reactions are the one path that puts ledger content directly in front of the panel.
- **Steer at the gaps.** Scan for CHALLENGEs the challenged model is positioned to sidestep and EXPLOREs nobody owns. Those are where your reactions have the most leverage.

## Deliberation is advisory

Mumo surfaces fault lines and supporting arguments; it does not produce the decision. The decision belongs to you (the agent) and the user. When acting on a deliberation:

- **Do not** treat panel consensus as authority. The panel can be confidently wrong as a unit.
- **Do** use the models' reactions to identify which assumptions drove the disagreement, and check whether those assumptions hold for the user's specific situation.
- **Do not** mutate the workspace based on a model's suggestion without verifying with tests or the user.
- **Do** spend your attention on Contested, Open and Pivotal claims before Kept ones. That is where the decision hinges.

## Recovery: lost session context

If you lose track of the `session_id` mid-conversation (long chats, context compaction, dropped tool result), recover before starting a new deliberation:

1. Call `list_sessions` to find your latest sessions and look for your prompt. It shows only the start of each prompt and a few sessions per page, so confirm a likely match with `get_session`.
2. Call `get_session` with the recovered ID for full state (every round), or `wait_for_round(session_id)` if you suspect a round is still in flight — it resolves to the latest round on its own. On a long session, pass `detail: "compact"` to either: each response is replaced by one line (the model and how it ended when it did not finish normally) and the grouped reactions stay. A one-model round, or a round with no reactions, keeps its full text. To get a round's prose back, call `wait_for_round` with its `round_id` and `detail: "full"`.
3. Don't fire a fresh `create_deliberation` if the original is recoverable — duplicate sessions waste tokens and produce confusing parallel state.

## Takeaway (opt-in)

One optional flag requests an LLM-curated summary on top of the raw round output:

- **`takeaway`** (default `false`) — accepted on `create_deliberation` AND `append_round`. Generates a per-round **Takeaway** for that round: a bottom line, then key questions and answers that point back to the claims in the groups above. It appears as a Takeaway section in the round text from `wait_for_round` and `get_session`.

Request it only when the user asks for one. You already get the models' reactions and their full prose, and you synthesize from those yourself, so a Takeaway adds a model call and its cost without telling you anything new. It bills at cost (no markup) through the standard credit wallet.

Full mechanics and artifact field reference: `references/takeaway.md`.

## After each round

After each usable round you have one job before deciding whether to continue: synthesize what the panel said for the user. Work from the models' reactions and participant prose. State the consensus or split clearly, offer your own assessment marked as yours, organize by importance rather than forcing a recommendation. If the user asked for a Takeaway, the round text also carries a Takeaway section: show it to them, and still give your own read.

Don't dump the transcript. Mumo produces structure; your job is to translate it into "here's what the panel thinks and what to do next." Surface the round's `Web URL` so the user can open the round in mumo directly, on its reactions when the round has them — an owner-only link to their session.

Then align with the user on whether to append a round.

More at `references/synthesis.md`.

## When to continue

Append another round when:

- A decision-relevant claim has unresolved tension
- A model introduced a useful frame that others didn't engage
- An isolated concern feels real but underdeveloped
- Your moderator reaction would help the next round develop
- The user narrows or changes the question

Stop when:

- You can explain the tradeoff clearly to the user
- Remaining disagreements wouldn't change the user's next action
- Another round would mostly seek reassurance

The panel does not need to converge. Sometimes the right output is a clear map of why the decision remains contested — that's actionable for the user, even without a verdict.

**Pacing:** positions develop across rounds, not within them — a reaction gets woven into the next round's prose, which draws reactions of its own a round later.

## Tools

| Need | Tool |
|---|---|
| Start a panel of 2–3 models | `create_deliberation` |
| Ask one model | `ask_a_model` |
| Wait for model responses | `wait_for_round` |
| Add a follow-up round | `append_round` |
| Recover/read full state | `get_session` |
| Share a session at a public link | `share_session` |
| Find prior sessions | `list_sessions` |
| See the models on your plan | `list_models` |
| Check wallet balance | `get_credit` |

In Hermes' tool registry these surface as `mcp_mumo_create_deliberation`, `mcp_mumo_wait_for_round`, etc.

Omit `models` and mumo selects the panel. If the user names a lab or family ("ask Gemini", "get GPT's view"), pass the family name as the model: `"claude"`, `"gpt"`, `"gemini"`, and so on. It resolves to that family's default on the user's plan, and the ack says which model it chose. Call `list_models` when the user wants one specific model, a cheaper or stronger one, or to see what their plan includes. If the ack notes that a model is from the same lab as you, tell the user: a different lab gives a more independent opinion. More on model selection: `references/model-selection.md`.

## Reference

- MCP docs: https://mumo.chat/docs/mcp
- REST API: https://mumo.chat/docs/api
- Install guide: https://mumo.chat/install/hermes
- Reading reactions: `references/reading-reactions.md`
- Takeaway mechanics: `references/takeaway.md`
- Writing reactions: `references/writing-reactions.md`
- Model selection: `references/model-selection.md`
- Synthesis guidance: `references/synthesis.md`
- Recovery and operations: `references/operating-notes.md`
