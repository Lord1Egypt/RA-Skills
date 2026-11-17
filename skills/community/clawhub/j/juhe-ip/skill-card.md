## Description:

Queries IPv4 geolocation details including country, province, city, and ISP through the Juhe IP lookup API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer user questions about public IPv4 address location and ISP ownership. It supports single-IP and batch lookup workflows and returns private, reserved, unsupported, or failed query states when lookup is not appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Juhe API key and queried public IP addresses may be sent over plaintext HTTP.

Mitigation: Review the skill before installation and change the script endpoint to HTTPS before using a real API key.

Risk: Passing an API key on the command line can expose it through shell history or process inspection.

Mitigation: Prefer the JUHE_IP_KEY environment variable or a protected local configuration file for key storage.

Risk: Public IP addresses queried through this skill are sent to the Juhe service.

Mitigation: Use the skill only when sending the target IP addresses to Juhe is acceptable for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-ip)
- [Juhe IP API documentation](https://www.juhe.cn/docs/api/id/1)
- [Juhe platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text summaries, tables, and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_IP_KEY. Single-IP output includes a text summary and JSON; batch output includes a table and JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
