## Description:

OpenTelemetry ingestion skill for Huawei Cloud AgentArts observability that helps configure traces, metrics, logs, GenAI semantic conventions, SDK or Collector setup, and ingestion diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to connect Java, Python, Node.js, Go, or Collector-based OpenTelemetry telemetry from AI and application workloads into Huawei Cloud AgentArts agent-ops. It also guides verification of ingestion paths, GenAI span attributes, IAM permissions, and troubleshooting checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live cloud mutations and privileged internal API examples.

Mitigation: Use a sandbox or least-privilege Huawei Cloud project first, verify the internal deliverConfig API and te_admin role requirement with Huawei Cloud documentation or an administrator, and confirm cleanup steps for created businesses and forwarding configs.

Risk: Telemetry can include prompts, personally identifiable information, secrets, or business tokens if instrumentation is configured carelessly.

Mitigation: Keep IAM credentials and business tokens out of logs and config files, review exported telemetry for sensitive data before enabling export, and avoid placing full prompts, responses, passwords, keys, or PII in trace attributes.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [IAM policies](artifact/references/iam-policies.md)
- [OpenTelemetry GenAI semantic conventions](artifact/references/genai-semconv.md)
- [Verification method](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [hcloud CLI installation guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud hcloud CLI installation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud APM CLI reference](https://support.huaweicloud.com/clir-apm/APM-cli.html)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer)
- [AgentArts API overview](https://support.huaweicloud.com/api-agentarts/agentarts_07_0002.html)
- [ShowOpsTrace API](https://support.huaweicloud.com/api-agentarts/ShowOpsTrace.html)
- [ShowOpsAgentMetricTrend API](https://support.huaweicloud.com/api-agentarts/ShowOpsAgentMetricTrend.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, API examples, code snippets, and configuration fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cloud-mutating commands or API calls; users should verify endpoints, permissions, and secrets handling before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
