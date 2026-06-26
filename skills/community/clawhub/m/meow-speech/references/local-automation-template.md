# Local Auto Task Template (Low-Token)

Use this as the compact host-side template for meow-speech automation.
It is designed to keep decisions simple and messages short.

## Minimal state

Store only:
- `proactive_enabled`: true/false
- `timezone`: `Asia/Shanghai`
- `preferred_channel`: `feishu` | `telegram` | `local`
- `last_user_activity_at`: ISO timestamp
- `last_proactive_sent_at`: ISO timestamp
- `pending_idle_job_id`: string|null
- `bedtime_job_id`: string|null

## Decision rules

### Bedtime
- If user opted in, keep exactly one daily bedtime job.
- Run at `23:50` local time.
- If a bedtime job already exists, update it instead of creating a duplicate.
- Message length target: 1 short line.

### Idle-time
- Only enable if user explicitly wants quiet-time check-ins.
- Use one re-arming one-shot job, not a tight loop.
- Re-arm only after new user activity.
- Default delay: `30-60 min` after last activity.

### Sending policy
- Prefer the active external channel.
- If no channel is available, draft locally.
- Never send more than one proactive message per day unless explicitly requested.

## Low-token judgment template

When deciding whether to act, evaluate in this order:
1. Is proactive mode enabled?
2. Is there a due bedtime job?
3. Has the user been quiet long enough for idle mode?
4. Is there a recent proactive send already today?
5. Which channel is active?

If the answer to 1 is no, stop.
If the answer to 2 is yes, send bedtime.
If the answer to 3 is yes and 4 is no, send one idle check-in.
Otherwise do nothing.

## Recommended bedtime copy

- `晚上好，人～ 该睡觉啦 ( ๑-๑ )`
- `人，猫来提醒你晚安啦…`

## Recommended idle copy

- `人今天好安静呀…猫来看看你 (｡･･｡)`

## Token-saving rules

- Keep rule evaluation in host state, not in chat prompts.
- Use fixed short templates instead of generating new wording every time.
- Avoid multi-step language reasoning in the message body.
- Prefer update-in-place for jobs.
