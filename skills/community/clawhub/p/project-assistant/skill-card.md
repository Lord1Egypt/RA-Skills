## Description:

Project Assistant helps agents initialize software projects, analyze project structure, answer implementation questions, manage reusable project Q&A, and produce documentation update suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcipher](https://clawhub.ai/user/northcipher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, testers, DevOps engineers, and product stakeholders use this skill to understand an existing project, initialize project documentation, find code locations, assess change impact, and preserve project Q&A for later reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write .claude project state, generated documentation, Q&A cache files, and local configuration.

Mitigation: Run it only in intended project directories and review generated or modified files before relying on them.

Risk: The skill scans project configuration and environment files and may encounter secrets.

Mitigation: Avoid running it on untrusted repositories or projects containing secrets until path containment, secret redaction, and opt-in secret scanning are fixed.

Risk: Feishu tokens may be stored in local JSON configuration.

Mitigation: Use least-privilege tokens, avoid shared machines for token-bearing configs, and rotate tokens if local configuration may have been exposed.

## Reference(s):

- [Project Assistant homepage](https://github.com/Northcipher/project-assistant)
- [Configuration guide](references/guides/config.md)
- [Project initialization guide](references/guides/init.md)
- [Q&A documentation guide](references/guides/qa.md)
- [Feishu documentation guide](references/guides/feishu.md)
- [Example conversations](references/guides/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands, file paths, generated project documentation, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project documentation, Q&A cache files, and local configuration state when the user invokes the corresponding workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
