# Privacy — Read Scope, Quoting, And What Leaves The Folder

Scope: who reads the journal and under what conditions. In this domain privacy is not a compliance section; it is the load-bearing condition for the entries being honest.

**Contents:** [Read Scope](#read-scope) · [The Quoting Rule](#the-quoting-rule) · [What May Leave The Folder](#what-may-leave-the-folder) · [Secrets Versus Private](#secrets-versus-private) · [Third Parties](#third-parties) · [No-Go Topics](#no-go-topics) · [Sharing An Excerpt](#sharing-an-excerpt) · [Shared Devices And Coercion](#shared-devices-and-coercion) · [The Honest Limits](#the-honest-limits)

**At the start of every session** read `## Read Scope` in `~/Clawic/data/journal/memory.md` and `no_go_file` if `config.yaml` sets one. These two are read unconditionally, before any entry is opened, because their entire function is to gate what may be opened.

## Read Scope

`agent_read_scope` governs which past entries may be opened without being asked:

| Value | May open | Notes |
|---|---|---|
| `on-request` (default) | Nothing, unless the user asks or the task they gave requires it | "Write my weekly review" requires the week; "how was your day" requires nothing |
| `recent` | The last 14 days | Enough for continuity, not enough to build a profile |
| `full` | The whole corpus | Only when the user has said so explicitly; still excludes the lists below |

Independent of the value, three things are **never** opened: anything named in `## Read Scope`, anything matching `no_go_file`, and any entry belonging to a never-reread practice (`practices.md`).

- **Say what you opened**, in one line, every time: "Read the 12 entries from 20-26 July." Unstated reading is the thing that makes people write less honestly.
- **Never read to "understand them better".** Curiosity is not a task. If historical context would genuinely improve the answer, ask for it and name the window you want.
- **A search is a read.** Grep results are entry content (`storage.md`).
- Scope applies to your own earlier turns too: a user who says "forget what I told you about that" gets that topic added to `## Read Scope`, not re-raised later because it is still in the transcript.

## The Quoting Rule

Rule 9, applied:

- Entry text goes in the entry file. Nowhere else — not a shared box, not a project file, not a contact row, not a review, not a summary the user is about to paste somewhere.
- **Reviews and analyses paraphrase and count; they do not quote.** "Four entries mention the interview" is a review line. Two sentences from the 19th is not, even though it would read better.
- Never quote an entry back at the user in an unrelated conversation. "You wrote in March that you hated that job" is technically true, contextually a betrayal, and reliably the last thing said before someone stops writing.
- The one exception is a quote the user asks for, in this conversation, delivered in the reply and written nowhere (Sharing An Excerpt).

## What May Leave The Folder

Only derived, neutral fields, and only into their declared shared box:

| Leaves | Goes to | Never goes with it |
|---|---|---|
| A mood rating (integer + scale + date) | `~/Clawic/data/health/mood.md` | The entry, the reason, the events of the day |
| A person's name, role, channel — **only when the user asks** | `~/Clawic/data/contacts/contacts.md` | Anything written about them, any characterization, any sentiment |
| A one-sentence decision summary for a tracked project | `~/Clawic/data/projects/<project>.md` | The deliberation, the emotional context, the people involved |
| A compensation figure the user asks to track | `~/Clawic/data/finances/` | The negotiation, the resentment, the comparison to a colleague |
| Anything else | Nowhere | — |

Everything else — entries, reviews, decisions, work log, artifacts — stays inside `~/Clawic/data/journal/`. When in doubt the answer is "it stays", because the cost of over-sharing here is not a merge conflict, it is the practice.

## Secrets Versus Private

Two different problems, both real, handled differently.

- **Private** is most of the journal: names, feelings, health, money, conflict, doubt. It is protected by staying in the folder, by read scope, and by full-disk encryption (`storage.md`). It is not stripped, because stripping it would empty the journal.
- **Secret** is a value that authenticates something. It is never written under `~/Clawic/data/` at all, in any file, including files the user pastes in.

Which items fall on which side is one pair of lists, and it lives in `memory-template.md` — kept in one place because a rule split across two files diverges, and the divergence is discovered the day something is written that should not have been. For anything on neither list the test is what it does, not how it feels: a value that **authenticates** something is secret and never written; a value that merely **exposes** is private and stays exactly as the user wrote it.

The pointer replaces the value where it stood: `the password is <keychain:home-router>`. Say in one line that you did it — silent redaction leaves the user believing something was saved that was not.

## Third Parties

The journal is full of people who did not consent to being in it.

- **Never characterize them in a shared box.** A contact row says "sister, prefers voice notes", never "difficult about the house".
- **Never analyze them.** A pattern about someone else's behaviour, derived from one person's writing about them on their worst days, is both unreliable and not yours to produce (`patterns.md`).
- **Redact on any export or excerpt**: names to initials or roles, employers to "work", identifying detail removed. Do this by default and say you did it; the user can put a name back deliberately.
- **Names of minors, health details of others, and anything disclosed to the user in confidence** never leave the folder in any form.

## No-Go Topics

`no_go_file` is a plain list of topics never to prompt about, analyze, or resurface. It is the mechanism for "don't bring that up again".

- Add to it the moment the user says any version of that sentence — no confirmation question, no discussion.
- Read it before every prompt (`prompts.md`), every analysis (`patterns.md`), every review (`review.md`) and any on-this-day resurfacing.
- The user may still write about the topic. The list constrains **you**, not them, and a no-go topic appearing in a fresh entry is captured normally without comment.
- Removing an item requires the user to say so explicitly. Never infer that a topic is reopened because they mentioned it once.

## Sharing An Excerpt

When the user asks for something from the journal to send to a therapist, a partner, or a doctor:

1. Ask what the recipient needs — usually a period and a topic, not the entries.
2. Prefer a summary they can read and approve over raw entries. Raw entries contain the sentences people forget they wrote.
3. Redact third parties by default (above).
4. Produce it **in the reply**. Do not write a shareable file unless asked; if asked, it goes to `artifacts/shared-<date>-<recipient>.md` so there is a record of what left.
5. Show it to the user before it goes anywhere, in full.
6. Note the fact of sharing — date, recipient, window — in `## Practice`, without the content.

## Shared Devices And Coercion

- If the device is shared with someone the entries are about, file permissions and encryption are partial answers. Say so plainly rather than implying safety that does not exist.
- Concrete options, in order: a separate account on the device; a journal folder on removable media; an encrypted container mounted only while writing (`storage.md`); or writing on paper and not digitizing.
- Do not create a "hidden" folder and imply it is protected. Obscurity fails against exactly the person it needs to work against.
- When the writing describes monitoring, control, or threats, the abuse row in SKILL.md Red Flags applies, and the priority is a local support line, not a storage change.

## The Honest Limits

Say these once, when relevant, and do not repeat them as disclaimer:

- **Anything typed or dictated into a hosted assistant reaches that provider before it becomes a file.** This skill writes local files; it cannot change what happens upstream of it. Material that must never leave the device gets written directly into the entry file offline and listed in `## Read Scope`.
- **A personal journal is not privileged the way clinical notes can be.** In some jurisdictions it is discoverable in litigation. This is not a reason to write less honestly; it is a reason to know it, particularly for a work journal (`work-journal.md`).
- **A backup in someone else's cloud is a copy in someone else's custody** (`storage.md`).
- **Deletion is a real option.** If the user wants an entry gone, delete the file, delete any reference to it in `memory.md` and the reviews, and say what was removed. Never argue for keeping it, and never keep a copy.

**Write in the same turn:** a topic the user closes, to `no_go_file`; an entry or period they do not want reopened, to `## Read Scope` in `memory.md` (dates and a label, never content); a change to `agent_read_scope`, to `config.yaml`; a share, a deletion, or an encryption decision, as one dated line in `## Practice`. Formats: `memory-template.md`.
