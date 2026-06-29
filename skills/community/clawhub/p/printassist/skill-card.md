## Description: <br>
PrintAssist helps an agent print and prepare PDF, Office, and image files from plain-language requests, including layout changes, page ranges, watermarks, document edits, and optional Adobe Creative Cloud photo edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nilsgollub](https://clawhub.ai/user/nilsgollub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill on Windows systems to let an agent prepare files, configure print parameters, preview layout-heavy jobs, and send supported documents or images to configured printers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send files directly to configured printers, including sensitive or incorrectly selected documents. <br>
Mitigation: Require explicit confirmation or preview before printing, and verify the printer, page range, copy count, color mode, and duplex settings before execution. <br>
Risk: The skill can modify Office documents, delete slides, and remove PDF password protection. <br>
Mitigation: Save transformed files as new copies by default and require user approval before document edits, slide deletion, or PDF decryption. <br>
Risk: Setup and operation rely on local Windows tools with access to files and printers. <br>
Mitigation: Install and run the skill only on trusted Windows hosts with reviewed printer configuration and approved dependency installation. <br>


## Reference(s): <br>
- [ClawHub PrintAssist package page](https://clawhub.ai/nilsgollub/printassist) <br>
- [Claude Code](https://claude.ai/code) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [Python](https://www.python.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline commands and Python script calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only release that requires Python, configured printers, and optional Adobe Creative Cloud authentication for photo editing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
