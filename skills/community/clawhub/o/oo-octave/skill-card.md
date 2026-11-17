## Description:

Use this skill for any Octave request, including reading, creating, and updating data, instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to read Octave workspace information and run supported Octave agent actions, including updates where appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code and introduce broader agent changes without clear approval.

Mitigation: Review and pin the CLI installation, inspect changes to other agent skills, connect only the intended Octave workspace, and retain confirmation for data changes.

## Reference(s):

- [Octave homepage](https://www.octavehq.com/)
- [Octave API quickstart](https://docs.octavehq.com/quickstart)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [JSON connector results with natural-language summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions marked write can change Octave data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
