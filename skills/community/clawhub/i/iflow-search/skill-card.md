## Description:

Web search, image search, and webpage content fetch via the iFlow Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflow-ai](https://clawhub.ai/user/iflow-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the web, search images, and fetch readable webpage content through the iFlow Search API when current or URL-specific information is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and fetched URLs are sent to the iFlow Search API.

Mitigation: Avoid submitting sensitive queries or confidential URLs unless that data sharing is acceptable for the deployment.

Risk: The documented setup can expose or persist the iFlow API key in shell history or shell configuration.

Mitigation: Use protected secret storage or a temporary environment variable, and do not print the API key during setup checks.

Risk: The shell scripts build JSON request bodies from command-line input.

Mitigation: Avoid attacker-controlled inputs and validate result counts until the scripts use safe JSON encoding.

## Reference(s):

- [iFlow Search skill homepage](https://github.com/iflow-ai/iflow-skills/tree/main/skills/iflow-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IFLOW_API_KEY and network access to the iFlow Search API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
