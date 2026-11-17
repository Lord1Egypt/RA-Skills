---
name: "kid-safe-assistant-setup"
description: "Deploy a locked-down OpenClaw chat assistant for a child: sandboxed tools, safety rules, photo/voice chat, parent progress digest"
---

# Kid-safe OpenClaw assistant — setup playbook

Deploys a locked-down, web-chat-only OpenClaw assistant for a child, on a
resource-constrained home server, plus a private weekly progress digest for
the parent. Derived from a real deployment (two children sharing one
container on a 4GB mini PC running Home Assistant OS + Docker).

Use this when a parent wants to give a child their own AI assistant for
homework help, with hard safety boundaries and without exposing an admin
dashboard, raw tool access, or the parent's own accounts.

## 1. Decide: new container or new agent in an existing one

- If the host has headroom for another ~1.5GB container, create a dedicated
  `openclaw-<child>` container (own image, own network, own volume).
- If memory is tight (check `free -h` / swap usage first), add the child as
  a second **agent** inside an existing kid-assistant container instead:
  workspace at `~/.openclaw/workspace-<child>`, its own SOUL/IDENTITY/USER/
  AGENTS files, own WhatsApp account if used. This roughly halves memory
  versus a second full container. Disable unused plugin modules (browser,
  canvas, ollama, openai, talk-voice, xai, etc.) to shrink RSS further —
  keep only what's actually used (e.g. device-pair, a TTS provider,
  whatsapp).

## 2. Lock down tools before anything else

- `tools.profile: minimal` plus an explicit `tools.deny` list covering exec,
  fs, web, browser, sessions, messaging, plugins — the child's assistant
  should have **zero** tool access, full stop. Disable `elevated`.
- Verify on a **fresh** session id (`--session-id $(date +%s)`, since a
  reused session can recall tools from its own history even after the
  profile changes) that no tools are exposed.
- If the underlying CLI backend exposes its own toolbox independent of
  `tools.deny` (e.g. a `claude` binary giving Bash access outside OpenClaw's
  control), neutralize it (e.g. rename `claude` → `claude.disabled`) so the
  model can't reach it.
- Never give the child's container a Docker socket or SSH key to the host.

## 3. Write the persona (SOUL / IDENTITY / USER / AGENTS)

In the child's own language, tutoring tone:
- Short answers, no long lectures, warm but never condescending.
- Homework: guide with questions and hints, don't hand over the answer;
  explain the method on a neighboring example if the child is stuck.
- Games only when they're disguised revision (quiz, vocab, logic puzzles);
  decline pure entertainment requests and offer a revision-flavored version.
- Hard rules that don't bend even if the child insists, claims parental
  approval, or role-plays around them: no adult/violent/hateful content, no
  cheating/hacking help, never asks for or retains personal info (address,
  school name, phone numbers, passwords, photos of people).
- The assistant never claims to have done something it can't (sent, saved,
  searched, executed) — since it has no tools, it says so plainly.
- Sensitive-topics clause: if the child mentions distress, bullying,
  violence, or danger, respond seriously, don't minimize, point to a
  trusted adult and the relevant local helplines.
- State plainly that only the parent can change these rules.

Add capability clauses to match whatever the web chat page actually offers
(see §4) — don't let the persona say "I can't do X" for something the page
already supports. Concretely worth including: reading photos of lessons/
sheet music (name it as a specific capability, e.g. "you know how to read a
score exactly like a math exercise" — a generic "I can help with school
subjects" undersells it and the model will otherwise deny the capability by
default), light language-learning tutoring (vocabulary, short exercises, not
grammar lectures), and how the child should interpret "read this aloud"
requests given the actual TTS mechanism in place.

## 4. Build the web chat front-end (no admin dashboard exposed)

A parent generally wants the child to have "a chat page like mine" without
the config/dashboard access that would let them read a sibling's
conversations or change rules. Build a minimal reverse-proxy web app instead
of exposing the OpenClaw dashboard:

- One tiny Node HTTPS server (self-signed cert fine for LAN use), one URL
  path + one password per child, session cookie (HttpOnly, Secure,
  SameSite=Strict), brute-force lockout (e.g. 5 fails → 10min IP block).
