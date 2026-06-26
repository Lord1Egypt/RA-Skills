## Description: <br>
Query Kimi Code Plan quota and usage information, including subscription quota, usage percentage, reset time, and API key status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doraohm1](https://clawhub.ai/user/doraohm1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through checking Kimi Code Plan quota, reset timing, membership level, model access, and high-level API key status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow opens a user's Kimi Code account pages and can expose private usage, membership, and API-key metadata. <br>
Mitigation: Ask the agent to report only the quota and high-level API-key status needed, avoid sharing masked key fragments or identifiers, and delete quota.png after use if it contains account details. <br>


## Reference(s): <br>
- [Kimi Code](https://www.kimi.com/code) <br>
- [Kimi Code Console](https://www.kimi.com/code/console) <br>
- [ClawHub Skill Page](https://clawhub.ai/doraohm1/kimi-code-quota) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with browser automation commands and a quota summary table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create quota.png during the browser workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
