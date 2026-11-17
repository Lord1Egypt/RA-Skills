## Description:

Vedic astrology REST API integration for Panchanga, Kundali, KP system, aspects, dasha, muhurta, compatibility, transits, remedies, calendars, and related Jyotish workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[degen0root](https://clawhub.ai/user/degen0root)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let agents register for and call PanchangaAPI endpoints for Vedic astrology readings, calendars, timing recommendations, compatibility checks, and chart analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Astrology requests may send sensitive birth date, birth time, and location data to api.moon-bot.cc.

Mitigation: Use the skill only with informed user consent and avoid sending more personal data than the requested astrology workflow requires.

Risk: The skill describes automated paid requests and payment-link flows.

Mitigation: Require explicit user approval for the amount, account, and payment method before allowing an agent to pay or create payment links.

Risk: Reusable API keys may be exposed in URLs, Telegram links, logs, or shared transcripts.

Mitigation: Keep API keys in headers or environment variables, redact them from logs, and avoid embedding reusable keys in URLs or chat links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/degen0root/skills/panchanga-api)
- [PanchangaAPI homepage](https://api.moon-bot.cc)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request examples and shell command examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current date/time handling and may use PANCHANGA_API_KEY for authenticated requests.]

## Skill Version(s):

4.3.0 (source: ClawHub server release evidence; artifact frontmatter says 4.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
