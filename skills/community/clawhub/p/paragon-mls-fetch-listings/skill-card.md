## Description:

Fetch all active property listings from a Paragon MLS shared listing GUID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate analysts, developers, and agents use this skill to resolve a Paragon MLS shared link or GUID into the active property listings behind it. It is intended for shared-listing workflows where the individual parsed property records are needed for downstream review or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external local paragon-mls-mcp project and npm build step that are outside the submitted package.

Mitigation: Review and control the referenced MCP source and npm dependencies before installation, run it with low privileges and no sensitive local credentials, and prefer a packaged or integrity-checked executable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/paragon-mls-fetch-listings)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with a bash example; the MCP tool result is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying listing fetch returns a count and parser-normalized properties array.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
