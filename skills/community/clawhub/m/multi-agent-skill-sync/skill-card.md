## Description:

One source of truth for local AI agent skills: audit Codex, Claude, OpenClaw, OpenCode, workspace skills, and shared roots; score hygiene, diff conflicting installs, deduplicate into one canonical source, and migrate the same layout across machines with restorable backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donttal](https://clawhub.ai/user/donttal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skill Sync to audit local skills across multiple AI agent hosts, review duplicate or conflicting installs, and preview or apply convergence around a canonical skill source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore and import flows can apply untrusted backup manifests and mutate files outside the intended skill roots.

Mitigation: Run preview commands first, inspect planned paths, use --apply only after review, and restore only from backup runs or manifests you generated and trust.

Risk: Convergence operations can replace local skill copies with symlinks.

Mitigation: Use strict dedupe for identical portable skills when possible and keep the generated backup run available for rollback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/donttal/skills/multi-agent-skill-sync)
- [Compatibility Model](references/compatibility.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; optional text, JSON reports, and layout manifest files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is the default; apply and restore flows can mutate local skill roots and write restorable backups.]

## Skill Version(s):

1.2.1 (source: server release metadata, created 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
