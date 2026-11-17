## Description:

Ingests public Git repositories or repositories on a configured Gitea server into a Research KB with code understanding, incremental comparison, source traceability, and catalog/index maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to convert Git or configured Gitea repositories into Research KB wiki pages, source manifests, repository snapshots, and catalog/index updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Gitea credentials while reading and writing repository content.

Mitigation: Use a tightly scoped Gitea bot token, keep repository URLs and platform configuration trusted, and avoid embedding tokens in git URLs.

Risk: Repository files may be untrusted and could expose sensitive paths or misleading content during sampling.

Mitigation: Run only against trusted repositories, block symlink traversal during sampling, and clean or sanitize worktrees after use.

## Reference(s):

- [Gitea Repo Ingest on ClawHub](https://clawhub.ai/myd2002/skills/gitea-repo-ingest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown wiki pages plus JSON context, validation, and result envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Research KB pages, source traceability manifests, catalog/index updates, repository snapshots, and repository-level sourceItems records.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
