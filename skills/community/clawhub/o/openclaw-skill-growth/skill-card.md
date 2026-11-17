## Description:

OpenClaw Skill Growth helps users make OpenClaw Skills observable, diagnosable, and safely improvable over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuai-daidai](https://clawhub.ai/user/shuai-daidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw skill maintainers use this wrapper to discover, install, and operate a plugin that observes skill runs, diagnoses recurring failures, proposes improvements, previews patches, and supports guarded apply and evaluation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the wrapper can lead users to clone and run external npm code that was not packaged or pinned in the reviewed artifact.

Mitigation: Pin the GitHub repository to a reviewed commit or release tag, inspect package scripts and dependencies, prefer npm ci with a lockfile when available, and run a dry-run before using it on real skills.

Risk: Generated proposals or apply flows could introduce incorrect or misleading changes into skill files.

Mitigation: Review reports and patch previews before applying changes, keep backups enabled, limit access to skill directories that can be restored, and compare outcomes after each change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuai-daidai/skills/openclaw-skill-growth)
- [Project homepage](https://github.com/Shuai-DaiDai/openclaw-skill-growth)
- [GitHub release v0.1.0](https://github.com/Shuai-DaiDai/openclaw-skill-growth/releases/tag/v0.1.0)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs users to an external TypeScript project and its generated reports, proposals, patch previews, evaluations, and JSON artifacts.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter and changelog list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
