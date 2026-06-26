## Description: <br>
Query, create, and manage Notion databases and pages using the 2025-09-03 API format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-tw](https://clawhub.ai/user/kai-tw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query Notion databases, create database entries, update page properties, and add content blocks through the Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion API key can read or edit every page or database shared with the integration. <br>
Mitigation: Use a dedicated least-privilege Notion integration and share only the specific pages or databases intended for the task. <br>
Risk: Batch updates or page writes can change Notion content unexpectedly. <br>
Mitigation: Review proposed updates before running them and test against non-critical pages or databases first. <br>
Risk: Untrusted text or property names passed into the shell helper can lead to malformed JSON or unsafe requests. <br>
Mitigation: Do not pass untrusted text directly into the helper; validate Notion IDs and use jq-based escaping for JSON values. <br>
Risk: A local plaintext API token can be exposed through weak file permissions. <br>
Mitigation: Store the token only at the configured secret path and restrict it with chmod 600. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kai-tw/notion-2025-api) <br>
- [API reference](references/API_REFERENCE.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Security report](SECURITY.md) <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion 2025 API upgrade guide](https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands, curl requests, and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; requires a Notion API key stored at the configured local secret path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
