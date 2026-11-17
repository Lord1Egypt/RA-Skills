## Description:

Deprecated skill for syncing the Kilocode provider model list in openclaw.json with the live Kilo AI API, preparing approved patches, and reporting sync results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumemaka](https://clawhub.ai/user/guillaumemaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this deprecated skill only when they still need the legacy Kilocode model sync workflow for OpenClaw. It fetches model data, creates snapshots, diffs, and patch files, applies approved changes to openclaw.json, restarts the gateway, and records or sends status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is deprecated and may be unnecessary because Kilocode Gateway is built into OpenClaw.

Mitigation: Use the built-in OpenClaw gateway for normal operation and run this skill only for a documented legacy need.

Risk: Patch application can rewrite OpenClaw gateway configuration and restart the gateway from weakly validated patch files.

Mitigation: Restrict who can create or modify patch files, review the exact patch JSON before approval, keep backups, and verify gateway health after restart.

Risk: The workflow can send operational details to a hardcoded Telegram destination.

Mitigation: Confirm Telegram is an approved destination and that the recipient is correct before sending sync or failure details.

Risk: The workflow loads credentials from the user's OpenClaw environment file.

Mitigation: Limit credential exposure, avoid broad environment sourcing where possible, and ensure KILOCODE_API_KEY is scoped to the required API access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guillaumemaka/skills/kilocode-model-sync)
- [Kilo AI Gateway Models API](https://api.kilo.ai/api/gateway/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON script output, patch and diff JSON files, configuration updates, and status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KILOCODE_API_KEY and access to the user's OpenClaw workspace; the skill is explicitly deprecated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
