## Description:

This skill generates CP2K input drafts for quantum chemistry calculations from natural-language requests and local structure files, using documentation-backed defaults and explicit assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemon1044](https://clawhub.ai/user/lemon1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational chemists, and materials researchers use this skill to turn simple CP2K job requests and local .xyz structures into first-pass input drafts with a short review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CP2K settings may be scientifically inappropriate for charge, spin, periodicity, k-points, convergence, or unusual systems.

Mitigation: Review the generated input and report before running, especially charge, multiplicity, periodicity, k-points, cutoff, basis, pseudopotential, and convergence assumptions.

Risk: The skill is documentation-only and does not validate CP2K convergence or prove that selected defaults are optimal.

Mitigation: Treat outputs as first-pass drafts and perform convergence testing or expert review before production calculations.

Risk: The documented workflow currently supports local .xyz structures and does not retrieve structures from external databases.

Mitigation: Provide the intended local structure file and manually verify any structure source used outside the skill.

## Reference(s):

- [CP2K Task Map](references/cp2k-task-map.md)
- [CP2K Defaults](references/cp2k-defaults.md)
- [CP2K Kind Defaults](references/cp2k-kinds.md)
- [Ambiguity Policy](references/ambiguity-policy.md)
- [Design Rules](references/design-rules.md)
- [Job Spec Schema](references/job-spec-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/lemon1044/skills/input-file-skill)
- [Publisher Profile](https://clawhub.ai/user/lemon1044)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [CP2K .inp draft plus Markdown report and optional normalized JSON job specification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated inputs are draft-quality starting points and should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
