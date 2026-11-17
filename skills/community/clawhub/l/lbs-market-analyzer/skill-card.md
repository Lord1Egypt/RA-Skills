## Description:

Comprehensive geo-spatial market intelligence and site selection evaluation using AMAP (Gaode) LBS API for competitor distribution, site selection, flow analysis, market gap identification, and AMAP API key provisioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raphaelxiao](https://clawhub.ai/user/raphaelxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business operators use this skill to fetch AMAP point-of-interest data and turn it into competitor density, site selection, traffic-flow, and market-gap analysis for a target address or trade area.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The key automator can open an AMAP browser session, create an AMAP application, and generate a Web Service key.

Mitigation: Run the automator only in a trusted local environment, or manually provide AMAP_KEY through an approved secret-management workflow.

Risk: The skill can persist the AMAP key in .env and browser login state in ./amap_session.

Mitigation: Treat .env and ./amap_session as sensitive, keep them out of source control and shared folders, and rotate any exposed key.

Risk: Live analysis depends on AMAP API availability, quota, and key validity.

Mitigation: Check AMAP status/error codes and validate quota and key configuration before relying on analysis output.

## Reference(s):

- [Analysis Logic](references/analysis-logic.md)
- [AMAP API Reference](references/amap-api-guide.md)
- [AMAP Developer Console](https://console.amap.com/dev/key/app)
- [AMAP REST API Base URL](https://restapi.amap.com/v3)
- [ClawHub Skill Page](https://clawhub.ai/raphaelxiao/skills/lbs-market-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
