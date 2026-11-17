## Description:

UK street-level crime data: reported crimes by location, police force directory, and case outcomes from data.police.uk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, journalists, researchers, and public-interest analysts use this skill to query UK street-level crime reports, police force listings, and case outcomes for location-based analysis and applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration runs an unpinned npm package automatically, allowing mutable third-party code to execute locally.

Mitigation: Pin mcp-remote to a reviewed exact version or run it in a restricted environment with minimal filesystem, environment-variable, and credential access.

## Reference(s):

- [Pipeworx UK Police Pack](https://pipeworx.io/packs/ukpolice)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-ukpolice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP configuration snippets and curl examples for invoking UK police-data tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
