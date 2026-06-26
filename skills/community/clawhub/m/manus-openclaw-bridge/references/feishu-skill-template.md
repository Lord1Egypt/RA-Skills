# Feishu skill template

## Goal

Give another OpenClaw instance a clean pattern for routing Feishu chat requests into Manus.

## Direct-message pattern

Recommended behavior in Feishu DM:
- If the message starts with `Manus,` or `manus:`
- treat the rest of the message as a Manus task prompt
- submit it through `scripts/manus_prompt.sh`
- wait for completion
- return image/file/text results into the same conversation

## Group-chat pattern

Recommended behavior in Feishu groups:
- require the user to @mention the bot
- require the message to start with `Manus,` or `manus:`
- strip the prefix and submit only the remainder

This reduces false positives.

## Suggested agent behavior

1. Acknowledge briefly if the job may take time.
2. Submit the Manus task.
3. Parse the task id.
4. Wait and collect outputs.
5. If files exist, send files first.
6. If only text exists, summarize the useful result.
7. If the task errors, show the real error/status.

## Example routing policy

Use Manus routing when all are true:
- current surface is Feishu
- user intent is clearly generation/research/deck work delegated to Manus
- message matches trigger rule

Do not route to Manus when:
- the user is just asking what Manus is
- the message casually mentions Manus without being a command
- the bot is in a busy group and there is no explicit trigger

## Example pseudo-flow

```text
if feishu_dm and message startswith Manus-trigger:
    prompt = strip_trigger(message)
    submit Manus task
    wait for result
    send outputs back

if feishu_group and bot_mentioned and message startswith Manus-trigger:
    prompt = strip_trigger(message)
    submit Manus task
    wait for result
    send outputs back
else:
    handle normally
```

## File return recommendation

- image -> send inline image/file
- pptx/pdf/docx -> send file + one-line explanation
- multiple outputs -> best artifact first, extras after if still useful
