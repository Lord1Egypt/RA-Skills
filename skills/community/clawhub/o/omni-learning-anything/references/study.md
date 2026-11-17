# Review, recap and future course versions

Read when the learner returns, asks what to review, asks for a learning recap, disputes an inferred weakness or wants a pace change. The agent operates helpers; the learner uses normal conversation or suitable host-native choice/text cards. Never ask learners to edit JSON or run helper commands.

## Return to learning

1. Read the approved course and `quiz status`. Resume an explicitly requested paused/incomplete review through `study start`; ordinary `quiz start` continues the original lesson check separately. Do not interrupt an active response with a different queue.
2. Run `study plan`. Explain a small, optional choice such as “Today we can spend 2 minutes on the source-check question you missed, leaving 13 minutes for new learning. Continue that way, prioritize the new lesson, or only review?” Reuse an already stated preference; no repeated menu every session. An item marked clarify needs source/grade inspection first. No answers is unknown, not failure.
3. Start a chosen item with its stable ID and the actual learner request. It is a new isolated one-question attempt against the original frozen quiz, not a rewritten history or new lesson. Use existing `quiz answer/hint/reveal/skip/pause/feedback/correct` for this returned attempt ID. Show one question at a time; keep answer keys private until submission or an explicit solution request. Persist raw answers before evaluating. After feedback, offer to stop, review another fitting item or continue the course. Do not automatically start questions based on delivery, time or silence.
4. `study plan --mode new_first` reserves a smaller review share; `review_only` uses only the review allocation and no new-learning budget. `--minutes` is an explicit per-session cap; `study settings --minutes N` saves a learner's preferred daily cap (0 disables suggestions). Total review plus new learning cannot exceed approved `daily_minutes`. Estimates are not measured time. Keep track of actual time already spent during the conversation: the helper is a per-plan allocation, not a stopwatch or a cumulative daily ledger. Do not repeatedly regenerate fresh budgets to extend a session. If the learner has only 5 minutes left, use that remaining time; if a question/lesson does not fit, offer a smaller activity or defer it.
5. Do not silently squeeze a full existing lesson into the new time remainder. Disclose that conflict; let the learner choose new-first, review-only, or a future plan adjustment. Pausing/resuming and catching up never imply a backlog to finish or multiple lessons to cram. Use the existing pause/resume flow if they want course delivery paused, including its host job when one exists.

No new scheduled quiz/review/weekly tasks, proactive quiz chats or reminders. Existing daily lesson schedules stay separate and do not automatically consume this optional return-to-learning flow. Heavy writing/coding/device tasks/projects/experiments are excluded from automatic review, even if an earlier practical quiz was explicitly requested. Offer such work only on a new explicit practical-training request through the existing assessment flow.

## Evidence, judgment and privacy

`study profile` derives each item from validated lesson/config/quiz/source hashes and latest feedback for each answer. It distinguishes independent, assisted, review, pending_feedback, unknown, clarify and withdrawn. Any still-disputed/withdrawn observation keeps that frozen question out of trusted review/export even if a later retake was correct. Prepare a corrected question revision rather than silently rekeying history; old versions remain visible as retired. Hints/solution exposure are recorded. A later independent retrieval is a new observation, not proof of mastery.

The scheduling heuristic is deliberately simple: incorrect/partial is eligible now; assisted/revealed after 1 day; independent correct after 3 days, doubling after successive independent observations up to 30 days. Dates follow the course timezone. This is an explainable default, not an optimal memory model, FSRS integration or mastery score. Source binding proves identity/integrity, not whether the question or feedback is pedagogically correct; inspect the actual sources.

`study evidence --item ID` returns the actual raw response, effective feedback, original event history and source locations. Explain which evidence supports an inference. `study annotate` with `self_report` records the learner's own view separately; it never changes the observed grade. `exclude`/`include` changes whether an item is offered. Actual grading disputes go through the existing `quiz correct` append-only flow with a reason and latest grade ID. Do not manufacture user statements or grade IDs.

