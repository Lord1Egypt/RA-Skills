## Description:

This skill helps agents connect Apple Notes Snapshot to local hosts, run notesctl MCP, diagnose attach failures, separate AI Diagnose from MCP, and verify the control-room proof path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prove Apple Notes Snapshot's local macOS control room, wire the read-only-first MCP lane into a local host, and distinguish local preflight issues from host attach issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal setup path can run unverified code from GitHub and install a recurring local job.

Mitigation: Review the referenced apple-notes-snapshot repository before running notesctl, prefer a specific audited commit with checksum or signature verification, run one-time proof commands first, and enable the recurring install only after understanding how to inspect and remove the scheduled job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/notes-snapshot-control-room)
- [Install And Attach](references/install-and-attach.md)
- [Usage And Proof](references/usage-and-proof.md)
- [Apple Notes Snapshot landing](https://xiaojiou176-open.github.io/apple-notes-snapshot/)
- [Quickstart](https://xiaojiou176-open.github.io/apple-notes-snapshot/quickstart/)
- [Proof page](https://xiaojiou176-open.github.io/apple-notes-snapshot/proof/)
- [MCP provider guide](https://xiaojiou176-open.github.io/apple-notes-snapshot/mcp/)
- [For Agents overview](https://xiaojiou176-open.github.io/apple-notes-snapshot/for-agents/)
- [Public skills pack docs](https://xiaojiou176-open.github.io/apple-notes-snapshot/for-agents/public-skills/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on local proof, MCP attach boundaries, and host configuration guidance.]

## Skill Version(s):

1.0.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
