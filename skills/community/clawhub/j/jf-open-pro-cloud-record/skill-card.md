## Description:

JFTech cloud storage skill for JFTech devices that helps agents query cloud video lists, retrieve playback or download URLs, and query cloud alarm messages for devices with an active cloud storage plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with JFTech camera cloud storage: listing videos, obtaining HLS playback or MP4 download URLs, and checking alarm history. It requires configured JFTech OpenAPI credentials, a bound device, and an active cloud storage plan.

### Deployment Geography for Use:

China Mainland (CN), Asia (AS), Europe (EU), and North America (NA)

## Known Risks and Mitigations:

Risk: Sensitive camera credentials could be sent to an unintended API host if JF_ENDPOINT is changed.

Mitigation: Set JF_ENDPOINT only to documented official JFTech regional hosts and run the skill where other users or wrappers cannot alter environment variables.

Risk: Playback/download URLs, app secrets, device tokens, serial numbers, and alarm history may expose private camera data.

Mitigation: Treat these values as secrets, avoid logging or sharing them, and review console output before forwarding it to other systems.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-cloud-record)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown or plain text with shell command examples and console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return video lists, alarm records, and playback or download URLs. The artifact documents playback/download URLs as valid for 24 hours.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