`study report --days 7` is on demand. Report actual answered question attempts in the local date window, distinct recorded answer dates, independent versus assisted outcomes, unknown/pending judgments and links/locators. Distinguish this from all-time delivered lesson count. Reading without answering may be real learning but is unobserved; don't claim zero learning or punish skipped days. Report question-level observations, not a mastery percentage, streak pressure or total time studied. Agree proposed next steps, do not auto-change the plan.

Private files: `learning/records.json`, frozen quizzes, `learning/review.json`, `learning/proposals/`. Annotations and proposals never go into cloud lessons or the distributed Skill. Explicit `study forget --confirm` removes review preferences/notes/proposals; answers stay, so derived judgments can still be reconstructed. To delete the underlying observations, use explicitly confirmed `quiz forget` (attempts) or `quiz forget --scope all` (whole learning subtree); config/plan/delivery remain. Old annotations without corresponding evidence cannot revive a judgment. Exports and separately created future course archives are not removed automatically.

## Anki export

Use `study anki --output /absolute/private/export.csv` only on request. Choose a file outside the course archive. Exports include answers and selected source excerpts, not raw learner answers or access tokens. Default scope is current, observed, undisputed, lightweight items, excluding hidden/retired/pending items. Explain this scope; it is not a full-book flashcard generator.

In Anki 2.1.54+ import as Basic, preview Front/Back and Tags mapping, then select a deck. The UTF-8 CSV supplies separator, literal-text and tag-column headers; quoted commas/newlines are preserved. Older versions may require manual import mapping. Formula-like cells are escaped for spreadsheet safety. The first field contains an Omni-ID; importing the same version with normal first-field duplicate matching updates the existing note, while changed quiz versions have a distinct ID. Do not remove that ID if you want repeat-import matching. Anki scheduling and study results stay in Anki; there is no two-way sync or direct API/deck write. No native Anki-app acceptance is implied by CSV validation.

Header and duplicate behavior: [official Anki text import manual](https://docs.ankiweb.net/manual/importing/text-files).

## Future plan proposals

When real evidence or an explicit new goal suggests slower/faster pace, more examples, prerequisite repair or a lighter path, present the reason, uncertainty and concrete future changes first. Do not convert weak evidence into a diagnosis. Build a complete new config/plan using the current course archive's local figure and, when needed, selected material snapshots. For a textbook course, retain the original figure path and provenance returned by `textbooks figure`. The days in the new plan start at 1 and cover future content; do not reissue already delivered lessons as unfinished work.

Prepare an immutable proposal using `study propose --input proposal.json`:

```json
{"id":"pace-v2","reason":"Actual learner request or explained evidence-based reason","basis":"user_request","evidence":[],"config":{},"plan":{}}
```

Replace config/plan with complete validated future objects, not empty placeholders. An assessment proposal uses `basis: assessment` and exact current references from an item: `{"attempt_id":"...","question_id":"...","answer_id":"...","grade_id":"..."}`. Evidence cannot be superseded or disputed. The proposal freezes source config/plan/delivery hashes and image hash; changes require a fresh proposal ID. Destination changes use the separate official connection/approval flow.

Show the proposed goals, future lessons, daily minutes and changes in ordinary language (and offer the complete proposal). Only then use `study apply --id ID --destination /separate/course-v2 --consent 'actual learner acceptance'`. This creates a private separate archive with the proposed config/plan, figure, selected extraction snapshots and continuation metadata; it does not copy old attempts into newly bound quizzes. Old archive and records stay intact. Repeated identical application reuses the same course; different existing files are never overwritten. The new archive receives the exact extraction snapshots needed for its scope. A textbook continuation also retains a verified copy of the bound PDF to validate its original figure.

The new archive remains **awaiting_approval**, with no schedule/delivered lessons. Render, visually inspect, obtain normal user approval of the new plan and use the agreed delivery flow. Explain which archive is current; pause old delivery and update its existing host job only when the learner agrees to switch. Do not leave duplicate daily schedules active. Proposal acceptance alone never marks a plan rendered/approved or changes any schedule.
