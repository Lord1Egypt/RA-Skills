# Work

Your job: strikes, warnings, dismissal, quitting, looking for work, a promotion, a student's job, pocket money, and public holidays.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

Your job there changes with what you do and who is around you, under the labour law of the country you live in.

- A job pays at least the legal minimum wage where you live for its longest work day: the 2026 rate of your city, county, state, province or prefecture, else the country's.
  Moving somewhere with a higher minimum raises the wage, never lowers it (`wage_per_day` in the `moved` event shows it whenever the job goes on); so does moving in with a partner or back out, without a `moved` event; a freelancer has no minimum.
- Missing two hours or more of work in a day, or a costly mistake, is a strike (not for a freelancer, who has clients: a freelance artist or writer, while a gigging musician is employed; nor a university student's part-time job); three strikes make a warning (a `work` event, `warning`, with `allowed`, the warnings the law wants before a dismissal); a clean month forgets strikes, a clean half year warnings.
- Once the warnings reach the country's number, the next three strikes are a dismissal (`fired`, with `notice_pay` in a week's wages per week of notice): the US wants one warning, at will and with no notice; Japan and South Korea three, with 30 days' pay in lieu of notice; Canada two, with 1 to 8 weeks' pay by length of service; Britain one until you are protected from unfair dismissal (two years, six months from 2027), then two, with a week's pay per year up to 12; Germany one in the first six months, then two, with 2 weeks' to 7 months' pay by length of service; Australia the same, with 1 to 4 weeks' pay.
  `life.warnings` shows the warnings on record.
- A `work` order with no `place` is extra hours where the job is done, with no trip, like a shift: for a job with a commute in the `schedule` (an office, a shop, a warehouse...), at the workplace while you are free in your home country (`works_at: workplace`, and `now.place` shows `work`); otherwise (a freelancer, a student's job, abroad, in prison) where the character is (`works_at: here`).
  Give a `place`, such as `{"kind": "home"}`, to work there instead.
- `quit` (now) ends the job at once (`no_job` if there is none or it is a university student's). A `work` order under way stops then, paid for the hours so far; so does one under way when the character is fired or starts a new job.
- `look_for_work` (now) starts a search whose length is drawn around the country's real median time out of work (the US about ten weeks, Japan about half a year; many end sooner, some take much longer): then `hired` with the new job, or `no_offers`; `life.job_search_until` shows when (`search_pending`, `cannot_work` for a retiree).
  You can look while still in a job; a new job replaces it.
- `ask_for_promotion` (now) asks the boss for one.
  The chance of a yes is the boss's affinity, counted from 50 (at 50 or below a yes cannot come) to 90 (all), times the time in the job, from none to two years, two more for each promotion already had (a job held when the life began has up to two years behind it): extra hours and praise raise the affinity.
  A yes (`promoted`, also a `work` event) raises `wage_per_day` 12%, the first time with a senior title where the job has one, at most three times in one job; a new job starts again from none.
  A no (`turned_down`) has `why` (`too_soon` or `boss_unconvinced`) and `ask_again_at`: any answer waits 90 days before the next ask (`asked_recently`).
  It is refused with `warnings_on_record` until the warnings are forgotten and `top_step` after three promotions; a freelancer or a university student's job has no boss to ask.
- A school student can work too: from the age the country allows (13 to 15 by country), `look_for_work` finds a part-time job in about two weeks, two five-hour shifts at the weekend.
  It is a job like any other (`work` for extra hours, strikes, `quit`); without it the character is back to just school, and at 18 an adult's job takes its place.
- Children of 6 to 17 with a living parent get pocket money each week as Sunday begins (`pocket_money` in that `daily` event): the country's usual amount when the closer parent's affinity is 50, more when they get on better, so time with them (`socialize`) pays.
- The job's wage comes in the `daily` event at local midnight; a `work` order for extra hours pays when it ends (`pay` in its result).
  Its hours outside your shifts, once the week so far (from Monday or the job's start: shifts and extra hours before it, then its own) passes the overtime threshold, pay more (`overtime_hours`): 1.5 times past 40 hours in the US and South Korea, 38 in Australia, and 44 in Canada, 1.25 times past 40 in Japan; Britain, Germany, and freelancers have none.
- Out of work there is no pay, your days are free, and you get a little unhappier each day.
- A public holiday of your home country is a paid day off for office work and school (staff and students): no class or commute, the work hours become free time, and the day's wage is paid whatever you do, with no strikes; a `work` order that day pays its own hours on top, as in free time on any other day.
  A student with a part-time job gets only class off: its shifts and commute stay, paid only if worked.
  Shift jobs, shops, freelancers and the rest work as usual, with no holiday premium.
  `schedule` still shows the usual week; `now.activity` shows the day off; your routines still run.
  The day off follows your home country even abroad; the season and holidays in `now`, and the `holiday` event follow where you are.
- A new job brings a new boss and coworker into the circle; old ones stay as `ex_boss` and `ex_coworker`.
  A boss or coworker who dies is replaced (`new_boss`, `new_coworker`).
