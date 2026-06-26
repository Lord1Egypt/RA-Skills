## Description: <br>
Jike Geo helps agents monitor brand visibility across AI search engines, analyze mentions, generate GEO optimization questions and articles, and guide distribution workflows for owned media channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzoob](https://clawhub.ai/user/mzoob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, content, and growth teams use this skill to evaluate how brands appear in AI search results, compare visibility across supported AI platforms, and generate GEO-focused questions, articles, and publishing records. Developers or operators must configure the JIKE_GEO_SECRET_KEY credential before using the CLI-backed workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business, product, competitor, or launch details provided to the skill may be used with web search or external GEO services. <br>
Mitigation: Avoid providing confidential strategy, customer data, unreleased product details, or other sensitive business information unless that external use is acceptable. <br>
Risk: Incorrect company profile inputs can reduce the quality of generated GEO questions and articles. <br>
Mitigation: Base company fields on user-provided facts or verified public sources, and ask the user to confirm missing business details before saving profile data. <br>


## Reference(s): <br>
- [Jike Geo ClawHub Skill Page](https://clawhub.ai/mzoob/jike-geo) <br>
- [Jike Geo Homepage](https://jike-geo.100.city) <br>
- [Workflow Guide](references/workflow-guide.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [API Key Setup Guide Image](https://file.dso100.com/geo_guide.png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_GEO_SECRET_KEY credential; some API-backed tasks are asynchronous and may require polling.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
