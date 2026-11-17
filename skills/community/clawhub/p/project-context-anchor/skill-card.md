## Description:

Writes AI_CONTEXT.md into the project root as a dynamic project snapshot that captures the tech stack, recent git diffs, key decisions, active plan, and an AI_BOOTSTRAP_BLOCK for cross-session recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao3333](https://clawhub.ai/user/xiao3333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to create a repo-local AI_CONTEXT.md handoff document for preserving project state, active work, and restart context across AI sessions or tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated AI_CONTEXT.md file can persist recent chat, project context, git summaries, private URLs, customer data, proprietary plans, or credentials in a repo-visible location.

Mitigation: Review and redact AI_CONTEXT.md before committing or sharing it, scan it for secrets when appropriate, and add it to .gitignore for private or sensitive projects.

Risk: The skill intentionally writes a project-local context file instead of using normal memory behavior, which may surprise users who expected private session memory only.

Mitigation: Install and invoke the skill only when a repo-local handoff document is desired, and confirm the target project root before running it.

Risk: Recent git diffs and commit messages may expose sensitive implementation details or secrets in the generated snapshot.

Mitigation: Inspect the generated Current Status, Recent Diff, and Bootstrap Block sections before distribution, and use secret scanning or manual redaction for shared repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown file with a compact AI_BOOTSTRAP_BLOCK]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a repo-local AI_CONTEXT.md file that may include scanned project state, git diffs, active plans, and recent-session context.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
