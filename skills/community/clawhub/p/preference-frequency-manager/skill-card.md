## Description:

Designs subscriber preference centers and frequency opt-down ladders, including topic and cadence choices, preference-to-suppression mappings, and a SEND N sub-item note for preference-center and frequency options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, lifecycle, and email operations practitioners use this skill to design preference centers and unsubscribe opt-down paths that offer topic selection, cadence reduction, pause options, and explicit suppression or frequency rules. It helps preserve a reachable one-click unsubscribe while giving fatigued subscribers lighter alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process email preference, opt-out, and consent-related data.

Mitigation: Use sanitized exports where possible and avoid including unnecessary personal or sensitive subscriber data.

Risk: Incorrect suppression or cadence rules could affect subscriber consent handling or email frequency.

Mitigation: Review proposed suppression, pause, cadence, and topic rules before applying them in an ESP or consent registry.

Risk: Memory handoffs could persist preference-center planning details longer than intended.

Mitigation: Confirm before saving memory notes and limit saved details to the operational summary needed for follow-up work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/preference-frequency-manager)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured preference-center specifications, opt-down ladders, rule mappings, SEND N sub-item notes, and handoff summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose memory handoffs and pending decisions; no hidden code execution behavior is disclosed in the security evidence.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
