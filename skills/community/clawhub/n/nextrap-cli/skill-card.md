## Description:

Use Nextrap CLI to investigate public attack intelligence by IP, URL, or product name. Search the product catalog and request logs, inspect context and path statistics, or manage CLI authentication and updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextrap-net](https://clawhub.ai/user/nextrap-net)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use the skill to investigate public request intelligence using IP addresses, URLs, product names, and existing log identifiers. It helps summarize observed activity and its limits, with CLI commands for reproducibility when useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has partial scan coverage and notes an unresolved local path-like reference.

Mitigation: Review the unresolved reference and scan coverage before installing. For CLI downloads, follow the skill's installation guidance to verify the archive against the matching release checksums.

## Reference(s):

- [Business interpretation and investigation limits](references/business.md)
- [Query inputs and scope](references/query.md)
- [Log records and context](references/log.md)
- [Machine output and result interpretation](references/output.md)
- [CLI installation instructions](references/install.md)
- [Nextrap CLI releases](https://github.com/nextrap-net/nextrap-cli/releases/latest)
- [Nextrap CLI installation page](https://www.nextrap.net/developer#cli-install)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown findings with relevant evidence and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains query scope and evidence limits; does not treat observed requests as proof of successful attacks.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
