## Description: <br>
Provides Lerwee monitoring system API integration guidance, signature-authenticated request examples, and a Python client for monitoring objects, alerts, events, agents, users, and related operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lerwee](https://clawhub.ai/user/Lerwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to configure signed Lerwee API requests, call documented monitoring and operations endpoints, and adapt the included Python client for controlled integration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad administrative and remote-control operations can change or delete resources, alter users and roles, install or uninstall agents, close alerts, modify CMDB or network data, or execute scripts. <br>
Mitigation: Use least-privilege credentials and require explicit human confirmation before destructive or privileged operations. <br>
Risk: The security evidence reports weak safety guidance and insecure example credential handling, including an HTTP private-IP endpoint and credential-like examples in the artifact. <br>
Mitigation: Replace examples with a trusted HTTPS endpoint, remove credential-like values, and rotate any credential that resembles the examples before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lerwee/lerwee-api) <br>
- [API endpoint reference](artifact/references/api_endpoints.md) <br>
- [Monitoring API details](artifact/references/api_details_monitor.md) <br>
- [Device detection API details](artifact/references/api_details_device.md) <br>
- [Alert and event API details](artifact/references/api_details_alert.md) <br>
- [Business view and topology API details](artifact/references/api_details_business.md) <br>
- [User and permission API details](artifact/references/api_details_user.md) <br>
- [Monitoring types reference](artifact/references/monitoring_types.md) <br>
- [Error codes reference](artifact/references/error_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces signed API request guidance and client-code examples for Lerwee environments; responses from called APIs are JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
