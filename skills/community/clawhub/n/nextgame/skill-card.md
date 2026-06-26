## Description: <br>
Create and upload a mobile-compatible HTML game with wallet-linked configuration and preview image for thenext.games. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianclan](https://clawhub.ai/user/brianclan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game creators use this skill to prepare a mobile-compatible HTML game, create the required config.json, index.html, and preview.png files, upload them to the listed game-publishing service, and share the resulting thenext.games URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads game files to an external service that may make them publicly accessible. <br>
Mitigation: Before running upload commands, inspect config.json, index.html, and preview.png, confirm the destination and gameFolder name, and do not upload secrets, private workspace files, copyrighted material, or content that should not be public. <br>
Risk: The listed upload interfaces do not overwrite existing files, so duplicate or unintended gameFolder names can fail or publish to the wrong location. <br>
Mitigation: Choose a unique English gameFolder name, verify it before each upload, and check API responses before sharing the resulting thenext.games URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianclan/nextgame) <br>
- [Game upload service](https://www.idlab.top) <br>
- [Published game URL format](https://thenext.games/game/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload instructions and file-format guidance for config.json, index.html, and preview.png.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
