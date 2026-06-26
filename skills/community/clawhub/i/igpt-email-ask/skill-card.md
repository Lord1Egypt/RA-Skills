## Description: <br>
Secure, per-user-isolated email reasoning and analysis via the iGPT Context Engine API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sammy-spk](https://clawhub.ai/user/Sammy-spk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to ask questions over connected email context, summarize threads, extract action items and decisions, assess sentiment or risk, and produce text or structured JSON answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to sensitive connected email data and an iGPT API key. <br>
Mitigation: Install only when the user trusts iGPT for the connected mailbox, use the intended API key, and revoke the datasource when access is no longer needed. <br>
Risk: Email summaries, action items, and sentiment or risk assessments may be incomplete or misleading. <br>
Mitigation: Verify important conclusions against the original emails before acting on them. <br>
Risk: The required SDK adds a local Python dependency. <br>
Mitigation: Install the SDK in an isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sammy-spk/igpt-email-ask) <br>
- [iGPT Playground](https://igpt.ai/hub/playground/) <br>
- [iGPT API keys](https://igpt.ai/hub/apikeys/) <br>
- [iGPT documentation](https://docs.igpt.ai) <br>
- [iGPT Ask API reference](https://docs.igpt.ai/docs/api-reference/ask) <br>
- [iGPT security model](https://docs.igpt.ai/docs/security/model) <br>
- [igptai Python SDK](https://pypi.org/project/igptai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell setup commands, text responses, JSON, schema-validated JSON, and streaming SSE chunks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IGPT_API_KEY and a connected email datasource; supports quality tiers and normalized error objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
