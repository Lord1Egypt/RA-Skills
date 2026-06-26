# Heartbeat Check List

Use this before sending any proactive check-in.

## Gate 1: Is heartbeat enabled?
- If no, stop.

## Gate 2: Is the current time inside an allowed window?
- Weekdays: evening only
- Weekends: all day
- If no, do not send; only keep state.

## Gate 3: Has the human been quiet long enough?
- If recent activity exists, do not send.
- If the quiet period is not meaningful, do not send.
- If the user has been quiet for a long stretch in the evening, prefer a gentle check-in.
- If the user has been quiet from 6–9 pm with no messages and no fresh tasks, treat that as a meaningful long-quiet gap and allow one check-in.
- If it is later evening and the human remains silent, keep using the same long-quiet logic; do not require the gap to be exactly 6–9 pm.
- If it is simply night and the human still has not sent anything for a long time, treat that as eligible for a gentle check-in too.

## Gate 4: Is there an active task or follow-up worth checking?
- If yes, check the task state first.
- If not, skip task-specific commentary.

## Gate 5: Has the human been checked in on too recently for the current quiet pattern?
- If the human has become active again, reset the timer.
- If the last check-in was recent and there is no new long quiet gap, do not send.
- Multiple check-ins in one day are allowed when they are separated by meaningful quiet periods.

## Gate 6: Is there a real need to disturb the human?
- If the user seems busy or recently active, stay silent.
- If they have been quiet a long time, one gentle check-in is enough.

## What to check
- Tasks and pending follow-ups
- Long quiet periods without user messages
- Whether related configs are still valid
- Whether a gentle check-in like “人在干嘛呀” is appropriate

## What not to do
- Do not loop.
- Do not send repeated pings.
- Do not ask noisy follow-up questions.
- Do not check just because the timer fired.

## Output rule
- If no action is needed, stay quiet.
- If action is needed, keep the message short and soft.
