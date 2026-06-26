## Description: <br>
Professional Adobe Photoshop automation via ExtendScript bridges for text updates, filters, action playback, layer creation, and image export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative automation users use this skill to let an agent control Adobe Photoshop on Windows or macOS for active-document edits, filters, recorded actions, and PNG/JPEG exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local Photoshop scripting power that can modify open documents and local files. <br>
Mitigation: Use backed-up PSDs, review generated ExtendScript before execution, and avoid running it against sensitive folders or untrusted prompts. <br>
Risk: Export commands can write files wherever the current user account has access. <br>
Mitigation: Confirm export paths before execution and constrain outputs to expected project directories. <br>
Risk: Photoshop modal dialogs, missing active documents, or mismatched layer names can cause commands to fail or hang. <br>
Mitigation: Close Photoshop dialogs and verify the active document, target layers, and action names before running automation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdul-karim-mia/photoshop-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Markdown status messages and generated ExtendScript executed through local Photoshop automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Adobe Photoshop on Windows or macOS; commands operate on the active document.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
