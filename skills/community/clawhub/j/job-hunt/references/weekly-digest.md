# Weekly digest: remind, then run a discover round with the user present

Read this when the user asks for a weekly job email, wants to change or stop it, or
when a digest session starts you with this file. The design (and its 2026-11-02
revision) is kept in the source repository, https://github.com/addsumtech/job-hunt.

Once a week, at the slot the user chose, an hourly check (`digest.py tick`) asks
them in a dialog whether to run this week's digest. **Run now** opens a Terminal with
a Claude Code session that follows "The run" below, with the user present: login
hand-offs and browser consent clicks work, and LinkedIn may be searched under the
normal source policy. **Later**, or no answer, asks again after three hours; at most
three reminders a day; three days without a digest stop the reminders until the next
weekly slot. The email goes only to the user: at most five roles they have not been
sent before, each read in full, with a link, why it fits and the real gaps. No score
and no interview or offer probability.

## Before offering it

The weekly digest is optional, and it asks real work of the user, so it is the
user's decision. Never set it up unless they say yes after hearing what it needs:

- an email tool the agent can use to **send and search** their own mail (for Claude
  Code, a Gmail MCP server they have authorised; its login can lapse and must then be
  renewed), and an address of their own to receive it;
- **macOS** for the reminder dialog (Linux gets a notification with the command to run;
  other systems are not supported);
- being **present** when they click Run now on the reminder (Monday or whichever slot
  they pick): the search runs in their daily browser, which asks for their consent
  each time, and logged-in sites may need them to log in;
