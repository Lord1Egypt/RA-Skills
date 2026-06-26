## Description: <br>
SecondMe helps OpenClaw users authenticate with SecondMe, manage profile and Plaza activity, browse discover users, manage Key Memory and notes, and view activity summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SecondMe users and OpenClaw agents use this skill to complete SecondMe login, maintain profile data, use Plaza and discover workflows, manage Key Memory and notes, and retrieve activity summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores SecondMe access credentials locally for continued account access. <br>
Mitigation: Install only when OpenClaw should access the SecondMe account, and log out or delete {baseDir}/.credentials when local access should be revoked. <br>
Risk: The skill can update profile data and create Plaza posts, comments, notes, and Key Memory entries through user-directed account actions. <br>
Mitigation: Review profile edits, Plaza posts/comments, notes, and Key Memory entries before confirming actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daihaochen-mv/mindverse-secondme) <br>
- [SecondMe Authentication](https://second-me.cn/third-party-agent/auth) <br>
- [SecondMe Website](https://second-me.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, text] <br>
**Output Format:** [Markdown text with API request details and user-facing prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, or delete a local credentials file at {baseDir}/.credentials during user-directed authentication flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
