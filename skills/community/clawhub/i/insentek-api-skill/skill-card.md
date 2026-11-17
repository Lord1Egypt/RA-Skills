## Description:

Enables agents to query Insentek OpenAPI IoT device data, including device lookup, latest and historical readings, trend analysis, comparisons, and file exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xddcode](https://clawhub.ai/user/xddcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to retrieve and analyze Insentek IoT device telemetry through an agent interface. It supports conversational queries, reports, cross-device comparisons, and CSV, Excel, JSON, or HTML export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Insentek API credentials are stored on the user's machine and could be exposed through shell history, logs, generated URLs, or unsafe sharing.

Mitigation: Use the interactive login flow, never send appid or secret in agent chat, avoid command-line secret flags, and rotate credentials if exposure is suspected.

Risk: Changing INSENTEK_API_BASE can direct credentialed requests to an endpoint outside the default Insentek OpenAPI service.

Mitigation: Keep the default HTTPS endpoint unless the replacement endpoint is fully trusted and controlled by the user or organization.

Risk: Large telemetry exports or reports can contain sensitive operational device data.

Mitigation: Prefer summarized chat output, use file exports intentionally, and review generated CSV, Excel, JSON, or HTML files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xddcode/skills/insentek-api-skill)
- [Publisher profile](https://clawhub.ai/user/xddcode)
- [Insentek OpenAPI reference](reference/api-doc.md)
- [Interaction guide](docs/interaction.md)
- [Analysis and report guide](docs/analysis.md)
- [Script usage guide](scripts/README.md)
- [Insentek OpenAPI endpoint](https://openapi.ecois.info)
- [E eco cloud portal](https://cloud.ecois.info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with JSON from helper scripts and optional CSV, Excel, JSON, or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires locally configured Insentek API credentials and Python 3.10+ for script execution; raw data shown in chat is limited by the artifact's guardrails.]

## Skill Version(s):

1.2.2 (source: server release evidence, SKILL.md frontmatter, skill.json, package.json, README, CHANGELOG released 2026-05-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
