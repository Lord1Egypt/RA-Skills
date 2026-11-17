## Description:

Orchestrates OpenClaw Agent Swarm workflows for multi-project coding automation across Obsidian task intake, coding-agent execution, Codex review, Git provider merge request or pull request flow, merge, sync, and task closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matzoh](https://clawhub.ai/user/matzoh)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to dispatch, monitor, review, and merge multi-project coding tasks through a local agent-swarm workflow. It supports Obsidian task intake, Git worktrees, tmux-based agent sessions, GitLab or GitHub review flows, notifications, and post-merge synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give background agents broad ability to change, push, review, and merge code with key safety prompts disabled.

Mitigation: Install only in a dedicated sandbox or service account with narrowly scoped repository tokens, and require explicit approval before push, merge request or pull request creation, and merge.

Risk: Automated dependency installation, trusted task intake, notifications, and cleanup can affect repositories or external channels without close human review.

Mitigation: Keep Obsidian intake trusted, require explicit approval before npm install, and disable or tightly control webhook notifications and cleanup until reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matzoh/skills/matz-swarm)
- [README](README.md)
- [Skill Definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, status summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch local automation scripts, tmux sessions, Git provider commands, and notifications based on user intent and configured registry values.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
