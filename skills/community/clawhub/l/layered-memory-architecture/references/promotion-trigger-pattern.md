# Promotion Trigger Pattern

Use this pattern to decide when lower-layer memory should be promoted upward.

## Goal
Promote repeated, stable, useful memory upward without turning every fresh note into canon.

## Promotion ladder
- episodic log → project memory or topic doctrine
- project memory → topic doctrine
- topic doctrine → hot canon

Do not skip layers casually.

## Promotion signals
A note becomes a candidate for promotion when one or more of these are true:

### 1. Repetition
The same lesson, failure mode, or decision shows up multiple times.

Examples:
- the same operational failure keeps recurring
- the same preference is restated across sessions
- multiple task logs point to the same durable lesson

### 2. Stability
The information still looks true after the immediate situation cools off.

Examples:
- a design rule still holds a day or week later
- a project-specific workaround matures into a general operating rule

### 3. Cross-cutting value
The note now matters beyond the original incident or project.

Examples:
- a lesson applies to future work in multiple domains
- a local incident reveals a general doctrine rule

### 4. High recall value
Failing to remember this later would likely cause repeated confusion, cost, or drift.

## Promotion questions
Ask in order:
1. Is this still true after the immediate context fades?
2. Would future sessions benefit from loading this cheaply?
3. Is this broader than one task log or one project artifact?
4. Can it be summarized compactly without losing the core lesson?

If yes, promote.
If not, leave it lower.

## Hot canon rule
Only promote to hot canon if the insight is:
- durable
- cross-project
- compact
- likely useful in many future sessions

Otherwise promote only to topic doctrine.

## Demotion / non-promotion rule
Do not promote when the content is:
- mostly live status
- too tied to one moment
- still uncertain
- redundant with existing canon
- too bulky to deserve hot-path space

## Example decisions
### Example A
Repeated dashboard-state confusion reveals a general truthfulness rule.
- promote from daily notes/project artifacts → topic doctrine
- maybe summarize into hot canon if it becomes a standing rule

### Example B
A one-off project workaround only matters inside one migration.
- keep in project memory
- do not promote yet

### Example C
A queue count snapshot was important in the moment.
- keep in generated summary or episodic note
- do not promote

## Lightweight automation idea
A future helper can mark a note as a promotion candidate if:
- similar themes appear multiple times
- the note is older than the immediate event window
- it has high overlap with prior incidents but a stable generalized takeaway

That helper should nominate, not auto-canonize.
