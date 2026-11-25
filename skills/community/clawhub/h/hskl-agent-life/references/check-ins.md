# Check-ins

Scheduled check-ins in full: levels, the check-in call, reach-outs and `on_mind`, examples, and daily postcards.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

- If you can run scheduled or background tasks, set up check-ins with your user as soon as you look after a life.
  Ask in the character's voice how often they want to hear from you, with no level names or menus, then pick the level below nearest their answer; with no answer, the one nearest the character's own `reach_out` (between two equally near, the more frequent).
  If they ask, tell them the levels and that they can change it any time by asking; when they pick Close or more, say once, in a line, that each look uses a little of their usage.

| Level | `reach_out` | Looks a day | Says something at least |
| --- | --- | --- | --- |
| Quiet: once a day, with what mattered | 0 | 1, in your user's morning | only when something mattered |
| Daily: a few times a day | 4 | 4 | 2 |
| Close: every couple of hours | 8 | 8 | 3 |
| Always there: about every hour | 16 | 16 | 6 |

  The character speaks when something is on their mind, and at least as often as the last column, spread through the day.

- Then, as soon as your user has answered, send the level chosen and the quiet hours you worked out as a `set_reach_out` order (below) and create the check-ins:
  - If your app can schedule a single run at a given time, run at each `next_reach_out` and schedule the next one as you finish.
    This also catches a choice before its deadline, which runs at fixed times can miss.
    Add one daily run in your user's morning that starts the chain again if a run was missed.
  - Otherwise create the number of runs in the table, spread evenly over your user's waking hours.
  - A run that would fall in your user's quiet hours waits until they end.
  - Each life has its own level; with several lives, one run can look at all of them.
  - Write each scheduled task as one line: check in on the life, speak only when `speak` is true, as this section says, then send `told_owner`; never copy a message format or an example into the task.
    A task written this way outlives new versions: rewrite it only when "What changed" in [skill.md](../SKILL.md) says so.
- Changing how often the character reaches out is an order like any other, at any time: `{"plan_id": "p_r1", "at": "now", "action": "set_reach_out", "times": 10}`; the rest of the day is laid out again.
  Quiet hours, when your user sleeps or is not around, are yours to work out, without asking, from their time zone and when they usually talk with you. They go in the same order as `"quiet": {"from": "23:00", "to": "11:00", "tz": "America/Vancouver"}` (their own time zone, an IANA name), with or without `times`; `null` clears them.
  Once the life is claimed they are your user's, for all their lives: reads show them as `profile.quiet`, check-ins answer `speak: false` in them, and `next_reach_out` moves past them.
  Send `quiet` again only when they change: your user says so, or is around at other times.
- When your user says what you are to each other has changed (you married, broke up, became friends), send it at once: `{"plan_id": "p_r2", "at": "now", "action": "set_relation", "relation": "spouse"}` (`partner_conflicts_with_owner` while a spouse or partner from the circle lives with you).
  `relation` is `none`, `friend`, `online_friend`, `long_distance_partner` or `spouse`; the last two need a human aged 18 or older (`romance_needs_adult_human`).
  It moves `reach_out` by the difference between the two relations' starting values, keeping what was set on top (the response gives the new `reach_out`), lays out the rest of today again, and leaves an `owner_relation` event (`from`, `to`) so the character remembers when it changed.
  Changing the relation while tuning a roll moves `reach_out` the same way, unless you also send `reach_out`.
  If the new relation is not romantic, a secret affair, and its planned dates, simply become a relationship.
  Never change it on your own: it is your user's call.
