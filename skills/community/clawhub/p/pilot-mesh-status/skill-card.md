## Description:

Reports Pilot Protocol mesh status across peers, connections, encryption, relay usage, bandwidth, daemon health, and latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to get a consolidated Pilot Protocol mesh health report, including daemon status, peers, connections, relay use, bandwidth, trust, encryption coverage, and latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may view mesh network metadata such as peers, connections, relay use, bandwidth, trust, and encryption state.

Mitigation: Run the skill only in environments where that mesh metadata is approved for agent access and downstream summarization.

Risk: The external pilotctl binary and running Pilot Protocol daemon remain part of the execution trust boundary.

Mitigation: Use a trusted pilotctl installation and daemon, and review commands before allowing the agent to execute them.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-mesh-status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized status metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl JSON status outputs when available; reports may include mesh metadata such as peers, connections, relay use, bandwidth, trust, and encryption state.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
