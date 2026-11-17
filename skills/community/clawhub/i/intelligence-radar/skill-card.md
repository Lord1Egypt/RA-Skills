## Description:

Intelligence Radar extracts a company name, triggers backend intelligence collection, polls for results, returns a sales strategy summary with an H5 report link, and can associate the company with a customer record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Sales employees use this skill to prepare for customer visits, understand recent company developments, analyze partnership opportunities, and generate concise sales talking points from public information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords and cached authentication tokens.

Mitigation: Use only where chat-based password handling is formally accepted or replaced, and protect token storage according to local policy.

Risk: The skill makes remote backend requests and depends on trusted service endpoints.

Mitigation: Install only in a controlled environment after verifying the backend IP and enforcing HTTPS.

Risk: The skill may persist agent configuration by registering itself in AGENTS.md.

Mitigation: Remove that persistence behavior or explicitly approve it before deployment.

Risk: The skill can create customer records.

Mitigation: Require clear user confirmation with the company name before customer creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/intelligence-radar)
- [Format templates](artifact/references/format-templates.md)
- [Mapping rules](artifact/references/mapping-rules.md)
- [Example transformation](artifact/examples/example-transformation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with inline report links and operational shell/API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include progress updates, sales strategy bullets, an H5 report URL, and customer-add confirmation prompts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
