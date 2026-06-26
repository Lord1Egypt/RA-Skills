# Long Task Handoff Protocol Reference

Load this file only when the bundled Python manager is unavailable, when auditing or modifying the skill, or when an agent needs to understand the full protocol. Normal use should rely on `scripts/handoff_manager.py`.

## Objective

Make long-running agent work restartable and transferable with minimal user effort. The active handoff is a current authoritative restart packet, not a transcript or project wiki.

## Trigger Policy

Trigger automatically when:

- context is compacted, summarized, restored, resumed, or trimmed
- a low-context or context-folding runtime hook fires
- the user explicitly asks for a handoff, transfer packet, restart-session handoff, or cross-agent handoff
- an agent is about to recommend a new session or cross-agent transfer
- a fresh session has an explicit active-handoff signal, such as `handoffs/ACTIVE.md`, a provided handoff path, or a runtime resume marker

Do not trigger merely because the user says continue or keep going, or merely because a task has many changed files. These can be inputs after the skill is triggered by an explicit handoff signal, but they are too broad for triggering by themselves.

## Compaction Thresholds

- First visible compaction: update handoff quietly.
- Second visible compaction: update handoff and validate `handoffs/ACTIVE.md`.
- Third visible compaction: update handoff and briefly say restart is advisable.
- Fourth visible compaction or observed state loss: update handoff and strongly recommend restart.

## Fresh Session Recovery

When a new session starts with a continuation request and an explicit handoff signal exists, search before asking the user to restate context:

1. `handoffs/ACTIVE.md`
2. latest `handoffs/session-handoff-*.md`
3. agent-specific workspace handoff locations
4. OS temp path only if a previous agent explicitly reported it

After finding a handoff, verify branch, commit, key files, and test state before editing. If there is no active-handoff signal, do not invoke this protocol just for an ordinary continuation request.

## Handoff Scope

Include only restart-critical state:

- updated time
- supersedes and authoritative status
- current branch, commit, and working tree state if available
- current goal
- completed work this turn
- delta since last update
- current test results
- key files and artifacts
- current state
- unfinished items
- next actions
- commands and verification
- fact sources
- decisions and constraints
- blockers, risks, and open questions
- known risks
- do-not-redo and do-not-do items
- suggested skills or tools
- sensitive information handling
- restart instruction

Put durable project knowledge in repo documentation and reference it by path. Examples: README, ADRs, PRDs, issues, test docs, developer docs, and code-adjacent comments.

## Exclusions

Never include:

- API keys, tokens, passwords, cookies, private keys, or secret values
- `.env` contents
- long chat logs or transcript dumps
- stale plans
- unverified guesses presented as facts
- descriptions that conflict with the current code, files, tests, or branch state

## Update Discipline

Automatic updates should rewrite the active handoff as a current snapshot plus concise delta.

Do:

- replace stale sections in place
- keep `Delta Since Last Update` short
- remove resolved risks and obsolete plans
- replace contradicted facts with current verified state
- keep `ACTIVE.md` pointing to the only current authority
- treat older timestamped handoffs as historical records

Do not:

- append a new mini-handoff below the old one
- preserve old plans for completeness
- keep multiple current authorities
- make the user copy long restart prompts

## Manager Payload Shape

When passing JSON to `handoff_manager.py --input-json`, use any subset of:

```json
{
  "task_name": "Short task name",
  "agent": "Codex",
  "current_goal": "One sentence goal.",
  "completed_this_turn": ["..."],
  "delta_since_last_update": ["..."],
  "current_test_results": ["..."],
  "key_files": ["path - reason"],
  "durable_docs": ["path - reason"],
  "candidate_repo_doc_updates": ["..."],
  "current_state": ["..."],
  "unfinished_items": ["..."],
  "next_actions": ["..."],
  "files_and_artifacts": ["path - reason"],
  "commands_and_verification": ["command - result"],
  "fact_sources": ["..."],
  "decisions_and_constraints": ["..."],
  "blockers": ["..."],
  "known_risks": {"high": "none", "medium": "none", "low": "none"},
  "do_not_redo": ["..."],
  "do_not_do": ["..."],
  "suggested_skills": ["..."],
  "supersedes": "none"
}
```

Keep values concise. The manager provides default fallback text for missing fields.

## Runtime Hook Contract

Preferred integration:

```text
after_context_compaction:
  handoff_manager.py update --event context_compaction --compaction-count N

before_context_eviction:
  handoff_manager.py update --event before_context_eviction --compaction-count N

after_session_resume:
  handoff_manager.py recover --workspace .

fresh continuation request:
  handoff_manager.py recover --workspace .
```

If hooks are not available, the model should still call the manager when it sees compaction, resume, or continuation language in context.

## Manual Fallback

If Python is unavailable, write a Markdown handoff manually using the same required fields listed in "Handoff Scope". Keep it concise, validate it by inspection, and state that script validation could not run.
