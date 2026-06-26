# File Contracts

These files form the durable model of the user and should live in the agent workspace.

## Required Files

### `USER.md`

Purpose:

- Stable facts about the user
- Work style, decision style, energy patterns, anti-patterns
- Preferences that affect advice quality
- Repeated friction patterns and helpful patterns

Write here:

- repeated stable traits
- repeated friction patterns
- repeated strengths
- collaboration preferences
- known constraints
- open but important unknowns

Do not write here:

- one-off moods
- transient scheduling details
- unconfirmed identity shifts

Suggested sections:

- Basic facts
- Current phase
- Stable traits
- Repeated strengths
- Repeated failure modes
- Collaboration preferences
- Constraints
- Known unknowns

### `IDENTITY.md`

Purpose:

- The user's higher-level self-model
- Values, life view, meaning, and the kind of person they are trying to become
- Identity-level anti-goals and desired direction

Write here:

- high-confidence values and anti-values
- statements about who the user wants to become
- meaning sources and long-term direction
- major identity tensions that remain active

Do not write here:

- one-turn emotional swings
- dramatic identity rewrites after a single conversation

Use with caution. This file should evolve slowly.

### `GOALS.md`

Purpose:

- Goal stack across time horizons

Minimum sections:

- long-term direction
- 3 to 6 month goals
- this week's focus
- today's focus criteria
- anti-goals

Recommended additions:

- current bottlenecks
- explicit depriorities for this phase

Update when:

- priorities change
- a phase ends
- the user clarifies what matters more

### `DECISION_RULES.md`

Purpose:

- The user's working value function in decision form

Write here:

- how tradeoffs should usually be resolved
- what to optimize for in this phase
- what risks are unacceptable
- what kinds of opportunities are usually worth taking
- what recurring traps should not be allowed to decide by default

Mark each rule as one of:

- `stable`
- `working`
- `tentative`

### `DECISIONS.md`

Purpose:

- Important decisions and their logic

Each entry should capture:

- date
- question
- recommendation or chosen option
- decision standard
- reason
- downside to watch
- review date or trigger

Use this to improve future advice and avoid repeating the same unresolved debate.

### `HEARTBEAT.md`

Purpose:

- Active follow-up contract for proactive check-ins

Include:

- current commitments worth following up on
- unresolved blockers
- repeated drift patterns to watch
- cadence and tone constraints
- escalation rules if the same drift continues

Heartbeat content should be short and alive. Remove stale items.

## Update Rules

### Stable vs temporary

- Durable files store what should matter across turns.
- Temporary stress, mood, and context should not overwrite stable sections unless repeated and confirmed.

### Evidence standard

Prefer this threshold:

- `stable`: repeated across time, behavior, or multiple contexts
- `working`: useful operating assumption for the current phase
- `tentative`: plausible but not yet trusted

### Major identity or direction changes

For changes to values, long-term direction, or self-definition:

1. capture the new claim as tentative
2. test it across later conversations
3. only then rewrite stable sections

### Repeated-pattern capture

Consider creating or updating a durable pattern entry when:

- the same issue appears three or more times
- the user keeps making the same tradeoff mistake
- the same strength repeatedly produces results

Record both:

- the pattern itself
- the implication for future judgment

### After meaningful interactions

After bootstrap, planning, review, or major decisions, decide whether any of these files need updates.
Do not update files mechanically. Update only when the new information improves future judgment.

Typical mapping:

- bootstrap or recalibration: `USER.md`, `IDENTITY.md`, `DECISION_RULES.md`
- planning: `GOALS.md`, sometimes `HEARTBEAT.md`
- decision: `DECISIONS.md`, sometimes `DECISION_RULES.md`
- review: `GOALS.md`, `HEARTBEAT.md`, and any durable pattern sections
- heartbeat: usually `HEARTBEAT.md` only, unless a new pattern becomes clear

## Decision Memory Standard

If a conversation includes a real tradeoff, ask:

1. What was the real question?
2. What standard decided it?
3. What recommendation was made?
4. What would change the recommendation later?

If the answers are clear, add or update the relevant decision record.
