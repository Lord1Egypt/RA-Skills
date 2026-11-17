## Description:

Guides coding agents in using the Kilo Code CLI for headless coding tasks and read-only workspace diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bottanicals](https://clawhub.ai/user/bottanicals)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to delegate one-shot coding tasks with `kilo run` and inspect files, symbols, search results, and diagnostics with `kilo debug`.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic approvals can permit shell actions during delegated coding tasks.

Mitigation: Prefer explicit per-run approvals and a scoped project directory; use `--auto` only in a disposable sandbox.

Risk: Command execution, session sharing, or cloud session options can expose project data or change state.

Mitigation: Review `--command` before use and avoid `--share` or cloud options for sensitive work.

## Reference(s):

- [Kilo CLI reference](https://kilo.ai/docs/code-with-ai/platforms/cli-reference)
- [Skill source (server-resolved GitHub import)](https://github.com/BottaniCals/agent-skills/tree/main/skills/kilo-cli)
- [Kilo Code skill on ClawHub](https://clawhub.ai/bottanicals/skills/kilo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Text, Guidance]

**Output Format:** [Markdown guidance and CLI JSON or text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the external `kilo` CLI; delegated coding runs may change project files.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
