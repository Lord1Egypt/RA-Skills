## Description: <br>
Provides JFTech device cloud storage workflows for querying cloud video lists, retrieving playback or download URLs, and querying cloud alarm messages for devices with an active cloud storage plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run JFTech cloud-camera storage tasks from an agent, including video list lookup, playback or MP4 download URL retrieval, and alarm-message lookup. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles surveillance footage metadata, playback URLs, app secrets, and device tokens. <br>
Mitigation: Use only in trusted environments, keep credentials out of shared shells, logs, and screenshots, and treat returned playback or download URLs as sensitive access links. <br>
Risk: The configurable JF_ENDPOINT can direct credentialed API requests away from expected regional JFTech domains. <br>
Mitigation: Set JF_ENDPOINT only to official JFTech regional domains documented for CN, AS, EU, or NA deployments. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-cloud-record) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-like API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose sensitive playback or download URLs returned by the JFTech cloud API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
