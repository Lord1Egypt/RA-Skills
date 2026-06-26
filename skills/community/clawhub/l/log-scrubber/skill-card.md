## Description: <br>
Automatically redacts API keys, tokens, and secrets from workspace logs and memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heather-Herbert](https://clawhub.ai/user/Heather-Herbert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan OpenClaw workspace logs and memory files for secret-like values, preview redactions with dry-run mode, and apply local redaction when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying redaction can overwrite workspace log and memory files. <br>
Mitigation: Run the dry-run command first and review the listed files before applying changes. <br>
Risk: Backup files may retain original unredacted secrets. <br>
Mitigation: Handle .bak files carefully after applying redaction, and delete or store them securely once they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text terminal output and modified workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create .bak backups containing original file contents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