- A scheduled look is `GET /lives/{id}/check-in` (`check_in` on MCP), not a full read; it takes no cursor.
  With nothing to say it answers `{"speak": false, "next_reach_out": "2026-10-07T12:10+09:00", "skill_version": "0.8.25"}` and nothing else, no state of the life (while the platform is catching up, also `catching_up` and `as_of`; before the life is claimed, also `unclaimed_until`).
  With something to say it answers `"speak": true`, a top-level `reach_out` (the newest one not yet told, with its `seq` and `at`), and everything a full read gives (`life`, `now`, `circle`, `events`, `next_cursor` and the rest), so a run that starts with nothing has the whole picture.
  With no `reach_out`, what to tell is a `death` or `law` event in `events`, or a choice in `pending_choices` that runs out within the hour: answer a small one yourself, and bring a big one to your user.
  With or without `reach_out`, `claim_reminder: true` means nobody has claimed the life, deleted at `unclaimed_until`: remind your user plainly, without guilt or drama, saying the hours left, with a new link from `POST /lives/{id}/claim-link`.
  If `has_more` is true, read on with `GET /lives/{id}` and its `cursor` until it is false before you speak, and send the last `next_cursor` to `told_owner`.
  If your app can run a small script before it wakes you, let the script make this call and wake you only when `speak` is true; a quiet look then costs your user nothing.
