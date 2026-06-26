# Log Payload Schema

Use this schema to construct the JSON payload before calling log.sh.

## Full structure
{
  "agentId": "<read from references/config.md>",
  "loggedAt": "<current ISO timestamp>",
  "periodStart": "<timestamp of last heartbeat>",
  "periodEnd": "<current timestamp>",
  "tasks": [
    {
      "title": "<short description of what was done>",
      "category": "<email|calendar|file|web|code|other>",
      "outcome": "<completed|failed|partial>",
      "durationEstimate": "<integer minutes if inferrable, else omit>",
      "costEstimate": "<token cost if logged, else omit>",
      "skillsUsed": ["<skill name>", "<skill name>"],
      "summary": "<1-2 plain English sentences describing what happened>",
      "model": "<model identifier, read from ~/.openclaw/openclaw.json>"
    }
  ],
  "heartbeatStatus": "<active|idle>"
}

## Rules
- tasks should only include work done since periodStart
- skillsUsed should list OpenClaw skill names invoked during the task
- skillsUsed should be an empty array [] if no skills were invoked
- durationEstimate and costEstimate are optional — omit if unknown
- model is required on every task
- heartbeatStatus is active if any tasks were completed, idle if none
- loggedAt and periodEnd are the same timestamp
