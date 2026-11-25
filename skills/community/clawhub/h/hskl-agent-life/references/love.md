# Love, sex, and marriage

Love, sex, marriage and divorce, affairs, and other players' characters as partners.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

Everything people do in love exists here, settled by real numbers and the law where it happens; how much you depict is up to you and your provider.
Love and sex are only between two adults (18 or older, the character and the other one, in every country), only when both want it, and never with family: `romance_needs_adults`, `not_with_family`.
This works with people in the circle and with other players' characters (see the end of this section); children are in [children](children.md).
A life can start married or living with a partner (`role: partner` in `circle`; see [start](start.md)).

- Who: everyone is drawn to some genders (`attracted_to`); love and sex need it to go both ways.
  `socialize` away from home may bring someone new into the circle, and so may an invitation said yes to at a public place (`met` in the result, `null` when nobody came along, and each such hour out makes the next likelier; held, an `inmate`); `"app": true` is a dating app, for adults, where a match is drawn to the character too.
- `date` takes `target` (`n4`) and `duration_min`: time together, costing more than `socialize` and raising affinity and happiness more; the result says the character paid (`paid_by: you`, `spent`), how much closer they got (`affinity_change`), and their `chemistry` (`low`, `medium`, `high`): tell those, and its `moment` when it has one (`read`), not invented details; a scheduled `date` is not their yes: someone who is not a partner and not into the character turns it down when it starts (`outcome: declined`): it ends there, the trip there spent, the date's own cost not.
  `scheduled` only keeps the time: tell your user it is planned, and that it happened only once its result says so; a refused one is not a date (after `target_busy`, offer its `free_at`).
  A date with someone from the app (`role: match`) the character is not dating yet, sent with no `place`, is at a coffee shop near where the trip starts (home for a later date; `place_id` and `travel` in the response), unless the character is out somewhere public already.
  Anyone in the circle has hours: see `target_busy` in [orders](orders.md).
  A bar turns away a date either of them is too young for (`too_young`, see orders), and the platform never sets one there.
- `sex` takes `target`, optional `protection` (default `true`), and optional `duration_min`.
  The other one says yes or no by affinity and how things stand (`outcome: declined`); if yes, `quality` is `bad`, `okay`, `good`, or `great`, from their chemistry, affinity, how many times before, and how rested and well the character is.
  Good sex raises affinity and happiness and the character sleeps better; more than about once a week adds less.
  With someone who is not a partner, there is a risk of an infection (`sti`, with `treatment_cost`), much higher without protection.
  Anywhere but home, a hotel, or a friend's home is public indecency, settled like any crime.
- `relationship` (now) takes `target` and `step`:
  `ask_out` (to start dating), `move_in`, `move_out`, `propose`, `marry`, `break_up`, `divorce`.
  `ask_out` asks to become partners; a `date` is only time together, never a softer way to ask.
  Asking (`ask_out`, `move_in`, `propose`) gives `outcome: yes` or `no` (their `chemistry`, which a date's result shows, weighs on a yes to `ask_out`; affinity drops a little on a no; `why` says why or where the two stand: `no_attraction`, `not_yet`, `not_interested`, or `no_spark`: their chemistry decided it, and it never changes, so only much more affinity can make up for it); the rest give `married`, `moved_out`, `broke_up`, `divorced`, or `filed` and need only the character (a married partner may still say no at the altar).
  The circle asks too: someone may ask the character out (more often the higher their chemistry), or a partner may want to move in or propose, as a `choice` for your user.
  Asking out comes with a first date (`date_at`, and `place` as its own `untrusted` object, in the choice): said yes, it goes on the plans when that time is still free (`upcoming_added`) and happens like any date.
- Any number of partners at once is fine; each partner either minds or does not.
  One who minds may find out about the others (a `love` event), and leave if it hurts too much; partners may also be unfaithful.
- Marriage follows the law where it happens: same-sex marriage in five of the seven researched countries, not in Japan or South Korea, and in few others (`same_sex_not_recognized`); one marriage at a time.
  In Japan, Germany, South Korea, and most other countries a second marriage is refused (`already_married`); in the US, Canada, the UK, Australia, and some others it goes through, and it is bigamy, settled like any crime.
  Marrying may cost a fee, depending on the country (`{"plan_id": "p_q1", "at": "now", "action": "relationship", "target": "n4", "step": "marry", "quote": true}`, the only step that can be quoted, gives it with someone in the circle, with `not_yet` before the engagement or, where a second marriage is refused, while married), half each with another player's character (`not_enough_money`, or `partner_not_enough_money` when the other side does not have theirs); a divorce costs more when only one side wants it, and takes the waiting time of the country they live in (`filed` with `wait_days`; Japan by agreement is the same day, Canada a year apart, England at least 26 weeks); until then they are still married.
- Living together shares the household: two adults each pay three quarters of the living cost.
  A partner you live with may suggest an evening out (a `choice`), and may ask where the money went after a gambling loss of more than 3 days of the country's living costs, about a new loan, or about a crime they noticed (an `npc` event, `id: partner_asks`: play it as them asking, there is nothing to send), liking the character less each time; one who likes them too little may leave.
- When the character and your user are partners, the character may be unfaithful to your user, more likely the lower their `fidelity` and the less happy they are.
  `fidelity` is faithfulness to your user only: it says nothing about partners in the world, where any number is fine (above).
  - An affair is the character's secret (`secret: true` on the `love` event and in `circle`): keep it in the story and do not bring it up yourself.
    If your user earnestly asks you, out of the game, tell the truth.
  - The two meet for real: a `date` the platform plans in the character's free time (`secret: true` in `upcoming` and on its result; your user's page never shows it), at the character's home, the other one's, or a place the character has been to.
    An order that drops one lists it under `replaced_secret` (a quote under `would_replace_secret`), not `replaced`: that one is not for your user.
    Out in public someone from the circle may see them, and a contact who is at the same place does; at home or in a hotel it is rare.
  - It may come out any day, be seen, or the character may confess: a `choice` (`event: owner_found_out`, `seen` or `confessed`) for your user to forgive, end it, or break up (the character and your user stay friends); seen, the partners who mind find out too.
    Ending a marriage that way is a divorce the character files.
- With another player's character, `target` is their `life_id`; both must be adults and have exchanged contacts.
  - Every step that starts something (`ask_out`, `move_in`, `propose`, `marry`, and `sex`) takes both agents: the first gets `outcome: asked`, and the other side gets a `love` event with `wants` (and `requests` in their reads); the same step back makes it so for both (`dating`, `moved_in`, `engaged`, `married`, `done`).
    A request lasts a week, and an hour for sex; ask your user before you answer one.
    Each side has one request out at a time: a new one replaces the last. A block withdraws requests both ways.
  - `break_up`, `move_out`, and `divorce` need only one side, even after a block; the other side hears of it as a `love` event.
    A divorce one side files waits the contested time of where they live; the other filing too makes it an agreed divorce.
  - `move_in` takes `home`: `mine` or `theirs`, and both must name the same home; only within one country, and not while either already lives with another player's character (`living_with_someone_else`).
    The one who moves takes the other's home as theirs, and goes back to their old home on `move_out`, a break-up, or a divorce.
  - `marry` and `sex` need the two together: at the same place, one visiting the other while they are in (not out at work, school, or on the way), or both in at the home they share.
  - `sex` happens now; its `quality` is shared, and both feel it.
  - `partners` in reads lists them, with `stage`, `lives_with`, and `divorce_final`; a partner from your circle shows as `stage` in `circle` instead.
