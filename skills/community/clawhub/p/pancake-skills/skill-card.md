## Description: <br>
Pancake Skills helps agents interact with the Pancake Platform API to manage pages, conversations, messages, customers, statistics, tags, posts, users, media uploads, and chat plugin operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suminhthanh](https://clawhub.ai/user/suminhthanh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to run Pancake Platform API workflows from an agent session, including page administration, customer conversation handling, messaging, analytics, media upload, and staff assignment tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe scripting around URL encoding can mishandle sensitive values used in authenticated API requests. <br>
Mitigation: Review or patch scripts before installation, including changing url_encode to pass values as Python argv. <br>
Risk: High-impact account and messaging actions may occur without sufficient write confirmation. <br>
Mitigation: Require CONFIRM_WRITE=YES for token generation and chat-plugin sends, and use the skill only in trusted sessions where those actions are intended. <br>
Risk: Pancake access tokens and customer data may be exposed through logs or chat history. <br>
Mitigation: Avoid pasting tokens into shared transcripts, keep tokens out of logs, and run the skill only where Pancake customer data handling is authorized. <br>


## Reference(s): <br>
- [Pancake OpenAPI specification](references/openapi-pancake.yaml) <br>
- [Pancake API base URL](https://pages.fm) <br>
- [Pancake support contact](https://www.pancake.biz/contact) <br>
- [ClawHub skill page](https://clawhub.ai/suminhthanh/pancake-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute authenticated Pancake API requests when the user provides access tokens and enables write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
