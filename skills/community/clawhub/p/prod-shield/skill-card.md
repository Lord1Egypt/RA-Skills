## Description:

ProdShield applies hardened execution guardrails before an agent runs commands, manages infrastructure, changes databases or files, calls APIs, deploys, installs dependencies, or handles credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2eux](https://clawhub.ai/user/2eux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill as a production-safety checklist before commands that could affect live systems, data, infrastructure, dependencies, or credentials. It helps the agent identify environment risk, prefer dry-runs, require explicit confirmation, and guide recovery when dangerous actions or credential exposure are involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional scanner setup examples can introduce package, container, or hook changes if followed without review.

Mitigation: Pin tool versions or container digests, review packages before use, mount repositories read-only where possible, and install pre-commit hooks only with explicit user approval.

Risk: The skill is intentionally conservative and may interrupt commands that affect ambiguous environments, dependencies, credentials, or production-like resources.

Mitigation: Confirm the environment and scope, use dry-runs or previews when available, and require explicit current-message approval before irreversible or production-impacting actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2eux/skills/prod-shield)
- [Publisher profile](https://clawhub.ai/user/2eux)
- [Dangerous Commands Reference](references/dangerous-commands.md)
- [Environment Detection Patterns](references/environment-patterns.md)
- [Git & GitHub Credential Safety Reference](references/git-credential-safety.md)
- [Recovery Playbook](references/recovery-playbook.md)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Yelp detect-secrets](https://github.com/Yelp/detect-secrets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no binaries, scripts, or external runtime dependencies are included.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
