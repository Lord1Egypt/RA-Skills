## Description: <br>
Use when the user asks for GitHub Trending, GitHub hot repositories, daily/weekly/monthly trending repos, trending projects by programming language, spoken-language filtered GitHub trends, or trend analysis of popular GitHub projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei1125](https://clawhub.ai/user/liuwei1125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical analysts, and external users use this skill to fetch public GitHub Trending repositories and turn them into concise trend reports by date range, programming language, and spoken-language filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and makes outbound requests to public GitHub pages. <br>
Mitigation: Run it in an approved environment with expected network access, and review the script before deployment. <br>
Risk: Results depend on GitHub page structure and network availability. <br>
Mitigation: Check for script errors, empty results, and the reported source URL before relying on a report. <br>
Risk: Trend explanations can overstate causes if inferred beyond the fetched repository facts. <br>
Mitigation: Keep factual fields tied to script output and label broader trend analysis as grounded interpretation. <br>


## Reference(s): <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown trend reports or JSON repository data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports daily, weekly, and monthly ranges, optional programming-language and spoken-language filters, and a configurable repository limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
