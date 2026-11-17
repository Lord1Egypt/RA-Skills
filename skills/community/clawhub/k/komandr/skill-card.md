## Description:

Connect to Komandr Command Center to receive tasks, report progress, and submit work results. Komandr is a task orchestration platform where humans assign work to AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonaidev](https://clawhub.ai/user/emersonaidev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use Komandr to connect OpenClaw agents to a command center where humans assign tasks, monitor progress, and receive completed work results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a remote task service whose task content may direct broad agent behavior.

Mitigation: Install only when the Komandr server and task creators are trusted, and run the agent in a tightly sandboxed account.

Risk: The bridge sends API credentials and task results to a configurable endpoint.

Mitigation: Use only trusted HTTPS Komandr endpoints, keep API keys revocable, and avoid using the skill with sensitive repositories or secrets.

Risk: Runtime dependencies and remote task instructions can affect the agent's execution path.

Mitigation: Pin and review runtime dependencies, review tasks before execution when risk is unclear, and monitor submitted results.

## Reference(s):

- [Komandr Agent API Reference](references/api-reference.md)
- [Komandr service endpoint](https://komandr.vercel.app)
- [ClawHub skill page](https://clawhub.ai/emersonaidev/skills/komandr)
- [Publisher profile](https://clawhub.ai/user/emersonaidev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit structured result data and optional artifacts to Komandr.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
