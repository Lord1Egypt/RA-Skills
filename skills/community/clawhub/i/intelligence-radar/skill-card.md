## Description: <br>
Collects and analyzes public company intelligence for sales teams, returning a strategy summary, an H5 report link, and customer-record follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales employees use this skill to prepare for customer visits, research company updates, identify cooperation opportunities, and generate concise sales strategy prompts from recent public intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Employee credentials and bearer tokens may be exposed because the skill asks for passwords in chat, sends credentials to a configured HTTP service, and caches shared tokens locally. <br>
Mitigation: Install only when the backend operator is trusted; prefer authentication outside chat, HTTPS-only endpoints, per-skill scoped token storage, and restrictive token-cache permissions. <br>
Risk: Company queries, user prompts, and collected intelligence are sent to a configured backend service for analysis. <br>
Mitigation: Confirm users are comfortable sending this data to the service, minimize sensitive inputs, and review organizational data-sharing requirements before use. <br>
Risk: The skill can modify customer records by creating a customer entry after the user replies to add it. <br>
Mitigation: Require explicit confirmation before record creation and scope the token used by the skill to only the customer actions it needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/intelligence-radar) <br>
- [Format templates](references/format-templates.md) <br>
- [Mapping rules](references/mapping-rules.md) <br>
- [Example transformation](examples/example-transformation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with progress messages, sales-strategy bullets, H5 report links, and optional shell/API command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and python3 on linux or darwin; may cache employee bearer tokens locally and call a configured HTTP service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
