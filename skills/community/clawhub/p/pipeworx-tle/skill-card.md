## Description:

Fetch and search Two-Line Element sets for satellites by NORAD ID or name, providing orbit data for tracking and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, satellite operators, and analysts use this skill to retrieve current TLE orbit data by NORAD catalog ID, search satellites by name or keyword, and inspect recent satellite records for tracking or orbital analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Satellite lookup inputs such as NORAD IDs or search terms are sent to the disclosed Pipeworx gateway.

Mitigation: Confirm the external service is acceptable for the intended workflow and avoid submitting secrets or personal data in tool arguments.

Risk: Returned TLE data may be stale or unsuitable for safety-critical orbital operations without independent validation.

Mitigation: Use retrieved TLEs for tracking and analysis workflows only after checking freshness and validating against authoritative mission or operations data where required.

## Reference(s):

- [ClawHub Pipeworx tle listing](https://clawhub.ai/b-gutman/skills/pipeworx-tle)
- [Pipeworx TLE MCP gateway](https://gateway.pipeworx.io/tle/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses may include satellite names, NORAD IDs, epoch dates, and TLE line data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
