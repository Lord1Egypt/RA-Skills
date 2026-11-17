## Description:

Deploy and manage hosted OpenClaw or Hermes AI agent bots on OpenClaw Launch from your coding agent, using the OpenClaw Launch developer API. Create a bot, check its status, chat with it, connect it to Telegram, start, stop, restart or delete it. Use when the user asks to deploy, host, spin up, list, chat with or tear down an OpenClaw or Hermes bot on OpenClaw Launch. Requires an OpenClaw Launch API key in OPENCLAW_LAUNCH_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zackchewa](https://clawhub.ai/user/zackchewa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to deploy and manage hosted OpenClaw or Hermes bots through OpenClaw Launch, including checking status, chatting, connecting Telegram, and controlling bot lifecycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan rates the skill benign with medium confidence, but coverage is partial because a local path-like reference could not be resolved; it also reports requests to an external service.

Mitigation: Review the reported external service use before installation and account for the scan's incomplete coverage.

Risk: Creating bots can incur hosting and model costs; stopping a bot does not end Scale hosting charges, and auto-reload can charge the account.

Mitigation: Before creating a bot, confirm its framework, size, and billing; check plan limits and rates, and delete the bot when Scale hosting should end.

Risk: Deleting a bot permanently erases its data and history.

Mitigation: Require explicit confirmation naming the bot before deletion, and delete only the bot the user identified.

Risk: The API key can control bots created with that key and shares account balance and plan limits; exposing it could enable unwanted actions or charges.

Mitigation: Use a dedicated agent key, keep it in the environment, never print or share it, and revoke it if it may have leaked.

## Reference(s):

- [OpenClaw Launch Build & Resell](https://openclawlaunch.com/build-and-resell?utm_source=skill-listing&utm_medium=listing&utm_campaign=openclawlaunch-skill)

## Skill Output:

**Output Type(s):** [API responses, Text, Shell commands, Configuration instructions]

**Output Format:** [JSON API results and concise text summaries, with shell command examples where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCLAW_LAUNCH_API_KEY; TELEGRAM_BOT_TOKEN is optional for Telegram connection.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
