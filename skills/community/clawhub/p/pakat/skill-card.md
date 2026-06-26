## Description: <br>
Interact with the Pakat email marketing API to manage mailing lists, subscribers, campaigns, templates, transactional emails, segments, campaign statistics, and delivery logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hadifarnoud](https://clawhub.ai/user/hadifarnoud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing operators use this skill to make authenticated Pakat API requests for email list management, campaign operations, transactional email workflows, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live Pakat account, including account creation, email sending or scheduling, deletions, unsubscribes, and subscriber-data imports. <br>
Mitigation: Require explicit user confirmation before state-changing, destructive, or email-sending actions. <br>
Risk: The Pakat API key grants access to account operations if exposed or reused outside the intended environment. <br>
Mitigation: Store PAKAT_API_KEY securely and restrict it with scoped keys if Pakat supports scoping. <br>
Risk: User-provided HTML content may be unsafe if encoded through shell patterns that interpolate untrusted input. <br>
Mitigation: Use heredocs or temporary files for base64 encoding rather than echoing unsanitized content. <br>


## Reference(s): <br>
- [Pakat Skill Page](https://clawhub.ai/hadifarnoud/pakat) <br>
- [Pakat API Key Page](https://new.pakat.net/customer/api-keys/index) <br>
- [Pakat API Reference](references/api_reference.md) <br>
- [Pakat OpenAPI Specification](references/openapi.json) <br>
- [Pakat Website](https://pakat.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and PAKAT_API_KEY for live Pakat API operations.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
