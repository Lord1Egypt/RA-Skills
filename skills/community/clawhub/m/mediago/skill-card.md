## Description: <br>
Download videos from m3u8/HLS streams, Bilibili, and direct URLs using MediaGo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caorushizi](https://clawhub.ai/user/caorushizi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and media operators use this skill to configure a running MediaGo instance and ask an agent to start and monitor downloads from HLS, Bilibili, or direct video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the MediaGo service URL and optional API key in a local configuration file. <br>
Mitigation: Use a MediaGo API key scoped for this workflow, keep ~/.mediago-skill.json private, and rotate the key if the workstation or repository environment is shared. <br>
Risk: The skill sends user-provided video URLs to a running MediaGo instance and starts downloads. <br>
Mitigation: Review requested URLs before starting downloads and use MediaGo in an environment with appropriate storage, network, and content-use controls. <br>
Risk: The skill depends on a reachable local or LAN MediaGo API endpoint. <br>
Mitigation: Bind MediaGo only to trusted interfaces, require an API key when exposed beyond localhost, and verify the configured endpoint before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caorushizi/mediago) <br>
- [MediaGo Project](https://github.com/caorushizi/mediago) <br>
- [MediaGo Releases](https://github.com/caorushizi/mediago/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-language status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write MediaGo connection settings to ~/.mediago-skill.json and report download status from the local MediaGo API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
