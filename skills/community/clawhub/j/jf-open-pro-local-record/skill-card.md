## Description: <br>
Helps agents manage JFTech device local recordings, including recording calendars, file lists, playback and download URLs, local alarm images, and stream switching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, play back, download, and adjust local recordings on bound JFTech devices with TF-card or hard-drive storage. <br>

### Deployment Geography for Use: <br>
Global, with documented regional API hosts for China, Asia, Europe, and North America. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles device credentials, device tokens, and private playback, download, and alarm-image URLs. <br>
Mitigation: Treat all configured credentials and returned media URLs as confidential, avoid logging or sharing them, and rotate tokens if exposure is suspected. <br>
Risk: Endpoint selection is controlled by JF_ENDPOINT and could send signed requests to an unintended host. <br>
Mitigation: Keep JF_ENDPOINT set to an official JFTech regional host before running API actions. <br>
Risk: The current CLI has a duplicate --stream-type argument defect that can prevent normal startup. <br>
Mitigation: Review and fix the argument conflict before relying on the playback or record-list commands in production. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill listing](https://clawhub.ai/jftech/jf-open-pro-local-record) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill's helper script can print recording metadata, playback or download URLs, and alarm image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
