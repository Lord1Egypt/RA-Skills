## Description:

Fetch data from social, video, news, finance, productivity, and desktop applications using OpenCLI with Chrome login sessions and Browser Bridge automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellotombruce](https://clawhub.ai/user/hellotombruce)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve website and application data, run OpenCLI commands, and produce structured outputs without configuring separate service APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenCLI automation can access authenticated browser sessions, private account data, desktop applications, messages, posts, purchase-related actions, writes, and deletions.

Mitigation: Use a dedicated browser profile with only the required accounts and require explicit human confirmation before private reads, messages, posts, purchase-related actions, writes, or deletions.

Risk: The security review notes under-disclosed authenticated account access, desktop app control, and unverified install components.

Mitigation: Review the skill before installing, verify the exact npm package and Browser Bridge extension source, and avoid elevated privileges during installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellotombruce/skills/opencli-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured output options including table, JSON, YAML, Markdown, and CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read from or act through authenticated browser sessions and desktop applications.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
