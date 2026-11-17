## Description:

Lint Markdown files for formatting issues, broken links, and style consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to check Markdown files for formatting, style, and link issues before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional external link checking makes outbound requests to URLs found in Markdown files.

Mitigation: Leave --check-external-links disabled for untrusted Markdown or run the skill in a sandbox that blocks localhost, private IP ranges, metadata endpoints, unsafe redirects, and excessive URL checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/markdown-linter-cli)
- [Publisher profile](https://clawhub.ai/user/derick001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON lint report with file-level issues, severities, suggested fixes, and summary counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable line length, ignored rules, globbed inputs, and optional external link checking.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
