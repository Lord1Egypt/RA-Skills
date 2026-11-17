## Description:

Run OSINT investigations from chat - email, username, domain, IP, phone, photo geolocation, plus news, social, and link-graph intelligence - using the osint-mcp tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snuri00](https://clawhub.ai/user/snuri00)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to route authorized OSINT investigations across identifiers, web signals, social sources, image geolocation, and entity-link graphing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install and persistently run mutable external code from GitHub.

Mitigation: Review and pin the osint-mcp source before installing, and prefer an isolated virtual environment or container.

Risk: Person, breach, and geolocation results can be sensitive or uncertain.

Mitigation: Configure only task-specific API keys, treat results as estimates, corroborate findings, and use the skill only for authorized investigations.

## Reference(s):

- [osint-mcp project homepage](https://github.com/snuri00/osint-mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and tool-selection instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference sensitive OSINT results, breach data, and geolocation estimates that require corroboration and authorized use.]

## Skill Version(s):

2.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
