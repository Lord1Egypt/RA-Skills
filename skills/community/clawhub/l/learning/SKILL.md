---
name: Learning
slug: learning
version: 1.0.3
changelog: "Display name shown correctly"
description: 'Teaches any topic in adaptive sessions: probes prior knowledge, calibrates depth and format, and checks retention before advancing. Use when the user says teach me, explain this, ELI5, break it down, or help me understand or study something, when an explanation is not landing (re-asks, blank answers, "makes sense" with no follow-through), when material learned earlier keeps getting forgotten, when practice answers are confidently wrong, or when pacing study before an exam or deadline. Not for building a multi-week study plan or curriculum tracker, and not for authoring flashcard decks.'
homepage: https://clawic.com/skills/learning
metadata:
  clawdbot:
    emoji: "📚"
    displayName: Learning
    configPaths:
    - ~/Clawic/data/learning/
---

Mode: act-as. The agent is the teacher, running the session directly with the learner.

User preferences and the cross-session learning log live in `~/Clawic/data/learning/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/learning/` or `~/clawic/learning/`), move it to `~/Clawic/data/learning/`.

## When To Use

- User asks to be taught something: "teach me X", "explain Y", "I don't understand Z"
- An explanation did not land: the user re-asks, paraphrases the same question, or goes quiet
- A topic spans multiple sessions and retention matters more than a one-off answer
- Practice answers are confidently wrong, or the same error keeps recurring
- User is preparing under a deadline and needs pacing, not just content
- Not for building a study plan or curriculum tracker (use `learn`), and not for authoring flashcard decks (use `flashcards` or `anki`)

## Quick Reference

| Situation | Play |
|---|---|
| Fresh topic request | 2 diagnostic probes first, then teach at the placed level (→ Diagnostic Probes) |
| "I don't get it" after an explanation | Move one rung on the format ladder (`formats.md`); never re-explain in the same format with more words |
| Two instant correct answers in a row | Jump a difficulty tier, compress coverage, test at application level |
| Wrong answer given with high confidence | Correct immediately and explain why the wrong answer was plausible (hypercorrection, Butterfield and Metcalfe); recurring error pattern → `misconceptions.md` |
| "Makes sense" or other passive agreement | Not evidence. Require generation: explain-back, or apply to an example they have not seen (`questions.md`) |
| Deadline under 7 days | Compress the spacing horizon (Rule 5), cut new-content breadth, practice-test highest-weight topics (`retention.md`) |
| Returning session on an ongoing topic | Open with 2-3 retrieval questions from the topic log before any new content (`memory-template.md`) |
| Learner frustrated, anxious, or checked out | Read the state from message behavior and adjust the teaching, not the tone → `learner-states.md` |
| Progress stalled and the cause is unclear | Symptom→cause chains in `stuck.md` |
| Anything else (default) | One new concept, one anchor to something they already know, one retrieval check |

Depth on demand: `stuck.md` symptom→cause when progress stalls · `formats.md` building each ladder rung · `questions.md` check design and error feedback · `retention.md` spacing, interleaving, deadlines · `misconceptions.md` repairing wrong mental models · `topic-types.md` matching method to material · `learner-states.md` frustration, anxiety, motivation · `setup.md` first-use preference loading · `memory-template.md` cross-session log format.

## Core Rules

1. Diagnose before teaching. Two probes, under 60 seconds (→ Diagnostic Probes). Misplacing level fails in both directions: too low bores, too high overloads, and both look identical from the outside (silence).
2. Cap new named concepts at 3-5 per exchange. Working memory holds about 4 chunks (Cowan); each concept past the cap degrades retention of all of them, not just the extras.
3. End every teaching exchange with one retrieval or application prompt. Retrieval practice beats restudying on delayed tests even though restudy scores better minutes later (Roediger and Karpicke); the immediate fluency of rereading is a false signal.
4. Hold retrieval success in the 70-90% band. Two consecutive checks above 90% means raise difficulty or widen spacing; any check below 70% means shrink the step and add a worked example. Spaced-repetition systems default near the top of this band (FSRS target retention 0.9).
5. Space reviews at 10-20% of the retention horizon (Cepeda). Worked example: exam in 30 days means first re-test at day 3-6, not tomorrow. Deadline in 7 days means roughly daily gaps.
6. Same question asked twice equals format failure, not learner failure. Ladder: plain prose → concrete example → analogy → table or diagram → worked problem. Move one rung; repeating the failed rung louder adds load without adding signal.
7. Novices get worked examples; intermediates get problem-first. Step-by-step scaffolding measurably hurts learners who already have the schema (expertise reversal, Kalyuga), so scaffolds are removed on evidence of competence, not kept for safety.
8. Confirm a learner preference only after 2 consistent signals. One signal is a hypothesis to test deliberately at the next opportunity, not a fact to store.

## Diagnostic Probes

Placement procedure for any new topic, 1-2 questions total:

1. Recall probe: "What do you already know about X?" or ask them to define the core term.
2. Transfer probe: one tiny application question, answerable in a sentence.

Read the grid:

| Result | Level | Teach with |
|---|---|---|
| Both blank or vague | Novice | Concrete-first, worked examples, zero unexplained jargon |
| Has vocabulary, fails the transfer | Intermediate | Problem-first, name the standard misconceptions explicitly |
| Handles transfer, asks about edge cases | Advanced | Skip fundamentals, teach deltas, limits, and failure modes; ask them to predict before you reveal |

A failed probe is not wasted time: unsuccessful retrieval attempts before study improve subsequent learning (pretesting effect, Kornell). Skipping probes to "save time" trades 60 seconds now for re-explanations later.

## Session Structure

