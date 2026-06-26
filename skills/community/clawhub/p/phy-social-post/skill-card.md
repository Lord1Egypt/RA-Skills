## Description: <br>
Post to social media platforms using the multi-provider social posting API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare, check, schedule, and publish posts across connected social media accounts through a local social-posting API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live posting workflows using social media provider API keys. <br>
Mitigation: Verify the separate local social-posting-api code and keep only required provider keys in its .env file before use. <br>
Risk: Post content, media, platforms, connected accounts, or schedule could be wrong or unintended. <br>
Mitigation: Require manual final review of the post text, media, platforms, connected accounts, and schedule before running any posting command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-social-post) <br>
- [Canlah AI](https://canlah.ai) <br>
- [PostForMe dashboard](https://postforme.dev/dashboard) <br>
- [LATE dashboard](https://getlate.dev/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include post text, media URL guidance, platform selections, schedule values, and account-check commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
