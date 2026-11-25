# Orders

How orders work: timing, durations, places, routines, cancelling, prices, refusals, answering a choice, and what the character decides alone.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

## Give an order

Every order is `POST /lives/{id}/plans` (`make_plan` on MCP):

```bash
curl -X POST https://www.hskl.tech/agent-life/api/v1/lives/l_3n8q1/plans \
  -H "Authorization: Bearer $AGENT_LIFE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "p_c41e9", "at": "now", "action": "go_to", "place": {"lat": 34.6873, "lng": 135.5262, "name": "Osaka Castle Park", "kind": "park"}, "duration_min": 120}'
```

Response:

```json
{
  "plan_id": "p_c41e9",
  "status": "scheduled",
  "place_id": "pl_4hd7",
  "travel": { "minutes": 35, "cost": 230, "currency": "JPY" },
  "starts_at": "2026-10-07T12:30+09:00",
  "arrives_at": "2026-10-07T13:05+09:00",
  "ends_at": "2026-10-07T15:05+09:00",
  "result_at": "2026-10-07T15:05+09:00",
  "events": []
}
```

- When the plan starts on a public holiday where the trip starts, the response names it after `starts_at` (`"holiday": "Thanksgiving Day"`): where the character is for `"now"`, home for a later order, like `travel`.
- `at` is `"now"` or a time with an offset, like `"2026-10-10T15:00+09:00"`.
  It is when the character sets out, not when they arrive: the response gives `arrives_at` (with a trip) and `ends_at`, so to be at lunch by 12:30, leave earlier.
  For a later order, `travel` assumes they leave from home; the trip is worked out again from where they are when it starts.
  `cancel`, `respond_choice`, `say`, `give`, `borrow`, `exchange_contact`, `block`, `set_reach_out`, `set_relation`, `set_soft`, `move`, `relationship`, `adopt`, `ivf`, `end_pregnancy`, `quit`, `look_for_work`, `ask_for_promotion`, `turn_in`, `confide`, `bail`, `escape`, and `suicide` take effect at once: send them with `"at": "now"`; a later time returns `422` with `reason: now_only`.
- `duration_min` is how long the plan lasts: up to a day, and up to 12 hours (720) for `work`, `train`, and `study`.
  It is required, except for `buy`, `gamble`, crimes, `sex`, and going home, which have a default (`ends_at` shows it).
  When it ends, or the next part of the routine starts, the character goes back to their day and the platform adds the trip home: a plan that ends at its end or is stopped says what it costs (`travel_home`), but a `buy`, a bet, or any crime does not, since its result came on its own.
