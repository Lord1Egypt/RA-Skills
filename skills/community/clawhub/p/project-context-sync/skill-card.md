## Description:

Automatically updates PROJECT_STATE.md after each commit with recent git information and optional AI-generated summaries to preserve project status and next-step context for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe3112](https://clawhub.ai/user/joe3112)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users install this skill in a Git repository to keep a local PROJECT_STATE.md current after commits, giving future agent sessions concise context about recent changes, current focus, and suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent Git post-commit automation and modifies the shared post-commit hook file.

Mitigation: Review existing post-commit hooks before installing or uninstalling, and inspect the hook after installation to confirm only the intended project-context-sync command was added.

Risk: With ai_summary enabled, commit metadata and changed-file context can be sent to the configured Clawdbot gateway.

Mitigation: Disable ai_summary for repositories where commit metadata should not enter the AI workflow, or enable it only with an approved local gateway configuration.

Risk: The generated PROJECT_STATE.md can influence future agent behavior through inferred focus and suggested next steps.

Mitigation: Review the generated PROJECT_STATE.md before relying on it as agent context, especially after sensitive or ambiguous commits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joe3112/skills/project-context-sync)
- [Publisher Profile](https://clawhub.ai/user/joe3112)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, YAML configuration, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates PROJECT_STATE.md and .project-context.yml; optional AI summaries use a configured local Clawdbot gateway and fall back to raw Git information when unavailable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
