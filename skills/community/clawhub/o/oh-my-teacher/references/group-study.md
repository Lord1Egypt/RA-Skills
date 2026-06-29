# Group Study

Use this file for `/group-quiz` when multiple students are studying the same course together. The skill acts as a neutral quizmaster and facilitator.

For interaction modes used in group settings — Feynman mode for peer explanation rounds, Examiner mode for quiz grading — see `references/interaction-modes.md`. For question generation and grading rubrics, see `references/question-types.md`.

## Setup

1. Ask for participant count and names/nicknames.
2. Confirm they share the same course and materials, using the current snapshot.
3. Ask for turn-based or buzzer-style format.

## Turn-Based Mode

1. Assign a turn order.
2. Generate one question visible to all participants.
3. The designated participant answers; others wait until grading is complete.
4. Grade publicly, optionally assign points, then rotate.
5. Track a compact scoreboard.
6. End with common mistakes and recommended `/fix` topics per participant.

## Buzzer-Style Mode

1. Post a question visible to all.
2. First participant to signal readiness or type an answer gets the attempt.
3. If incorrect, keep the question open for others.
4. Track the scoreboard after each scored answer.

## Group Features

- Peer explanation round: after a correct answer, ask the participant to teach the idea back in Feynman mode.
- Collaborative problem: generate a harder multi-step problem and let the group discuss before solving.
- Individual weakness detection: summarize weak points per participant from incorrect answers.

## Environment Notes

- Agent shell: write the scoreboard to `.oh-my-teacher/group-scoreboard.md` when useful.
- Plain chat: output the scoreboard inline after each round.
- RAG notebook: same as plain chat, citing course materials when generating questions.
