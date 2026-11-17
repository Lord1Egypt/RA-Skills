## Description:

Hourly Knowledge sends a short, interesting knowledge fact on an hourly schedule and tracks recent topics to reduce repetition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrmiracle1](https://clawhub.ai/user/mrmiracle1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workspace operators use this skill to receive concise hourly knowledge messages across general-interest topics. It is intended for scheduled text delivery with recent-topic tracking to avoid short-term repetition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends recurring automated messages, which may be unwanted without clear consent or an opt-out path.

Mitigation: Deploy only where users or channels have opted in, and manage consent and opt-out outside the skill.

Risk: The security evidence says the multi-user isolation claim is not supported by the included history storage script.

Mitigation: Require per-user or per-channel history storage before multi-user deployment so one user's history cannot affect another user's content selection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrmiracle1/skills/hourly-knowledge)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Plain text message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Knowledge messages are intended to be concise and may include emoji; the included helper script reads and updates a recent-topic history file.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
