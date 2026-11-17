## Description:

Run your agent's jobs 24/7 without keeping a Mac mini or laptop awake. Use when the user wants a task to run every morning or on a schedule, wants it to keep going while their computer sleeps, or is setting up a home server just to keep the agent online. Moves the job to a Nodo cloud computer and phone over MCP; new workspaces get 5,000 free credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

People who want recurring agent tasks to keep running while their own computer is asleep can use this skill to set up and test a scheduled workflow on Nodo, then review its run results and costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent sign-ins keep accounts active in the cloud workflow environment.

Mitigation: Use accounts appropriate for the task and confirm how to stop schedules and revoke stored sessions.

Risk: Scheduled workflows can send or publish content without a person reviewing each run.

Mitigation: Enable an approval step before workflows send or publish content when review is needed.

Risk: Cloud workflow usage can incur costs, and the setup guide was unavailable for inspection.

Mitigation: Review OAuth permissions and current pricing, and check the setup guide before connecting the service.

## Reference(s):

- [Nodo MCP setup guide](https://mcp.nodo.com/start.md)
- [Nodo](https://nodo.com)
- [ClawHub release](https://clawhub.ai/otto-iron/skills/nodo-always-on)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe workflow steps, schedules, approval points, and run results.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
