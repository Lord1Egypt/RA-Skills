## Description:

Interview Coach helps users prepare for job interviews with mock interviews, role-specific questions, answer feedback, STAR-method practice, salary negotiation guidance, confidence support, and local progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this skill to practice interviews, improve behavioral and technical answers, prepare follow-up messages, and track weak areas and practice history locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores interview-prep profile details, practice answers, scores, and weak areas in local files.

Mitigation: Review or delete ~/.openclaw/interview-coach when that local history should no longer be retained.

Risk: The broad help trigger may activate the skill more often than intended.

Mitigation: Use explicit interview-prep requests when invoking it and review responses before relying on saved progress or guidance.

Risk: Company-specific preparation is based on general knowledge and not real-time company data.

Mitigation: Verify company facts, interview processes, and role requirements against current official or recruiter-provided information.

## Reference(s):

- [Interview Coach ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/interview-coach-ai)
- [Publisher profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown-style conversational guidance with occasional JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local profile, practice history, weak areas, and saved-answer files under ~/.openclaw/interview-coach.]

## Skill Version(s):

1.1.0 (source: server release metadata; changelog: v1.1.0 - Removed exec permission)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
