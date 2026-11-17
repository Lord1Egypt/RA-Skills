## Description:

Query Indian NPS (National Pension System) fund NAV data, scheme info, returns, and history via the free npsnav.in REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanaksinghal](https://clawhub.ai/user/kanaksinghal)

### License/Terms of Use:


## Use Case:

Developers, analysts, and finance users use this skill to look up Indian NPS scheme NAV, scheme information, returns, and historical fund data through the npsnav.in public API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the examples sends requested scheme codes or search terms to npsnav.in.

Mitigation: Avoid sending sensitive or unnecessary query terms, and confirm the external data-sharing posture before use.

Risk: The skill returns public fund data that may be delayed, incomplete, or unsuitable as the sole basis for financial decisions.

Mitigation: Verify important values against authoritative NPS, Protean eGov Technologies, or NPS Trust sources before acting on them.

Risk: The artifact describes the API as free for non-commercial use.

Mitigation: Review npsnav.in usage terms before business, commercial, or redistribution use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kanaksinghal/skills/npsnav)
- [Publisher profile](https://clawhub.ai/user/kanaksinghal)
- [npsnav.in](https://npsnav.in)
- [npsnav API base URL](https://npsnav.in/api)
- [NPS funds list](https://npsnav.in/nps-funds-list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl and jq examples, plus plain-text or JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; no authentication or API keys are required.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
