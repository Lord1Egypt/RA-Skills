## Description: <br>
Rust-native MCP server for fast, local processing of Excel, Word, PowerPoint, and PDF files with reading, writing, form filling, and skill execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdnaimino](https://clawhub.ai/user/xdnaimino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect MCP clients to local Office and PDF document processing. It supports reading documents into structured outputs and creating or modifying Excel, Word, PowerPoint, and PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install or run a package source they did not intend to trust. <br>
Mitigation: Verify the Cargo package and source identity before installation. <br>
Risk: The MCP server can read or modify Office and PDF documents, including potentially sensitive files. <br>
Mitigation: Use it only with documents the user is comfortable allowing an MCP server to process, and review requested file paths before execution. <br>
Risk: Form filling, overlays, and propagated edits can create incorrect or unintended document changes. <br>
Mitigation: Prefer writing output copies and review generated documents before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xdnaimino/office-oxide-mcp) <br>
- [Artifact README](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, configuration] <br>
**Output Format:** [Markdown or JSON responses, configuration snippets, and generated or modified Office/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against local documents; users should verify package source and review document reads or writes before deployment.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
