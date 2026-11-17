## Description:

Evidence-based techniques for building habits and changing behavior, including starting exercise, quitting unwanted habits, building a daily practice, and making repeated change attempts stick.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get structured habit coaching for building healthy routines, breaking unwanted habits, designing environments, and setting realistic expectations for behavior change. Agents use it to produce practical, evidence-based guidance tailored to the user's habit, constraints, and risk context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access even though release evidence does not show a clear need for that capability.

Mitigation: Install it only in a sandboxed environment, or remove or deny filesystem access unless a reviewed deployment explicitly requires it.

Risk: The install command is unpinned and server-resolved provenance is unavailable.

Mitigation: Use a version-pinned, provenance-checked install path and verify the release hash before deployment.

Risk: Habit coaching can be insufficient when a user describes addiction, compulsive use, or substance withdrawal risk.

Mitigation: Use the skill's referral posture: treat habit techniques as supplementary and direct the user to appropriate professional or crisis support resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/habit-formation)
- [Publisher profile](https://clawhub.ai/user/howtousehumans)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured explanations, examples, action plans, and referral language when habit coaching may be insufficient.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No generated files or external API calls are described by the skill; it provides conversational coaching content.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
