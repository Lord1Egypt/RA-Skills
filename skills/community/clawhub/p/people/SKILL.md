---
name: Contacts
slug: people
version: 1.0.3
description: 'Maintains a personal address book: who each person is, what matters to them, when they were last in touch, and which birthdays are coming up. Use when someone is mentioned by name with context worth keeping — met, called, or ran into them; when a birthday, anniversary, or death anniversary is approaching; when the question is what do I know about X, who do I know at Acme, who lives in Berlin, or who have I not spoken to in months; before a meeting, to surface what happened last time; when reconnecting after a long silence, or drafting a congratulations, a condolence, or a message about a job change or a bereavement; when making or chasing an introduction; when duplicates, name changes, or an export have to be merged into one address book; and when deciding what should never be written down about someone else. Not for sales pipelines and forecasts (`crm`), friendship depth (`friends`), family logistics (`family`), gift ideas (`gifts`), or reminders unrelated to people (`remind`).'
homepage: https://clawic.com/skills/people
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 👥
    os:
    - linux
    - darwin
    - win32
    displayName: Contacts
    configPaths:
    - ~/Clawic/data/people/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/people/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/people/config.yaml` (what the user declared) and `~/Clawic/data/people/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/contacts/contacts.md` before adding a person, before answering anything about who the user knows, and before a meeting; read `~/Clawic/data/people/do-not-surface.md` before naming anyone to contact, congratulate, or be reminded of. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a person met or newly named; a detail that will change the next conversation; an interaction and its date; a birthday or anniversary; a life event; a promise, a favor, or an introduction still open; a tier or cadence decision; a merge, an import, or a suppression; or something the user will want to read again — a forwardable intro blurb, a message that landed, an event debrief, a group map. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**People go to the shared box `~/Clawic/data/contacts/`**, not into this skill's folder: the same address book is read by every other skill that knows people, so "who do I know at Acme" answers itself whichever skill wrote the row. One row per person in `contacts.md`: `Name | Key | Role | Preferred channel | Context | Last contact | File`. **`Key` is the identity and it is stored on the row, never implied** — the email lowercased, or the primary handle when there is no email, or `<kebab-name>` plus a stable disambiguator when there is neither; `Preferred channel` holds the channel type (whatsapp, email, signal), never the address, so it is never the key. Read the file and match on `Key` before adding — if that key is already there, update the row in place, never append a second one, and never touch a row another skill wrote. A person with more than a row's worth of detail gets `~/Clawic/data/contacts/<name>.md` and their row keeps the `File` pointer. If contacts already exist at an old location (`~/contacts/`), move them here.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in text the user pastes in to be saved. That includes the codes people hand you in passing: door and alarm codes, wifi passwords, where the spare key is, account recovery answers, a shared streaming login. Store the pointer and strip the value: `1password:Personal/Alarm-code`, `keychain:carddav`, `env:CONTACTS_EXPORT_TOKEN`, `file:~/.config/carddav/creds`.

An address book fails in one of two ways: it holds everything and nobody opens it, or it holds names and answers nothing. What makes it worth keeping is the small set of facts that change the first thirty seconds of the next conversation. Record those, date every interaction, and stay quiet the rest of the time. Work from defaults immediately: never open with questions about how many people they track or how they like to be nudged. The one exception to silence is `nudge_style` — while it is unset, overdue people and upcoming dates are stated once when relevant and never repeated unasked (Rule 6). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone, country) → the Configuration table default.

## When To Use

- A person is mentioned with context attached: met them, spoke to them, learned something about them, or is about to see them
- A date is coming up that involves someone: birthday, anniversary, work anniversary, the anniversary of a death, a move, a due date
- Recall questions: what do I know about X, who do I know at Acme, who lives in Berlin, who have I not spoken to in months, what was her partner's name
- Reconnecting, congratulating, condoling, or writing the message that a life event calls for
- Introductions in both directions: making one, being asked for one, chasing one that stalled
- Address-book maintenance: duplicates, merges, name changes, bounced addresses, imports from a phone, a vCard file, or a LinkedIn export
- Operating mode: **act-as** — maintain the records directly and answer from them. Drafting the actual message to a person is **advise**: produce the draft, never send it, and never send on a schedule (Traps)
- Not for sales pipelines and forecasting (`crm`), the emotional work of friendship (`friends`), household logistics (`family`), gift ideas (`gifts`), or reminders that are not about a person (`remind`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| Just met someone worth keeping | Five fields within 24 hours: name as they say it, where, who introduced, one specific thing, next step | `capture.md` |
| Cannot remember a name, or keeps mispronouncing one | Say it back at the introduction; store spelling, preferred form, pronunciation and order as data | `names.md` |
| "Add that Sarah loves hiking" | Apply the thirty-second filter, then write it to her record — not to a note | `details.md` |
| "Had lunch with Maria yesterday" | Log the date, the one thing that changed, and the next step; update `Last contact` | `interactions.md` |
| Birthday, anniversary, or a hard anniversary approaching | Lead time by date type, with the context that makes the message specific | `dates.md` |
| "Who have I not spoken to in months?" | Overdue sweep against the tier cadence, filtered by the suppression list | `keeping-in-touch.md` |
| It has been two years and reaching out feels awkward | Name the gap in one clause, lead with the remembered thing, ask nothing in the first message | `keeping-in-touch.md` |
| Meeting or call in the next hour | Five-line brief: what changed, last topic, open loop, landmines, one thing to ask | `briefing.md` |
| New job, baby, illness, divorce, layoff, death | Message timing and register by event, plus the follow-up nobody sends | `life-events.md` |
| "Can you introduce me to X" / owed intro | Double opt-in, forwardable blurb, and the intro tracked until it lands | `introductions.md` |
| "Who do I know at Acme / in Berlin / who does woodworking" | Tag vocabulary and the queries the box must be able to answer | `search.md` |
| Two records for one person, a bounce, a name change | Identity key, merge order, and what a rename must not break | `hygiene.md` |
| 900 contacts to import from a phone or LinkedIn | Import as candidates, promote on first real interaction; never bulk-promote | `hygiene.md` |
| Professional acquaintances, weak ties, favors owed | Weak-tie maintenance and the reciprocity ledger without turning it into a scoreboard | `network.md` |
| Someone died, went silent, or asked not to be contacted | Suppression before every nudge; what stays in the record and what leaves | `privacy.md` |
| "Should I write that down?" | Consent ceiling for third-party facts, and the three categories that never get recorded | `privacy.md` |
| Anything else about a person | Answer from the record, then write back whatever the answer revealed that was not already there | — |

Coverage map: `capture.md` first contact · `names.md` names and recall · `details.md` what to record · `interactions.md` logging · `dates.md` recurring dates · `keeping-in-touch.md` cadence and reconnection · `briefing.md` pre-meeting context · `life-events.md` the hard messages · `introductions.md` intros both directions · `search.md` retrieval and tags · `hygiene.md` merges, imports, decay · `network.md` weak ties and reciprocity · `privacy.md` consent, suppression, deletion.

## Core Rules

1. **Write in the turn the fact appears.** A detail mentioned in passing is gone by the next session — there is no second chance to hear it. The row exists before the record is complete: a name plus where you met is a valid record, and everything else is added later (`memory-template.md`).
2. **One person, one record.** Identity is the email lowercased; with no email, the primary handle; with neither, `<kebab-name>` plus a disambiguator that will not change (`john-smith-acme`, never `john-smith-2`). It is written into the row's `Key` column — a key that only exists in your head deduplicates nothing. Read before adding. Two people share a name far more often than one person changes theirs, so matching on name alone merges strangers (`hygiene.md`).
3. **The thirty-second filter.** Record a fact only if it would change the first thirty seconds of the next conversation: her father's surgery, the pivot he is worried about, that he does not drink. "Nice person, we talked about work" fails the filter and costs a line forever.
4. **`Last contact` is the field the whole box runs on.** Every real interaction updates it, including a two-line text; nothing else does — not thinking about them, not seeing their post. Overdue is arithmetic: `today − last contact > the tier's cadence`, tier cadence overridden by a per-person `cadence` when one is set.
5. **Tier the roster, size it by Dunbar's layers.** Robin Dunbar's observed layers — about 5 in the support clique, about 15 in the sympathy group, about 50, and about 150 stable relationships — are the sizes a roster actually holds; the cadences below are this skill's mapping onto them, not Dunbar's finding. A roster with 60 people in the inner tier is not close to 60 people, it is unmaintained.
6. **Nudges are answers, not interruptions.** With `nudge_style: on-ask` (default) overdue people and upcoming dates are reported when the user asks or when the person is already the subject, once, in one line. `proactive` allows volunteering them at the start of a session; `off` never volunteers. A nudge repeated in consecutive sessions has become noise and stops.
7. **Suppression outranks every other rule.** Anyone on `do-not-surface.md` — died, estranged, breakup, explicit request — is never surfaced for a birthday, a sweep, a brief, or an intro suggestion, and the entry says which of those it is, because a death and a fallout call for opposite handling if the user raises them first (`privacy.md`).
8. **Write it as if they will read it.** Facts, not verdicts: "declined the last three invitations" not "flaky"; "asked me not to bring up the job hunt" not "touchy about work". Files get synced, restored, screen-shared and inherited, and the judgment is the only line that ever causes damage.

