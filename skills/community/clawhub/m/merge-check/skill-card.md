## Description: <br>
Analyze a GitHub pull request for mergeability by assessing technical, architectural, process, social, and compliance factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to assess whether a GitHub pull request is likely to merge and to identify concrete blockers, strengths, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries GitHub through the user's local gh login and may include private repository metadata, review text, and PR discussion in the analysis. <br>
Mitigation: Use a GitHub account or token with the least repository access needed for the PRs being reviewed. <br>
Risk: Mergeability predictions can be incomplete when GitHub API calls fail or return partial data. <br>
Mitigation: Review any error fields or missing data noted by the script before relying on the final recommendation. <br>


## Reference(s): <br>
- [PR Rejection Vector Taxonomy](references/rejection-taxonomy.md) <br>
- [ClawHub skill page](https://clawhub.ai/tag-assistant/merge-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown report supported by JSON gathered from the GitHub CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report includes a mergeability score, risk factors, strengths, recommendations, and a verdict.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
