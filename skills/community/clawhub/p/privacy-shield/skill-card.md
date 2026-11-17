## Description:

Manages sensitive data access by marking resources with privacy levels and enforcing share, export, display, and internal-use restrictions through a centralized registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobu2020](https://clawhub.ai/user/xiaobu2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Privacy Shield to mark sensitive files, directories, and rule categories, then check whether planned operations such as sharing, exporting, displaying, or internal use are allowed before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review states that the core permission check can mistakenly treat some sensitive paths as public.

Mitigation: Treat results as advisory until path matching is fixed or compensated for with normalized, component-aware path checks and review before sharing or exporting data.

Risk: The security guidance warns against elevated-privilege use or attacker-controlled WORKSPACE values.

Mitigation: Run the tool with least privilege in a trusted workspace and do not use it as the sole approval gate for external disclosure.

## Reference(s):

- [Privacy Shield ClawHub skill page](https://clawhub.ai/xiaobu2020/skills/privacy-shield)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON registry examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command usage can create or update a JSON privacy registry and JSONL audit log.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
