## Description: <br>
Analyze Kuaishou workflows with JustOneAPI, including user Search, user Published Videos, and video Details across 7 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make authenticated JustOneAPI requests for Kuaishou user search, profile lookup, published video lookup, video details, comments, video search, and share-link resolution. It is suited to creator research, account monitoring, content performance analysis, and market or keyword tracking when the user provides the required identifiers or filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is passed in request URLs, which can expose it through logs, traces, browser history, or shared command output. <br>
Mitigation: Use a scoped, revocable token where possible, keep JUST_ONE_API_TOKEN out of chat and screenshots, and avoid logging full request URLs. <br>
Risk: Kuaishou profile, video, and comment responses may contain personal or platform-governed data. <br>
Mitigation: Handle returned data according to Kuaishou and JustOneAPI terms and applicable privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-kuaishou) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link) <br>
- [Kuaishou operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API-backed response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected response fields or raw backend JSON when needed for troubleshooting.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
