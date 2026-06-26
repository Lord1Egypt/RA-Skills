## Description: <br>
Monitor Google Trends - get trending searches, compare keywords, and track interest over time. Use for market research, content planning, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satnamra](https://clawhub.ai/user/satnamra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing, research, SEO, and content-planning users use this skill to retrieve daily Google Trends, compare keyword interest, and identify related topics or regional search interest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web requests to Google Trends may be rate limited or fail if Google changes its RSS or Explore endpoints. <br>
Mitigation: Use the skill for lightweight trend checks, handle failed requests gracefully, and verify important findings in Google Trends directly. <br>
Risk: Passing arbitrary text into shell commands can create quoting or command-injection risk. <br>
Mitigation: Use two-letter country codes and URL-encoded keywords, and review generated shell commands before execution. <br>


## Reference(s): <br>
- [Google Trends skill page](https://clawhub.ai/satnamra/google-trends) <br>
- [Google Trends Daily RSS](https://trends.google.com/trending/rss?geo=US) <br>
- [Google Trends Explore](https://trends.google.com/trends/explore?q=bitcoin&geo=US) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and trend summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make public web requests to Google Trends and may produce country-specific trend lists when supplied a country code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
