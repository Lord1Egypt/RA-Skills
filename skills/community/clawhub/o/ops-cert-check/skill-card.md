## Description:

SSL/TLS Certificate Check & Renewal SOP. Covers certificate validation (PEM/CRT/JKS), Nginx certificate update, Let's Encrypt wildcard application, and emergency response for expired certificates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill as a certificate operations runbook for checking SSL/TLS validity, updating Nginx and JKS certificates, applying Let's Encrypt wildcard certificates, and coordinating expired-certificate response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production TLS certificate changes can disrupt service or deploy mismatched certificate, key, or chain files.

Mitigation: Require approval, back up current certificates and configs, verify certificate/key/full-chain matching, test Nginx configuration, and confirm the served certificate after reload.

Risk: DNS API tokens, root access, cron jobs, and deploy hooks can create credential exposure or unauthorized automation risk.

Mitigation: Use least-privilege DNS credentials, protect secrets outside version control, test renewal with a dry run, and ensure cron or deploy hooks are administrator-owned, minimally scoped, logged, and reviewed.

## Reference(s):

- [Aliyun CLI credential configuration](https://help.aliyun.com/zh/cli/configure-credentials)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks, checklists, tables, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes production certificate operations steps that require human approval, backups, dry runs, and administrator review before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
