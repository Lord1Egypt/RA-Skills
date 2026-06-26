## Description: <br>
Gladia helps an agent operate Gladia transcription workflows through an OOMOL-connected account, including listing, retrieving, starting, uploading, downloading, and deleting transcription-related data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage Gladia pre-recorded transcription jobs through the oo CLI with an OOMOL-connected Gladia account. It supports read workflows, media upload and download, job creation, and explicit deletion of transcription data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start transcription jobs and upload audio or video files to Gladia. <br>
Mitigation: Confirm the exact payload, media source, and intended account effect with the user before running write-tagged actions. <br>
Risk: The skill can delete a Gladia pre-recorded transcription job and associated data. <br>
Mitigation: Require explicit user approval for the target transcription job before running the destructive delete action. <br>
Risk: The skill depends on an OOMOL-connected Gladia account and sensitive credentials managed outside the skill bundle. <br>
Mitigation: Use the documented oo CLI authentication and connection flow only after an action fails for authentication or connection reasons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-gladia) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Gladia homepage](https://app.gladia.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects returned by the oo CLI when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release version and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
