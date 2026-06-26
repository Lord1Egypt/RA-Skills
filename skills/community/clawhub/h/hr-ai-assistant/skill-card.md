## Description: <br>
HR AI Assistant helps agents answer HR questions and generate HR policies, forms, job descriptions, reports, and related documents through the HRrule AI service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aijuntao](https://clawhub.ai/user/aijuntao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR staff, managers, and business users use this skill to request HR consultation, labor-law-oriented Q&A, and draft HR documents such as employee handbooks, job descriptions, performance forms, compensation materials, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HR prompts and document context may contain employee, compensation, legal, or company-confidential information that is sent to HRrule. <br>
Mitigation: Minimize sensitive details before use and confirm that the organization is comfortable sending the content to HRrule. <br>
Risk: API keys may be exposed if pasted into chat or stored in an overly broad local configuration file. <br>
Mitigation: Use a protected HRRULE_API_KEY environment variable or a carefully permissioned config file, and avoid sharing real API keys in chat transcripts. <br>
Risk: The skill can produce generated document links or downloaded attachments that may contain sensitive or unreviewed content. <br>
Mitigation: Review generated attachments before opening, sharing, or relying on them for HR decisions. <br>
Risk: Credential transmission through query-string API keys can be logged by clients, proxies, or services. <br>
Mitigation: Prefer wss:// endpoints and avoid query-string API keys where the integration allows a safer authentication method. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aijuntao/hr-ai-assistant) <br>
- [HRrule AI service](https://ai.hrrule.com/) <br>
- [HRrule AI WebSocket API Reference](references/api_reference.md) <br>
- [HRrule AI Example Prompts](references/example_prompts.md) <br>
- [Installation Guide](INSTALL.md) <br>
- [Usage Guide](USAGE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and streamed text with optional code blocks, shell commands, and generated document download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call HRrule over WebSocket, stream responses, and return links or downloaded attachments when the HRrule service provides generated files.] <br>

## Skill Version(s): <br>
2.5.9 (source: server release evidence and CHANGELOG.md, released 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
