## Description:

Guides agents through building Hugo blogs optimized for AI-readable pages, RSS feeds, minimal templates, and nginx deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byron-mckeeby](https://clawhub.ai/user/byron-mckeeby)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create and deploy a Hugo blog with agent-readable content structure, metadata, RSS output, and nginx configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daily update workflow includes administrator-level nginx validation and reload commands.

Mitigation: Run nginx validation and reload as separate administrator-approved deployment steps with an explicit confirmation or deployment gate.

Risk: The Hugo configuration enables raw HTML rendering.

Mitigation: Keep raw HTML disabled unless required, and review or sanitize any content that needs raw HTML.

Risk: Generated post titles are written into content and filenames.

Mitigation: Validate or escape post titles before generating content files.

Risk: The nginx example enables access logging for agent traffic.

Mitigation: Set log retention, privacy, and access policies before enabling production access logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/byron-mckeeby/skills/hugo-blog-agent)
- [Ananke Hugo theme](https://github.com/theNewDynamic/gohugo-theme-ananke)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, TOML, HTML, YAML, nginx, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, content generation, RSS, nginx, validation, and operations guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
