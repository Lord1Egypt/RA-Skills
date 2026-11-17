# Dates — Birthdays, Anniversaries, And The Ones That Hurt

A date is the only part of an address book that acts on its own schedule. It is also where an automated system does the most damage, because a date fires whether or not the relationship still exists.

**Read `## Dates` in `~/Clawic/data/people/memory.md`** — or `~/Clawic/data/people/date-index.md` if the `## Boxes` index points there — before answering any question about what is coming up, and **read `do-not-surface.md` before surfacing any of them** (SKILL.md Rule 7).

**Contents:** [The Date Types](#the-date-types) · [Lead Times](#lead-times) · [Storing A Date](#storing-a-date) · [Hard Anniversaries](#hard-anniversaries) · [Age And Milestone Arithmetic](#age-and-milestone-arithmetic) · [The Weekly And Annual Scans](#the-weekly-and-annual-scans) · [What Makes The Message Land](#what-makes-the-message-land)

## The Date Types

| Type | Worth storing when | Note |
|---|---|---|
| Birthday | `inner` and `regular` tiers, always; `orbit` only if volunteered | The one date most people expect to be remembered by someone |
| Children's birthdays | You know the family and see them | Stored on the parent's record as `(child's name), via (parent)`; the child is not a contact |
| Wedding or partnership anniversary | You were there, or they mark it publicly | Congratulating the wrong couple is a real risk — check the partner field is current |
| Work anniversary or start date | Professional contacts you want a reason to reach | A same-week note is high-yield and low-cost; nobody else sends one |
| Death anniversary of someone they lost | They have marked it before, or told you the date | See Hard Anniversaries — the rules are different |
| Diagnosis, treatment, or recovery milestone | They framed it as a milestone themselves | Only on their terms; never invent an anniversary of an illness |
| Move-in date in a new city | Anyone who moved | Drives the 30-day follow-up, which is the message nobody sends |
| Divorce or separation date | Never as a date to mark | Store as context on the record; there is no message |
| Citizenship, graduation, sobriety, a launch | They mark it | Ask nothing; if they mention marking it, store it |
| Anything else | The user says it matters | Store with its lead time and its handling note |

## Lead Times

Lead time is how far ahead the date is surfaced, not when a message is sent. Default is `birthday_lead_days` (5); the `Lead` cell on that date's row in `## Dates` overrides it for that date alone.

| Date | Default lead | Why that lead |
|---|---|---|
| Birthday | 5 days | Enough to arrange something, close enough that it is not forgotten again |
| Milestone birthday (30, 40, 50, 60…) | 3 weeks | It needs a plan or a gift, and a plan needs weeks (`gifts`) |
| Children's birthday | 5 days | Usually a message to the parent, not the child |
| Wedding anniversary | 5 days | Same logic as a birthday |
| Work anniversary | 2 days | It only reads as attention if it is close to the day |
| Death anniversary | 1 day | Surfaced late on purpose: it is a message on the day, or none |
| Move-in +30 days | 2 days | The check-in message, timed to the week the novelty ends |
| Birth of a child +2 weeks | 2 days | Week one is noise; week three is silence (SKILL.md Message Moments) |
| Anything else | 3 days | Default row |

Two dates within three days of each other for the same person collapse into one surfacing, not two.

## Storing A Date

- Format `YYYY-MM-DD`. When the year is genuinely unknown, `--MM-DD` — that is a fact, not a gap, and it says explicitly that age arithmetic is unavailable.
- The **person's record is the authority**; the `## Dates` table is the ordered view over it. If they disagree, the record wins and the index row is corrected in the same turn (`memory-template.md`).
- Every date line carries who it belongs to, what it is, and the handling note if it needs one. A date with no handling note gets the default treatment for its type.
- Never store an **age**. Ages are computed from the year and are wrong within twelve months otherwise.
- Never harvest dates. A birthday scraped from a profile the user has not been told about is a date the person did not share; store it only if they gave it, or if the user already knew it.
- A date learned from a third party is secondhand and carries its source (`details.md`), because the classic failure is congratulating someone on an anniversary that ended last year.

## Hard Anniversaries

The anniversary of a death, of a diagnosis, or of a loss follows inverted rules, and getting them wrong is the most expensive mistake this skill can make.

- **Only mark it if they have marked it.** If they have posted about it, told the user the date, or asked to be checked on, it is stored. Otherwise it is not stored at all, and certainly not surfaced.
- **On the day, never early.** An early message forces them to hold the date in their head for another three days.
- **Short.** "Thinking of you today" is a complete message. Anything longer asks them to reply at length on a day they may not want to.
- **Roughly the first three years**, unless they continue to mark it. After that, surfacing it can reintroduce a date they have deliberately let recede — the record keeps the date, the surfacing stops.
- **The person who died goes on `do-not-surface.md`**, with their own dates removed from the index, in the same turn the death is learned. This is the specific failure the whole suppression mechanism exists to prevent.
- A first birthday, first Christmas, or first anniversary after a loss is harder than the anniversary itself for many people. If the user knows the loss, the note goes on the record, not on the calendar.

## Age And Milestone Arithmetic

- Age today = current year − birth year, minus one if the date has not passed this year. Store only the birth year.
- Milestone birthdays are multiples of ten, plus 18, 21, 65 depending on the culture — and they are surfaced at three weeks, not five days, because the response required is different in kind.
- "How old is her son now?" is answered from the birth year and stated as a computation, not as a stored fact: "Sofia was born in 2019, so she is 6 or 7 depending on the month."
- Anniversary counts work the same way: the year is what is stored, "their tenth" is derived.

## The Weekly And Annual Scans

Both live in `## Due` and are subject to `nudge_style`.

- **Weekly**: everything falling inside its lead window, one line total, with the context needed to write the message. Never a list of names alone — a name without its detail generates a generic message, which is the outcome this skill exists to avoid.
- **Annual**: once a year, scan the next twelve months for milestone birthdays and round-numbered anniversaries, which are the only ones that need a runway. This is also when dates for people who left the roster are removed.
- Both scans filter through `do-not-surface.md` before producing a single name.
- A `quiet_until` date in `config.yaml` suppresses both — after a bereavement, during a crunch, over a holiday — and the suppression is honored silently, with no note that a nudge was withheld.

## What Makes The Message Land

The date is the trigger; the record is the content. A message that says only "happy birthday" competes with forty identical ones and adds nothing to the relationship.

- Lead with the specific thing from `## Details` or the last log entry: the climbing trip, the new job, the kid starting school.
- One question is enough, and it should be answerable in a sentence.
- Match the channel on the record. A birthday message on a channel they never read is not a message.
- Never send it automatically, never on the user's behalf, and never as a template with the name substituted. The entire value being delivered is that a person remembered (SKILL.md Traps).

**Write in the same turn**: the date into the person's record, its row into the `## Dates` table in `~/Clawic/data/people/memory.md` — `MM-DD`, who, what, year, lead, notes, ordered by `MM-DD` — splitting to `~/Clawic/data/people/date-index.md` past the threshold — and, when a scan runs, its date into `## Due`. A death also writes the person onto `~/Clawic/data/people/do-not-surface.md` and removes their dates from the index (`memory-template.md`).
