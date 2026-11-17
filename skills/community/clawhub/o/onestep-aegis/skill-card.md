## Description:

Orchestrates Claude Code sessions through the local Aegis HTTP and MCP bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onestepat4time](https://clawhub.ai/user/onestepat4time)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to spawn, monitor, coordinate, and clean up local Claude Code sessions via Aegis HTTP or MCP workflows for implementation, review, CI repair, and parallel agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation templates can approve shell and permission prompts without human review.

Mitigation: Use auto-approval only in sandboxed sessions with allowlisted commands; otherwise log, review, or reject untrusted requests.

Risk: The MCP setup can create a persistent Aegis MCP entry backed by an unpinned package invocation.

Mitigation: Prefer project-scoped MCP setup and pin the aegis-bridge package version before routine use.

Risk: Transcripts, prompts, memory entries, and repository context may pass through the local Aegis service.

Mitigation: Treat local Aegis data as sensitive, restrict service access, and avoid placing secrets in prompts or shared memory.

## Reference(s):

- [Agent Template](references/agent-template.md)
- [Aegis API Quick Reference](references/api-quick-ref.md)
- [Heartbeat Template](references/heartbeat-template.md)
- [Workflow Examples](references/workflow-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Aegis server on 127.0.0.1:9100 and optional MCP configuration.]

## Skill Version(s):

0.6.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
