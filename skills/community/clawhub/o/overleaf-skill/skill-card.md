## Description: <br>
Sync and manage Overleaf LaTeX projects from the command line. Pull projects locally, push changes back, compile PDFs, and download compile outputs like .bbl files for arXiv submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aloth](https://clawhub.ai/user/aloth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and academic authors use this skill to manage Overleaf LaTeX projects from an agent-assisted command-line workflow, including sync, compilation, PDF download, and arXiv preparation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an Overleaf session cookie, which can grant account access if exposed. <br>
Mitigation: Treat the cookie like a password, keep .olauth and config files out of git and shared folders, avoid pasting it where it may be logged, and run logout or revoke the browser session if exposed. <br>
Risk: Push or sync operations can upload local changes back to Overleaf projects. <br>
Mitigation: Review changes before push or sync and use dry-run or status-style checks where available before modifying shared projects. <br>
Risk: The installation flow depends on the external olcli package and publisher distribution channels. <br>
Mitigation: Install only when the publisher and package source are trusted, and review the package source and release metadata before deployment. <br>


## Reference(s): <br>
- [Overleaf Skill on ClawHub](https://clawhub.ai/aloth/overleaf-skill) <br>
- [Overleaf API Reference](references/API.md) <br>
- [olcli on npm](https://www.npmjs.com/package/@aloth/olcli) <br>
- [Homebrew tap](https://github.com/aloth/homebrew-tap) <br>
- [Overleaf](https://www.overleaf.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of olcli to create or modify local project files and download Overleaf compile outputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
