## Description:

OpenList helps an agent use the OpenList HTTP API for auditable file browsing, move, rename, single-path delete, offline task creation, task management, and audit review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okami-horo](https://clawhub.ai/user/okami-horo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent perform common OpenList file and task workflows through a preview-and-apply process with audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated OpenList file and task changes can bypass or weaken the documented confirmation model.

Mitigation: Use the preview-and-apply workflow for modifying actions, store plan files privately, review normalized paths and object types before delete apply, and treat task cancellation as an immediate state-changing action.

Risk: A token with broad OpenList permissions can make unintended file or task changes more damaging.

Mitigation: Use a least-privileged OpenList token and keep the token out of committed files.

Risk: Misconfigured transport security can expose OpenList requests or credentials.

Mitigation: Prefer HTTPS with verified certificates; disable TLS verification only for controlled self-signed environments.

Risk: Chinese-only documentation may cause users to miss operational or safety requirements.

Mitigation: Install and use the skill only when the operator understands the documentation and can follow the confirmation and rollback guidance.

## Reference(s):

- [OpenList skill release page](https://clawhub.ai/okami-horo/skills/openlist-skill)
- [Publisher profile](https://clawhub.ai/user/okami-horo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON operation plans or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit JSON plans, JSON results, audit event identifiers, task identifiers, hints, and rollback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
