## Description: <br>
Controls JFTech smart pet feeders by checking feeding support, issuing one-time feed commands, managing scheduled feeding plans, and toggling pet-detection settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers with JFTech feeder credentials use this skill to check device capability, feed an online bound device, manage feeding schedules, and configure pet-detection switching. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America via the JFTech regional API hosts listed in the skill metadata. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can feed a real device and change feeding schedules. <br>
Mitigation: Review feed amounts, schedule changes, and target device identity before allowing an agent to run feed or schedule-changing actions. <br>
Risk: The skill uses powerful device credentials and a configurable API endpoint. <br>
Mitigation: Keep JF_APP_SECRET and JF_DEVICE_TOKEN private, and set JF_ENDPOINT only to trusted JFTech regional API hosts. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub release page](https://clawhub.ai/jftech/jf-open-pro-feed-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with environment-variable setup and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API calls that return JSON from JFTech feeder endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
