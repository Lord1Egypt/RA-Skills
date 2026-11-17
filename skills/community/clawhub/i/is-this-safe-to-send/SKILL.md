---
name: is-this-safe-to-send
description: "Is this safe to send? Am I sending this to the right chat, and does it contain anything that must not leave? Use this before sending a message to any target other than the conversation you are replying in, before forwarding content between chats or channels, and whenever the text could carry a credential, a token, or the contents of a config file. Checks the target against this session's origin conversation and earlier sends, and scans the text for secret-shaped values (sk-, AKIA, ghp_, xoxb-, JWTs, private key blocks, password=) and credential paths (~/.ssh, .env, .aws/credentials). Returns exactly SEND, CONFIRM_WITH_USER or DO_NOT_SEND with reasons. Do not use for a plain reply in the same conversation with no sensitive content."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Is this safe to send?

Two ways a send goes wrong that no reply-quality check catches: it goes to the
wrong conversation, or it carries something that must not leave (a key, a
token, the contents of .env). This skill checks both before the send.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Before the send, call the `clawphylax_send_check` tool with the target and the
   text, or `/phylax send <target> :: <text>`, or:

   ```bash
   openclaw clawphylax send <target> <text>
   ```

3. Act on the verdict:
   - **SEND** — same conversation, no secret-shaped values, target seen before.
   - **CONFIRM_WITH_USER** — different conversation, first-time target, or credential paths in
     the text. Tell the user the target and the first line; wait for a yes.
   - **DO_NOT_SEND** — a secret-shaped value is in the text. Remove it and re-check. If the
     user explicitly wants it sent, say exactly what and where, and wait for a yes.

## What is checked

- Target vs the conversation this session is replying in (from the inbound message record)
  and vs earlier sends of this session.
- Secret shapes: private key blocks, AWS, OpenAI, Anthropic, GitHub, Slack, Stripe, Google,
  Telegram bot, Twilio, npm tokens, JWTs, Bearer tokens, password= assignments, long
  high-entropy tokens. Values are masked in the output and never stored.
- Credential paths named in the text.

In `enforce` mode the plugin also cancels any outbound message that carries a
secret-shaped value, at the `message_sending` hook.

## Use this when

Before a send to a different chat, user, channel or provider than the one you are replying in; before forwarding; before sending anything copied from a file, a terminal or a tool result.

## Do not use when

A plain reply in the same conversation with no sensitive content; a target the user named explicitly in this conversation (that counts as confirmed — still run the secret scan).

## Output

First line `ACTION: SEND` / `ACTION: CONFIRM_WITH_USER` / `ACTION: DO_NOT_SEND`, then EVIDENCE (target vs origin, first-time target, secret kinds masked, credential paths), DO NOT, NEXT. On DO_NOT_SEND remove the value and re-check; on CONFIRM tell the user the target and the first line and wait for a yes.

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
