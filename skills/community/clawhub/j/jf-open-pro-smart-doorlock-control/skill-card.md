## Description: <br>
JFTech smart door lock control skill for checking door-lock support, logging in to a device, obtaining a device API token, and sending a remote one-key unlock command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to integrate JFTech smart door locks with an agent workflow for device capability checks, token retrieval, configuration lookup, device login, and remote unlock operations. <br>

### Deployment Geography for Use: <br>
China mainland, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remotely unlock a physical smart door lock, and the security evidence reports weak documented safeguards around immediate unlock actions. <br>
Mitigation: Install only when the publisher is trusted, restrict who can invoke the skill, and require explicit confirmation or stronger authorization before every unlock command. <br>
Risk: The skill depends on API credentials, app secrets, device serial numbers, and device tokens for lock operations. <br>
Mitigation: Store credentials outside prompts and logs, scope them to the intended device and region, rotate tokens when exposed, and avoid sharing unlock-capable environment variables. <br>
Risk: A configurable endpoint could send lock-control requests outside the intended regional JFTech host. <br>
Mitigation: Pin JF_ENDPOINT to the intended JFTech regional host before use and review any endpoint changes before executing device actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-smart-doorlock-control) <br>
- [JFTech open platform documentation](https://docs.jftech.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech account, app credentials, device serial number, device token, and regional API endpoint configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
