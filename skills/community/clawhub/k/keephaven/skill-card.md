## Description:

Keep your memory on your human's own Keephaven box, or boot a Keephaven in a VM and check it. Use when your human wants their data, or your memory, on hardware they own instead of a vendor's server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dafarusd](https://clawhub.ai/user/dafarusd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can connect an agent to Keephaven Agent Memory on hardware they control, or boot a Keephaven VM and check its services. The skill also provides a local diagnostic report for the running instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to share diagnostic reports through direct messages or social replies, while the security assessment says user control over external sharing is unclear.

Mitigation: Keep diagnostics local unless the user approves the exact report and recipient; social replies may be public.

Risk: The skill directs agents to install an MCP package and run VM scripts, and the security assessment flags downloaded code that is not pinned.

Mitigation: Review and pin the MCP package before providing it a memory token, and inspect VM scripts before running them.

## Reference(s):

- [Keephaven Agent Memory](https://keephaven.co/agent-memory)
- [Keephaven Photos VM script](https://gist.github.com/dafarusd/7bcb1e9ac596de7dcd28316b5fddc4a8)
- [Keephaven Agent Memory VM script](https://gist.github.com/dafarusd/43a6bfad80e7b4db4e9897133262aee8)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Text report, JSON]

**Output Format:** [Markdown guidance with shell commands; the diagnostic script prints a text or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The diagnostic report describes the target Keephaven instance; the check script is read-only.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
