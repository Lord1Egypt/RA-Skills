## Description:

Agent Pheromone Network interface for querying and publishing verified execution paths to a collective intelligence network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiechengyuan](https://clawhub.ai/user/xiechengyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use Mycelium to seek prior task strategies, publish reviewed execution summaries, and submit feedback on whether a retrieved path helped. It is intended for complex strategic tasks where agents benefit from shared task memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task goals, execution summaries, feedback, and the Mycelium API key can be used with a remote service.

Mitigation: Use the skill only for data that is appropriate to share with the service, and avoid secrets, regulated data, private customer data, or proprietary workflows.

Risk: The remote endpoint is externally configurable through MYCELIUM_API_URL.

Mitigation: Leave MYCELIUM_API_URL unset unless the replacement endpoint is fully trusted, and prefer an isolated Python environment for installation.

Risk: Privacy protections may be overstated if scrubbing misses sensitive details in a task path.

Mitigation: Review the summarized JSON before any publish action and require explicit current-session confirmation before sending it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiechengyuan/skills/mycelium)
- [Mycelium Platform](https://mycelium-platform.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MYCELIUM_API_KEY and optional OPENCLAW_AGENT_ID; publish flows require explicit confirmation before sending reviewed summaries.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter reports 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
