## Description:

The Horoscope skill helps agents provide Western zodiac forecasts, personality profiles, compatibility readings, and Chinese astrology workflows using local data, the Ohmanda API, and documented taibu MCP integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for daily horoscope lookups, zodiac personality details, compatibility analysis, or Chinese astrology-style readings when taibu MCP is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chinese astrology workflows may involve sharing birth date and time details with the configured taibu MCP provider.

Mitigation: Use taibu MCP features only when users understand what birth details are being shared and trust the configured provider.

Risk: Documented CLI examples may not behave as written because the scripts contain test harnesses instead of argument parsing.

Mitigation: Review script behavior before relying on the CLI examples in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/horoscope)
- [Ohmanda horoscope API](https://ohmanda.com/api/horoscope/{sign}/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted text with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live horoscope text from Ohmanda, local zodiac reference data, or taibu MCP guidance when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
