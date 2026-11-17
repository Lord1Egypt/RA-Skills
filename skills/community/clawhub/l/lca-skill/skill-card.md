## Description:

AI-guided Life Cycle Assessment using openLCA. Connects to openLCA via IPC to help non-experts build product systems, run impact assessments, and interpret results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manmeet3591](https://clawhub.ai/user/manmeet3591)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sustainability practitioners, and non-expert LCA users use this skill to connect an agent workflow to openLCA, build product systems, run life cycle impact assessments, and interpret or compare environmental impact results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create product systems and run calculations through the user's openLCA IPC server, so mistaken selections may affect assessment work.

Mitigation: Confirm process, product system, and impact method identifiers before execution, and use a test or backed-up openLCA database for write-like operations.

Risk: The olca-ipc dependency is specified with a minimum version rather than an exact locked version.

Mitigation: Use a pinned dependency or lockfile when deploying the skill in reproducible or controlled environments.

Risk: Assessment results depend on the selected database, functional unit, system boundary, and LCIA method, and may be misleading if those choices are unsuitable.

Mitigation: Document the functional unit, system boundary, database, and impact method, and have material decisions reviewed by an LCA practitioner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manmeet3591/skills/lca-skill)
- [Project homepage](https://github.com/manmeet3591/claw_lca)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON bridge outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the olca-ipc package, OPENLCA_IPC_PORT, and a reachable openLCA IPC server.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
