## Description:

Explores authorized, publicly visible website pages, captures screenshots, layout, interactions, and assets, then guides agents to build a static or client-side frontend visual replica without backend or non-public content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zai-org](https://clawhub.ai/user/zai-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to document and approximate the frontend visual presentation of websites they own or are explicitly authorized to replicate. It is intended for static or client-side mockups, design study, and frontend reconstruction, not backend behavior or non-public content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can interact with page controls during exploration, including controls that may submit forms, trigger account actions, or leave the target domain.

Mitigation: Run in an isolated browser profile with no saved credentials or payment data, and require manual approval before clicking forms, action buttons, or external navigation.

Risk: The workflow downloads discovered assets, which can fetch unexpected files or an excessive number of files.

Mitigation: Restrict downloads to safe http/https URLs from expected hosts, apply size and count limits, and review or scan downloaded files before reuse.

Risk: Website visual replication can create copyright, terms-of-service, or privacy issues if used without authorization or against restricted content.

Mitigation: Require explicit authorization before use, respect robots.txt and rate limits, avoid login-protected areas, and exclude credentials, personal data, and copyrighted text unless rights are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zai-org/skills/glmv-web-replication)
- [Publisher profile](https://clawhub.ai/user/zai-org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and generated frontend files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a website replication blueprint and frontend-only static or client-side replica; excludes backend behavior, authentication, databases, credentials, and non-public content.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