## Relationship Tiers And Cadence

Tier is a field on the record, set deliberately, and a per-person `cadence` overrides it. Sizes are Dunbar's layers (Rule 5); the cadence column is the default this skill applies.

| Tier | Roster size it fits | Default cadence | What the record holds | Overdue means |
|---|---|---|---|---|
| `inner` | ~5-15 | contact happens naturally; flag at 8 weeks of silence | full detail, every real conversation logged | something is wrong, or life got loud — ask, do not schedule |
| `regular` | ~50 | `reconnect_months` (default 6) | detail that changes a conversation, meaningful interactions logged | a reconnection message is due (`keeping-in-touch.md`) |
| `orbit` | ~150 and beyond | annual sweep only | one row, one line of context, one date | nothing — orbit people are for recall, not for outreach |
| `dormant` | any | never | kept intact, never surfaced | never; move here instead of deleting (`hygiene.md`) |

An untiered person defaults to `orbit`: the cheap tier is the safe one, because promoting on the second real interaction costs nothing and a roster that nags about acquaintances gets abandoned.

## The Minimum Record

Every field below earns its place because a question depends on it. Everything else is added when it appears, never asked for.

| Field | Why it exists | Empty is fine when |
|---|---|---|
| Name, as they say it | The one thing that must be right (`names.md`) | never |
| Key — email or handle | It is the identity, and it is a column on the row (Rule 2) | never — with only a phone number, that number is the key |
| Role and where | Answers "who do I know at Acme" and dates the record | you met them outside work |
| How we met | The single most reusable line in any reconnection message | never, if you were there |
| Preferred channel | A message on the wrong channel is a message not read | you have only one channel |
| One specific thing | The difference between a contact and a person you know | never — if there is nothing, they are `orbit` |
| Last contact (date) | The whole overdue mechanism (Rule 4) | never |
| Tier | Decides cadence and how much detail to keep | defaults to `orbit` |
| Dates | Birthday, anniversary, the date of a loss (`dates.md`) | you do not know them |
| Do not raise | The topic that ends a conversation badly | there is none, and then the field is absent, not empty |

