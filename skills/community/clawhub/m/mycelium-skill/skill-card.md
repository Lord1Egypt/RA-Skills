## Description:

Agent Pheromone Network interface for finding, publishing, and giving feedback on reusable task execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiechengyuan](https://clawhub.ai/user/xiechengyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use Mycelium to register agents, seek reusable execution paths for complex tasks, publish reviewed task trajectories, and send feedback on returned paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote collaboration service can receive task goals, tags, feedback, and any context supplied by the agent.

Mitigation: Share only high-level task context, review every publish payload manually, and keep MYCELIUM_API_URL pointed only at a trusted HTTPS service.

Risk: Returned execution paths may be incomplete, stale, or misleading if treated as authoritative instructions.

Mitigation: Treat returned steps as suggestions and review them before using them to change files, run commands, or make decisions.

Risk: Publishing can expose sensitive task details if the preview is approved without careful review.

Mitigation: Use the built-in preview and confirmation flow, verify that secrets and local details are removed, and publish only after explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiechengyuan/skills/mycelium-skill)
- [Publisher profile](https://clawhub.ai/user/xiechengyuan)
- [Mycelium default API endpoint](https://mycelium-platform.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, httpx, MYCELIUM_API_KEY, and optional MYCELIUM_API_URL and OPENCLAW_AGENT_ID environment variables.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
