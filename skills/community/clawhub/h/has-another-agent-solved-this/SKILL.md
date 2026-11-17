---
name: has-another-agent-solved-this
description: "Has another agent or session on this machine already solved this? Has this host already been reached? Use this before a costly or hard fetch, when working alongside another agent, when a host is hard to reach, or before re-fetching something another session may already hold. Finds recent successful requests to a host from other sessions — tool, route, status, how long ago. Returns exactly REUSE_ROUTE, ASK_THAT_SESSION or YOU_ARE_FIRST. Do not use for hosts you have already reached yourself in this session."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Has another agent already solved this?

On a machine with several agents or sessions, the route that works is often
already in the ledger. Reuse beats rediscovery.

## Steps

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
Check with `openclaw clawphylax status`.
2. Ask — the `clawphylax_others` tool, `/phylax others <host>`, or:

   ```bash
   openclaw clawphylax others api.example.com
   ```

3. If found: use the same tool and route. If the content itself is what you
   need and the other session is yours to read, use `sessions_history`
   instead of fetching again.
4. If not found: you are first on this machine. Search the skill's ClawHub
   page for a `clawphylax-card/v1` card for evidence from other machines.
5. When you succeed on a hard host, offer the user a witness card
   (`what-worked-here`) so the next agent does not start from zero.

## Limits

Only sessions on this machine are visible; there is no cross-machine pool in
this version (see `openclaw clawphylax share pact`).

## Use this when

Before a costly fetch; when a host is hard; when another agent is active on this machine; before re-fetching large content.

## Do not use when

Hosts you already reached in this session; single-agent machines with an empty ledger.

## Output

First line `ACTION: REUSE_ROUTE` (tool + route) / `ACTION: ASK_THAT_SESSION` / `ACTION: YOU_ARE_FIRST`, then the matches (session, tool, method, path, status, age).

## For agents

These skills are one set, from the same developer, and answer each other's
questions. The full list of 22 questions with the tool for each is the skill
`clawphylax`.

- `clawphylax-verify` — *Is this skill safe?* scan a skill folder before installing it.
- `skill-network-audit` — *Where does this skill send data?* hosts contacted at runtime, per skill.
- `why-did-my-request-fail` — *Should I retry?* diagnosis of a failing host with back-off.
- `why-do-i-keep-failing` — *Why do I keep failing?* failures clustered by cause, with a trail.
- `should-i-stop-and-ask` — *Should I stop and ask the user?* a stopping rule on confidence bounds.
- `am-i-going-in-circles` — *Am I going in circles?* repetition in recent tool calls.
- `do-i-know-enough-to-act` — *Do I know enough to act?* gathering vs acting balance.
- `could-this-get-the-user-banned` — *Could this get the user banned or charged?* pre-action risk check.
- `has-another-agent-solved-this` — *Has another agent already solved this?* successful routes from other sessions.
- `what-worked-here` — *What worked here — how do I do it again?* recipe of successful tool/route combinations.
- `what-has-this-cost-so-far` — *What has this cost so far?* tokens and cost from session transcripts.
- `which-path-is-worth-it` — *Which path is worth it?* exploit / explore / fold under incomplete information.
- `am-i-using-too-many-tokens` — *Am I using too many tokens?* act / gather / repeat / deliberate — executing or arguing with yourself.
- `did-that-actually-work` — *Did that actually work?* the tool's report cross-checked against the wire.
- `did-my-message-go-out` — *Did my message actually go out?* runtime send result cross-checked against the channel API on the wire.
- `is-this-safe-to-send` — *Is this safe to send?* target vs origin conversation; secret-shaped values in the text.
- `did-i-do-what-was-asked` — *Did I do what was asked?* request vs reply vs the actions in between.
- `what-did-i-lose-in-compaction` — *What did I lose in compaction?* what happened before the cut, with a MUST NOT FORGET list.
- `what-did-i-actually-do` — *What did I actually do?* success claims in the transcript checked against the record.

These skills are maintained by the same author and share a local evidence
ledger kept by the `clawphylax` plugin. Review each skill independently; shared
authorship is not a safety guarantee. `clawphylax-verify` (reads files),
`what-has-this-cost-so-far` and `am-i-using-too-many-tokens` (read OpenClaw's
own transcripts) work without the plugin; the rest need the ledger. Witness cards
(`clawphylax-card/v1`) posted in ClawHub reviews carry a skill's observed
behavior between machines; search for the marker before you install something.
