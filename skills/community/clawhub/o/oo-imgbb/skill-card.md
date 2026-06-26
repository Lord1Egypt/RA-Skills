## Description: <br>
ImgBB (imgbb.com). Use this skill for ANY ImgBB request, including reading, creating, and updating data through the OOMOL-connected ImgBB connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to upload images to ImgBB through an OOMOL-connected account and receive hosted image metadata. It is suited for workflows that need connector-managed credentials and live action schema inspection before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image uploads send selected content to ImgBB through an OOMOL-managed connection. <br>
Mitigation: Confirm the exact image payload and intended upload effect with the user before running the write action. <br>
Risk: The skill depends on OOMOL account authentication, an ImgBB connection, and available OOMOL billing credits. <br>
Mitigation: Run one-time login, connection, or billing recovery steps only after a matching command failure. <br>
Risk: Installer or login commands can change the local environment or open account flows. <br>
Mitigation: Use the documented setup steps only when the oo CLI or required connection is missing. <br>


## Reference(s): <br>
- [ImgBB homepage](https://imgbb.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-imgbb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON responses] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo connector schema output before constructing action payloads; upload_image returns hosted image metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
