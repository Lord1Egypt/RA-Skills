## Description: <br>
Bash CLI wrapper and OpenClaw skill for Massive's public REST API that helps Codex or OpenClaw agents query Massive market-data endpoints from shell workflows, use OpenClaw-style secret references, keep logs free of secrets, and integrate JSON responses into agent pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to query Massive market-data REST endpoints from shell workflows with JSON output, pagination support, OpenClaw-style credential inputs, and safe logging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published bundle is missing the main scripts/massive executable that the skill instructs agents to run. <br>
Mitigation: Do not install this bundle as-is; ask the publisher to provide a complete package including scripts/massive before use. <br>
Risk: The missing executable prevents direct review of API-key handling, SecretRef exec support, logging redaction, and allowed network destinations. <br>
Mitigation: Review the supplied executable for credential handling, secret redaction, and network destination controls before deployment. <br>


## Reference(s): <br>
- [Massive REST Usage Notes](references/massive-api.md) <br>
- [OpenClaw Secrets Integration](references/openclaw-secrets.md) <br>
- [Security Requirements](references/security.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/oscraters/massive) <br>
- [Publisher Profile](https://clawhub.ai/user/oscraters) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline bash commands; CLI responses are JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects bash, curl, jq, and a Massive API key supplied through MASSIVE_API_KEY_REF or MASSIVE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
