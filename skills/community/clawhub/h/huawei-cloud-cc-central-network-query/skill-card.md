## Description:

Queries Huawei Cloud Cloud Connect Central Network instances, attachments, and connections through read-only hcloud CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and network engineers use this skill to inspect Huawei Cloud CC Central Network topology, connection status, and attachment configuration without issuing create, update, or delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation guidance includes running remote installer content with bash.

Mitigation: Review and replace the installation step with Huawei Cloud official package instructions and checksum or signature verification before installing.

Risk: The bundled test script can list Huawei Cloud Central Network topology in the configured account.

Mitigation: Run tests only with a least-privilege account limited to cc:centralNetworks:list and cc:centralNetworks:get, and avoid production accounts unless topology listing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cc-central-network-query)
- [Huawei Cloud hcloud CLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [API Reference](references/api-reference.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [CLI Installation Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with hcloud CLI command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require user-supplied region, domain ID, and relevant central network resource IDs; the documented workflow is read-only.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
