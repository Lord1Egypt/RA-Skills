## Description: <br>
Vimeo (vimeo.com). Use this skill for ANY Vimeo request: reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate Vimeo through an OOMOL-connected account, including reading account and video information, organizing videos, uploading or replacing videos from URLs, and managing folders, showcases, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Vimeo account state through upload, update, replacement, tagging, folder, showcase, and removal actions. <br>
Mitigation: Confirm the exact action, target, and payload with the user before running any write action. <br>
Risk: Destructive actions can delete videos, delete folders, remove tags, or remove videos from organizational containers. <br>
Mitigation: Require explicit approval for destructive actions and verify the target identifier before execution. <br>
Risk: The connector depends on an OOMOL-connected Vimeo OAuth account and the oo CLI. <br>
Mitigation: Authorize OAuth only when the user trusts OOMOL and the oo CLI with the requested Vimeo scopes, and use setup steps only after authentication or connection failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-vimeo) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Vimeo](https://vimeo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the oo CLI against the Vimeo connector and may return JSON responses containing connector data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
