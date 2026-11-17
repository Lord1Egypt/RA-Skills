## Description:

Inspect tmux panes as JSON: snapshot, diff, and classify Claude/Codex/Copilot agent state across the whole fleet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandriscoll](https://clawhub.ai/user/dandriscoll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Muxray to inspect tmux panes running terminal coding agents, classify each pane's program and state, and summarize snapshots or diffs without scraping raw terminal bytes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Go install target uses a mutable @latest version, which may change after review.

Mitigation: Prefer a pinned muxray release or verified binary before deployment.

Risk: The README mentions a curl pipe-to-shell installer that executes remote installation code.

Mitigation: Do not use the README curl | sh installer in managed environments; use the reviewed Go install path or a pinned release artifact.

Risk: Fleet-wide scans can expose tmux pane text that may contain secrets or unrelated user content.

Mitigation: Use targeted pane commands for single-pane questions, reserve scan for explicit fleet-wide inspection, and summarize or redact raw pane text.

## Reference(s):

- [Muxray ClawHub Listing](https://clawhub.ai/dandriscoll/skills/muxray)
- [Muxray GitHub Repository](https://github.com/dandriscoll/muxray)
- [Muxray JSON Contract](references/json-contract.md)
- [Inspect Agent Example](examples/inspect-agent.md)
- [AgentSkills Format](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Muxray command results are JSON on stdout with JSON errors on stderr; pane excerpts may require redaction before reporting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
