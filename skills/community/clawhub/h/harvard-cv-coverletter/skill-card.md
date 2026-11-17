## Description:

Creates Harvard-standard CVs, resumes, and cover letters as .docx files using user-provided information and Harvard Office of Career Services formatting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midnightstudioai](https://clawhub.ai/user/midnightstudioai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and career-document authors use this skill to turn supplied background details into Harvard-style resumes, CVs, and cover letters without inventing missing personal information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install an unpinned npm package globally, persistently changing the runtime environment.

Mitigation: Use a pinned project-local dependency or require explicit approval before any global npm installation.

Risk: Generated resumes and cover letters may contain sensitive personal information.

Mitigation: Review output paths and final documents carefully before sharing or deploying the skill in shared environments.

## Reference(s):

- [Harvard Office of Career Services](https://ocs.fas.harvard.edu)
- [ClawHub Skill Page](https://clawhub.ai/midnightstudioai/skills/harvard-cv-coverletter)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the docx npm package v9+; generated documents may contain sensitive personal information.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