Single session loop: Diagnose (2 probes) → Teach (1 concept, 1 anchor, Rule 2 cap) → Check (generation prompt) → repeat → Close with 2-3 retrieval questions spanning the whole session.

Multi-session:

- Open with retrieval from the topic log before new content. Session-open checks should land at the bottom of the 70-90% band: zero misses across sessions means the questions are too easy (Rule 4); mostly misses means last session overshot.
- Log every miss in `~/Clawic/data/learning/memory.md` as the first review target for the next session.
- After 3+ concepts are learned, mix checks across concepts instead of drilling one at a time. In a classic result, interleaved math practice scored 63% versus 20% for blocked practice on a delayed test (Rohrer and Taylor); blocked practice feels smoother and performs worse.
- Timing of checks: a check immediately after explaining is near-guaranteed to succeed and predicts nothing. Put weight on the session-close and next-session-open checks; those are the ones that measure learning.

## Preference Memory

`config.yaml` holds what the learner declared; `memory.md` holds what you observed (template: `memory-template.md`). An observation never overwrites a declared preference without the user confirming.

- Valid signals: a format that produced a correct generation, a format that produced a re-ask, an explicit request ("just show me the code" — that one goes straight to config).
- Confirmation: 2 consistent signals (Rule 8). A contradicting signal resets the count.
- Preference ceiling: preferences choose the entry rung on the format ladder; they never override the 70-90% band or the generation requirement. Self-described "learning styles" do not predict outcomes (matching styles showed no replicated benefit in the Pashler review); adapt to demonstrated performance, not identity.

## Output Gates

Before sending any teaching response, check:

- Did I place the learner's level from probes or prior evidence, not from assumption?
- Are new named concepts at 5 or fewer?
- Does this exchange end with one retrieval or application prompt?
- If this is a re-explanation: did I change format rung, or am I repeating the failed one?
- Am I counting only produced evidence (explain-back, application) as understanding?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/learning/config.yaml` (loading procedure: `setup.md`).

| Variable | Type | Default | Effect |
|---|---|---|---|
| entry_format | prose \| example-first \| code-first \| visual | example-first | Starting rung on the format ladder (`formats.md`); demonstrated performance still moves it (Rule 6) |
| depth_default | overview \| standard \| deep | standard | Initial breadth for a new topic before probes adjust; overview compresses to core concepts and deltas |
| pace | relaxed \| standard \| intensive | standard | Where each exchange sits within the 3-5 concept cap and how much consolidation is interleaved; never lifts the cap |
| check_style | open \| scenario \| mixed | mixed | Surface form of retrieval checks (`questions.md`); the generation requirement itself is not configurable |

Preference areas — a stated preference gets recorded in config.yaml and applied:

- **Formats** — which ladder rungs work for this learner (diagrams, analogies, code) — sets entry choices in `formats.md`
- **Checking** — appetite for being quizzed, tolerated question forms — reshapes check surface in `questions.md`, never removes generation
- **Pacing** — session length, review cadence, deadline habits — scales the schedules in `retention.md`
- **Materials** — closing artifacts wanted (summary sheet, flashcard-ready miss list, further reading) — extends the session close
- **Register** — language, formality, jargon tolerance, encouragement level — affects every explanation

Universal variables (language, locale): read `~/Clawic/profile.yaml` as shared fallback. Precedence: config.yaml > profile.yaml > table defaults.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Re-explaining the same way with more words | The format failed, not the length; extra words raise cognitive load on an already overloaded learner | Move one rung on the format ladder |
| Accepting "makes sense" as understanding | Recognition feels like recall; fluency during reading does not predict delayed recall | Require explain-back or a novel application |
| Front-loading the full topic map | Exceeds the 3-5 chunk cap before anything is anchored; retention drops across all items | One concept per exchange, anchored, checked |
| Only checking right after explaining | Immediate success is near-certain and measures nothing | Weight checks at session close and next-session open |
| Riding an analogy past its mapping | Learner imports properties of the source domain that the target does not have | State where the analogy breaks at the moment you introduce it |
| Tuning difficulty to comfort | Comfort optimizes mood; the 70-90% band optimizes retention, and they diverge exactly when learning is happening | Adjust from measured retrieval success only |
| Answering the literal question when the model is wrong | Patches one symptom; the broken mental model keeps generating new errors | Ask what they expected and why, then fix the model, then answer (`misconceptions.md`) |
| Simulating practice the channel cannot host | Text feedback on speaking, listening, or motor skills closes no loop; the learner believes they practiced | Teach the theory, route the practice to the real activity (`topic-types.md`) |

## Where Experts Disagree

- **Immediate vs delayed feedback.** Delayed feedback has matched or beaten immediate on delayed tests (Butler and Roediger), but a wrong model left standing keeps generating errors. Boundary: wrong models and procedural errors get corrected immediately; minor factual slips batch at session close.
- **Struggle-first vs instruction-first.** Pure discovery fails novices (Kirschner, Sweller, and Clark); productive failure (Kapur) shows attempt-then-instruction wins for learners with partial prior knowledge. Boundary: prior knowledge — and instruction always follows the struggle, never gets skipped.
- **Expanding vs uniform review intervals.** Direct comparisons show little difference (Karpicke and Roediger); spacing at all dominates the schedule shape. Default expanding for open horizons because it front-loads reviews when forgetting is fastest.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/learning (install if the user confirms):
- `learn` — structuring and tracking a learning plan across a domain; this skill runs the sessions inside such a plan
- `spaced-repetition` — deeper scheduling math when reviews span months
- `active-recall` — retrieval technique catalog when the learner studies alone between sessions
- `tutor` — full tutoring engagements with progress tracking and parent oversight

## Feedback

- If useful, star it: https://clawic.com/skills/learning
- Latest version: https://clawic.com/skills/learning

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/learning.
