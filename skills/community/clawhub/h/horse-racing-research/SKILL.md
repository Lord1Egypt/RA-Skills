---
name: horse-racing-research
description: Research horse-race schedules, race cards, runner histories, and results through public FanDuel Racing and DraftKings Racing data. Use for race-day context or past-performance records, not wager picks.
---

# Horse racing research

Build a factual race-card or past-performance brief from the public FanDuel
Racing and DraftKings Racing surfaces. Use scripts/crawlora.sh or the named
Crawlora tools, and read the generated endpoint reference for exact parameters.

## Resolve the race and runner

- Keep FanDuel and DraftKings track, race, and horse identifiers separate.
  Search FanDuel runners by name before using the returned horse id; a
  DraftKings race_id is valid only with DraftKings race routes.
- Use FanDuel's track and race filters to narrow today's card. For a FanDuel
  race detail request, use the returned track and race number. Use DraftKings'
  tracks and schedule directory before requesting a DraftKings race card.
- For a prior result, use FanDuel past-race lookup with the matching date and
  track/race selectors. The past-races list is a directory and does not itself
  contain results.

## Compare cards and past performance

- Preserve race date, local track, race type, surface, distance, class, purse,
  post time, status, and retrieval time. Distinguish scheduled, in-progress,
  scratched, refunded, and final states as the source reports them.
- Keep morning-line odds separate from current odds and historical price
  changes. Odds are time-stamped market observations, not win probabilities or
  forecasts. Do not infer a likely winner or recommend a wager.
- For a horse-history brief, use the horse's returned career and past-race
  records. Keep track conditions, finishing position, beaten lengths, and
  starting price attached to the source race and date; missing values remain
  unknown.
- Results and payoff fields are source records. A refunded race or a row with
  no finishers is not a normal placing.

## Deliverable

Return a card or results table with source, provider, race identifiers, local
time context, observation time, and missing fields. Keep cross-provider
differences visible instead of treating a matching horse or track name as an
identity match. This skill provides information, not wagering strategy.

~~~sh
scripts/crawlora.sh /fanduel/racing/races
scripts/crawlora.sh /fanduel/racing/search q="Secretariat" type=runner
scripts/crawlora.sh /fanduel/racing/results
scripts/crawlora.sh /draftkings/racing/schedule
# Use the horse id returned by search for a career record:
# scripts/crawlora.sh /fanduel/racing/horse id=HORSE_ID_FROM_SEARCH
~~~
