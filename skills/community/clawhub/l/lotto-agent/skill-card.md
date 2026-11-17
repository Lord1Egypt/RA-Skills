## Description:

lotto-agent is a private Chinese lottery assistant for number generation, public draw fetching, prize checking, reporting, and automation management without prediction or winning claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenjinliuu](https://clawhub.ai/user/wenjinliuu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Chinese lottery workflows through an agent or command line, including generating random entries, recording purchases, fetching public draw results, checking prizes, reporting spend and returns, and scheduling recurring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent local tasks and send task results through OpenClaw notifications.

Mitigation: Review scheduled tasks before enabling cron, disable unwanted tasks with the provided task controls, and configure notifications only for intended channels and chat IDs.

Risk: The skill fetches unverified public draw data.

Mitigation: Use only trusted draw-data sources, review the configured LOTTERY_PUBLIC_DATA_BASE_URL when overriding defaults, and cross-check results before relying on prize outcomes.

Risk: The skill stores lottery records, costs, and task state in a local SQLite database.

Mitigation: Keep the data directory private, review LOTTO_AGENT_DATA_DIR before use, and remove stored records when they are no longer needed.

Risk: Security evidence flags overbroad host-agent control for a private automation workflow.

Mitigation: Review the artifact and host permissions before installing, and run only the actions needed for the intended lottery automation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenjinliuu/skills/lotto-agent)
- [Public draw data source](https://raw.githubusercontent.com/wenjinliuu/lottery-data-repo/main/public_data)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and short Chinese text messages, with shell command examples for setup and automation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite records, recurring local tasks, and OpenClaw notification configuration.]

## Skill Version(s):

1.2.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
