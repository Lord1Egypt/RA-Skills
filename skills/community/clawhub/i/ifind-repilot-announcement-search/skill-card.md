## Description: <br>
Searches company announcement information for A-shares, funds, Hong Kong stocks, and U.S. stocks with natural-language queries, returning relevant announcement snippets and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenzisay](https://clawhub.ai/user/wenzisay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, investors, and research agents use this skill to retrieve public company announcements, financial reports, regulatory announcements, prospectuses, and related announcement snippets through the iFinD/RePilot API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an iFinD/RePilot token stored in a local config file. <br>
Mitigation: Treat the token as sensitive, avoid sharing config contents or transcripts containing it, and rotate the token if it may have been exposed. <br>
Risk: Search queries are sent to the iFinD/RePilot service and may contain sensitive business context. <br>
Mitigation: Use focused announcement-search queries and avoid including unrelated private information. <br>
Risk: The provider API can return no results, authentication errors, permission errors, or rate-limit errors. <br>
Mitigation: Report empty or failed searches clearly, do not invent announcement information, and avoid retrying 401, 403, or 429 responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenzisay/ifind-repilot-announcement-search) <br>
- [iFinD/RePilot platform](https://repilot.51ifind.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON results from the provider script, commonly summarized by the agent in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned data may include announcement titles, summaries, source URLs, publish dates, relevance scores, status messages, and related securities.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
