## Description: <br>
This skill teaches agents how to install or launch the NoteStore Lab MCP surface, prove the review flow on public-safe demo artifacts, and review one copied Apple Notes case root using derived artifacts instead of the live Notes store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, investigators, and MCP-aware agent users use this skill to set up a local NoteStore Lab review lane, validate it on demo artifacts, inspect one copied Apple Notes case root, ask bounded evidence-backed questions, compare case roots, and prepare public-safe exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may be pointed at a live Apple Notes store instead of copied evidence. <br>
Mitigation: Use the public-safe demo path first, then run the MCP lane only against one explicit copied case root. <br>
Risk: Package or repository source confusion could lead to running an unintended tool. <br>
Mitigation: Verify the PyPI package or repository source before running commands and prefer an isolated environment. <br>
Risk: Review output could overstate certainty or expose raw copied evidence. <br>
Mitigation: Ask bounded questions, prefer derived artifacts, and use public-safe export when sharing results. <br>


## Reference(s): <br>
- [Install And MCP Wiring](references/install-and-mcp.md) <br>
- [Usage And Proof](references/usage-and-proof.md) <br>
- [NoteStore Lab public demo](https://xiaojiou176-open.github.io/apple-notes-forensics/) <br>
- [Public proof page](https://github.com/xiaojiou176-open/apple-notes-forensics/blob/main/proof.html) <br>
- [Builder guide](https://github.com/xiaojiou176-open/apple-notes-forensics/blob/main/INTEGRATIONS.md) <br>
- [Distribution boundary](https://github.com/xiaojiou176-open/apple-notes-forensics/blob/main/DISTRIBUTION.md) <br>
- [Releases](https://github.com/xiaojiou176-open/apple-notes-forensics/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Analysis] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bounded to one explicit copied case root or the public-safe demo path; favors derived artifacts before raw copied evidence.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
