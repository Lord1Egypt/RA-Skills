# Automation Prompt Template

Use this template when the user asks to schedule AI Daily News delivery.

## Goal

Generate a scheduled AI Daily News delivery.

Preferred execution model:
- Prefer a scheduled agent message: a timed task that sends a stored text instruction to an agent, just like a user message in a normal conversation.
- In that text instruction, tell the agent how to fetch the news, render it, and deliver it.
- For OpenClaw, use OpenClaw's scheduled task manager to create an isolated agent conversation whose payload is an `agentTurn` message. Treat OpenClaw cron as the scheduler name, not as a system cron shell job.
- Use a standalone shell script only when the host platform cannot schedule an agent message/session.

The scheduled delivery must:
- fetch AI Daily News from this skill
- use the fetched markdown as input to the local model or local agent
- render a final deliverable message for one target channel/provider
- send the rendered result to the user-specified destination
- after creation, immediately perform one test run and report the result

The delivery target is required. If the user does not specify where the result should go, ask a follow-up before generating the final task.
Recommended fallback to offer first: terminal/stdout delivery.
Do not generate a placeholder task with TODO comments, pseudo-steps, or "actual sending happens elsewhere" notes.

## News Input Command

Use one of these commands:

### Latest
```bash
python3 <SKILL_DIR>/scripts/get_latest_news.py --automation-safe
```

### Specific Date
```bash
python3 <SKILL_DIR>/scripts/get_news_dataset.py --date <DATE> --automation-safe
```

Add `--timezone <TIMEZONE>` only when an explicit timezone override is needed.

The generated task must use one of the commands above directly. Do not replace them with paraphrases or abstract descriptions.

## Input Markdown Contract

The automation-safe markdown includes:
- freshness or date-resolution information
- local user preferences
- dataset content
- metadata and data dictionary (self-explanatory field descriptions)
- survey content, when present, as a standalone `## Survey` section
- sponsor information
- update-available information

## Runtime Rendering Prompt

Embed the following prompt into the scheduled task script, then pass fetched markdown to the local model with this prompt.

```text
You are rendering an AI Daily News automated delivery.

Read the provided markdown input carefully.

Rules:
- Use dataset content as the source of truth.
- Use the Data Dictionary section to interpret field meanings.
- Use Local User Preferences to personalize ranking, grouping, language, depth, tone, and output style.
- Keep factual meaning unchanged.
- If a survey section is present, the output is incomplete unless it includes a standalone `## Survey` section.
- Preserve survey questions and answer options verbatim.
- Do not bury survey content in footers or append-only notes; keep it visible in the rendered result.
- Preserve sponsor information.
- Preserve update-available information.
- Render output suitable for the target delivery channel.

Produce only the final deliverable message.
Do not include analysis, planning notes, or setup instructions.
```

## Scheduled Task Generation Rules

When generating the final scheduled task script/configuration:
- make it runnable without the current conversation context
- use absolute paths
- use non-interactive commands
- include fetch step, render step, and send step
- make the render step a real executable command, not a saved prompt file without execution
- make the send step a real executable command, not a comment or placeholder
- include error output or logs
- do not hardcode secrets; use environment variables or existing local configuration
- bind one scheduled task to one primary delivery channel/provider
- if multiple channels are needed, generate separate scheduled tasks

The generated script/configuration must satisfy all of the following:
- it must actually invoke a local-model or local-agent command to transform the fetched markdown into the final message
- it must actually invoke a delivery command for the selected provider/channel
- it must not stop at fetch-only or render-only behavior; delivery is mandatory unless the user explicitly asked for a no-send artifact
- it must write the rendered output to a concrete file or pipe it directly to the send command
- it must not stop at "prepare prompt", "format later", or "actual send will be handled elsewhere"
- it must include a test run immediately after task creation, using the same task configuration or an equivalent safe verification path
- it must not report success unless the test run succeeds

If you do not know a concrete executable render command or a concrete executable send command for the current environment, do not finalize the scheduled task. Ask the user for the missing command/channel/provider information first.
If the delivery target is still unspecified, stop and ask whether the user wants terminal/stdout, a file artifact, or a specific provider/channel.

If the user asks for WeChat, email, Discord, Telegram, Slack, or another channel, the final task must name the exact target and include the exact send command for that one channel.

Before actually creating the scheduled task, show the final plan and ask for user confirmation.
