## Description:

OTC Confirmation gives agents a one-time email confirmation workflow for sensitive, irreversible, or externally visible operations, with shell scripts for code generation, email delivery, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewis-404](https://clawhub.ai/user/lewis-404)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add human-in-the-loop confirmation before an agent performs external communication, destructive local changes, security-rule changes, deployments, or similar high-impact actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that the security gate is weaker than advertised and should not be treated as a strong authorization boundary.

Mitigation: Review the skill before deployment and add operation/session binding, expiry, attempt limits, atomic verification, and safer temp-file handling before relying on it for high-impact authorization.

Risk: The scanner reports a local code-execution bug and warns against passing untrusted operation text into the scripts.

Mitigation: Avoid untrusted operation descriptions, validate or escape email-rendered text, and use the skill only in a controlled environment until the issue is fixed.

Risk: SMTP credentials are required for the normal email workflow.

Mitigation: Use isolated SMTP credentials with limited privileges and rotate them if the agent workspace or logs may have exposed configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lewis-404/skills/otc-confirmation)
- [README](artifact/README.md)
- [OTC Trigger Categories](artifact/references/trigger-categories.md)
- [OTC Enforcement Checklist](artifact/references/enforcement-checklist.md)
- [OTC Enforcement Discipline](artifact/references/enforcement-discipline.md)
- [AI DevOps Agent Security Pack Overview](artifact/ai-devops-agent-security-pack/00_overview.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, JSON, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and OTC email environment variables for the SMTP workflow.]

## Skill Version(s):

3.1.0 (source: server release metadata and changelog, released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
