## Description: <br>
Fetches daily news summaries and article details from api.cjiot.cc, with support for date-based queries, hot-news ranking, and detail reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic240821](https://clawhub.ai/user/vic240821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve daily news lists, rank hot stories, and read article details for a selected date or article ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News dates and article IDs are sent to the disclosed third-party API at api.cjiot.cc. <br>
Mitigation: Use the skill only for public news lookups and avoid including sensitive private context in news requests. <br>
Risk: Broad news-related trigger words may invoke the skill during ambiguous conversations. <br>
Mitigation: Invoke it for explicit daily-news, dated-news, hot-news, or article-detail requests. <br>
Risk: Article detail responses may contain HTML in story and impact fields. <br>
Mitigation: Strip or convert HTML before presenting article details to users. <br>


## Reference(s): <br>
- [api.cjiot.cc API homepage](https://api.cjiot.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown summaries and Node.js console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and curl; sends selected news dates and article IDs to api.cjiot.cc.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
