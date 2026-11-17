## Description:

Run Paperclip locally for agent orchestration, AI company setup, and OpenClaw, Codex, or Claude control-plane operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, configure, and operate a local Paperclip control plane for coordinating AI companies, agents, issues, approvals, budgets, and adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable setup commands may install or run changing package code.

Mitigation: Pin a reviewed package version or repository commit, and run first-time setup in an isolated environment before using it with real workspaces.

Risk: Operational context may be persisted to local Paperclip memory files.

Mitigation: Confirm with the user before saving environment details or work context, and never store provider tokens or other secrets in memory files.

Risk: Configured Paperclip deployments, adapters, and model providers may receive operational data.

Mitigation: Use only trusted local or remote deployments and adapters, and verify the selected API base, gateway URL, and provider credentials before sending work data.

## Reference(s):

- [Paperclip ClawHub Listing](https://clawhub.ai/ivangdavila/skills/paperclip)
- [Paperclip Homepage](https://clawic.com/skills/paperclip)
- [Paperclip Repository](https://github.com/paperclipai/paperclip.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup steps, adapter selection guidance, memory file structure, and API or CLI commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
