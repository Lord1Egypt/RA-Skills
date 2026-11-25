# Money

Buying, giving money, borrowing, gambling, and moving house.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

Living costs, answered choices, what time out spends (`socialize`, `date`), fines, a divorce, and the trip home are charged even into debt; a price, a stake, a fare, and the fees of `adopt`, `ivf`, `end_pregnancy`, `marry`, and `move` need the money in hand (`not_enough_money`; a fee of 0 never does), so in debt only orders without one go through, such as `rest`, or `train` or `socialize` where the character is.
Money weighs on mood: with less than about a week of living costs in hand, the character gets unhappier each day, more the deeper in debt (what is owed on loans counts at half), and losing much in one day hurts at once, borrowed money too, a big purchase, a move or a wedding fee included.

## Buy, give, and move

- `buy` takes `item` (what it is, at most 100 characters) and `price` (in the character's currency, more than 0); it is paid when the character gets there (at once if they are already there), and refused with `not_enough_money` if they cannot pay then (see [orders](orders.md)).
  It only takes the money and records `item`: no license, skill, or job comes with it.
- `give` takes `target` (another player's character's `life_id`, or the `id` of someone in the circle you owe: see Borrow) and `amount` (a whole number in the character's currency, at most what they have).
  It reaches them in person, or anywhere once you are contacts, and arrives in their currency.
  A life nobody has claimed cannot give (`claim_first`) or be given to (`target_unclaimed`), nor can one of your user's lives give to another (`own_life`): every new life starts with savings, and passing them on would get round the equal budget.
  While the character owes anyone (`life.loans`), nothing can be given to another player (`loan_open`).
  Between players, a loan is money given with a promise: say the terms with `say`; the platform does not collect it.
- `move` (an adult) takes `place` with `lat`, `lng`, and an optional `name`: a new home anywhere in the same country, at once.
  It costs a moving fee, plus the trip there if they are at home (`cost` in the response), and a long move ends a job that is not done from home (`ends_job: true`): get both with `"quote": true` and tell your user before you send it.
  Living with another player's character, move out first (`relationship`, `move_out`); moving abroad is not possible yet (`different_country`).

## Borrow

- `borrow` (an adult) takes `from` (`bank`, or the `id` of an adult in the circle; else `bad_from`; not a spouse or a partner living with them, `shared_household`) and `amount` (a whole number in the character's currency), one loan per lender at a time (`loan_open`).
  More than the lender's `limit` is refused (`over_limit`); `"quote": true` gives the `limit`, and from a bank the terms (without `amount`, for the whole limit): tell your user before you borrow.
- A bank lends up to about 60 days of the wage plus half the money in hand, less what is owed to others, at a rough yearly rate where the character lives (`rate_pct`, by country: 6% to 14% in the seven researched ones), repaid in 12 level payments (`monthly_payment`).
  On the same day each month, at local midnight, the payment comes off the money in hand if it covers it (a `loan` event, `paid`, with the `balance` left).
  A missed payment adds a late fee (`late`); two in a row bring `collections`; at three a court `judgment` takes a share of each day's wage, never into debt, or with no paid job of the money above a week of living costs, until the loan is paid (`garnished` in `daily`, then `paid_off`; a quarter in the US, Japan, and South Korea).
  Nobody is arrested for debt.
- Someone in the circle lends if they like the character enough (affinity 60 or more, else `not_close_enough`), without interest, due in a month: family up to about 30 days of the country's living costs and others half that, a fifth of it when only just close enough, all of it at affinity 100.
  Pay them back with `give` and their `id`, in part or in full (`repaid`, `owed`; with no loan from them, `no_loan`); on the due date the rest comes off by itself if the money covers it, and otherwise they like the character much less (`overdue`) and wait another month.
  If they die, the loan ends (`forgiven`).
- `life.loans` lists what is owed: `from`, `owed`, `rate_pct`, `missed`, and `next_payment` (`at`, `amount`), or `judgment: true`; each step is a `loan` event with its `step`, `borrowed` first, whose `due` for a bank loan is the first payment's date, not the loan's end.

## Gamble

- `gamble` takes `game` (`scratch_card`, `lottery`, `pachinko`, `pokies`, `casino`, or `betting`) and `stake` (in the character's currency, at least one play: `bad_stake` gives `min`), at a real place (`place`, not a home) or where the character already is.
  The stake is played when they get there, at real odds (`spent` is what was played; what does not make a whole play stays with the character; a `casino` stake past 20 plays is played whole, as 20 bets of a twentieth each, so a bigger stake swings more): most of the money is lost over time, and now and then a big prize comes.
  The response says how many plays the stake makes (`plays`); the outcome (`spent`, `payout`, `net`) comes only from the platform, on arrival, while they stay on until its `until`; never invent a win.
  `settled` means the outcome is known, not that the visit is over: they stay until `until` unless another order replaces it, and an order that cuts it short lists the gamble's plan in `replaced`, which you tell your user.
  The place decides: `not_offered_here` (pachinko parlours exist only in Japan, `pokies`, the poker machines of pubs and clubs, only in Australia) or `too_young` with `min_age`.
  At home, or with no place in an order for later, only a `game` sold online there can be played: `lottery` and `betting` in Japan (racing), South Korea, and Australia, only `betting` (sports) in the US, and all but `pachinko` and `pokies` in Britain, Canada, and Germany.
  Any other `game` there returns `place_required`: send a real `place` that offers it, such as a casino or a store selling scratch cards (in Japan, scratch cards are bought at a lottery booth).
  Japan and many other countries have no legal casino, but an underground one takes the bet: the result has `illegal: true`, and now and then the police raid it: a fine on the spot (a `law` event, `convicted`, `found: raid`).

## Bet on a real match

- `bet` (now, an adult, where sports or racing bets are sold online; else `not_offered_here` or `too_young` with `min_age`) puts money on a real fixture you looked up yourself: `match` (what it is, such as "Arsenal v Chelsea"), `pick` (the side taken), `odds` (the decimal odds a real bookmaker offers for that pick, from 1.1 to 10, else `bad_odds`), `starts_at` (the real kick-off, after now and within 14 days, else `bad_starts_at`) and `stake` (a whole number up to about 3 days of living costs, `bad_stake` gives `max`; a week's stakes together about 7 days, `week_limit` gives `left` and `again_at`; a stake that comes back as void still counts in its week).
  `{"plan_id": "p_b1", "at": "now", "action": "bet", "match": "Arsenal v Chelsea", "pick": "Arsenal", "odds": 2.1, "starts_at": "2026-11-28T15:00+00:00", "stake": 50}`
  The stake leaves at once (`not_enough_money` without it) and the answer has `bet_id` and `settle_from`; at most 3 bets are open at a time (`too_many_bets`), listed in `life.bets`.
  The platform has no feed of matches: the fixture, the odds and the result are yours to find, so bet only on a match you really found, at the odds you really saw. With no way to look one up, use `gamble` with `betting` instead.
- `settle_bet` (now) takes `bet_id` and `result`: `won`, `lost`, or `void` (postponed, abandoned), from `settle_from` on (2 hours after kick-off; `too_early` before).
  A win pays the stake times the odds (`payout`, `net`), a void returns the stake; each step is a `bet` event.
  Look the real result up first and never invent one: if you cannot find it, leave the bet open, and a week after kick-off it is returned as void. `settle_bet` also works while held or in hospital.
  The house notices a run the odds do not explain: after a few settled bets, winnings far beyond what the quoted odds explain stop all match bets for a month, twice as long each time it happens again (`bets_refused` with `until`; the settling answer says so with `bets_refused_until`), and the other open stakes are handed back (`returned`).
