## Description:

Provides a playbook and local router that guides users through a nine-stage AI-agent governance workflow using independently published sub-skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

AI governance teams and developers use this playbook to sequence red-team, prompt defense, leak scanning, desensitization, kill-switch, badge, and release-gate work. Run the local router to find the relevant independently published sub-skill and its expected output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suite provides workflow guidance but does not itself perform security checks or enforce release gates; relying on its route table alone could leave a review incomplete.

Mitigation: Review each referenced sub-skill independently and confirm its findings and release gates before acting or providing it sensitive data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/governance-method-suite)
- [LGD Governance hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [Protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain-text route table and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists governance stages, sub-skill slugs, call guidance, and expected outputs; does not run the referenced sub-skills.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
