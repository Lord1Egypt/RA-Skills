## Description:

Replay OpenClaw cron job formatting and delivery decisions locally using a trusted local openclaw-cron-replay installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to replay saved OpenClaw cron job inputs and results locally, inspect likely final delivery text, and debug why a cron run produced or suppressed a message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replay inputs may include saved cron configuration, prompt, payload, result, or metadata files that contain secrets or sensitive operational details.

Mitigation: Review local cron job and result files for secrets before replaying or sharing outputs.

Risk: Running an untrusted or elevated local replay binary could expose local files or execute behavior outside the skill's plain-text guidance.

Mitigation: Use only a trusted local openclaw-cron-replay binary or inspected source checkout, and avoid root execution unless it is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/openclaw-cron-replay)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional replay outputs in Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local debugging and interpretation guidance; it does not perform real message delivery.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
