## Description: <br>
Configure multiple messaging platform accounts for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devilsen](https://clawhub.ai/user/devilsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add, merge, and verify configuration for multiple messaging accounts across supported channels while preserving existing accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow collects and applies messaging platform credentials, including bot tokens and account identifiers. <br>
Mitigation: Provide only the credentials needed for the accounts being added, require token redaction in output, and review the proposed configuration before applying it. <br>
Risk: Open messaging policies can expose an agent to unintended direct messages or group traffic. <br>
Mitigation: Use allowlists or closed/admin-only group policies unless broader access is intentional. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive credential placeholders; user-provided tokens should be redacted in responses and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
