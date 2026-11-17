## Description:

提供蘭泰式按摩（Lann Thai Massage）的门店查询、SPA 服务查询和在线预约功能，覆盖上海、杭州、成都等多城市门店。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lystrosaurus](https://clawhub.ai/user/lystrosaurus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistant builders use this skill to help customers find Lann Thai Massage stores and services, collect required booking details, and submit appointment requests through MCP or direct HTTP API calls.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The setup path can run an unpinned lann-mcp-server package or local package source.

Mitigation: Pin and verify the package source before use, and install only from a trusted Lann MCP server source.

Risk: Bundled test utilities can submit live booking requests with phone numbers.

Mitigation: Run tests only against a test endpoint or controlled environment, and avoid production booking data in test scripts.

Risk: Creating a booking sends phone numbers and appointment details to the Lann remote service.

Mitigation: Get clear user confirmation before submission, collect only required fields, and mask phone numbers in displayed confirmations or logs.

Risk: Server-resolved provenance is unavailable for this release.

Mitigation: Review the artifact contents, publisher profile, and security guidance before installation.

## Reference(s):

- [Lann Booking API Reference](artifact/references/api_reference.md)
- [Booking Confirmation Message Template](artifact/assets/booking_template.md)
- [Remote MCP Endpoint](https://open.lannlife.com/mcp)
- [Direct Booking API Endpoint](https://open.lannlife.com/mcp/book/create)
- [ClawHub Skill Page](https://clawhub.ai/lystrosaurus/skills/lann-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell Commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown responses with JSON request payloads, MCP configuration snippets, and direct API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May transmit phone numbers and booking details to the Lann remote service after user confirmation.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
