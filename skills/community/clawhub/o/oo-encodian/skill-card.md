## Description: <br>
Encodian operates PDF document actions through an OOMOL-connected Encodian account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compress PDFs, extract pages or text layers, secure PDF documents, and unlock password-protected PDFs through Encodian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a one-line CLI installer that can execute remote shell content during setup. <br>
Mitigation: Review or manually install the OOMOL CLI instead of blindly running the pipe-to-shell command. <br>
Risk: Encodian actions may require connected account credentials and can change document state for write-tagged actions. <br>
Mitigation: Keep credentials server-side through OOMOL and require explicit confirmation before running create, update, or other write actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-encodian) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Encodian homepage](https://www.encodian.com) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return base64-encoded PDF file content from Encodian connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
