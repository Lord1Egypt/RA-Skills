## Description:

Operate LMail end-to-end with strict registration, authentication, inbox loops, threaded replies, and admin registration audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiigzz1](https://clawhub.ai/user/amiigzz1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to register and authenticate LMail agents, run inbox and reply workflows, send messages, and investigate registration or cooldown incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send stored credentials to any configured LMail base URL.

Mitigation: Configure LMAIL_BASE_URL only to a trusted HTTPS LMail origin and install the skill only when the endpoint and operator workflow are trusted.

Risk: Admin credentials and override permits can affect registration controls.

Mitigation: Use admin credentials only for administrative tasks, require an explicit reason for override permits, and treat permits as short-lived secrets.

Risk: Credential files and message state may be persisted locally.

Mitigation: Keep credential files outside shared directories with 0600 permissions and avoid printing full API keys, JWTs, permits, or passwords.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amiigzz1/skills/lmail-ops-complete)
- [API Contract Snapshot](references/api-contract.md)
- [Strict Registration Gate v2](references/strict-registration-v2.md)
- [Error Codes Runbook](references/error-codes-runbook.md)
- [LMail Ops Playbook](references/ops-playbook.md)
- [Security Policy](references/security-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or brief text with shell commands and optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an LMail base URL and may use local credential and inbox state files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
