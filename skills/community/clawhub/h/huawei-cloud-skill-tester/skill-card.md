## Description:

An end-to-end framework for testing Huawei Cloud skills through single-skill checks, multi-skill orchestration, live-environment flows, and structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to assess Huawei Cloud AI Shell skills, test their functions and multi-skill flows, and review consolidated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence, citing risks to command execution, installation cleanup, authorization, and the reliability of its testing claims.

Mitigation: Consider avoiding installation, especially where cloud credentials or valuable existing skill installations are present; if evaluating it, use an isolated environment and review its actions first.

Risk: Real-environment phases can affect Huawei Cloud resources, and write cases can create, update, or delete resources when enabled.

Mitigation: Use a dedicated test account with limited permissions, keep ALLOW_WRITES=0 unless write tests are intentional, and confirm cleanup of any test resources.

Risk: Scanner coverage is partial, so some behavior remains unevaluated and the resulting reports do not establish that a skill is safe or correct.

Mitigation: Treat reports as partial test evidence and independently verify important behaviors and cleanup results.

## Reference(s):

- [Architecture](references/architecture.md)
- [Phase details](references/phase-details.md)
- [Output schema specification](references/output-schema-spec.md)
- [Credential handling protocol](references/agent-protocol.md)
- [Minimum IAM policies](references/iam-policies.md)
- [Huawei Cloud KooCLI guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud SDK reference](https://console.huaweicloud.com/apiexplorer/#/sdkcenter)
- [Huawei Cloud API reference](https://console.huaweicloud.com/apiexplorer/#/openapi)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Structured JSON phase results and consolidated Markdown reports, with Bash commands for running tests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API tests require Huawei Cloud credentials; write operations are gated by ALLOW_WRITES.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
