## Description:

Upload files to Giggle asset service and get public/download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload local generated or selected files to the Giggle asset service and return public preview and download URLs to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause agents to upload local files to externally hosted public links too broadly.

Mitigation: Use it only for files intentionally selected for external hosting, and avoid private documents, source code, credentials, logs, or business data unless the file and sharing scope are confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patches429/skills/giggle-files-management)
- [Giggle API](https://api.giggle.pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON upload results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, plus a Giggle asset service API key.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
