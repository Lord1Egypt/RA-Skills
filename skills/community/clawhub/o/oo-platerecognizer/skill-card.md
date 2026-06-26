## Description: <br>
Plate Recognizer helps agents read license plates from images and retrieve Snapshot Cloud usage through an OOMOL-managed connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Plate Recognizer through an OOMOL-connected account, read plates from selected images, and check current-month Snapshot Cloud usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Plate Recognizer account and sends selected vehicle images to Plate Recognizer Snapshot Cloud. <br>
Mitigation: Install only when this data flow is acceptable, connect Plate Recognizer intentionally, and send only images the user has selected for recognition. <br>
Risk: The setup path includes remote oo CLI installers and authenticated connector access. <br>
Mitigation: Review the oo CLI install source before running remote installers and use setup steps only after auth, connection, or missing-CLI errors. <br>
Risk: Future connector actions could write, delete, or modify data even though the current listed actions are read-oriented. <br>
Mitigation: Fetch the live connector schema before execution and confirm any write or destructive action payload with the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-platerecognizer) <br>
- [Plate Recognizer Homepage](https://platerecognizer.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live OOMOL connector schemas before execution and returns Plate Recognizer action data with execution metadata when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence metadata and release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
