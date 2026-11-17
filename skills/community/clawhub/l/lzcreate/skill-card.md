## Description:

LZ Create supports migrations from AWS, Alibaba Cloud, GCP, Huawei Cloud, and Azure to a Tencent Cloud Landing Zone by using a remote MCP server to scan source cloud resources, complete migration survey inputs, generate design documentation, and generate Terraform code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awaili](https://clawhub.ai/user/awaili)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud architects and migration engineers use this skill to run a Tencent Cloud Landing Zone migration workflow: generate or complete survey inputs, scan source cloud resources, query Tencent Cloud specifications, and produce design documentation and Terraform configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials and infrastructure data may be sent to a fixed remote MCP server over plaintext HTTP.

Mitigation: Use only a trusted HTTPS or self-hosted MCP endpoint, and avoid sending production secrets to the default plaintext endpoint.

Risk: Long-lived or broadly scoped cloud credentials could expose more access than the migration workflow needs.

Mitigation: Use short-lived, read-only, tightly scoped credentials and rotate or revoke them after the session.

Risk: Uploaded questionnaires, scan results, generated files, and session IDs may be accessible to the remote service during the session lifetime.

Mitigation: Treat uploaded and generated content as remotely accessible, avoid including unnecessary sensitive data, and protect session IDs.

Risk: Passing secrets directly on command lines can expose them through shell history or process listings.

Mitigation: Prefer credential files or safer secret-handling workflows instead of pasting secrets into command-line arguments.

## Reference(s):

- [MCP API Reference](references/mcp_api.md)
- [ClawHub Skill Page](https://clawhub.ai/awaili/skills/lzcreate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands; generated files include Excel surveys, Markdown design documents, resource inventories, and Terraform configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a session-based remote MCP workflow; generated workspace files can be listed and downloaded.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
