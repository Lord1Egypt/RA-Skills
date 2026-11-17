## Description:

AIFLC PDLC Family provides 11 injectable workflow packages that guide AI coding agents through professional software delivery from idea evaluation and project initiation through architecture, workspace generation, compliance, and test accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbmd](https://clawhub.ai/user/mbmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, product teams, and delivery managers use this skill to add structured product development lifecycle guidance to AI coding assistants. It helps agents produce planning, architecture, UX, workspace, governance, testing, routing, portfolio, and data-fabric outputs with human approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent instruction files can change how future AI sessions behave in the target workspace.

Mitigation: Install in a branch or disposable workspace first, use dry-run or manual installation, and review generated AGENTS.md, CLAUDE.md, Copilot, Cursor, and Kiro instruction changes before relying on them.

Risk: Installer workflows can write package, rule, state, dashboard, and workspace files into the target project.

Mitigation: Keep the workspace under version control, review the install manifest and generated file diff, and avoid full-auto execution until expected file writes are understood.

Risk: Bundled VS Code dashboard webviews have under-scoped scripting risks according to the authoritative security evidence.

Mitigation: Avoid the bundled dashboard extension until its webview uses safe data transfer, a restrictive content security policy, and pinned or bundled JavaScript.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mbmd/skills/pdlc)
- [ClawHub Publisher Profile](https://clawhub.ai/user/mbmd)
- [README](artifact/README.md)
- [Platform Capabilities](artifact/PLATFORM_CAPABILITIES.md)
- [Installer README](artifact/installer/README.md)
- [Command Dashboard](artifact/COMMAND_DASHBOARD.md)
- [Security Policy](artifact/SECURITY.md)
- [Rollback Plan](artifact/ROLLBACK_PLAN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated workspace/configuration files when the host agent supports file writes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent agent instruction files and generated workspace artifacts may affect future agent sessions after installation.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
