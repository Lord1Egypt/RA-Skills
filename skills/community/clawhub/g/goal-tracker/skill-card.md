## Description:

Track long-term goals with milestones, daily logging, MRR updates, weekly summaries, and accountability rhythms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alti-systems](https://clawhub.ai/user/alti-systems)

### License/Terms of Use:


## Use Case:

Individuals and teams use this skill to track long-term fitness and revenue goals by logging daily activity, MRR changes, wins, milestones, and weekly progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records personal goal progress, business wins, and MRR in local goal-tracker files.

Mitigation: Confirm that local storage under the configured goal-tracker path is acceptable for the user's privacy and business-data handling needs before using the logging commands.

Risk: The skill invokes absolute local paths under /root/clawd for tracker commands and dashboard generation.

Mitigation: Confirm that /root/clawd/tracker and /root/clawd/goal-tracker/ are the intended local tracker installation paths before executing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alti-systems/skills/goal-tracker)
- [Publisher Profile](https://clawhub.ai/user/alti-systems)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and goal-tracking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create or update local goal-tracker data files and generate an HTML dashboard.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
