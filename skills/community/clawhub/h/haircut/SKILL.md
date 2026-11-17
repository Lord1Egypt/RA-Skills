---
name: haircut
description: >-
  The barber for your coding agents' config. Weighs everything every agent on this
  machine loads (instruction files, memory, MCP servers, hooks, skills, commands,
  subagents, plugins, leftovers), prices each item in tokens from your own
  transcripts, and parks the dead weight with a receipt and an undo. Use this
  skill whenever the user mentions config bloat, a heavy or slow session start,
  tokens burned before the first word, too many MCP servers, hooks that are slow
  or fire on every prompt, skills or commands or plugins nobody invokes, cleaning
  up or auditing CLAUDE.md or AGENTS.md, Codex config, or asks what does my agent
  actually load, why is my context full before I type, which of these servers can
  I turn off, or what is this plugin costing me. Use it even when they only say
  the session feels bloated or startup got slow, and even when they mention
  /context, /doctor or /skill-doctor.
allowed-tools: Bash, Read, Write, AskUserQuestion, Glob, Grep
---

# haircut

haircut is five deterministic stages plus this one. The script scans, measures,
prices and proposes on its own. Your job is the conversation and the decision.
Keep it that way: do not recompute a number the script already produced, and do
not invent a verdict the report does not carry.

Match the size of the answer to the size of the question. Someone who asks "how
much do I pay before my first word" gets stage 1 and stage 2 and nothing more.
Nobody gets walked into a cleanup they did not ask for.

## 1. Measure

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/haircut.mjs" --json
```

Add flags only when the user asked for them:

- `--days N` changes the usage window (default 90).
- `--agents claude-code,codex` limits the scan. Valid names: claude-code, codex,
  opencode, cursor, gemini, copilot, windsurf, continue, claude-desktop, vscode.
- `--probe` measures the cost of MCP tool schemas by connecting to each
  configured server. It starts those servers the way the agent would, so use it
  only when the user asks to measure MCP schema cost, and tell them it will start
  their servers before you run it.

Everything in this stage is read-only. Claude Code transcripts take seconds;
Codex rollouts can take a minute on a machine with months of them, so say so
before you run it, and run it in the background if the user is waiting on
something else.

The command prints a JSON summary and the run folder path in `run_dir`. Read
`REPORT.md` from that folder next. Do not read `report.json`: it carries every
item in full and will swallow your context for nothing. Reach into it only if the
user asks about a specific item the report does not cover.

There is also `report.html` in the same folder, self-contained, for browsing and
deciding with a mouse. `node "${CLAUDE_PLUGIN_ROOT}/bin/haircut.mjs" report --open`
opens it. Offer it when the list is long or the user prefers to click; the page
exports the same `decisions.json` this skill writes in stage 4.

## 2. Tell the user what it found

Three things, in plain words, in this order:

1. **The before-first-word figure.** `headline.claude_code.before_first_word`
   gives `avg_cold` tokens across `cold_sessions` cold starts, worst case
   `max_cold`. This comes from the API's own usage fields in the transcripts, so
   call it measured, not estimated. If Codex was scanned, add
   `headline.codex.fixed_per_rollout.total` per rollout and the per-call MCP
   schema cost, which Codex pays again on every single model call.
2. **The three biggest savings** from `top_savings`: what each one is, what it
   costs over the window, why the script flagged it.
3. **The count per verdict** from `totals.by_verdict`, one short line each. PARK
   goes in the bag. TRIM stays but gets cut down. FIX is wanted but broken.
   ROTATE is a credential sitting in plain text. ASK is the user's call. KEEP
   stays. INERT costs nothing where it sits.

No table longer than ten rows. When a list runs long, name the top few and point
at `REPORT.md` for the rest. The user can read a file; what they need from you is
the shape of the problem.

## 3. Walk the ASK and ROTATE items

The report proposes. It never decides. Every item whose verdict is ASK or ROTATE
needs the user's answer before it can go into `decisions.json`.

Use the AskUserQuestion tool, at most four questions per round. Group items that
share a fate into one question (three unused servers from the same vendor, for
example) rather than asking eight times. Every option has to say two things: what
changes on disk, and what stops working. "Park it" on its own is not something a
person can judge.

Options that work:

- "Park it. The server is removed from the user config and its folder moves into
  the bag. Its tools stop appearing in any session until you restore it."
- "Keep it. Nothing changes, and it keeps costing about 1,200 tokens at every
  session start."

ROTATE is different: nothing moves and nothing is parked. The user rotates the
key themselves. Say which file holds it, never print the value or any fragment of
it, and ask whether to leave the item alone until the key is out of that file.

Never answer for the user. An item they skipped stays `later`, which changes
nothing.

## 4. Decide, then trim

Write `decisions.json` into the run folder, next to `REPORT.md`, with the Write
tool (not a shell heredoc). Start from the proposals and overwrite them with the
user's answers. If the user decided in the browser instead, they paste or save
the page's export into that same file and you continue from here:

```json
{
  "run": "<run id from the summary>",
  "items": {
    "<item id>": { "decision": "park", "note": "unused in 90 days, user confirmed" },
    "<item id>": { "decision": "keep", "note": "" }
  }
}
```

`decision` is `park`, `keep` or `later`. Only `park` moves anything, and `later`
is the safe default for whatever the user did not answer. Item ids are the `id`
field from the report; `decisions.template.json` in the same folder already lists
every candidate, so copy ids from there instead of typing them.

Then show the user the plain list of what will be parked, one line per item, name
and what stops working. Wait for an explicit yes. A topic change, silence, or
"sounds good" about something else is not a yes.

On yes, dry run first:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/haircut.mjs" trim <path to decisions.json> --dry-run
```

