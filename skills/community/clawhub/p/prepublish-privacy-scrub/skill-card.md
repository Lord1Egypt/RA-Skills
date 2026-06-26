## Description: <br>
Scan and remove sensitive data before publishing skills. Detect API keys, tokens, secrets, and personal info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill authors use this skill before publishing or pushing skill files to scan for secrets, redact common credential patterns, and complete a privacy checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scrub command can overwrite files in place while the documentation claims backups are made. <br>
Mitigation: Run it only on version-controlled or copied folders, review changes before publishing, and avoid broad use on directories containing binary or important non-skill files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dalomeve/prepublish-privacy-scrub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell code blocks and checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local scan and scrub guidance; no external logging is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
