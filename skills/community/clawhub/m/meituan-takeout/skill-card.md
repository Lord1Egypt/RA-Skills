## Description: <br>
Helps users authenticate with a Meituan account, claim available Meituan takeout coupon benefits, and query local coupon-claim history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-openplatform](https://clawhub.ai/user/meituan-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent skill to sign in to Meituan, claim available coupon benefits, and review prior coupon claims for selected dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains reusable Meituan login tokens and device identifiers on the user's machine. <br>
Mitigation: Install only for a trusted publisher and use the documented logout, clear-device-token, or local file deletion flows when the session should no longer persist. <br>
Risk: Login tokens may appear in command output or be shared with another Meituan authentication skill. <br>
Mitigation: Avoid sharing command transcripts that contain token output and set XIAOMEI_AUTH_FILE to isolate credentials when running in shared, sandboxed, or multi-agent environments. <br>
Risk: Coupon history is stored locally and can reveal account activity. <br>
Mitigation: Set XIAOMEI_COUPON_HISTORY_FILE to an isolated path when needed and delete the local history file when retained records are no longer desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meituan-openplatform/meituan-takeout) <br>
- [Meituan coupon service endpoint](https://peppermall.meituan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include coupon names, amounts, validity dates, masked phone identifiers, login status, error messages, and links returned by the service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
