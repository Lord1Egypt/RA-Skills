## Description:

Provides current time for IANA timezones or IP-based geolocation, lists IANA timezone strings, and converts datetimes between timezones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer timezone questions, convert meeting times, enumerate valid IANA timezone identifiers, and perform IP-based timezone lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP-based timezone lookup sends the queried IP address to gateway.pipeworx.io.

Mitigation: Use timezone-name lookup or conversion for sensitive cases; only use IP lookup with addresses you are comfortable sharing with the service.

## Reference(s):

- [Pipeworx Timezone Skill](https://clawhub.ai/b-gutman/skills/pipeworx-timezone)
- [Publisher Profile](https://clawhub.ai/user/b-gutman)
- [Timezone MCP endpoint](https://gateway.pipeworx.io/timezone/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Text responses, Markdown examples, and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timezone outputs can include datetimes, UTC offsets, offset differences, and IANA timezone identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