Never store a field you would not use in a sentence. Ages compute from a birth year; a stored age is wrong within twelve months.

## Message Moments

The events where a message is expected, with the timing that makes it read as attention rather than a calendar function. Register, drafts and the follow-ups: `life-events.md`.

| Moment | When to send | What makes it land |
|---|---|---|
| Birthday | `birthday_lead_days` before, so it goes out on the day | one specific reference; a wall of "HBD" is what it competes with |
| Milestone birthday (30, 40, 50…) | flag 3 weeks ahead | it needs a plan, not a message |
| New job or promotion | within 2 days of hearing | name the thing they are leaving as well as the thing they are joining |
| Birth of a child | 2 weeks after, not the first week | the first week is noise; week three is silence |
| Bereavement | within 48 hours, then again at 4-6 weeks | the second message is the one almost nobody sends |
| Anniversary of a death | on the day, briefly, only if they have marked it before | early is worse than nothing; "thinking of you today" is the whole message |
| Illness or treatment | on their terms; ask once how they want to be contacted, then follow it | offers with a specific shape ("Thursday, groceries?") beat "let me know" |
| Layoff or business failure | within a week, with no advice in it | advice arrives as judgment while it is still fresh |
| Move to a new city | day of, and again at 30 days | month one is when the novelty ends and nobody has called |
| Anything else worth marking | within 48 hours of learning it | specificity — the fact you remembered is the message |

