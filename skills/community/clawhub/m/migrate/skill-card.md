## Description: <br>
Export and import Clawdbot installations for migration between machines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrGoodB](https://clawhub.ai/user/MrGoodB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot operators use this skill to create portable backups and restore Clawdbot installations on another machine, including workspace files, configuration, managed skills, WhatsApp session state, and optional credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives can contain sensitive Clawdbot state, WhatsApp session data, transcripts, or credentials. <br>
Mitigation: Protect exported archives like account credentials, avoid --include-credentials unless required, and transfer or store archives only through trusted channels. <br>
Risk: Importing an archive can merge or overwrite an existing Clawdbot workspace and configuration, especially when --force is used. <br>
Mitigation: Import only archives created by a trusted operator and use --force only on a fresh or intentionally replaceable installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrGoodB/migrate) <br>
- [Publisher profile](https://clawhub.ai/user/MrGoodB) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated tar.gz backup archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Export output may include sensitive Clawdbot state when sessions or credentials are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
