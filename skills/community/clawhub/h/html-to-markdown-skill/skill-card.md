## Description:

Converts HTML content to Markdown from strings, files, and URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert HTML snippets, local HTML files, or fetched web pages into Markdown for documentation migration, content extraction, and saved article workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates conversion to external npm code that may change across installs.

Mitigation: Use a local pinned package version, review the dependency before installation, and avoid versionless global installs for managed environments.

Risk: URL conversion fetches remote pages and may process untrusted or unexpected content.

Mitigation: Review target URLs before conversion and prefer local file conversion when pages require authentication or come from untrusted sources.

Risk: File conversion can write Markdown output to paths chosen during use.

Mitigation: Confirm output paths before running conversion and avoid writing into directories that contain important source files unless intentional.

## Reference(s):

- [Skill page](https://clawhub.ai/sipingme/skills/html-to-markdown-skill)
- [Project GitHub](https://github.com/sipingme/html-to-markdown-skill)
- [npm package](https://www.npmjs.com/package/@siping/html-to-markdown-node)
- [Quick Start Guide](references/quick-start.md)
- [API Documentation](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The delegated converter returns JSON that includes success status, markdown content or error text, and length metadata.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
