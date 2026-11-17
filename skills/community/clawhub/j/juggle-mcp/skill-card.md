## Description:

Reads a Juggle family account from a shell, including bookings, sitter information, conversations, payment summaries, and public location rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Families use this skill to retrieve their Juggle babysitting and petsitting account information from a shell when the Juggle MCP tools are unavailable or when a script needs the data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the test-server setting could expose the Juggle password through a faulty host check.

Mitigation: Keep JUGGLE_BASE_URL unset and use separate dummy credentials for testing until parsed-host validation is fixed.

Risk: Raw account responses may contain private personal or payment data.

Mitigation: Prefer the named commands, which apply privacy allowlists, over raw get.

## Reference(s):

- [Juggle service](https://whyjuggle.com)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/juggle-mcp)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON account data with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account data; named commands filter sensitive fields.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
