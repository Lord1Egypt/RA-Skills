## Description:

Control Minecraft bots through a Mineflayer controller API using JSON actions and cron-driven autonomy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ene5135](https://clawhub.ai/user/ene5135)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create and control Minecraft bots through a trusted Mineflayer controller. It helps agents translate goals into JSON action batches, manage bot state, and run cron-triggered autonomy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron automation can keep issuing controller actions without continuous operator review.

Mitigation: Review before installing, add a clear disable or removal path for the cron job, and run it only in workspaces where persistent automation is expected.

Risk: The artifact instructs agents to overwrite a workspace-level CRON_PROMPT.md.

Mitigation: Back up any existing cron prompt and require explicit operator approval before replacing workspace-level automation files.

Risk: The skill uses bearer tokens and a hardcoded external controller URL.

Mitigation: Use a controller you operate and trust, replace the hardcoded ngrok URL, store credentials outside shared workspace files where possible, and use short-lived scoped tokens.

Risk: Open registration can allow token self-issuance when enabled.

Mitigation: Avoid open registration unless open access is intentional; prefer allowlisted proxy registration or operator-issued tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ene5135/skills/openclaw-minecraft)

## Skill Output:

**Output Type(s):** [JSON actions, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON payloads and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces controller requests for bot creation, connection, state polling, and batched actions; cron prompt expects a 30-second autonomous loop.]

## Skill Version(s):

0.1.26 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
