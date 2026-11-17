## Description:

Insentek OpenAPI lets agents query Insentek and E Ecology IoT device data in natural language, including real-time and historical sensor readings, trend analysis, cross-device comparisons, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xddcode](https://clawhub.ai/user/xddcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators with configured Insentek credentials use this skill to query, analyze, compare, and export IoT device data from Insentek-compatible deployments. Developers can also use it to install the skill, configure local authentication, and route agent requests through the provided CLI scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if the API endpoint or command arguments are influenced.

Mitigation: Install only from a trusted publisher, keep INSENTEK_API_BASE and --api-base pointed at the official HTTPS API, and avoid passing tokens on the command line.

Risk: Local credential material remains sensitive even when encrypted.

Mitigation: Protect ~/.config/insentek/credentials.json, maintain restrictive local file access, and clear credentials with the skill logout command when access is no longer needed.

Risk: Raw IoT data can be overexposed in conversation if full result sets are pasted into chat.

Mitigation: Use the skill's summary and row-limit behavior for chat responses, and export large or raw datasets to CSV, Excel, JSON, or HTML files instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xddcode/skills/insentek-openapi)
- [Insentek OpenAPI base URL](https://openapi.ecois.info)
- [E Ecology cloud console](https://cloud.ecois.info)
- [Getting started guide](docs/getting-started.md)
- [Interaction guide](docs/interaction.md)
- [Analysis guide](docs/analysis.md)
- [Platform setup guide](docs/platform-setup.md)
- [OpenAPI reference](reference/api-doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with shell commands, JSON previews, CSV/Excel/JSON exports, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation output is summarized with row limits; full raw data is directed to file exports.]

## Skill Version(s):

1.2.4 (source: server release evidence, SKILL.md frontmatter, skill.json, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
