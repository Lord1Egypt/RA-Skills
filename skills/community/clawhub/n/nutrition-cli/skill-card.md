## Description:

Nutrition CLI helps agents look up nutrition data, log meals, track intake against goals, compare foods, estimate calorie burn, and view trends from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javi23ruiz](https://clawhub.ai/user/javi23ruiz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer nutrition questions, configure daily targets, log meals with confirmation, and summarize diet trends through the nutrition CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive nutrition, allergy, diet, and health-context notes in memory.

Mitigation: Use it in private sessions, review retained memory entries, and remove or avoid the memory sections if long-term health-context retention is not desired.

Risk: The heartbeat and reminder behavior can create persistent prompts after installation.

Mitigation: Review or remove the heartbeat snippet before use, and enable cron reminders only for user-selected reminder types and times.

Risk: The release depends on the nutrition-cli package and nutrition data sources outside the skill artifact.

Mitigation: Install a pinned, reviewed nutrition-cli package and check the reported data source before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/javi23ruiz/skills/nutrition-cli)
- [Nutrition CLI onboarding script](artifact/ONBOARDING.md)
- [Nutrition memory template](artifact/MEMORY_TEMPLATE.md)
- [Nutrition heartbeat snippet](artifact/HEARTBEAT_SNIPPET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and occasional JSON-formatted CLI parsing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relies on the installed nutrition binary and may update private memory files or optional reminder jobs when the workflow calls for it.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
