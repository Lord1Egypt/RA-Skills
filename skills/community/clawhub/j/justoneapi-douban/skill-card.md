## Description: <br>
Analyze Douban Movie workflows with JustOneAPI, including movie reviews, review details, subject details, comments, and recent hot movie or TV data across 6 GET operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve exact Douban Movie data through JustOneAPI for review research, subject enrichment, sentiment sampling, catalog workflows, and movie or TV trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token is sent in URL query parameters and may appear in copied URLs, logs, screenshots, or error traces. <br>
Mitigation: Use a revocable or rotatable token, avoid sharing full request URLs or logs, and prefer a narrowly scoped token when the provider supports it. <br>
Risk: The skill depends on an external JustOneAPI service and a local Node.js runtime. <br>
Mitigation: Confirm node is available, keep JUST_ONE_API_TOKEN private, and handle backend errors by reviewing the operation ID and returned payload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douban) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown answer with selected JSON fields or raw JSON from JustOneAPI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; requests are GET calls with token, subject, review, sort, and page parameters.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
