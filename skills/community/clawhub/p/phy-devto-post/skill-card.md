## Description: <br>
Post articles to DEV.to using AppleScript Chrome control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to publish technical blog posts, showdev articles, and open source project announcements to DEV.to from a logged-in Chrome session on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact authority to publish through the DEV.to account currently logged in to Chrome. <br>
Mitigation: Require manual final confirmation before commands that post with published:true or click Publish, and review the exact title, tags, body, and published state. <br>
Risk: Publishing from the user's real browser session may affect the wrong DEV.to account or profile. <br>
Mitigation: Use a separate Chrome profile or test account when possible and confirm the active DEV.to account before publishing. <br>


## Reference(s): <br>
- [Phy Devto Post on ClawHub](https://clawhub.ai/PHY041/phy-devto-post) <br>
- [Canlah AI](https://canlah.ai) <br>
- [DEV Community](https://dev.to) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash, JavaScript, and article-template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces publishing instructions and command snippets; actual publication depends on a logged-in Chrome session and user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
