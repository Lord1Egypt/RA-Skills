## Description:

Calculate comprehensive numerology reports using Pythagorean or Chaldean systems, with support for English, Tamil, Telugu, Kannada, and Hindi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an OpenClaw agent to request name and birth-date numerology readings, lucky number calculations, and Pythagorean or Chaldean interpretations in supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends full name, birth date, language choice, session identifier, userId, and timestamp to portal.toolweb.in.

Mitigation: Tell users before the first request what data will be sent and avoid processing another person's personal details unless that person has agreed.

Risk: API calls may consume paid quota through the configured ToolWeb API key.

Mitigation: Confirm the user intends to make a billable request before calling the API for the first time in a session.

Risk: Interpolating user input into shell curl commands can be unsafe.

Mitigation: Use safe JSON serialization for request bodies and avoid constructing shell commands by directly embedding untrusted user text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/numerology-calculator)
- [ToolWeb API portal](https://portal.toolweb.in)
- [ToolWeb platform](https://toolweb.in)
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/)
- [ToolWeb MCP server](https://hub.toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown numerology report with inline shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends user-provided numerology inputs to portal.toolweb.in.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
