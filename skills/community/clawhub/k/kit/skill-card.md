## Description: <br>
Kit (formerly ConvertKit) API integration with managed OAuth for managing email subscribers, forms, tags, sequences, broadcasts, and custom fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to manage Kit email marketing resources through Maton-managed OAuth, including subscribers, tags, forms, sequences, broadcasts, custom fields, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY and can access subscriber and customer data in the connected Kit account. <br>
Mitigation: Install only when the user trusts Maton with the connected Kit account, keep MATON_API_KEY private, and avoid exposing credentials in logs or shared transcripts. <br>
Risk: Create, update, delete, broadcast, webhook, or subscriber-modification actions can change email marketing data or trigger downstream effects. <br>
Mitigation: Require explicit user confirmation of the target resource and intended effect before executing any write, delete, broadcast, webhook, or subscriber-modification action. <br>
Risk: When multiple Kit connections exist, requests may affect the wrong account if no connection is specified. <br>
Mitigation: Use the Maton-Connection header to select the intended connection before making account-specific requests. <br>


## Reference(s): <br>
- [Kit Skill on ClawHub](https://clawhub.ai/byungkyu/kit) <br>
- [Kit API Overview](https://developers.kit.com/api-reference/overview) <br>
- [Kit API Subscribers](https://developers.kit.com/api-reference/subscribers/list-subscribers) <br>
- [Kit API Tags](https://developers.kit.com/api-reference/tags/list-tags) <br>
- [Kit API Forms](https://developers.kit.com/api-reference/forms/list-forms) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline HTTP paths, JSON examples, and Python, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Kit account through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
