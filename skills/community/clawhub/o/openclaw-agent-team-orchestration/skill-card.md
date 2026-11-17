## Description:

Build and run multi-agent content production teams on OpenClaw with single-repo architecture, symlink-based file sharing, role-specialized AGENTS.md, and automated review-fix-score loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonlin1212](https://clawhub.ai/user/simonlin1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to set up and operate OpenClaw teams with writer, reviewer, scorer, and fixer roles for quality-controlled content production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can overwrite TOOLS.md files and repoint OUTPUT or KNOWLEDGE symlinks in OpenClaw workspaces.

Mitigation: Review or patch scripts/setup-team.sh before running it, use backups for important workspaces, and add explicit overwrite confirmation for TOOLS.md, OUTPUT, and KNOWLEDGE paths.

Risk: Untrusted or malformed agent IDs can affect generated workspace paths and configuration snippets.

Mitigation: Use only simple trusted agent IDs and validate IDs before running the setup script.

## Reference(s):

- [Architecture](references/architecture.md)
- [Build Guide](references/build-guide.md)
- [Workflow](references/workflow.md)
- [Role Templates](references/role-templates.md)
- [Lessons Learned](references/lessons-learned.md)
- [ClawHub Skill Page](https://clawhub.ai/simonlin1212/skills/openclaw-agent-team-orchestration)
- [Publisher Profile](https://clawhub.ai/user/simonlin1212)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role templates, orchestration workflow guidance, setup commands, and OpenClaw configuration snippets.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
