# Facilitation — Running The Room

**Before facilitating**, read the agenda or charter (`artifacts/` if `## Boxes` names one), the `Context` column of each attendee in `~/Clawic/data/contacts/contacts.md` (who decides, who blocks, who needs to be asked directly), and `~/Clawic/data/meetings/decisions.md` for anything already settled that might be reopened. Everything on this page is a script for the human in the room, not an action to take on their behalf.

**Contents:** [The First 60 Seconds](#the-first-60-seconds) · [Airtime Mechanics](#airtime-mechanics) · [The Difficult Attendee Catalog](#the-difficult-attendee-catalog) · [Keeping Time](#keeping-time) · [Getting To A Decision](#getting-to-a-decision) · [When You Are Not The Chair](#when-you-are-not-the-chair) · [Ending](#ending)

## The First 60 Seconds

Say four things, in this order, every time. It costs a minute and prevents most of the failure modes on this page.

1. **Output**: "By 10:25 we will have decided X."
2. **Method**: "Priya decides after hearing everyone" / "we need consent, object only if you can name a harm".
3. **Shape**: "Eight minutes of objections, then the decision, then five minutes of actions."
4. **Roles**: who scribes, who watches chat, who keeps time — never all three on the chair.

Then stop talking. A chair who speaks for the first five minutes has set the norm that this is a broadcast.

## Airtime Mechanics

Airtime is a fixed budget: in a 50-minute meeting with 8 people, the average share is 6 minutes. The default distribution is nothing like average, and the fix is structural, not social.

- **Written-first beats speaking-first.** Two minutes of silent writing before discussion produces independent positions; without it, the first speaker anchors the room and everyone else responds to them instead of to the question.
- **The chair speaks last on any question the chair also owns.** Otherwise the room is confirming, not contributing.
- **Rounds, by name, for anything expensive.** "I want one sentence from each of you" surfaces the objection that would otherwise arrive by DM tomorrow.
- **Hold silence to about seven seconds before filling it.** Rowe's wait-time work found that extending the pause to even ~3 seconds changes who answers and how much they say; the instinct to rescue silence at 2 seconds hands the floor to the fastest talker permanently.
- **Ask the quietest expert directly, by name and topic**: "Lena, you have shipped this twice — what breaks?" Generic "any thoughts?" gets nothing from the people whose thoughts you need.
- **Track who has not spoken** and call it out mechanically, without commentary about it.

## The Difficult Attendee Catalog

Each one is a role the room is producing, not a character flaw — the intervention is on the structure.

| Behavior | What it costs | Intervention |
|---|---|---|
| Dominates the discussion | Everyone else's turn | "Let me get Sam and Lena in on this, then come back to you." Then actually come back |
| Rambles without a point | The timebox | "What is your recommendation, in one sentence?" |
| Relitigates a settled decision | The whole meeting | "That was decided on 12 June, here's the entry — what new information changed?" (`~/Clawic/data/meetings/decisions.md`) |
| Silent for the whole hour | The expertise you invited them for | Direct, specific question; if it happens twice, ask them privately whether the meeting is worth their time |
| Attacks people rather than options | Psychological safety, permanently | Name it once, factually: "let's keep this on the options." If it recurs, take it out of the room (`difficult.md`) |
| Answers a question nobody asked | Ten minutes on an adjacent problem | "Parking lot — I'll add it with your name and a date. Back to the decision." |
| Says "I'm just thinking out loud" then decides | A commitment nobody agreed to | Read it back explicitly: "so the decision is X — is that what you mean?" |
| Arrives 10 minutes late and asks for a recap | The room's time, twice | Do not rewind. "Recap after; we're on item two." Recap in the notes, not live |
| Multitasking visibly | Signals the meeting is optional | Ask them a direct question. If half the room is multitasking, the meeting is the problem |
| The senior person who talks first | Anchors the room | Structure prevents it: written-first, or ask them privately to speak last |

**The parking lot only works if items leave it.** Every parked item gets a name and a date at the close, or it becomes the place where good objections go to die.

## Keeping Time

- **Announce the timebox before each item**, and the remaining time at its midpoint: "four minutes left on this."
- **At 80% of the slot, stop, regardless of state.** The close is not optional (SKILL.md Rule 4).
- **When an item overruns, choose out loud**: extend it and drop another item, or park it with an owner and a date. Silently letting it run is choosing to drop the last item, and the last item is usually the close.
- **When the room deadlocks**, name it and switch: "we're going in circles. Options are decide now with what we have, or Priya decides by Thursday with the data. Which?" Deadlock is almost never resolved by more discussion in the same room.
- **Ending early is a feature.** Give the time back explicitly; it teaches people that this meeting is honest about its length.

## Getting To A Decision

The sequence that converts discussion into a decision, once objections are on the table:

1. **State the exact question.** Not "what should we do about the CDN" but "do we migrate this quarter, yes or no".
2. **State the options, including doing nothing.** Two to four; if there are seven, the pre-work was not done.
3. **Ask for objections by name**, not for agreement. Agreement is cheap and reversible; the objection is the information.
4. **Apply the method.** Owner decides, or DACI's D decides, or consent (object only with a named harm), or a vote when the group is genuinely peer-level (`decision-rights.md`).
5. **Say the decision out loud in one sentence and ask if that is what everyone heard.** Half of all "reversals" are two people who left with different sentences in their heads.
6. **Ask for disagree-and-commit explicitly** from anyone who lost: "can you live with it and support it outside this room?" A "no" here is worth ten times a silent "yes".

## When You Are Not The Chair

Influence without the gavel, in order of leverage:

- **Before**: get the output named. One line to the organizer — "what are we deciding?" — reshapes more meetings than anything said inside one (`preparation.md`).
- **First question in**: whoever asks the first substantive question frames the discussion. Prepare it.
- **Offer the structure, do not seize it**: "would it help to take two minutes to write our positions first?" Chairs almost always say yes, and the meeting becomes the one you designed.
- **Make the close happen** when the chair forgets: at the five-minute mark, "before we go — what did we decide and who owns what?" No authority required, and it is always welcome.
- **After**: send your own summary of what you understood, to everyone. A written version becomes the version, and it is the strongest lever available to a participant.
- **Objections go in writing after the room**, not in a corridor. A corridor objection is deniable, reopens the decision later, and costs you the credit for having raised it.

## Ending

Run the close from SKILL.md, The Last Five Minutes — decisions, actions read back with owner-date-done-means, open questions with a chaser, next occurrence or explicitly none. Then say who sends the recap and by when (`recaps-and-minutes.md`).

**Write in the same turn as the close**: the record block in `records/<year>-<mm>.md`, the decision row in `~/Clawic/data/meetings/decisions.md`, each action item in `## Follow-Ups`, and anything you learned about how a person operates in the room into their `Context` in `~/Clawic/data/contacts/contacts.md` (`memory-template.md`). A facilitation script that worked twice on a hard recurring room is an artifact: `artifacts/facilitation-<situation>.md`, indexed in `## Boxes` the same turn.
