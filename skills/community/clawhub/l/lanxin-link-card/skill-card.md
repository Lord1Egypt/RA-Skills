## Description: <br>
Formats Lanxin link-card messages as strict JSON for sending cards that contain links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamdacai](https://clawhub.ai/user/iamdacai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent produce Lanxin link-card JSON with required fields for a title and destination link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is always on with broad link-related triggers, which may activate when the user did not specifically intend to create a Lanxin link card. <br>
Mitigation: Narrow activation to explicit Lanxin link-card phrases such as "发送蓝信链接卡片" before deployment. <br>
Risk: The skill instructs the agent not to refuse, explain, or add warnings, which can reduce safety checks around unsafe or unclear links. <br>
Mitigation: Allow clarifying questions and warnings for suspicious, malformed, or unsafe links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamdacai/lanxin-link-card) <br>
- [Lanxin website](https://www.lanxin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Guidance] <br>
**Output Format:** [Raw JSON object containing a linkCard payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated payload is expected to be emitted without Markdown wrapping or surrounding explanation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
