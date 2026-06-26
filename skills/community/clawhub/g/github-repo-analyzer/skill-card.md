## Description: <br>
Analyze GitHub repositories to summarize public repository statistics, contributor activity, languages, tech stack, and issue and pull request trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to research public GitHub repositories and quickly understand project activity, contributors, languages, repository metadata, and maintenance signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names or URLs requested by the user are sent to GitHub's public API. <br>
Mitigation: Use the skill only for public repositories or repository identifiers that are acceptable to disclose to GitHub. <br>
Risk: Unauthenticated public API requests may be rate-limited or return incomplete data. <br>
Mitigation: Treat the analysis as a current public snapshot and verify important repository metrics directly when precision matters. <br>


## Reference(s): <br>
- [GitHub Repo Analyzer on ClawHub](https://clawhub.ai/dagangtj/github-repo-analyzer) <br>
- [Publisher profile: dagangtj](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and JSON-formatted repository analysis from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script accepts a public GitHub repository in owner/repo or github.com/owner/repo form and returns repository metadata, counts, languages, contributors, dates, license, homepage, and topics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
