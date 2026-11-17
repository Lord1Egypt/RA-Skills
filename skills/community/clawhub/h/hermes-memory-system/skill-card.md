## Description:

Hermes adds persistent cross-session memory, task trajectory review, skill generation, and OpenClaw integration support for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory, task debriefing, reusable skill generation, and OpenClaw-compatible deployment guidance to agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and trajectory capture may store conversations, tool activity, file-operation traces, or code cases.

Mitigation: Review retention settings, scrub sensitive data, keep exports and webhooks disabled unless approved, and limit workspace access to trusted users.

Risk: Documented upgrade paths include downloaded code execution that the security evidence says should not be followed without independent verification.

Mitigation: Prefer trusted package installation paths and verify publisher identity, checksums, and signatures before running downloaded scripts or archives.

Risk: Backup pruning and recursive deletion commands can remove valuable workspace data if paths are wrong or backups are incomplete.

Mitigation: Use explicit path checks, verified backups, and dry-run review before running cleanup, rollback, or pruning commands.

Risk: Automatic skill generation can introduce inaccurate or unsafe reusable behavior into an agent workspace.

Mitigation: Keep approval gates enabled, review generated skills before installation, and scan generated content before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/hermes-memory-system)
- [ClawHub Homepage](https://clawhub.ai/skills/hermes-agent-skill)
- [CHANGELOG.md](artifact/references/CHANGELOG.md)
- [DEPLOYMENT_GUIDE.md](artifact/references/DEPLOYMENT_GUIDE.md)
- [TEST_GUIDE.md](artifact/references/TEST_GUIDE.md)
- [ACCEPTANCE_TEST_PLAN.md](artifact/references/ACCEPTANCE_TEST_PLAN.md)
- [VERSION_MANAGEMENT.md](artifact/references/VERSION_MANAGEMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proposed workspace changes, generated skill files, memory records, exports, and deployment commands for review.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json, config/hermes.yaml, and changelog released 2026-04-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
