## Description: <br>
Routes photo edit requests to OraHub workflows for color matching, passersby removal, background cutouts, and background replacement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orahub-ora](https://clawhub.ai/user/orahub-ora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this router to select and run the right OraHub image-editing workflow for local image paths or public image URLs. The bundled leaf skills handle validation, CLI execution, output naming, and media delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or update the OraHub CLI and start device-login or API-key setup. <br>
Mitigation: Approve install, upgrade, or authentication commands only when you intend to use OraHub for the requested photo-editing workflow and trust the orahub-cli package. <br>
Risk: User photos, local paths, or image URLs may be processed through OraHub during workflow execution. <br>
Mitigation: Run the skill only for photos or URLs you expect OraHub to process, and use the bundled public-URL validation and approval prompts before execution. <br>
Risk: VirusTotal telemetry was pending when the security verdict was generated. <br>
Mitigation: Treat the ClawHub clean verdict as based on artifact review and available scanner context, and re-check security evidence if deployment policy requires completed VirusTotal telemetry. <br>


## Reference(s): <br>
- [Platform compatibility and OraHub CLI rules](references/platform-compatibility.md) <br>
- [ClawHub skill page](https://clawhub.ai/orahub-ora/orahub-skills) <br>
- [Publisher profile](https://clawhub.ai/user/orahub-ora) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated image file paths or MEDIA delivery lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Leaf workflows produce edited image files, usually JPG or PNG, with predictable output names and batch summaries when applicable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
