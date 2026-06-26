## Description: <br>
Multi search engine integration with 16 engines (7 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handy01](https://clawhub.ai/user/handy01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run aggregated web searches across Chinese and international search engines, apply advanced operators and time filters, and summarize results into a core search report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may be transmitted to third-party search providers, despite artifact privacy text that says operations stay local. <br>
Mitigation: Use only searches you are comfortable sending to providers such as Google, Baidu, DuckDuckGo, Yahoo, Startpage, Brave, Ecosia, Qwant, and WolframAlpha; avoid credentials, regulated data, private URLs, and sensitive personal details. <br>
Risk: Provider selection and privacy behavior may be unclear to users. <br>
Mitigation: Review the selected search engines before use and prefer privacy-oriented engines when the query content is sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/handy01/handy01-multi-search-engine) <br>
- [Domestic Search Guide](references/advanced-search.md) <br>
- [International Search Guide](references/international-search.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown search report with example web_fetch calls and summarized results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries may be sent to third-party search providers selected by the skill.] <br>

## Skill Version(s): <br>
2.1.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
