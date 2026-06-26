## Description: <br>
PKU Treehole (北大树洞) anonymous forum CLI tool built in Rust for working with the Treehole crate, Treehole REST APIs, IAAA login flows, and PKU schedule, grade, calendar, and forum commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to understand, debug, and extend a Rust CLI for PKU Treehole, including authenticated login, post browsing and interaction, notifications, schedules, grades, and calendar queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward broad authenticated access to a user's PKU Treehole account, including schedule, grade, profile, posting, replying, and voting actions. <br>
Mitigation: Require user confirmation before login, account reads, posting, replying, voting, or other state-changing commands, and clear the saved session when persistent access is no longer needed. <br>
Risk: The skill depends on local treehole and info-auth binaries whose behavior is outside the instruction file itself. <br>
Mitigation: Install and run the skill only in environments where those local binaries are trusted and reviewed. <br>


## Reference(s): <br>
- [Treehole Skill Page](https://clawhub.ai/wjsoj/pku-treehole) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated CLI actions that should be confirmed before accessing account data or changing forum state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