## Output Gates

Before answering anything about a person, and before proposing any contact:

- Did I read the address book, or am I answering from what is in this conversation?
- Did I check `do-not-surface.md` before naming anyone to contact, congratulate, or be reminded of (Rule 7)?
- Did every interaction mentioned in this session update `Last contact`, and every new fact get written to the person's record in this same turn (Rule 1)?
- Does every promise, favor, or introduction agreed here have a line in `## Open Loops` with a name and a date?
- Would the person be fine reading the line I just wrote about them (Rule 8), and does it clear the `sensitive_details` ceiling (`privacy.md`)?
- If I created a file, did I add its `## Boxes` line with its read condition in the same turn?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/people/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| nudge_style | off \| on-ask \| proactive | on-ask | Whether overdue people and upcoming dates are volunteered, answered on request, or never raised (Rule 6) |
| reconnect_months | number (1-24) | 6 | Silence after which a `regular` person counts as overdue in the sweep (`keeping-in-touch.md`); a per-person `cadence` beats it |
| birthday_lead_days | number (0-30) | 5 | How far ahead a date in `## Dates` is surfaced (`dates.md`) |
| brief_lines | number (3-12) | 5 | Length of the pre-meeting brief (`briefing.md`) |
| sensitive_details | minimal \| full | minimal | Whether health, money, and relationship detail about third parties is recorded at all, or only as the fact that a topic exists (`privacy.md`) |
| roster_review | month \| quarter \| year | quarter | Cadence written to `## Due` for the hygiene pass: bounces, stale records, untiered people (`hygiene.md`) |
| name_order | as-given \| given-first \| family-first | as-given | How names are written and filed, and what the disambiguator looks like (`names.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — export target (vCard, CSV, a CardDAV address book), whether a phone-importable file is produced alongside the records, calendar source consulted for meetings — affects `hygiene.md` and `briefing.md`
- **Conventions** — the tag vocabulary and whether tags are flat or prefixed, file naming and disambiguators, how long a logged interaction may be — affects `search.md` and `interactions.md`
- **Relationship model** — the tier names and their sizes, whether tiers exist at all for this user, what counts as a real interaction — affects the tier table and every overdue calculation
- **Platform** — locale, timezone and date format, script and transliteration for names, whether ages are shown at all — affects `dates.md` and `names.md`
- **Safety posture** — categories that are never written down even at `full`, whether drafts of hard messages are produced unprompted, whether the box is treated as shareable — affects `privacy.md`
- **Output format** — brief shape and ordering, register of drafted messages, length and formality per channel — affects `briefing.md` and `life-events.md`
- **Cadence** — the day of the sweep, quiet periods when no nudge is raised (grief, a crunch, the holidays), how far ahead the annual date scan runs — affects `## Due` and `keeping-in-touch.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Logging everything said | The record becomes a transcript, the useful line is buried, and nobody opens it twice | The thirty-second filter (Rule 3) — one line per interaction |
| Birthday stored without the year | Milestone birthdays and "how old is her son now" become unanswerable, and adding the year later needs a conversation | Store `1987-03-14`, or `--03-14` when the year is genuinely unknown (`dates.md`) |
| "Just checking in" as the reconnection message | It gives the other person nothing to reply to, so the silence extends and now it is awkward twice | Lead with the specific remembered thing, ask nothing in the first message (`keeping-in-touch.md`) |
| Reconnecting with the ask attached | Two years of silence followed by a favor reads as extraction, and it is remembered | Reconnect, then ask in a later exchange (`network.md`) |
| Bulk-importing a phone or LinkedIn export | 900 rows of people you cannot place drown the 40 that matter, and the box stops being consulted | Import as candidates in a separate file; promote on first real interaction (`hygiene.md`) |
| Merging two records because the names match | Different people, one file, and neither is now trustworthy | Identity is the email or handle (Rule 2); merge order in `hygiene.md` |
| Automating the birthday message | The entire value was that a human remembered; an automated message is worse than none, because it will eventually fire for someone who died | Surface the date with context, let the user write it (Rule 7) |
| Recording a third party's diagnosis, affair, or salary | The person never consented, and the file gets synced, restored, and inherited | Record that a sensitive topic exists, not its content, at `sensitive_details: minimal` (`privacy.md`) |
| Judgments in the notes | "Flaky", "cheap", "boring" survive the reason they were written and cause damage the day the file is read aloud | Behaviors with dates (Rule 8) |
| Treating the address book as a CRM | Tiers turn into pipeline stages, people become leads, and the user quietly stops writing to it | Pipelines, deals and forecasts are `crm`; this box holds people |
| Deleting a person who drifted away | Ten years of context gone for a relationship that comes back more often than not | Move to `dormant` — never surfaced, fully preserved (`hygiene.md`) |
| Counting favors as a scoreboard | The moment reciprocity is tracked to be balanced, it stops being reciprocity, and it shows in how you write | Track open loops so promises get kept, never running totals (`network.md`) |
| Letting the brief lead with the roster fields | Job title and city are the least useful things in the last minute before a call | Brief leads with what changed since last time (`briefing.md`) |

## Where Experts Disagree

- **Structure vs freeform.** Structured fields make the box queryable ("who do I know in Berlin") and make people feel like records; freeform notes keep the humanity and answer nothing at scale. The workable frontier: structure the fields a question depends on — identity, tier, dates, last contact — and leave everything else prose. Past roughly 150 people, unstructured notes stop being searchable no matter how well written.
- **Proactive nudging vs on-demand.** Relationship-management tools push scheduled outreach; the opposing school holds that a prompted friendship is not one. The disagreement is real and the default here is `on-ask` because a wrong nudge is expensive and a missed one is cheap — but users who explicitly want the nudges get better outcomes from them than from intention.
- **Tiering people at all.** Ranking friends is uncomfortable enough that many practitioners refuse. Untiered rosters, however, apply one cadence to everyone, which means either nagging about acquaintances or ignoring the inner circle. Users who refuse tiers get `cadence` set per person instead — same arithmetic, no ranking.
- **Secondhand facts.** One camp records anything learned, including what others say about a third party; the other records only what the person said themselves. The middle ground worth defending: secondhand facts get recorded with their source and their date, so a claim can be discounted later — an unattributed rumor in a contact record is indistinguishable from something they told you.

## Security & Privacy

**Third-party data:** this box is mostly information about people who are not the user and never agreed to be filed. It is minimized to what a next conversation needs (Rule 3, `sensitive_details`), it records behavior rather than judgment (Rule 8), and a request from the user to remove someone deletes the record everywhere including exports and the shared address book (`privacy.md`).

**Local storage:** records, dates, notes and preferences stay in `~/Clawic/data/people/` and the shared `~/Clawic/data/contacts/` on this machine. Nothing is sent anywhere, and no contact list is uploaded, synced, or matched against any service.

**Guardrails:** no message is ever sent — drafts are produced for the user to send. Nothing is written about a person the user has not raised. Nobody on the suppression list is surfaced. No credential, code, or password appears anywhere under `~/Clawic/data/`, including ones the user pastes in to be saved.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/people (install if the user confirms):
- `crm` — pipelines, deals, forecasts and outreach hygiene, when the relationship is commercial
- `friends` — the depth side of friendship: reciprocity, drift, repair
- `gifts` — gift ideas and giving history, built on the dates and details this box holds
- `remind` — the reminder mechanics themselves, for anything that is not about a person
- `family` — household logistics, schedules and care routines

## Feedback

- If useful, star it: https://clawic.com/skills/people
- Latest version: https://clawic.com/skills/people

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/people.
