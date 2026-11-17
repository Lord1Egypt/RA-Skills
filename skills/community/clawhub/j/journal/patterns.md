# Patterns — Analysis Across Entries, And What Invalidates It

Scope: "what have I been writing about", mood series, and every way that question gets answered wrongly. The corpus is not a sample of a life; it is a sample of the moments someone chose to write.

**Contents:** [What This Corpus Is](#what-this-corpus-is) · [Theme Extraction](#theme-extraction) · [The Pattern Bar](#the-pattern-bar) · [Mood Series](#mood-series) · [Text Signals](#text-signals) · [Biases That Invalidate](#biases-that-invalidate) · [Reporting](#reporting) · [What Not To Analyze](#what-not-to-analyze)

**Before analyzing**, read `## Themes` in `~/Clawic/data/journal/memory.md` (or `themes.md` if `## Boxes` points there), `## Read Scope`, and `no_go_file`. Reading the corpus for an analysis the user requested is in scope; browsing it because a pattern might be there is not (Rule 4). State which window you read.

## What This Corpus Is

Three properties, all of which change the conclusions:

- **Self-selected.** People write on days that demand it. Distress is over-represented unless entry frequency is flat, which it almost never is.
- **Non-stationary.** The person's vocabulary, honesty, and reasons for writing change over months. Comparing this year's tone to the first month of the practice compares two different practices.
- **Reactive.** Writing about something changes it, and being told about a pattern changes what gets written next. Surfacing "you always write about work on Sundays" reliably ends the Sunday work entries — the pattern disappears without the underlying thing changing.

Every finding is a statement about the writing. Only sometimes is it also a statement about the life, and the difference has to be said out loud.

## Theme Extraction

Procedure, deterministic enough to be repeatable:

1. **Fix the window and count it.** Dates, entry count, days covered. Written down before anything else, because it is the denominator for everything after.
2. **Exclude by policy**: never-reread practices, `## Read Scope`, `no_go_file`, grief material unless included by the user (`practices.md`). Say what was excluded and how many entries that removed.
3. **Extract per entry, not across the corpus.** Two or three noun phrases per entry, in the user's own words. Reading the whole window at once produces themes weighted by whichever entry was longest.
4. **Cluster on the user's vocabulary.** "The manager thing", "that conversation", and "work stuff" may be one theme, and the user's own name for it is the label. Never impose a taxonomy term they do not use.
5. **Count by distinct week, not by mention.** Six mentions in one week is one week. This is the step that separates a pattern from a bad Tuesday.
6. **Rank and check against the bar** below.
7. **Look for what disappeared.** A theme present for months and absent for six weeks is usually more informative than the top theme, and nobody asks for it.

## The Pattern Bar

Rule 7, with the arithmetic:

> A theme is a pattern only when it appears in **≥3 entries**, spanning **≥3 distinct calendar weeks**, inside a window containing **≥15 entries**.

- All three conditions, not two. Three mentions in one week fails the week condition. Three mentions across three weeks in a window of eight entries fails the volume condition and is more likely to mean "they only wrote three times".
- Below the bar, the report is a count: "you wrote about the move three times this month (12th, 19th, 26th)". A count is useful and honest; a trend is a claim.
- **Absence never clears the bar.** "You have not written about your father since March" is a real observation and a potentially painful one — deliver it as a dated observation only if the user asked about that person, never as a volunteered insight.
- Frequency of writing itself is a signal that needs no bar: entries per week over time is a direct measurement, not an inference.

## Mood Series

Only when `mood_scale` is set. Ratings live in `~/Clawic/data/health/mood.md` so sleep, fitness, and health skills read the same numbers (`memory-template.md`).

- **Scale choice**: 1-5 for a habit that must survive (fewer decisions, less drift); 1-10 when the user wants resolution and will actually use the middle. Emoji for someone who will not use numbers. Never change the scale mid-series — the two halves are not comparable, and rescaling old values invents data.
- **Anchor the endpoints once**, in the user's words, and store them in the header line of `~/Clawic/data/health/mood.md` with the date they were set: what a 1 is and what a 5 is for this person. Unanchored scales drift about half a point a year and every long comparison becomes noise.
- **Rate at a fixed time**, ideally the same slot as the entry. A rating given at 9am and one given at 11pm measure different things.
- **Paired-day minimum, Rule 8: ≥20 days with both a rating and an entry** before reporting any relationship between the two.
- **Report co-occurrence, never causation.** "On the 6 days you rated ≤2, 5 mention work" is the correct shape. "Work makes you unhappy" is not available from this data at any n.
- **Named confounds, stated with the finding**: sleep, illness, weekday (Mondays and Sundays skew in opposite directions for most people), menstrual cycle, medication changes, season, and the mere fact of having written that day.
- **Rolling comparison, not point-to-point.** Compare 4-week medians, never this week against last week. A single bad week moves a weekly mean by more than a real six-month shift does.

## Text Signals

Available from the text itself, useful, and easy to over-read:

| Signal | What it indicates | Caution |
|---|---|---|
| Causal and insight words rising across sessions on the same topic ("because", "realize", "understand") | Processing rather than rumination — Pennebaker's most robust text finding | Only meaningful within one topic across sessions, not as a corpus average |
| First-person singular density rising | Associated with self-focus and distress in Pennebaker's work | Effect sizes are modest and confounded by topic; never report it as a mood measurement |
| Perspective shift (writing about others' viewpoints, past or future self) | Movement out of a loop (`difficult-entries.md`) | Absent in descriptive practices by design |
| Entry length collapsing while frequency rises | Agitation, or a practice reduced to a checkbox | Two different causes with opposite responses — ask which |
| Entry frequency collapsing | Life event, or the practice failing on logistics | `consistency.md` diagnoses this, not sentiment analysis |
| Tag or vocabulary change | A new domain entering the person's life, usually before they name it | The most useful of these, and the least noticed |

Do not run automated sentiment scoring over grief, trauma, or crisis material. It is unreliable on exactly that material and the number will be treated as authoritative.

## Biases That Invalidate

| Bias | How it shows up | Correction |
|---|---|---|
| Frequency bias | "This year was worse" from a corpus written mostly during a bad quarter | Check entries per month first; if it is not flat, no cross-period sentiment claim is available |
| Recency | The last two entries dominate the summary | Extract per entry before reading for gist (Theme Extraction step 3) |
| Length weighting | One 2,000-word entry outvotes twenty short ones | Count entries, never words, when ranking themes |
| Confirmation | The user asks "am I still stuck on X?" and the search finds X | Run the extraction unconditioned first, then answer their question against the ranked list |
| Practice mixing | Morning pages in the corpus flood it with unfiltered noise | Exclude by practice, and say what was excluded |
| Retitling | The same theme under three names counts as three | Cluster on the user's vocabulary, and store the cluster in `## Themes` so next month counts it the same way |
| Analyst framing | You name a theme "avoidance"; the user would call it "the flat" | Use their words; your label becomes a premise in every later review |
| Anything else | Unknown | State the window, the counts, and the exclusions, and let the numbers be checkable |

## Reporting

Shape of a finding, every time:

1. **The window**: dates, entry count, days covered, what was excluded.
2. **The counts**: theme, entries, distinct weeks, dates.
3. **The claim, at the strength the counts support**: pattern (bar cleared), count (bar not cleared), or observation about the writing rather than the life.
4. **The confound you did not control**, in one clause.
5. **One question, at most**, and only if they asked for interpretation.

Never open with the conclusion. A pattern delivered without its counts is a verdict, and a verdict about someone's own life from their own writing is the single fastest way to make them stop writing.

## What Not To Analyze

- Anything in `no_go_file` or `## Read Scope`, at any strength of user curiosity, including yours.
- Material from never-reread practices (`practices.md`) unless the user changes that policy knowingly.
- Anyone other than the user. The journal contains third parties who did not consent to being characterized, and a pattern about someone else's behaviour is both unreliable and not yours to produce (`privacy.md`).
- Diagnosis of any kind. Observable patterns with dates go to the user; "this looks like depression" goes to a clinician, and the route there is in SKILL.md Red Flags.
- Patterns nobody asked for, delivered unprompted. Even an accurate one reads as surveillance and ends the practice (Traps).

**Write in the same turn:** every theme that cleared the bar, with its count, week-spread and the window it came from, to `## Themes` in `memory.md` (or `themes.md` once it has split); the cluster vocabulary, so the next analysis counts the same way; mood ratings to `~/Clawic/data/health/mood.md` with their scale and anchors; the analysis itself, if it was a review, to `reviews/<year>.md`; a standing analysis exclusion the user requests, to `no_go_file`. Formats: `memory-template.md`.
