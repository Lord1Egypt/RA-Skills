## Description:

Configure or inspect a local execution policy gate when the user requests JEP Guard protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use JEP Guard to configure or inspect a local authenticated policy gate for explicitly integrated OpenClaw hook calls, including key provisioning, policy setup, daemon startup, and audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gate only protects execution paths that explicitly call its hooks; it is not an operating-system sandbox.

Mitigation: Integrate the hooks deliberately and use separate OS accounts or containers for mutually untrusted code.

Risk: Passive mode, a missing configuration, or an unstarted daemon does not provide execution protection.

Mitigation: Initialize configuration, provision allowed skills and policies, then start the daemon in full mode before relying on enforcement.

Risk: Local credentials, policy files, and audit records under ~/.jep-guard affect enforcement and accountability.

Mitigation: Protect the private state directory and files with restrictive permissions, back them up securely, and archive audit logs before bounded storage limits are reached.

Risk: This release is identified as a repair candidate and should not be treated as a security certification.

Mitigation: Run the IPC test suite and verify the target OpenClaw host integration before production reliance.

## Reference(s):

- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [skill.yaml](artifact/skill.yaml)
- [ClawHub skill page](https://clawhub.ai/schchit/skills/jep-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on explicit operator actions; it should not automatically start services, approve commands, mutate unrelated runtimes, or enable optional integrations.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter, package.json, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
