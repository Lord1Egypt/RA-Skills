## Description: <br>
Use the Go2.gg API to create and manage short links, inspect analytics, generate QR codes, configure webhooks, and manage link-in-bio galleries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rakesh1002](https://clawhub.ai/user/Rakesh1002) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, growth teams, and external agents use this skill to operate Go2.gg accounts: create branded short links, retrieve analytics, generate QR assets, manage webhooks, and publish link-in-bio pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using GO2GG_API_KEY can create, update, or delete Go2.gg account resources. <br>
Mitigation: Store the API key in the environment, review proposed account-changing calls before execution, and rotate or revoke the key when access is no longer needed. <br>
Risk: Webhook configuration can send event payloads to external endpoints. <br>
Mitigation: Use trusted HTTPS webhook URLs and verify Go2.gg webhook signatures before acting on received events. <br>
Risk: Short links, QR codes, and galleries can publish or redirect users to public destinations. <br>
Mitigation: Review destination URLs, publication status, expiration, password, and delete operations before making them live. <br>


## Reference(s): <br>
- [Go2.gg API documentation](https://go2.gg/docs/api/links) <br>
- [Go2.gg API keys dashboard](https://go2.gg/dashboard/api-keys) <br>
- [ClawHub Go2.gg skill page](https://clawhub.ai/Rakesh1002/go2gg) <br>
- [Rakesh1002 publisher profile](https://clawhub.ai/user/Rakesh1002) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with cURL and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Go2.gg API requests that require GO2GG_API_KEY; QR generation examples can be unauthenticated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
