## Description:

Helps an agent query Lann Thai Massage stores and services, collect required booking details, and create massage appointments through MCP or a direct booking API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lystrosaurus](https://clawhub.ai/user/lystrosaurus)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an assistant to find Lann Thai Massage locations, compare available massage and spa services, and complete appointment booking after confirming mobile number, store, service, party size, and time.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Booking requests send personal contact details, including a mobile number, to open.lannlife.com.

Mitigation: Collect only the details required for booking, show a masked mobile number during confirmation, and submit only after explicit user approval.

Risk: The included test helpers can call the live booking API and print request or response data.

Mitigation: Run tests only against a reviewed test endpoint or with non-real data, and avoid storing logs that contain booking details.

Risk: Local MCP setup may run an unpinned lann-mcp-server package or source tree.

Mitigation: Use a pinned and reviewed MCP server version, or use the documented remote endpoint after confirming it is trusted for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lystrosaurus/skills/lann-booking-skill)
- [Lann Booking API reference](references/api_reference.md)
- [Booking response templates](assets/booking_template.md)
- [Lann MCP service endpoint](https://open.lannlife.com/mcp)
- [Booking API endpoint](https://open.lannlife.com/mcp/book/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style assistant messages with booking confirmations, MCP/API parameters, and optional shell or client configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects and confirms booking parameters before submission; mobile numbers should be masked in user-visible summaries and logs.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