- a saved discover direction (an earlier round's `brief.yaml`) and search preferences.

Offer it at most once, after a discover round, with these needs stated; if they do
not answer yes, drop it.

## Setup

In a conversation, with the user present.

1. A master profile and `search-preferences.yaml` must exist; if the preferences do
   not, run discover's preference questions first (`modes/discover.md`).
2. Ask in one message, as selectable options where they are choices: which search
   direction (one of their earlier discover rounds' `brief.yaml`, or a new brief built
   with discover's brief questions); weekday and hour; the address (default: the
   master's contact email, shown for confirmation); the email language (zh or en).
3. Check that you have an email tool that can **send and search** mail and say which.
   For Claude Code that is a Gmail MCP server; note the directory whose config holds
   it (`--agent-cwd`), and make one harmless search to prove its login works (an
   expired login answers `invalid_grant`: ask the user to sign in again first). Without one, offer the file fallback (`--transport file`): the
   digest is written to `~/Downloads/job-digest/` with a desktop notification, and
   cancel or pause happens in a conversation or with `digest.py cancel` / `pause`.
4. Record the answers, then install the hourly check:

```bash
python3 scripts/digest.py setup --name "<name>" --recipient <address> --weekday <0-6> \
    --hour <0-23> --brief <path to brief.yaml> --language zh \
    --agent-command <absolute path of claude> --agent-cwd <dir with the email tool> \
    --python <absolute path of the prepared python> --words "<their answers>"
python3 scripts/digest.py install --name "<name>"
```

5. Run the first digest now, following "The run" below, so the user sees what they
   will get. It is a real email and counts as the first one sent.

Changing a setting is `setup` again (history is kept). Stopping is
`python3 scripts/digest.py cancel --name "<name>" --words "<their words>"`; pausing is
`python3 scripts/digest.py pause --name "<name>" --weeks <n> --words "<their words>"`.

## The run

You are in a session the user started from the reminder, so they are present; still
keep questions to what the round needs (a consent click, a login), because they chose
the search direction already.

0. **Unconfirmed send first.** `python3 scripts/digest.py status --name "<name>"`. If
   `pending_send` is set, an earlier run recorded a digest and stopped before
   confirming it. Search Sent mail for its exact `subject`
   (`in:sent subject:"<subject>"`). Found: run
   `python3 scripts/digest.py sent --name "<name>" --workspace <its workspace> --message-id <id>`
   and stop — that week's digest already went out. Not found: run
   `python3 scripts/digest.py send-failed --name "<name>" --workspace <its workspace> --reason "not in Sent"`
   and continue.
1. **Workspace.** `python3 scripts/digest.py workspace --name "<name>"` creates this
   run's folder (`searches/<date>-weekly-digest`) and prints its path, `<ws>`.
2. **Inbox, before any search.** Search the mailbox for messages from the recipient
   whose subject contains `[job-hunt weekly]` (replies to earlier digests). Read each
   one and save them as a JSON list of `{id, thread_id, from, subject, date, body}` in
   `<ws>/inbox.json` (an empty list when there are none), then run
   `python3 scripts/digest.py inbox --name "<name>" --messages <ws>/inbox.json`. The
   script, not you, decides what a reply means. `cancel`: send one short email to the
   recipient saying the digest is stopped and can be restarted by asking job-hunt,
   then stop. `pause`: stop. `continue`: go on. If the mailbox cannot be searched or
   read, run `python3 scripts/digest.py inbox --name "<name>" --unreadable "<reason>"`
   and stop: **nothing is sent**, because an unread cancel must win.
3. **Search.** Enter discover in `<ws>`
   (`python3 scripts/enter_mode.py --workspace <ws> --mode discover --because "weekly digest"`).
   Write `brief.yaml` from `digest.yaml`'s `standing_brief` with today's
   `created`/`slug` and `trigger_reason: weekly digest`. Then follow
   `modes/discover.md` without re-asking the brief or the preferences (the standing
   brief is the user's answer); sources, caps, stop signals, the login hand-off and
   `check_shortlist.py` work exactly as in any discover round.
4. **Only new.** `python3 scripts/digest.py filter --name "<name>" --workspace <ws>`
   prints the shortlist ids not sent before; pick only from those
   (`check_digest.py` refuses a role already sent).
5. **Read and explain.** For the best new rows within discover's detail band, read
   the full posting and run the candidate match (`check_candidate_match.py`), at most
   five. Write `digest-picks.yaml`:
   `{roles: [{id: <shortlist id>, why: <why it fits, from the posting and the profile>,
   gaps: <real gaps and hard barriers>}], unread: <new rows whose page could not be read>}`.
   A row that could not be read is not sent; it waits for next week.
   Write `digest-sources.yaml`: `{checked: [site], unchecked: [{site, reason}]}`.
6. **Compose and check.**
   `python3 scripts/digest.py compose --name "<name>" --workspace <ws>`, then
   `python3 scripts/check_digest.py --workspace <ws> --name "<name>"`. On findings,
   fix the inputs and compose again; if they cannot be fixed, stop: nothing is sent.
7. **Record, send, confirm.** `python3 scripts/digest.py presend --name "<name>" --workspace <ws>`
   gates the email again and records it as sent; it prints `to` (a list), `subject`
   and `body`. Only after it succeeds, send exactly those with the email tool. Then
   confirm with the message id the tool reports (reading that message back also gives
   its thread id, and shows the email arrived as composed; or find it with
   `in:sent subject:"<subject>"`):
   `python3 scripts/digest.py sent --name "<name>" --workspace <ws> --message-id <id>`
   (add `--thread-id <thread>` when you have it). If the send failed, run
   `python3 scripts/digest.py send-failed --name "<name>" --workspace <ws> --reason "<error>"`.
   Never send twice. With `--transport file`, run
   `python3 scripts/digest.py deliver-file --name "<name>" --workspace <ws>` instead
   of all of step 7. A week with nothing new still sends: the email says which
   sources were checked.

## What it never does

Run without the user having clicked **Run now** (or asked in a conversation), use a
paid API without asking, send to anyone but the recipient, apply or contact an
employer, or change the user's preferences without a "yes" reply to a question the
digest asked.