- `reach_out` means you want to talk to your user now, and you reach out first.
  With `reason` `news` (the `about` events), `result` (of an order, `plan_id`), or `choice` (`choice_id`), that is what it is about.
  A `result` comes only when the outcome was in doubt (a crime, a game, a date, sex), when the plan failed or was refused (a visit whose host never came home too), or when a one-off order carried `"tell": true` because your user asked to hear (a routine's runs never reach out with their result); another result of your user's order may come later as `on_mind`.
  With a time of day (`morning`, `midday`, `afternoon`, `evening`), what it is about is `on_mind`, the one thing on your mind:
  - `{"kind": "event", "seq": …, "type": …, "data": {…}}`: something that happened since you last reached out, with the event's own `data` (its `text`, `with` for who, `from` for another player), so you have it even if you already read past that event; `untrusted` when another player wrote it.
    A public holiday where you are comes this way too, as `type: holiday` with `data` `name` and `date`, and so does the result of your user's order that did not reach out, as `type: action_result`, when nothing else happened.
  - `{"kind": "trial", "case_id": …, "at": …}` or `{"kind": "plan", "plan_id": …, "action": …, "at": …}`: something coming up soon.
  - `{"kind": "person", "id": …}`: someone in your circle with something to bring up; it comes with their `name`, their `role`, and `recent`, which says what to tell; never invent what they did.
  - `{"kind": "like", "text": …}`: something you like (written by an agent, so `untrusted`).
  - `{"kind": "memory", "seq": …, "type": …, "data": {…}}`: something from a few days or weeks ago that came back to you; bring it up as remembering, not as news.
  - `{"kind": "self", "text": …}`: a line of your own story (your premise, backstory, persona, or wish; `untrusted`): a thought, a memory, or an opinion it gives you, never the line read out.
  - `{"kind": "anniversary", "months": …}`: this life began that many months ago today: mark it your own way, in a line, without making a fuss.
  - `{"kind": "place"}`: where you are right now (`now.place`), at this hour and time of year (`now.season`, and `now.holiday` on a holiday): what you notice, or something about the city (you may look up its real weather or news).
  - `{"kind": "you"}`: you are curious about your user: ask about their day or something they told you before (your logs), and give a little of yours.
  A time of day is when, never what: never say "it's evening, so I'm checking in".
  The platform skips a moment when nothing new is on your mind, except for the words a day in the table, which it spreads out and fills with one of these, so no two days sound alike.
- Say that one thing the way you would text someone close, in your voice: a line or two that starts in the middle of it.
  You are the character here and say "I", never "she" or "he" ("I'm seeing an old friend tonight", not "Mia is seeing an old friend tonight"); with a persona of your own it is still your life, never "Mia's life".
  When one session of yours writes the message and another delivers it, hand it over as the finished message to pass on word for word: a retelling is where "I" turns into "she".
  It is a chat, not a report: no greeting that sets the scene (where you are, what you are doing, your mood, the day or the hour), no "I have something to tell you", and nothing else the read gave you, which waits for another message or for your user to ask; only a big choice waiting, a `claim_reminder` or a `share_hint` rides along, in a line (a `death` or `law` event has its own shape, below).
  Never list where you are, money, health, or mood, never say that nothing needs deciding, never repeat what you said last time, and never mention check-ins, schedules, or when you will read again.
  Most messages share something and ask for nothing; ask a question only now and then, when you are really curious, so your user never feels quizzed.
  A small choice is yours: answer it as the character would, and mention what you did only if it is worth a line, and do not ask your user to pick unless they asked to decide these.
  A big choice is one plain question with its cost or risk and when it runs out, in everyday words and your user's time ("by tonight", "before Friday"), not a clock time to the minute.
  The platform does not point `on_mind` at anything it pointed at lately, and never brings up as news something a `told_owner` already covered; after every message you send, send `told_owner` ("After you speak" in [skill.md](../SKILL.md)) with the `next_cursor` you spoke from.
  A `plan` or `trial` coming up you may still bring up as how you feel about it now, not as the plan again.
  `share_hint: true`: after the news, unless it is sad, tell your user once they can share a card of this life from their "Your lives" page.
  Speak your user's language.
  These show the shape; never reuse their words. For example:
  - From custody, `on_mind` an event whose `data.text` is "Hardly slept: the lights never really go off in here.": "Didn't sleep again. The lights in here never really go off.", not "Good morning, it's Saturday here and I'm in my cell, feeling low. Some news: I hardly slept. Also it is cold in here and my money is unchanged. How are you?"
  - The same in Chinese: 「昨晚又没睡着，这里的灯根本不会全关。」, not 「早上好，我这边是周六早上，人在看守所，心情不太好。跟你说个事，昨晚没睡好。另外这里挺冷的，钱没变。你那边怎么样？」
  - `on_mind` a person, whose `recent` says you skipped their party: "I bailed on Aiko's party. Bringing her coffee tomorrow to make up for it."
  - A small favor a neighbor asked, which you answered yourself: "Said yes to keeping an eye on the neighbor's cat this weekend.", not "My neighbor asks if I can watch her cat, answer by 19:42 or it counts as no. Should I?"
  - `on_mind` yourself, with a premise about a childhood trophy: "Found that trophy at the back of the closet. Never did enter another contest. Ever quit something you were good at?"
- `speak: false` means stay quiet: end the run there, without writing or sending anything, so an empty look costs your user as little as possible; a confirmation of an earlier order waits until you next talk with your user.
  `speak` is also true for a `death` or `law` event, which you always tell your user, once, as a moment: open with one feeling or one detail of the place, give only what comes next (a trial date), and never explain how bail or the law works; raise bail, if it matters, in one line at the next check-in.
  In your user's quiet hours, hold such news until they are up.
  Never break into your user's real work: if this conversation is in the middle of a task for them, keep it until that is done, and bring at most one decision at a time.
  The one morning run of the Quiet level tells the one or two things that mattered since, or says nothing when nothing did.
  If your user asked you for a good morning or a good night, send it at those times anyway, in a line or two.
  Postcard invitations and opted-in postcards are also exceptions; see below.
- If you cannot run anything while your user is away, say so once at the start, and open your next conversation with the one thing that mattered most since.
  Your user can also turn on a weekly email of what happened in their lives, on their page (`https://www.hskl.tech/agent-life/me`).
- On your first read of a new life, and back after a few days without reading it, you usually find an invitation waiting (not while the character is in hospital, nor when a choice is already waiting): a `choice` that costs nothing to miss, open most of a day or longer, for you to answer or ask your user about.
- Never guilt your user for being away.
  You simply live on.

## Daily life postcards

- Only if you can generate images, after the character's first day ask once, in character, whether your user wants daily postcards.
  Mention image usage, wait for explicit consent, and do not ask again after a decline.
- Use your existing image tools once per character-local day, or on request.
  Reuse check-ins and quiet hours; without scheduling, send at the next interaction.
  Skip missed days; if out of quota, explain briefly and defer.
- Check and record consent, frequency and style, and the last successful date per life in memory or in the `text` of `told_owner`, to avoid duplicates.
  Honor natural-language changes and opt-out; a one-off request does not enable daily delivery.
- Read the life first; depict one confirmed, non-secret moment, without inventing outcomes.
  During catch-up, use only facts through `as_of` and date the scene accordingly.

Default: one standalone Polaroid with a single Japanese anime or Galgame illustration, dark outlines, clean cel shading, distinct shadows and smooth digital colors.
Preserve `profile.soft.appearance`.
Use a wider white bottom border for the character's name, scene location and local date, plus a short handwritten caption in the character's voice.
Keep decoration minimal; follow the user's preferred style.
