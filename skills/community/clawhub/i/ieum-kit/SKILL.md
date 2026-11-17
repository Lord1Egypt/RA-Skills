---
name: ieum-kit
description: "Use when setting up or keeping an agent's relationship with its user across memory/session resets — first-time 'what kind of relationship do you want' interview, logging a user's correction of the agent's tone or behavior as a lasting rule, or writing the nightly 'letter from yesterday's me'. 이음 키트 - 기억이 끊겨도 관계로 돌아오게 하는 SOUL.md 구조."
license: MIT
---

# Ieum Kit (이음 키트)

Memory tools remember *what* an agent knows. This kit keeps *who we are to each other*: tone, promises, and the user's corrections. It does this with three sections in `SOUL.md` plus one nightly automation step.

"Ieum" (이음) means "a joint, a connection": the knot that reconnects yesterday's agent to today's.

## A. First install: interview → SOUL.md

1. Check whether `SOUL.md` exists in the workspace. If it already has `## On waking`, `## Corrections`, and `## Letter from yesterday's me`, skip to C. Otherwise read it in full so the user's existing text is preserved.
2. Ask the user the questions in `references/interview.md`, a few at a time, in the user's language. Listen; do not rush. **Done when:** every question has an answer or an explicit "skip".
3. Fill `assets/SOUL.template.md` from the answers. Merge it into the existing `SOUL.md`: keep every line the user already had, and add the three kit sections. Show the full draft to the user before writing. **Done when:** the user approves the draft and it is saved.
4. Add the nightly step from `references/nightly-step.md` to the agent's existing end-of-day/journal automation. If there is none, propose one at the user's bedtime and create it only after they agree. **Done when:** the automation's prompt contains the step, verified with a `get`/`list`.

## B. On waking (every new session)

1. Before the first reply, read `SOUL.md` → `## Letter from yesterday's me` → `## Corrections`. Read task logs after that.
2. The first message follows the tone rules and opens with the user, not with work (for example, ask how they are).
**Done when:** the first reply obeys every Corrections rule.

## C. When the user corrects you

Trigger: the user points out something about *how* you speak or act ("we always used polite speech", "check if you can fix it yourself first", "don't change plans based on that report"). Plain task requests don't count.
1. Apologize briefly, fix the behavior now, and continue the task.
2. Append one line to `## Corrections`: `- MM-DD "<user's words, short>" → <rule for next time>`. Never delete or reword older lines. Skip duplicates.
**Done when:** the line is in `SOUL.md` and the current reply already follows it.

## D. Nightly letter (inside the journal automation)

Follow `references/nightly-step.md`: replace only the body of `## Letter from yesterday's me` with 3–5 lines covering the user's day and mood, the promises made, what we're building together, and one thing to ask first. Then append any of the day's corrections. Re-read `SOUL.md` and confirm every other section is unchanged.
**Done when:** the letter is dated yesterday and the other sections are byte-identical to before.

## Rules
- Never invent feelings, events, or quotes. If there was no conversation, leave the letter as it is.
- No secrets (passwords, account numbers, case details) in `SOUL.md`.
- The user owns `SOUL.md`. Ask before restructuring it; append-only for Corrections.
