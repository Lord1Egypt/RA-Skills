## Description: <br>
Cloudinary (cloudinary.com). Use this skill for ANY Cloudinary request - reading, creating, and updating data. Whenever a task involves Cloudinary, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Cloudinary assets through an OOMOL-connected account, including reading assets, listing uploads, uploading assets, renaming assets, and updating mutable asset fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Cloudinary assets through an OOMOL-connected account, including uploads, renames, and mutable asset updates. <br>
Mitigation: Review and confirm exact write payloads before approving uploads, renames, or updates. <br>
Risk: The skill requires sensitive Cloudinary access through OOMOL-provided credentials and connector infrastructure. <br>
Mitigation: Install only if the user intends to let an agent manage Cloudinary through the connected OOMOL account and trusts OOMOL as the connector provider. <br>


## Reference(s): <br>
- [Cloudinary homepage](https://cloudinary.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-cloudinary) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
