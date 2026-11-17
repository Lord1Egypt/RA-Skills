## Description:

Use when preparing for a job interview with a JD and your background — turns the STAR method from vague advice into a build system: mines your history for evidence, generates question-predictions from the JD, drafts STAR stories with a weak-spot flag on every answer, and pressure-tests with follow-up chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Job seekers and employees preparing for behavioral interviews can organize their experience into STAR stories, anticipate questions from a job description, and practice interviewer follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The story bank is stored as plaintext and may contain confidential employer or customer details.

Mitigation: Keep confidential employer or customer details out of the story bank, and back it up before modifying it.

Risk: A generated inline shell shortcut may be unreliable if copied directly.

Mitigation: Use the provided script and export stories to JSON for scoring instead of copying the generated shortcut.

## Reference(s):

- [Interview Forge Deep Reference](references/forge-guide.md)
- [ClawHub Skill Release](https://clawhub.ai/voronindenis5/skills/interview-answer-forge)
- [Publisher Profile](https://clawhub.ai/user/voronindenis5)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON, Shell commands]

**Output Format:** [Plain-text coaching feedback and prompts; JSON story data; shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Feedback depends on the supplied job description and story data and can include STAR section budgets, rule flags, and follow-up prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