Show the plan it prints. If it differs from what you told the user, stop and
reconcile before going further. Then run it for real:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/haircut.mjs" trim <path to decisions.json>
```

## 5. Receipt and undo

Print the receipt: what moved, what was edited, what was skipped and why. Every
operation is also written to `MANIFEST.jsonl` inside the bag.

Give the user the exact undo command with the bag id filled in:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/haircut.mjs" restore --bag <bag id> --dry-run
```

The real restore is the same line without `--dry-run`. The `/haircut:restore`
skill takes it from there.

Finally, tell them the current session already paid for what was just parked, so
nothing looks different yet. Start a new session and run `/haircut` again to see
the difference.

## Rules

- **Nothing is deleted.** Parked items move into a dated bag and `restore` puts
  them back. If the user asks you to delete something, park it and tell them
  where it went.
- **Never edit the content of CLAUDE.md, AGENTS.md or MEMORY.md.** haircut
  measures those files and reports what they cost per session. Rewriting the
  prose inside them is the user's job, or `/doctor`'s. Reporting that a file is
  large is fine. Trimming it is not.
- **Team files stay put.** A skill, command or rules file inside a shared repo
  may belong to colleagues. Say so out loud before proposing it, and let the user
  decide. The scanner marks those ASK for exactly this reason.
- **Never print a credential**, or a fragment of one, into the conversation. Name
  the file, name the item, stop there.
- **Read-only until the yes.** Scan, measure, probe and report change nothing.
  `trim` is the only command that touches anything, and it does not run before
  the user has approved a list they have actually seen.
- **Plugins are one unit.** A skill, hook or server that ships inside a plugin
  is not parked on its own. The move is to disable the plugin, and the report
  says so on those items.
- Report what the script found. If a number is missing, say it is missing. If
  the script failed, show its error and stop; do not reconstruct the audit by
  hand.

## What this adds

Claude Code already ships three checks, and they are good. `/context` shows what
the live session is carrying right now. `/skill-doctor` reports per-skill usage
over the last week. `/doctor` runs a checkup over recent transcripts and applies
fixes with confirmation. Say so if the user asks. haircut covers what they do
not:

- Every agent on the machine, not just this one. Codex in particular sends full
  MCP tool schemas with every model call and ships no config doctor of its own.
- Hooks priced in tokens and in latency per fire, from what they actually
  injected.
- Duplicates and scope shadowing: the same skill installed twice, a project
  setting quietly overriding a global one.
- A receipt. Every change lands in a manifest, and one command puts it all back.
