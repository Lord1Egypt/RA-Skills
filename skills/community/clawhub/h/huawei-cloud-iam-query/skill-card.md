## Description:

Queries Huawei Cloud IAM identity, access, policy, agency, access-key, MFA, login policy, security compliance, and quota information through read-only Python SDK scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and security operators use this skill to inspect Huawei Cloud IAM users, groups, policies, agencies, access keys, MFA devices, login and password policy settings, compliance settings, and account quotas without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Huawei Cloud calls and setup steps disable TLS verification.

Mitigation: Review before installing, run only on trusted networks, avoid untrusted proxies, and restore TLS verification before production use.

Risk: The environment setup can execute downloaded installer code when pip bootstrapping is needed.

Mitigation: Remove the get-pip download-and-execute fallback or verify installer integrity before execution.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin or verify dependencies before deployment.

Risk: Cloud credentials are required for queries.

Mitigation: Use least-privilege, preferably temporary Huawei Cloud credentials and avoid exposing credential environment variable values.

## Reference(s):

- [IAM Python Script Guide](references/iam/guide.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured query output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Huawei Cloud credentials and region or project scope; query scripts are intended to be read-only.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
