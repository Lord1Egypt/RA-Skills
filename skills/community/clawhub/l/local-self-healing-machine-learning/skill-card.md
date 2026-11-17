## Description:

A fully local machine learning engine that helps an OpenClaw agent learn from runtime errors without default telemetry, fingerprinting, or external network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephtandle](https://clawhub.ai/user/josephtandle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor local runtime history, cluster recurring failures, select repair strategies, and record outcomes for auditable self-healing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad OpenClaw session and memory data and use it to drive repository changes.

Mitigation: Install only in workspaces where this access is acceptable, prefer review mode, and set a narrow EVOLVER_SESSION_SCOPE.

Risk: Automated repair behavior can change local repository files.

Mitigation: Use --review or EVOLVE_BRIDGE=false for human oversight before applying changes.

Risk: Non-loopback embedding endpoints or an exposed dashboard can disclose local workflow data.

Mitigation: Keep OLLAMA_URL on loopback and do not expose the dashboard beyond localhost.

Risk: The documented Ollama install path uses curl piped to a shell.

Mitigation: Avoid that install path unless it has been independently trusted and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephtandle/skills/local-self-healing-machine-learning)
- [Publisher profile](https://clawhub.ai/user/josephtandle)
- [Author website](https://mastermindshq.business)
- [Ollama installation documentation](https://ollama.com/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and console text with inline shell commands and JSON-backed local state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audit records, feedback data, predictor state, and dashboard status data when run by an agent.]

## Skill Version(s):

2.0.1 (source: server release evidence; package.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
