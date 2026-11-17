## Description:

Preflight Prisma migration state before deploy; fails fast on drift, failed migrations, missing DB URLs, or unapplied migration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill in CI or pre-deploy workflows to check Prisma migration status and fail fast on drift, failed migrations, missing database URLs, or unapplied migration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deploy check can automatically run an unpinned Prisma package via npx in a sensitive CI or database environment.

Mitigation: Review before installing in CI or production deploy workflows; prefer a pinned Prisma dependency installed from a lockfile and invoke the local binary, or require npx to use an already-installed package when deployment secrets are present.

## Reference(s):

- [Prisma Migrate Guard on ClawHub](https://clawhub.ai/daniellummis/skills/prisma-migrate-guard)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and PASS/FAIL terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, node, and npx; exits 0 on healthy status and 1 on blocking migration issues.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