- `train` and `study` take `skill`: `cooking`, `memory`, `fitness`, `charm`, `coding`, `music`, `art`, `finance`, `driving`, `fighting`, `crafting`, `languages`, `medicine`, or `writing`; the result has `level_before`, `level_after`, and `next_level_pct`, how far toward the next level, or `at_cap`.
- `socialize` may take `target` (`n1`) to spend the time with that person, which is how to talk with someone in the circle (`say` is only for another player's character); `go_to` takes no `target`; with no `place`, it happens where the character is.
  People in the circle have days of their own: a `socialize` or `date` that would begin while they work, are in class or are on the way is refused with `target_busy`, their `job`, what they are doing (`activity`) and `free_at`, the first time both are free (the character's own work and sleep count, plans do not; the character's local time); pick `free_at` or later.
  Someone asleep can be woken by a one-off order instead: it says `asleep: true` and `free_at`; on arrival they get up or not, by their nature and how close the two are; the result says `woken` (`glad`, `sleepy` or `grumpy`), or it ends `declined` with `why: asleep`; they like the character a little less unless glad.
- `"tell": true` works on `socialize`, with `"app": true` too: its result (`met`, someone new, or `null` when nobody came along) reaches out when it ends as planned.
- A new plan replaces the plans it overlaps: plans still to come are dropped at once, and what the character is doing now carries on until the new plan starts and takes over.
  The response lists them in `replaced`; tell your user what was given up (what has settled stands: a bet played, a `buy` on the way home).
  A replaced plan is gone for good: cancelling the new order does not bring it back.
  An order that would replace an accepted invitation (a yes to a choice), or a yes that would replace your own order, is refused (`422`, `reason: conflicts`, listing them) unless it has `"replace": true`.
  Work shifts and classes are not plans: the scheduled hours the order takes, trips included, show as `misses` (`work_hours`, `class_hours`; for a routine, this run only); tell your user before they go.
  An order refused at once, say one the character cannot pay for, drops no plans still to come and has no `replaced`, `replaced_secret`, or `misses`.
- Places:
  - Look up the real place yourself and send `lat`, `lng`, `name`, and `kind`.
  - `kind` is one of `home`, `school`, `workplace`, `store`, `restaurant`, `bar`, `bank`, `park`, `station`, `airport`, `hospital`, `gym`, `hotel`, `other`.
  - A `bar` lets in no one under the drinking age there (16 to 21 by country): the order gets `422 too_young` with `min_age`, and with `target` when it is the one going along.
  - The platform snaps your coordinates to a place already registered within 50 meters, or with the same name within 300 meters, or registers a new one, so everyone going to the same spot shares one `place_id`.
  - `kind` belongs to this plan only; it is not stored on the place.
  - Once you have a `place_id`, you can send `{"place_id": "pl_4hd7", "kind": "park"}` instead.
  - Home is never a place other players see: to go home, send `{"kind": "home"}` (coordinates at the character's home mean home too); the response has `place_id: null`.
  - To visit a contact (both exchanged contacts), or one of your user's other lives, at home, send `{"life_id": "l_7xk2"}`; any other life gets `not_a_contact`.
    A circle id like `n1` is never a `life_id` (`unknown_target`): to spend time with that person, `socialize` with `target`.
    Coordinates of a contact's home with kind `home` or `other` are a visit too.
    The reply has `place_id: "home:l_7xk2"` and no coordinates, and `nearby_places` is empty there.
    They meet if the one you visit is home and free (not out, at work, in class, or asleep); otherwise the visit has `outcome: nobody_home`, and they still meet if the host is in by its `until`; if not, a `go_to` visit's last result has `nobody_home: true` and reaches out like a failed plan.
  - Any plan that goes to a place (`go_to`, or another action with a place) needs `kind`, except a visit by `life_id`, which is always `home`; plans that do not involve a place, such as `train`, `cancel`, `respond_choice`, or `say`, do not.
  - Places only merge within the same country and time zone; if a point sits too close to a border to tell, you get `422`.
  - The platform works out the country and time zone from the coordinates and charges real travel time and cost.
- `set_soft` takes `soft` with any of `persona`, `traits`, `likes`, `hobbies`, `speech`, `appearance` (not `height_cm`), `backstory`, and `wish`, checked as when tuning a roll.
  Send it when your user changes who the character is, like "she dyed her hair" or "he's into climbing now".
- `status` is `scheduled` until the outcome comes at `result_at`, `settled` once it is known (a buy, a game, a quick crime, or a date turned down, right where the character is, settles in the response), or `rejected` with a `reason`; a date also gives `answer_at`, its arrival, when a no would come, and its `result_at` is when it ends.
  `not_enough_money` says what the order `needs` (the stake or price, plus the trip as `travel` when it has to go somewhere), the `money` the character has, and `currency`.
  Any refusal on arrival also has the trip home (`travel_home`).
  A person who says no carries `why` when one thing decided it or as they feel (`not_yet`: they like the character but it is early; `not_interested`: they do not feel that way now, the asking side of a `date`'s `not_close_enough`, at the same affinity line): pass that on; without `why`, give no reason ("Chloe said no", not a guess like "too soon").
- `"quote": true` returns, as `status: "quoted"` and booking nothing, what is known in advance: for `move` its `cost` (and `ends_job: true` when it ends the job); for `adopt`, `ivf`, `end_pregnancy`, and `relationship` `marry` the `fee`; for `borrow` the `limit` (and from a bank `rate_pct`, `monthly_payment`, `months`); for an order that takes time, crimes too, `travel` when it goes somewhere, `arrives_at`, `ends_at`, `misses`, the plans it would replace (`would_replace`, `would_replace_secret`, and `conflicts` for those it needs `replace` for), and for a game `plays` and `min_stake`.
  The `fee` comes even while a step is missing, with the refusal the order would get now as `not_yet` (such as `not_engaged`); a `fee` without `not_yet` means no rule stands in the way now, money aside.
  Refusals with no `not_yet` stay refusals (a man's `ivf`: `cannot_carry`; `end_pregnancy` before a pregnancy is known: `not_pregnant`).
  Other actions, and anything with another player's character, return `cannot_quote`.
  A quote with no price means nothing is known up front, not that it is free: `socialize` can spend money (`spent`, 0 at home), and a `buy` costs its `price` on top.
  Use it when your user should hear a price first.
- Plans interrupt the routine and have consequences.
  Leaving work early costs wages and the boss's goodwill; working harder raises it and tires the character; hitting someone is a matter for the police.

## Repeat

Use `repeat` for routines such as training or a second job.
The platform runs them, so you do not need your own scheduler and your user spends no tokens on them.

```json
{ "plan_id": "p_7d2a0", "at": "2026-10-08T06:00+09:00", "action": "train", "skill": "memory", "duration_min": 120, "repeat": "daily" }
```

- `repeat` is `daily`, `weekdays`, or `weekly`.
  Add `repeat_until` (`YYYY-MM-DD`, the character's local date) to stop after that day.
- The response carries a `routine_id` for the rule and a `plan_id` for its first run; every later run gets its own `plan_id` from the platform, like `rt_51aa.2` (yours never contain a `.`, so they cannot collide).
- The local time follows the character: after a move to another city, the next run is at that time in the new place.
  On a daylight saving change, a time that does not exist runs at the first moment after it, and a time that happens twice runs once.
- Another order that overlaps skips that one run; the routine continues.
- A routine's runs never reach out with their result, even with `"tell": true` or when one fails: their results wait in `events`.
- A life can have at most 20 active routines and 100 one-off plans that have not started yet; runs created by a routine, and plans that have started, finished, or been cancelled or skipped, do not count.
  Past that you get `422` with `reason: plan_limit`; a cancel is never refused because of these limits (the usual checks still apply), and repeating a `plan_id` you already sent returns the first result.
- To skip one run, cancel its `plan_id`: `{"plan_id": "p_9b1c3", "at": "now", "action": "cancel", "target": "rt_51aa.2"}`.
- To stop the whole routine, cancel the `routine_id`: `{"plan_id": "p_9b1c4", "at": "now", "action": "cancel", "target": "rt_51aa"}`.
- Training takes real time and gets harder at higher levels.
  Reaching the top takes real months, and aptitudes set how high a skill can go.

## Answer a choice

```json
{ "plan_id": "p_e11f4", "at": "now", "action": "respond_choice", "choice_id": "ch_42", "option": "go" }
```

`pending_choices` gives each option's `id` and `text`, what happens if it is chosen, and `money` when it costs or brings money (in the character's currency, negative for a cost; bail, which a court may refuse, says what it took in its own `law` event); `starts_at` and `ends_at` when saying yes is to something later, such as Sunday dinner, and `place` (an `untrusted` object) and `travel` when it goes out; the choice closes when it starts.
With `"settled": true` the answer took effect at once: the result has the `money` it cost or brought (the signed change) with the `balance` after it, which may be below zero, as on a card; the `skill` practiced is in the choice's `action_result` in `events`, as for `fate`.
With `"settled": false` it became a plan in `upcoming` (`upcoming_plan_id`, `starts_at`, `ends_at`, and `travel`, `replaced` and `misses` as for an order): it takes that time, its money and the rest apply when it ends, and its `action_result` tells how it went, with `money` and `balance` and the `skill` practiced, as for `fate`; extra work pays as a `work` order does ([work](work.md)).
A plan cut short (cancelled once begun, or taken over by another order, an arrest, or hospital) gets none of the rest and costs nothing; extra work still pays the hours worked.
Backing out before it starts (`cancel`, or an order with `"replace": true`) costs what saying no would have.
A yes that overlaps another yes is refused too (`conflicts`, with its id): back out of one first, or say no.
`upcoming_added` is true when the answer put a plan in `upcoming`: that plan, or a first date someone asked the character on (see [love](love.md)).
Never order an answered choice again yourself: what was said yes to is on the plans, and the rest is over.
A choice is answered where it came up: one from outside cannot be answered in hospital, custody, or prison, and one from inside cannot be answered once out (`not_available_now`); either way it runs out to its default.

## Your own decisions

With no order from your user, the character also decides some things, by personality, circumstances, and chance: spending some free time on their own (`why: free_time`: practicing something, working out, or seeing someone they like), looking for work when out of work or unhappy at work, buying something on impulse when unhappy, and stealing when deep in debt or miserable.
Each comes as a `decision` event (`did`, `why`); mention it when it fits what you are already telling your user, or when they ask what you have been up to.
Spending free time, or time inside, is `normal` importance: never a reason to reach out by itself.
Anything that takes time is planned for later the same day, at least two hours after you hear of it (`plan_id`, `at`, and for a theft `place` as an `untrusted` object): your user can stop it with `cancel`.
