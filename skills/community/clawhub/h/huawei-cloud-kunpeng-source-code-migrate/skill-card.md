## Description:

Analyze C/C++/ASM/Fortran/Go/Java/Python/Scala source code migrability to the Kunpeng ARM64 platform using Huawei DevKit CLI, SSH-based setup, optional Huawei Cloud Kunpeng ECS provisioning, and migration report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess source-code portability to Huawei Kunpeng ARM64, install or access DevKit, scan supported projects, and collect migration reports. It is suited to migration planning for C/C++/ASM/Fortran/Go/Java/Python/Scala projects and can provision a Kunpeng ECS instance when the user does not already have a suitable server.

### Deployment Geography for Use:

Global, with automated Huawei Cloud provisioning documented for Guiyang Region 1.

## Known Risks and Mitigations:

Risk: The workflow can provision Huawei Cloud resources and may upload or scan source code on a remote host.

Mitigation: Confirm provisioning explicitly, prefer an existing hardened server when appropriate, and review resource cleanup instructions before running any deletion commands.

Risk: The security evidence flags high-risk root-password SSH and plaintext credential persistence patterns.

Mitigation: Prefer a non-root key-based or hardened account where feasible, avoid writing MIGRATE_SSH_PASS to shell profiles, verify SSH host keys out of band, and rotate or delete generated root passwords after use.

Risk: Migration reports may contain source paths, issue locations, and project details.

Mitigation: Store reports in controlled locations, share them only with intended reviewers, and remove temporary remote report files when the assessment is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-kunpeng-source-code-migrate)
- [Skill overview](artifact/SKILL.md)
- [Prerequisites](artifact/references/prerequisites.md)
- [Scripts guide](artifact/references/scripts-guide.md)
- [Prepare server task](artifact/references/task-prepare-server.md)
- [Scan source code task](artifact/references/task-scan-source-code.md)
- [DevKit CLI reference](artifact/references/devkit-cli-reference.md)
- [Migration report guide](artifact/references/migration-report-guide.md)
- [IAM policies](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline bash and Python snippets, environment configuration steps, and generated migration report files such as HTML, JSON, CSV, or TXT.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for user confirmation before source scanning or cloud provisioning and saves downloaded reports to a fixed local report directory unless the user requests otherwise.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
