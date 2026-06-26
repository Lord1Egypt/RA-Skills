## Description: <br>
Exports selected OpenClaw configuration files, skills, or other files as compressed archives and uploads them to tmpfile.link for download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eraycc](https://clawhub.ai/user/eraycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to package selected OpenClaw skills, configuration files, or other chosen paths into tar.gz archives and share them through tmpfile.link download links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can archive and upload broad local file paths to a public third-party host. <br>
Mitigation: Use it only for explicitly selected non-sensitive paths, and inspect the archive contents before sharing the generated link. <br>
Risk: Configuration files, tokens, credentials, private skills, proprietary data, or internal prompts may be exposed if selected for upload. <br>
Mitigation: Do not use the skill on secrets or private/internal material unless the user has reviewed the exact archive and accepted the external sharing risk. <br>
Risk: Uploaded files are hosted outside the local environment and may remain available for the host's retention period. <br>
Mitigation: Share links only with intended recipients and treat anonymous uploads as temporary public file sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eraycc/openclaw-file-exporter) <br>
- [tmpfile.link upload API endpoint](https://tmpfile.link/api/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Terminal output with download links and raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a tar.gz archive up to 100MB and uploads it to tmpfile.link.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
