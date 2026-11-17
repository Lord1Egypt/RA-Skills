## Description:

Designs, tracks, and repairs personal habits, including streaks, completion rates, routines, quit plans, relapse restarts, reviews, and disruption handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to design, log, review, and repair recurring personal habits, including quitting unwanted behaviors and maintaining routines through disruptions. The agent can read and update local Clawic habit files when tracking events, reviews, routines, quit plans, restart protocols, or configuration changes are produced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain plaintext local records about routines, misses, capacity constraints, contacts, health metrics, or paid subscriptions.

Mitigation: Review before installing, grant access only to folders you are comfortable with, and avoid saving sensitive health or financial details unless persistence is explicitly desired.

Risk: The skill may write to shared contacts, health, and finance stores and sometimes delete rows it created without a clear prior consent step.

Mitigation: Require confirmation before shared-store writes or deletions and review the named file changes during use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/habits)
- [Clawic Habits page](https://clawic.com/skills/habits)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text responses, with local Markdown and YAML records when persistence is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain plaintext local records under the configured Clawic habit, contacts, health, and finances paths.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
