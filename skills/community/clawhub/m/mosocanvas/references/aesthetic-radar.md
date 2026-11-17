# Aesthetic radar

The radar is an evidence pipeline, not a feed of fashionable images. Run it separately from live
direction work; the skill consumes a dated snapshot.

## Daily collection contract

Run one scheduled collection per local calendar day when fresh trend input is required:

1. query the declared design/aesthetic scope across at least three source classes;
2. capture raw URLs, project/creator identity, timestamps, and visible evidence;
3. normalize recurring mechanisms without saving copyrighted imagery into the skill;
4. compare with the previous seven snapshots for velocity, recurrence, and saturation;
5. have a reviewer reject literal copies, weak attribution, and single-source conclusions;
6. write an immutable dated snapshot and validate it with `scripts/trend_validate.py`;
7. keep the last valid snapshot when collection fails, but mark it stale after expiry.

The collector and reviewer must be separate passes. A collector may propose a signal but may not
assign final confidence to its own finding.

The accepted snapshot uses `moso.trend-snapshot/0.2`. It must bind the collector and reviewer to
different identities and context IDs. Cover at least three source classes, not merely three URLs:
curated showcases, practitioner portfolios, editorial/trend reports, community engagement surfaces,
or model galleries. Do not count mirrors, reposts, the same creator, or multiple pages on one domain
as independent corroboration for a signal.

## Preserve native ideation

Create zero-reference directions before opening the snapshot. Trend exposure can anchor choices and
reduce structural variety. After ideation, use the radar to:

- detect saturated visual tropes;
- find emerging mechanisms relevant to the carrier;
- test whether a direction feels current for a documented reason;
- identify mechanisms to avoid or deliberately counter.

## Record signals

Every signal needs:

- source URL and platform;
- captured and observed timestamps;
- creator/project attribution;
- available engagement or curation evidence;
- recurring visual mechanism, not only a style label;
- carrier and audience relevance;
- rights/use status;
- confidence and expiry date.

Any `falling`, `stable`, `rising`, or `spiking` velocity claim requires at least two dated prior
snapshot references inside the seven-day baseline plus a written comparison. With insufficient
history, record `unknown`; never infer velocity from one day's engagement count.

Track independent dimensions:

- **velocity:** recent change in attention;
- **curation:** editorial or professional selection;
- **recurrence:** appearance across independent creators/sources;
- **novelty:** distance from the recent baseline;
- **relevance:** fit to task, audience, and carrier;
- **saturation risk:** likelihood of reading as a template.

Do not collapse these into one “hotness” score.

## Source policy

Use multiple source types where available: juried/curated showcases, practitioner portfolios,
platform trend reports, and observable repeated mechanisms. A single viral post is weak evidence.
Respect access terms and record missing metrics rather than inventing them.

## Freshness

- Mark a snapshot stale after its declared expiry.
- Prefer a 24-hour expiry for daily monitoring; use a shorter expiry during unusually fast-moving
  launch cycles.
- Never call a historical trend “today's hottest” without a current capture.
- Keep the snapshot immutable after use; write a new version for the next collection.
- State when live browsing or source access was unavailable.

Validate snapshots against [../schemas/trend-snapshot.schema.json](../schemas/trend-snapshot.schema.json).
