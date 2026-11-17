## Description:

OpenTangl Plugin connects OpenClaw agents to OpenTangl lifecycle tools for queue review, task proposal, workflow execution, autopilot runs, wiring audits, and merge pipeline management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8co](https://clawhub.ai/user/8co)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this plugin to operate OpenTangl from an OpenClaw chat session, including reviewing queues, proposing or executing tasks, running workflows, auditing multi-repo wiring, and managing PR merge flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact automation can change repositories, create commits and PRs, run merge flows, or prune queue state when mutating tools are enabled.

Mitigation: Enable mutating tools only for trusted workspaces, review proposed actions before execution, and run with least-privilege repository and GitHub permissions.

Risk: The plugin may use an unpinned npx tsx fallback in the user's environment if a trusted OpenTangl binary is not configured.

Mitigation: Configure an explicit trusted bin path to a preinstalled OpenTangl executable and avoid relying on the npx fallback.

Risk: The plugin operates with access to the configured workspace, git/GitHub tools, and AI-provider credentials.

Mitigation: Use a dedicated workspace and least-privilege account, scope credentials narrowly, and install only where OpenClaw is intended to operate OpenTangl.

## Reference(s):

- [OpenTangl documentation](https://opentangl.com)
- [OpenTangl Plugin on ClawHub](https://clawhub.ai/8co/skills/opentangl-plugin)
- [8co publisher profile](https://clawhub.ai/user/8co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [OpenClaw tool responses as text or Markdown, often containing command output, code changes, workflow results, configuration snippets, or PR and merge guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger OpenTangl actions that read repository state, write queue files, run workflows, create commits, open PRs, wait for CI, merge, or escalate depending on enabled tools and user configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
