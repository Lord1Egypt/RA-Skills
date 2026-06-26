## Description: <br>
Provides keyword-based web search guidance for using Miaoda's CLI search-summary command to retrieve AI-generated internet search summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nice1234-h](https://clawhub.ai/user/nice1234-h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route general internet lookups through miaoda-studio-cli search-summary, choosing text or JSON output for follow-on analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may expose secrets, private business details, or confidential personal data to the underlying search and summarization service. <br>
Mitigation: Do not enter sensitive data unless the user trusts the Miaoda CLI and its underlying service for that information. <br>
Risk: The skill has broad activation wording that may make Miaoda CLI search summaries the preferred path for web lookups. <br>
Mitigation: Install it only when that routing behavior is intended, and verify miaoda-studio-cli is installed from a trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nice1234-h/miaoda-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples and optional text or JSON CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries are constrained to 1-500 characters by the artifact guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
