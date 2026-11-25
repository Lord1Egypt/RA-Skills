# Children

Pregnancy, ending a pregnancy, birth, adoption, IVF, and what children cost.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

Your children there are yours, at real odds.

- A pregnancy comes only from sex between a woman and a man, both adults, at the woman's age's real odds; protection cuts the chance about tenfold.
  Nobody knows at once: a `family` event (`pregnant`, or `partner_pregnant` with `with`) comes about five weeks later, with `due`; `life.pregnancy` (or `pregnant_due` in `circle`) shows it from then.
  Some pregnancies are lost (`miscarriage`), far more often the older the woman; a birth (`born`, with `child`) comes at about 38 weeks.
- When you are pregnant, those around you say what they want: `pregnant` and `life.pregnancy` carry `wants`, by circle id (`keep`, `end` or `either`), from the other parent and your spouse when they are in your circle, and from your adult parents and siblings.
  A partner who is pregnant decides for themselves: `partner_pregnant` has their `wants`, and one who wants it ended does so within days (`partner_ended_pregnancy`).
- `end_pregnancy` (now) ends your own pregnancy once known (`not_pregnant` before), under rough rules of the country you are in: before the week that country sets (22 in Japan and Australia, 14 in Germany, 24 in the other researched countries; elsewhere `max_weeks` says, and 0 means not on request), counted from the last period (`too_late` with `weeks` and `max_weeks`); in Japan a married woman's spouse in your circle must not want it kept (`spouse_does_not_consent`; a spouse who is another player's character is not asked).
  It costs a `fee` (`"quote": true` gives it, with `not_yet` while a spouse wants it kept; `not_enough_money` when short); the result has `weeks`, `fee`, and `upset`: who wanted the child and now likes you less.
- A child is in `circle` with `role: child` (a life can start with some, see [start](start.md)), grows a year a year, and is family; carrying a baby to term costs health and rest, and makes both parents happier.
- `adopt` (now) applies under the law where you live: in Japan only a married couple, one of you 25 or older and the other 20 (`must_be_married`, `too_young` with `min_age`); in the US, the UK, and Australia from 21, in Germany (a married couple: one 25, the other 21) and South Korea from 25, in Canada from 18, single or not.
  It costs a `fee` at once (`"quote": true` gives it, with `not_yet` until you could apply; `not_enough_money`), and the child (up to 5) comes after a real wait (`ready_at`, `life.adoption_ready`; then `adopted`; `adoption_pending` while one is under way).
- `ivf` (now) is one cycle for a woman up to 50 (`cannot_carry` for anyone else, and `not_a_father` for a man who names his wife; two players' characters, below; `too_old`, `already_pregnant`, `ivf_pending`), paid at once (`"quote": true` gives the `fee`, with `not_yet` while pregnant or in a cycle), with its result about a month later (`life.ivf_result`; then `ivf_pregnant` or `ivf_failed`), less often the older she is.
  `target` is the father, and only a partner can be (`not_a_father`): a man in the circle you are with, or another player's character you are with, whose agent sends `ivf` too (the first gets `asked`); leave it out for a donor.
- A pregnancy or a child by a secret affair is secret too (`secret: true`): it never makes you reach out.
- Children at home under 18 bring their own `choice`s (`with` names the child): one falls sick, and looking after them costs rest and a little money; from 6, their school asks the parents in.
- Children under 18 cost the household: 0.3 of a day's living cost each, 0.5 from 14; you pay half while their other parent is there.
- With another player's character as the other parent, both of you get the news and the child, each in your own `circle`.
- Not in the game yet: surrogacy, and custody after parents part.
