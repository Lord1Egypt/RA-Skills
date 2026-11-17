## Description:

This skill helps agents extract structured business data from Google Maps search results through the BrowserAct Google Maps Search API template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to collect business lead details from Google Maps by keyword, language, country, and result limit. It is intended for agent-assisted searches such as finding local businesses and returning structured place information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BrowserAct API keys can be exposed if pasted into chat or stored insecurely.

Mitigation: Configure BROWSERACT_API_KEY through a protected environment variable or secret manager, avoid sharing it in chat, and rotate any key that has already been shared.

Risk: Google Maps search terms, locale settings, and the BrowserAct bearer token are sent to BrowserAct.

Mitigation: Review the data being sent before installation and use the skill only when sharing those values with BrowserAct is acceptable.

Risk: Automated collection from Google Maps can return incomplete, stale, or policy-sensitive business data.

Mitigation: Review returned business details before relying on them for outreach, analytics, or other downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/google-maps-search-api)
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)
- [Google Maps](https://www.google.com/maps)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON-like structured business details printed by a Python script, with Markdown guidance for setup and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and sends search parameters to BrowserAct; automatic retry is limited to one additional attempt for non-authorization failures.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
