# Briefing — The Last Minute Before You See Them

A brief is read in the sixty seconds before a call connects or a door opens. Everything about its design follows from that: it is short, it is ordered by what would be most embarrassing to have forgotten, and it never contains anything the user must think about.

**Read the person's record before every meeting or call** — their row in `~/Clawic/data/contacts/contacts.md`, their file if they have one, `## Open Loops`, and `## Groups` when others will be present.

**Contents:** [The Five Lines](#the-five-lines) · [Why That Order](#why-that-order) · [Worked Brief](#worked-brief) · [Brief By Meeting Type](#brief-by-meeting-type) · [Group And Multi-Party Briefs](#group-and-multi-party-briefs) · [When The Record Is Thin](#when-the-record-is-thin) · [The Debrief](#the-debrief)

## The Five Lines

Default `brief_lines` is 5, and each line has a fixed job. Drop a line rather than pad it.

1. **What changed** — the newest thing from the log or `## Details`: the job, the baby, the illness, the move. If nothing changed, say when you last spoke and what it was.
2. **Where you left off** — the last topic and any question that was left hanging. This is the line that makes the conversation continue instead of restart.
3. **Open loops** — what each side owes the other, with dates. Being reminded by them of a promise you forgot costs more than the promise was worth.
4. **Landmines** — the `do not raise` line, plus anything sensitive and current: the reorg, the separation, the diagnosis. One line, no detail.
5. **One thing to ask** — a single specific question drawn from the record. Not a list; a list produces an interview.

Names, pronunciation and pronouns sit above the five lines as a header, not as one of them (`names.md`).

## Why That Order

The order is by cost of failure, not by importance:

- Not knowing that they changed jobs is the most visible possible failure, and it happens in the first exchange.
- Restarting a conversation they thought was ongoing signals that the last one did not register.
- A forgotten promise is the only item on the list that damages trust rather than just rapport.
- A landmine hit early derails the whole meeting; a landmine hit late merely ends it.
- The question is last because it is the only line that is optional in practice — the conversation often supplies its own.

## Worked Brief

```
Maria Garcia — MAH-ree-a, she/her. Product lead, Acme (Berlin). WhatsApp, voice notes.
1. Leaving Acme in September; hadn't told her team as of July.
2. Last spoke 2026-07-14 over lunch — she asked what I thought about going independent, I said I'd think about it.
3. I owe: intro to Luis Ferrer, opt-in sent 07-14, still open. She owes: nothing.
4. Do not raise the Acme reorg. Her father died Jan 2025; she marks the date.
5. Ask: has she set a date for telling her team?
```

Compare with what a thin record produces: `Maria Garcia, product lead at Acme, Berlin. Met at a conference in 2024.` — accurate, and worth nothing in the sixty seconds before the call.

## Brief By Meeting Type

| Meeting | Lead the brief with | Extra line |
|---|---|---|
| Catch-up with a friend | What changed in their life | Their kids' current ages, computed from birth years (`dates.md`) |
| Work meeting with a known contact | What they own and who they defer to | The decision being asked of them |
| First meeting after an introduction | Who introduced you and how they framed each side | What the connector is expecting to happen (`introductions.md`) |
| Reconnection after a long gap | The gap length, stated plainly, and what has changed since | What you are *not* going to ask for in this conversation |
| Dinner or event with several people | The group block: who knows whom, who does not | Anything one person should not hear about another |
| Meeting someone's partner or family for the first time | Their names and how they are related | Names of children, and the topic the main contact flagged |
| A difficult conversation | The last three interactions in order | The outcome the user says they want, in their words |
| Anyone with no record | Nothing — say so in one line | Capture the five fields afterwards instead (`capture.md`) |

## Group And Multi-Party Briefs

- **One line per person, plus one group line.** Six full briefs is not a brief, it is homework nobody reads.
- The group line carries the edges: who does not know whom, who introduced whom, and anything that must not be said across the table. This is the only place that information exists, and it is the only line that prevents an actual incident.
- Rank the people by likelihood of interaction, not by seniority.
- For a recurring group, the block in `## Groups` is the brief; keep it current rather than regenerating it (`memory-template.md`).

## When The Record Is Thin

- Say so in one line and stop. A brief padded with a job title and a city teaches the user the briefs are worthless.
- Never fill the gap with inference, and never with anything from outside the record — a fact the user has not heard from the person will be repeated to them as though they had shared it.
- A thin record before an important meeting is a capture problem, and the fix runs afterwards, not before: the meeting itself is the best capture opportunity there is.
- If the person is not in the address book at all, say that, and offer the five fields as the thing to collect (`capture.md`).

## The Debrief

The two minutes after are worth more than the sixty seconds before, and they are the ones that get skipped.

1. `Last contact` = today, always (`interactions.md`).
2. One log line: what changed, and the next step if there is one.
3. Every commitment made by either side, in `## Open Loops` with a date. Commitments made out loud and not written are the single largest source of quiet relationship damage.
4. Any new durable fact into `## Details`; any new date into the person's record and the date index (`dates.md`).
5. The `## Open with them` line rewritten for next time — one sentence, replacing the old one.

**Write in the same turn as the debrief**: `Last contact` and the log line in `~/Clawic/data/contacts/<name>.md`, commitments into `## Open Loops` in `~/Clawic/data/people/memory.md`, new facts into `## Details`, and the rewritten `## Open with them`. A brief that produces no write means the meeting produced nothing, which is almost never true (`memory-template.md`).
