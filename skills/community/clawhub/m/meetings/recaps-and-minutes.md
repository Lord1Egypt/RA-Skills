# Capture, Recaps And Minutes — Turning A Meeting Into A Record

**Before writing any record**, read `record_style` and `record_location` in `config.yaml`, the previous block for this series in `records/<year>-<mm>.md`, and `~/Clawic/data/meetings/decisions.md` for the entries this meeting touches. **Before processing a pasted transcript**, read the Secrets section of `memory-template.md`: a raw transcript is the densest source of credentials and off-record content in this domain.

**Contents:** [Capture During Versus After](#capture-during-versus-after) · [What Survives](#what-survives) · [Transcript To Record](#transcript-to-record) · [From A Voice Note Or Scribble](#from-a-voice-note-or-scribble) · [The Recap](#the-recap) · [Formal Minutes](#formal-minutes) · [Distribution](#distribution)

## Capture During Versus After

| Mode | When it wins | Failure mode |
|---|---|---|
| Live scribe (a person, not the chair) | Decision-heavy meetings, 4+ attendees | Scribe stops contributing; rotate it |
| Chair writes only the close | Small internal syncs | Everything before the close is lost — fine, that is the point |
| Transcript, edited after | Long, external, or legally sensitive | Nobody edits it, and a transcript is not a record |
| Nothing during, written within 2h | Trust-building meetings where a laptop kills the room | Written at 23:00 with three items missing |

The default that fails least: **capture decisions and actions live, in the meeting's own words, and write the rest within two hours.** Recall of who committed to what degrades fastest in the first hours — the same-day recap is not a discipline preference, it is the accuracy window.

## What Survives

A record is not a transcript of the discussion. Four things survive, in this order (`record_style: decisions-first`):

1. **Decisions** — the sentence, the decider, the method, and what was rejected.
2. **Actions** — `owner — verb + object — date — done means`. No team owners, no "ASAP".
3. **Open questions** — with the person who chases the answer and by when.
4. **Context that changes a future decision** — the number that killed an option, the constraint nobody knew about, the client's actual words about their problem.

Everything else is cut: the discussion path, who was persuaded by whom, the jokes, the tangents. `full-notes` adds a Discussion section for meetings whose reasoning matters later; `verbatim` keeps quoted lines with attribution and exists for board, legal, and client-commitment contexts only.

**Quote the user's counterpart verbatim on three things**: commitments, numbers, and complaints. Paraphrased commitments are how two organizations end up with different memories of the same sentence.

## Transcript To Record

Automatic transcripts are raw material with predictable defects. The pass, in order:

1. **Strip credentials before anything else.** Passcodes, dial-in PINs, passwords read out loud, secret links — replaced by pointers, or dropped (`memory-template.md`).
2. **Drop anything off the record.** Compensation, performance, health, legal advice, unannounced personnel changes — not summarized, not redacted, simply not written.
3. **Find the decisions.** They hide behind "okay, let's do that", "fine, go ahead", "yeah, ship it". Convert each into an explicit sentence with a decider — and if the transcript does not show who decided, that is a finding to flag, not to guess.
4. **Find the commitments.** "I'll take a look" is not an action item. Convert it or drop it; if it matters, message the person: "is Thursday realistic for the vendor comparison?"
5. **Attribute carefully.** Diarization mislabels speakers, especially in a shared room with one microphone — never attribute a commitment to a name the transcript is not sure about.
6. **Check the numbers against the source.** A transcript hears "fifteen" as "fifty" often enough that any figure that decides something gets verified before it enters the record.
7. **Compress ruthlessly.** A 60-minute transcript is ~8,000 words; the record is 150-300. If the summary is long, the meeting had multiple purposes and the record should be split by decision.

Store the raw transcript only if the user asks (`transcripts/`); say in one line that the record was written and the transcript was not kept.

## From A Voice Note Or Scribble

Users describe a meeting in fragments: "Just had product sync. Launch moved to March 15. Sarah's handling the QA contractor. I need to tell stakeholders."

Convert with these rules, and ask at most one question:

- **Every "someone is handling X" becomes an action item with a date**, or an explicit "no date agreed" — which is itself useful information.
- **Every date mentioned is a decision** until proven otherwise: "launch moved to 15 March" is a decision with a decider, and the decider is worth one question if it is not obvious.
- **First person "I need to..." is an action item owned by the user**, with `done means` inferred from the verb.
- **Unstated attendees**: infer from the series in `## Series`, and write what you inferred rather than leaving it blank.
- **The single allowed question** is the one that blocks a write: who decided, or by when. Everything else gets recorded as unknown.

## The Recap

Governed by `recap_policy`. Shape, in this order, and never longer than a screen:

```
Subject: <Meeting> — decisions and next steps

Decided: <one sentence each, with the decider>
Actions: <owner — what — date>
Open: <question — who chases — by when>
Not discussed: <anything on the agenda that got dropped>
Next: <date, or none planned>

Corrections by <date/time> — otherwise this is the record.
```

- **"Not discussed" is the line everyone omits** and the one that prevents an absent stakeholder assuming their item was handled.
- **The correction deadline turns the recap into the record.** Without it, disagreements about what was agreed surface at delivery time.
- **Same day.** A recap that arrives on Thursday for a Monday meeting has already been overtaken by three DMs.
- **External recaps are shorter and more careful**: decisions, dates, and the next step. Anything that reads as a new commitment gets checked before sending (`external.md`).

## Formal Minutes

For boards, associations, works councils, and anything with statutory or contractual force. Different genre, and the difference is not style:

- **Required elements**: date, time, place or platform; attendance with role, apologies, and whether quorum was met; each item with proposer and outcome; resolutions in their **exact final wording**; votes for/against/abstained, with abstentions attributed when the rules require; conflicts of interest declared; time of close; date of the next meeting.
- **Minutes record decisions, not discussion.** Naming who argued what in formal minutes creates discoverable liability and chills the debate; keep the reasoning in the pre-read or the board pack, not the minutes.
- **Draft within a week, circulate for correction, approve at the following meeting**, and mark the approved version as such. Only the approved version is the record.
- **Attachments by reference** — "the Q2 pack, appended" — rather than pasted in, so the minutes stay readable.
- Approved minutes are an artifact: `artifacts/minutes-<body>-<period>.md`, indexed in `## Boxes`, read before the next meeting of that body.

## Distribution

- **Everyone affected, not everyone present** (SKILL.md Rule 8). The absent decision-maker who reads the recap does not reopen the decision in two weeks.
- **One channel, permanently.** The recap that lands in a different place each time cannot be found when it matters.
- **Actions also go to their owner directly.** An action item read in a group thread is an action item nobody has personally received.
- **Redact before sending wider.** Names, numbers and candour that were fine in the room may not be fine in a channel with 200 people; if the honest recap cannot be sent wide, send a short public version and the full one to the room.

**Write in the same turn as the recap**: the record block in `records/<year>-<mm>.md` (or `record_location`), each decision as a row in `~/Clawic/data/meetings/decisions.md`, each action in `## Follow-Ups` with owner, date and definition of done, any new attendee in `~/Clawic/data/contacts/contacts.md`, and approved formal minutes as an artifact with its `## Boxes` line (`memory-template.md`). A recap that was sent but never stored is a record the user cannot search three months later.
