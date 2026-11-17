## Description:

Launch non-blocking interactive Claude Code tasks for slash-only plugins like ralph-loop, with completion callback routing when explicitly enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edxi](https://clawhub.ai/user/edxi)

### License/Terms of Use:


## Use Case:

Developers and operators use Dispatchi to start non-blocking Claude Code sessions for slash-command driven ralph-loop tasks, capture run metadata and output, and optionally route completion callbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches unattended local coding sessions in the background.

Mitigation: Run it under a low-privilege account with access only to approved repositories and result directories, and monitor or cancel runs when needed.

Risk: Unsafe project or task names could affect path handling.

Mitigation: Restrict project and task names to simple safe identifiers before invoking the skill.

Risk: External callback routing can share completion information outside the local environment when enabled.

Mitigation: Keep ENABLE_CALLBACK disabled unless external sharing is intended, and configure explicit approved group settings before enabling it.

Risk: Permission modes such as bypassPermissions can reduce review before local agent actions.

Mitigation: Avoid bypassPermissions or similar modes unless the execution environment is isolated and the requested action has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edxi/skills/miniade-dispatchi)
- [Claude Code headless mode documentation](https://code.claude.com/docs/en/headless)
- [Claude Code Agent Teams documentation](https://code.claude.com/docs/en/agent-teams)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text status with configured result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a background local Claude Code session and writes task metadata and captured output under configured result paths.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