- The server holds the real gateway token; the browser only ever sends
  plain text/images and never reaches the gateway directly. It proxies to
  the gateway's OpenAI-compatible `/v1/chat/completions` endpoint with
  `model: openclaw/<agentId>` and a `user: web:<child>:<conv>` session key.
- Conversation history: keep an **append-only** JSON file per child
  (`{conv, messages:[{role, text, ts}]}`), where "new conversation" just
  increments `conv` and pushes a `sep` marker — never truncate history. This
  is what makes a later progress digest (§6) possible.
- Split the container into two volumes: app code **read-only**, data
  (history JSON + TLS certs) **read-write**. Readonly code is a deliberate
  hardening choice — see §5 for how to still deploy updates to it.
- Nice-to-have UI features that matter more than they sound for a kid doing
  homework: photo upload (resize client-side before sending, cap count and
  size), browser-native speech-to-text for dictation, and browser-native
  text-to-speech for read-aloud. Default the read-aloud toggle to **on**
  (auto-speak every reply, not just on tap) — a "press this button to hear
  me" instruction is a paper cut kids won't reliably do. If the assistant
  might reply in more than one language (e.g. language-learning), detect the
  reply's language client-side (simple keyword/diacritic heuristics are good
  enough) and pick a matching browser TTS voice instead of hardcoding one
  locale.

## 5. Editing a read-only app-code volume

If the code volume is mounted `:ro` into the running container (recommended,
§4), you can't `docker exec` a write into it. Use a disposable helper
container that mounts the **same named volume without `:ro`**:

```bash
cat new-file | docker run --rm -i -v <app_volume>:/srv/chat alpine \
  sh -c 'cat > /srv/chat/<file>'
```

Piping through stdin like this avoids host/container path-namespace
mismatches (a bind-mount source path that doesn't exist on the actual Docker
host gets silently auto-created as an empty directory, which breaks a plain
`docker cp` or `-v hostfile:...` approach if your shell isn't actually on
the Docker host). Then recreate or restart the real container — if it reads
the file into memory once at startup rather than per-request, a restart is
required for the change to take effect. Reconstruct the `docker run` command
from `docker inspect <container>` (image, cmd, port bindings, cap-drop,
memory, healthcheck, log config, volumes) if the original command wasn't
saved, rather than guessing flags.

## 6. Private weekly progress digest for the parent

Rather than giving the parent raw transcript access (which reopens the
privacy/trust question the whole design avoids), add a narrow, token-gated,
read-only export the parent's own (full-access) assistant can pull from on a
schedule:

- Add a `GET /export/<child>?token=...&since=<ms>` route to the web chat
  server, guarded by a random shared-secret token (`crypto.timingSafeEqual`,
  not `===`) stored in an env file — separate from the per-child login
  passwords. It returns only `{role, text, ts}` for messages at/after
  `since`; nothing else about the account.
- On the parent's own assistant (the one with full tool access), create a
  weekly cron job (`agentTurn` payload, `--announce --channel whatsapp --to
  <parent>`) whose prompt: loads the export token from a credentials file,
  computes "7 days ago" itself, `curl`s the export endpoint for each child,
  and asks the model to summarize subjects covered / homework done /
  perceptible progress — explicitly instructed to never repeat the raw
  message text, only a synthesis. Test it once with a manual trigger
  (`openclaw cron run <id>`) before trusting the schedule, and check
  `openclaw cron runs --id <id>` for delivery status.
- Keep this cron rare (weekly, not daily) and make sure it always produces a
  visible message — a cron with no delivery path or that fires needlessly
  often is exactly the kind of silent quota-burner to avoid.

## Pitfalls seen in practice

- A reused session id can leak tools/instructions from before a config
  change — always test policy changes on a fresh session id.
- `tools.profile: coding` (or similar) can silently strip the `message`
  tool from a cron job, so a task "succeeds" but delivers nothing — always
  give cron jobs an explicit `--announce`/delivery target and check a real
  run's delivery status, not just its exit code.
- A container's built-in Docker healthcheck may default to the base image's
  own port/path (e.g. a gateway healthcheck on a proxy image that actually
  serves a different port) — override `--health-cmd` explicitly for the
  real service when recreating a container from a stock image.
- If two children/agents share one WhatsApp-style channel plugin, a config
  patch to the account/binding list usually **replaces the whole array** —
  always resend all existing bindings together, not just the one you're
  adding.
