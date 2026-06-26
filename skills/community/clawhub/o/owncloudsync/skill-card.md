## Description: <br>
Check that new files on Google Drive are present on OwnCloud and send an email report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SydneyPhoenix26](https://clawhub.ai/user/SydneyPhoenix26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to compare recently created or imported Google Drive files against an OwnCloud file inventory, then generate a daily email report showing files that are present, missing, or older on OwnCloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper file-inventory service can expose broad OwnCloud file metadata if reachable by untrusted clients. <br>
Mitigation: Restrict the service to localhost or a trusted network and require reviewed credentials before enabling it. <br>
Risk: Default credentials and example account values appear in configuration artifacts. <br>
Mitigation: Replace all default credentials and placeholder account values before installation or execution. <br>
Risk: The generated inventory and email report may disclose filenames, freshness, and endpoint details. <br>
Mitigation: Store generated inventory files with restrictive permissions and confirm that emailing detailed file reports is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SydneyPhoenix26/owncloudsync) <br>
- [Publisher profile](https://clawhub.ai/user/SydneyPhoenix26) <br>
- [Homebrew install formula for gog](https://github.com/steipete/homebrew-tap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for running the sync script, configuring owncloud.json, and reviewing generated email report statuses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
