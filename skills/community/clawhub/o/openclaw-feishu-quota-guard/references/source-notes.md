# Source Notes

This skill was drafted from the following sources.

## Video trigger

- Bilibili video: [所有OpenClaw接飞书机器人的，请立即检查额度 免费额度烧完之前，教你两种解决办法，让你立省大几百年费](https://www.bilibili.com/video/BV1fvcuzVEsc/)

What could be verified directly:

- BVID: `BV1fvcuzVEsc`
- Publish time: 2026-02-09 23:26:49 +08:00
- Title points to a quota-burn problem specific to `OpenClaw + Feishu`

What is inferred from the video title plus public comments:

- One remediation path is to avoid burning cloud quota on background checks by moving those checks to a local API/model.
- Another remediation path is to reduce or cache the repeated Feishu health/heartbeat checks so they stop hitting the model so often.

Public comments that informed the skill design included:

- users saying a local API avoids the quota concern
- users lowering heartbeat cadence to `1 hour`
- users mentioning Feishu probing too frequently
- users mentioning a cached health link

## Current OpenClaw docs

- Heartbeat docs: [docs.openclaw.ai/heartbeat](https://docs.openclaw.ai/heartbeat)
- Gateway heartbeat docs: [docs.openclaw.ai/gateway/heartbeat](https://docs.openclaw.ai/gateway/heartbeat)
- Feishu channel docs: [docs.openclaw.ai/channels/feishu](https://docs.openclaw.ai/channels/feishu)

Source-backed facts used in this skill:

- Current OpenClaw Feishu uses WebSocket event subscription by default, so not every Feishu setup is a public webhook setup.
- Webhook mode still exists and uses `verificationToken`.
- Heartbeat defaults to `30m` in docs, or `1h` for some detected auth modes.
- `0m` disables heartbeat.
- An effectively empty `HEARTBEAT.md` skips the heartbeat run and saves API calls.
- `lightContext` exists as a heartbeat cost-control knob.

Design choice:

- Because the video and comments point to both "expensive heartbeat/model calls" and "Feishu health probing", this skill first identifies whether the user's setup is the official/current plugin or a legacy/custom bridge before applying a fix.
