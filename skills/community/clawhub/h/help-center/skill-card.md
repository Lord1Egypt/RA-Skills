## Description:

Build and run help centers with provider selection, migration playbooks, workflow mapping, content taxonomy, and support deflection metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Support leaders, content operators, and developers use this skill to plan, migrate, launch, and operate a help center with provider comparisons, taxonomy rules, ticket workflow mapping, and deflection metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update local planning notes under ~/help-center/ if the user approves.

Mitigation: Ask before creating or modifying local planning files, and choose explicit activation during setup if automatic engagement is not desired.

Risk: Planning notes may contain support model details, provider choices, compliance constraints, and rollout decisions.

Mitigation: Store only explicit user-approved decisions and constraints, keep memory concise, and keep files inside ~/help-center/.

Risk: Provider selection or migration recommendations could affect public support operations if applied without review.

Mitigation: Score vendor and custom-stack options against stated constraints, document rejected options, and use migration QA, rollback, and launch checklists before production changes.

## Reference(s):

- [ClawHub Help Center Skill](https://clawhub.ai/ivangdavila/skills/help-center)
- [Help Center Homepage](https://clawic.com/skills/help-center)
- [Setup](artifact/setup.md)
- [Provider Matrix](artifact/provider-matrix.md)
- [Build Your Own Stack](artifact/build-own-stack.md)
- [Migration Playbook](artifact/migration-playbook.md)
- [Content Operations](artifact/content-ops.md)
- [Launch Checklist](artifact/launch-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Files]

**Output Format:** [Markdown with checklists, scoring tables, playbooks, and local planning-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local planning files under ~/help-center/ after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
