# What Not to Write Down

Some material makes the note worse the moment it is in there: it survives longer than the situation, it is readable by more people than intended, and it cannot be un-written. This file is the decision, not the redaction — redaction mechanics for credentials are in `memory-template.md`.

**Contents:** [The Record Test](#the-record-test) · [Never Written](#never-written) · [Written Carefully](#written-carefully) · [Redaction](#redaction) · [Recording Other People](#recording-other-people) · [Work Versus Personal](#work-versus-personal) · [Deletion](#deletion) · [Sensitive Traps](#sensitive-traps)

**Before writing anything in this territory**, read `safety_posture` in `~/Clawic/data/notes/config.yaml` — `never_write` lists the topics and clients the user has already excluded, and it governs over anything here.

## The Record Test

Four questions, in order. The first "no" stops the writing.

1. **Who can read this in three years?** Assume: the user, anyone with the device, anyone the vault is shared with, and — for work notes — the employer, an auditor, and the opposing side in a dispute. Notes are ordinary business records and are routinely produced in HR processes and litigation.
2. **Does it still help then?** A judgment about a colleague helps for a week and is a liability for a decade. A decision with its reasoning helps forever.
3. **Is it mine to keep?** Another person's health, pay, immigration status, or private conversation is theirs. Storing it in a searchable corpus is a decision made on their behalf.
4. **Would writing it change what I would say out loud?** If the note has to be phrased defensively, the honest version does not belong in a note.

What passes all four: decisions, evidence, commitments, observable behaviour with dates, things the user personally owns.

## Never Written

Into any note, on any platform, however convenient:

- **Credentials of any kind** — passwords, tokens, API keys, recovery codes, MFA seeds, PINs, private keys, connection strings with a password. Pointer only, `<kind>:<locator>` (`memory-template.md`).
- **Full payment and identity numbers** — card numbers, bank accounts, national ID, passport numbers. Last four digits are an identifier and are fine; the full number is not.
- **Another person's health information** — diagnoses, medication, appointments, pregnancy, mental-health disclosures. Including when they told you themselves.
- **Someone else's pay, equity, or performance rating.**
- **Legal advice received under privilege**, copied into a general-purpose corpus: it can waive the privilege that made it worth getting.
- **Anything under an NDA that names the counterparty and the terms**, in a corpus synced to a consumer platform.
- **Recordings or transcripts of people who did not consent.** In several jurisdictions recording without all-party consent is itself unlawful; the note inherits the problem.
- **Speculation about a person's character, motives, or protected characteristics** — age, family status, origin, religion, disability, orientation. Not as an observation, not as context, not as a joke.

## Written Carefully

Legitimate to record, with a shape that keeps it useful and defensible:

| Material | Wrong shape | Right shape |
|---|---|---|
| A colleague's performance | "Alice is careless" | "Third missed deadline this quarter: 06-14, 07-02, 07-19" |
| A conflict | "Bob was hostile" | "Bob objected to the scope change; said the estimate was made without engineering" |
| A candidate | "Not a culture fit" | "No example of handling conflicting requirements when asked twice" |
| A client dispute | "They're trying to scam us" | "Invoice 214 disputed 2026-07-12; the scope change was agreed verbally on 06-30, confirmed by email 07-01" |
| Your own frustration | In the meeting note | In a personal journal note, marked private, never in the shared record |
| Salary discussion in a 1-on-1 | The number, in the vault | "Comp discussed; outcome recorded in the HR system" |

The pattern: **observable, dated, attributed, and specific**. That version is more useful to the user *and* survives being read by the subject.

## Redaction

When the user pastes text to be saved, redact before writing, never after — an unredacted write has already happened, and sync has already propagated it.

- **Credentials** → pointer in place: `password: <1password:Work/DB/prod>`.
- **Third-party personal data that is not needed** → drop it, do not mask it. A masked field still says the fact existed.
- **Third-party personal data that is needed** → reduce to the minimum that works: "the vendor contact confirmed on 07-14", not their medical reason for the delay.
- **Say what was removed, in one line.** Silent redaction leaves the user believing the note is complete.
- Redaction does not apply retroactively to what the platform already synced: if a secret reached a network platform, it is compromised and must be rotated, not deleted (`sync.md`).

## Recording Other People

- **Attendee lists are fine; private disclosures are not.** Someone mentioning their divorce in a 1-on-1 said it to you, not to your searchable corpus.
- **Quoting is a commitment to accuracy.** If it is in quotation marks it must be verbatim; a remembered paraphrase in quotes is how a note becomes evidence against the person who wrote it (`meetings.md`).
- **Ask before recording a call**, every time, and record the fact that consent was given with the date. This is a legal requirement in some jurisdictions and a relationship requirement everywhere.
- **Shared vaults change the answer to every question here.** Before a vault is shared, a pass over 1-on-1 and interview notes is not optional.

## Work Versus Personal

The one case where splitting the corpus is the right answer, despite the friction:

- **The employer can access what is on their device or in their tenant.** Personal notes in a work vault are readable by the employer, in some jurisdictions lawfully and without notice.
- **Work notes in a personal vault are the mirror problem**: they may be the employer's property, they are discoverable through the user personally, and they usually breach a policy the user agreed to.
- **The split is by ownership, not by topic.** A side project on personal time is personal even when it is technical; a client conversation is work even when it happened at dinner.
- If the corpus is not split, at minimum keep client and employment material out of consumer network platforms and record which clients are excluded in `safety_posture.never_write`.

## Deletion

- **Deleting the note does not delete the copies**: sync history, backups, the platform's trash, version history, and any export. Deletion in a synced corpus is a request, not a guarantee.
- **A secret that was written is rotated, not deleted.** Rotating is the only action that actually removes the exposure.
- **Deletion requests about another person** (they ask you to remove what you wrote about them) are honoured in the note *and* in the places the note propagated — say which those are.
- **Never quietly delete a business record** to make a situation look better. Keep it, and add the correction with its date; a corrected record is defensible and a missing one is not.

## Sensitive Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| "It's just my private notes" | Devices are shared, vaults get synced, employers have access, litigation reaches them | The record test |
| Characterizing instead of describing | Outlives the mood; unusable as evidence; damaging when read by the subject | Observable, dated, specific |
| Storing a credential "temporarily" | Temporary storage syncs in seconds and lives in history forever | Pointer, always |
| Masking instead of dropping | The masked field still discloses that the fact exists | Drop what is not needed |
| Redacting after writing | The write already propagated | Redact before |
| Deleting a written secret | The copies remain in history and backups | Rotate it |
| Recording a call without asking | Unlawful in some jurisdictions, corrosive in all | Ask, and record that you asked |
| Mixing work and personal in one vault | Both sides become accessible to the wrong party | Split by ownership |
| Deleting an inconvenient record | Turns a bad note into a worse problem | Correct it, with a date |

**Write triggers for this file** — in the same turn: topics, clients and categories the user excludes to `safety_posture.never_write` in `config.yaml` (a declaration, so it belongs in config, never in memory); a redaction performed, stated in one line in the reply and never as hidden metadata; a consent given or refused for recording, as a dated line in the note itself; a deletion or correction request, and where the note had propagated, to `artifacts/<kebab-name>.md` with its `## Boxes` line when it needs to be re-read. Formats and thresholds: `memory-template.md`.
