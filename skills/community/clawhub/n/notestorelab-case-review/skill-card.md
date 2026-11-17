## Description:

Guides agents through installing NoteStore Lab's local MCP lane and reviewing one copied Apple Notes case root using demo proof, derived artifacts, and bounded case questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, reviewers, and MCP-aware agent operators use this skill to install or launch NoteStore Lab, prove the workflow on public-safe demo artifacts, and review one copied Apple Notes case root without touching the live Notes store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a locally installed PyPI package, so installation depends on trusting that package supply chain.

Mitigation: Install only when the NoteStore Lab package is trusted, prefer a virtual environment or sandbox, and avoid admin or root privileges.

Risk: Reviewing live Apple Notes data could expose or affect user content outside the intended case boundary.

Mitigation: Run the MCP process only against copied case data and limit it to the specific case root intended for review.

## Reference(s):

- [Install And MCP Wiring](references/install-and-mcp.md)
- [Usage And Proof](references/usage-and-proof.md)
- [NoteStore Lab public demo](https://xiaojiou176-open.github.io/apple-notes-forensics/)
- [Public proof page](https://github.com/xiaojiou176-open/apple-notes-forensics/blob/main/proof.html)
- [Builder guide](https://github.com/xiaojiou176-open/apple-notes-forensics/blob/main/INTEGRATIONS.md)
- [Releases](https://github.com/xiaojiou176-open/apple-notes-forensics/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local, case-root-scoped guidance; no hosted service output.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
