# Review — Weekly To Annual

Scope: the scheduled reread. This is where a journal stops being a write-only archive and starts paying for itself.

**Contents:** [Rules That Apply To Every Review](#rules-that-apply-to-every-review) · [Weekly](#weekly) · [Monthly](#monthly) · [Quarterly](#quarterly) · [Annual](#annual) · [On This Day](#on-this-day) · [Reviewing Someone Else's Cadence](#reviewing-someone-elses-cadence) · [When A Review Finds Nothing](#when-a-review-finds-nothing)

**Before any review**, read `## Due` in `~/Clawic/data/journal/memory.md` for what is overdue, `## Open Threads` for what the last review left hanging, and the previous review in `reviews/<year>.md`. A review that does not reference the last one produces the same three observations every month. Reading the window's entries is in scope for the review the user asked for, whatever `agent_read_scope` says about idle browsing — but exclude anything in `## Read Scope`, `no_go_file`, or a never-reread practice (`practices.md`).

## Rules That Apply To Every Review

1. **Fixed question set per cadence.** Improvised questions produce a different review every time and nothing comparable across periods.
2. **Count before you conclude.** Every claim carries its numbers: entries in the window, days covered, how many mention the theme. Rule 7's bar decides whether a count becomes a pattern.
3. **The output is short and it is written down.** A review that lives only in the chat is a review that never gets referenced, which means the next one repeats it. It goes to `reviews/<year>.md`.
4. **One carry-forward, maximum three.** A review that produces nine intentions produces zero. The carry-forward goes to `## Open Threads` and gets checked at the next review by name.
5. **Do not moralize the numbers.** "Three entries this week" is a fact. Whether that is a problem is the user's call, and a nudge in a review is still a nudge (`consistency.md`).
6. **Excluded material stays excluded.** Morning pages, expressive-writing days, grief entries, and anything in `## Read Scope` are not review inputs unless the user says otherwise, and their absence is stated in one line so a partial review is never presented as a complete one.

## Weekly

The highest-value cadence and the only one most people sustain. 15-25 minutes.

**Inputs**: the week's entries, interstitials, mood ratings if any, and last week's carry-forward.

**Question set**, in order:

1. What actually happened this week? (Facts before interpretation — otherwise the loudest day writes the whole review.)
2. What took more energy than it should have?
3. What went better than expected, and what did I do that caused it?
4. What did I avoid all week?
5. What is still open from last week's carry-forward, by name?
6. What is the one thing to carry into next week?

**Output**, appended under `## <YYYY-Www>` in `reviews/<year>.md`:

- Entries: `n` across `d` days.
- Themes with counts (`work: 4, sleep: 3`).
- The avoided thing, named.
- One carry-forward.
- Anything that crossed Rule 7's bar this week, with the entry dates.

If the week has fewer than three entries, run the review anyway on what exists and say so. A thin week is a data point about the week, and skipping the review is how the cadence dies.

## Monthly

30-45 minutes, and a different job from the weekly: the weekly asks what happened, the monthly asks what is repeating.

**Inputs**: the four or five weekly reviews first, then entries only where a weekly flagged something. Reading a month of entries linearly produces recency bias and takes four times as long.

**Question set**:

1. Which themes appeared in three or more weeks? (These are the patterns; a theme in one week was that week.)
2. What did I say I would carry forward, and did any of it happen?
3. What changed in how I write — length, frequency, slot, tone?
4. What decision did I make this month, and is its review date scheduled? (`practices.md`)
5. What is genuinely different from last month, and what only felt different?
6. What am I still tolerating? (Same answer three months running is the finding.)

**Output**, under `## <YYYY-MM>` in `reviews/<year>.md`: entry count and days covered, themes with week-spread, carry-forward outcomes (done / dropped / still open), mood summary if the paired-day minimum is met (Rule 8), and one carry-forward.

Bullet-journal users run the monthly migration in the same session (`practices.md`) — the two are the same act of deciding what survives.

## Quarterly

Exists for two things the monthly cannot do:

- **Decision reviews.** Every entry in `decisions/<year>.md` whose review date has passed gets scored: prediction right / wrong / unclear, and confidence against outcome. Read the entry before recalling what happened. Calibration becomes readable at roughly 20 reviewed decisions.
- **Direction.** Is the work, the relationship, the health situation in the same place as three months ago? A quarter is the shortest window in which "nothing is changing" is a valid finding rather than impatience.

Also: prune the tag vocabulary (`storage.md`), check the backup restored at least once (`storage.md`), and confirm the `## Due` table matches reality.

Output under `## <YYYY>-Q<n>` in `reviews/<year>.md`, including a decision-scoring table.

## Annual

The long one. 2-3 hours, and it is worth the whole year of writing.

**Inputs**: the twelve monthly reviews, the four quarterlies, and only then a targeted pass at entries the monthlies flagged.

**Question set**:

1. What closed this year? (Endings first — people default to a highlight reel and miss the endings entirely.)
2. What carried over from last year, unchanged?
3. What did I believe in January that I no longer believe?
4. What did I do for the first time?
5. Who was in this year that was not in the last one, and who left?
6. What did the hardest month teach me, and does it still hold?
7. What would the January version of me not believe about today?
8. What is the one sentence for this year?
9. What is the theme for next year — a direction, not a resolution list?

**Output**: `artifacts/annual-review-<year>.md`, its own file, because it is read whole and re-read in future years. Its `## Boxes` line goes in the same turn. The one-sentence summary and the next-year theme also go into `reviews/<year>.md` under `## <YYYY> Annual` so the yearly file stays a complete index of the year's reviews.

Do not run an annual review in the last week of a hard December. It becomes an indictment. Mid-January is a better date and there is no rule that says otherwise.

## On This Day

Resurfacing an entry from one, three, or five years ago on the same date.

- **Opt-in only**, separate from `nudge`, because it can surface a death, a breakup, or a diagnosis with no warning.
- Exclude anything in `## Read Scope` or `no_go_file`, and exclude the grief corpus unless the user explicitly included it.
- Deliver it as the entry's opening line and its date, never as a summary. The user decides whether to open it.
- Its real value is calibration: last year's crisis, read today, recalibrates today's crisis better than any reframe you could write.

## Reviewing Someone Else's Cadence

When `review_cadence` is `none` and the user asks for "a review" anyway, ask nothing — pick the window from what exists: a week if they wrote this week, a month if the entries are sparse, the whole corpus if there are fewer than 20 entries. State the window you chose in one line.

## When A Review Finds Nothing

It happens, and it is a legitimate output. Say it in one sentence, record it with its entry count under the period heading in `reviews/<year>.md` — a review that found nothing still has to be there, or the next one repeats the search — and stop. Do not manufacture a theme from two mentions to make the review feel productive — a fabricated pattern gets acted on, and the next review inherits it as a premise (Rule 7).

**Write in the same turn:** every review to `reviews/<year>.md` under its period heading; the annual review to `artifacts/annual-review-<year>.md` with its `## Boxes` line; carry-forwards to `## Open Threads` in `memory.md`, and close the ones resolved; themes that cleared Rule 7's bar to `## Themes`; decision scores back into `decisions/<year>.md`; the review's run date into `## Due` so the next one has a next-due date. Formats: `memory-template.md`.
