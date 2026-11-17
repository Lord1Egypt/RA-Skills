## Description:

A two-module agent skill that guides burnout recovery using a Maslach-style assessment and supports a 14-day behavioral sleep improvement protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an agent to assess burnout and sleep patterns, follow staged behavioral protocols, set reminders, and create notes for boundaries, energy audits, and sleep routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists sensitive mental-health, sleep, and alcohol-related information across sessions.

Mitigation: Confirm where agent state is stored, how it can be deleted, and whether retention matches the user's expectations before use.

Risk: The skill can schedule reminders and create notes through calendar and filesystem tools.

Mitigation: Require user approval before creating reminders or files, and show the exact timing, destination, and content before saving.

Risk: The server security guidance flags the unpinned npx installer as a review concern.

Mitigation: Prefer a pinned or preinstalled trusted ClawHub CLI, or verify the installer source before running the command.

Risk: The skill covers burnout, sleep problems, crisis resources, possible sleep apnea, alcohol use, and depression flags.

Mitigation: Keep medical guidance conservative, preserve the skill's escalation language, and direct users to qualified professionals or crisis services when red flags appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/mental-reset-suite)
- [Gerber et al., exercise as burnout intervention](https://doi.org/10.1186/1756-0500-6-78)
- [Edinger et al., CBT for adults with insomnia](https://doi.org/10.5664/jsl.8558)
- [Chang et al., evening light-emitting eReaders and sleep](https://doi.org/10.1073/pnas.1418490112)
- [988 Suicide and Crisis Lifeline](https://988lifeline.org/)
- [Open Path Collective](https://openpathcollective.org)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with structured prompts, checklists, reminder actions, and YAML state definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create user-approved reminders and persist burnout, sleep, alcohol-related, and mental-health state across sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
