## Description:

Chuck Norris jokes - random, by category, or keyword search from chucknorris.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Chuck Norris jokes through agent tools, including random jokes, category-based jokes, category listings, and keyword search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned remote MCP bridge package.

Mitigation: Review the bridge before installation, prefer a pinned and reviewed version, and run it in a sandbox with limited filesystem, environment-variable, and network access.

Risk: The explicit joke category may return adult or offensive content.

Mitigation: Avoid the explicit category unless that content is intentional for the deployment.

## Reference(s):

- [Pipeworx Chuck Norris Pack](https://pipeworx.io/packs/chucknorris)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-chucknorris)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Text or JSON responses from MCP tool calls, with JSON MCP configuration for setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl according to metadata; example setup uses an MCP remote bridge.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
