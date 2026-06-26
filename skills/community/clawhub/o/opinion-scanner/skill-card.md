## Description: <br>
Scans public web and social sources for a company or person, labels items as positive, negative, or neutral, preserves original links, and produces a structured Markdown public-opinion report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, communications teams, and agents use this skill to gather recent public information about a named company or person, classify public sentiment, and prepare a sourced reputation report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can profile named individuals through public-source reputation analysis. <br>
Mitigation: Use it only for lawful, legitimate public-interest or authorized analysis, and avoid targeting private individuals without a valid reason. <br>
Risk: Generated reports may persist sensitive names, links, and summaries in shared or long-lived workspace storage. <br>
Mitigation: Confirm the report save location before use, restrict access to generated reports, and remove or redact sensitive reports when they are no longer needed. <br>
Risk: Automated sentiment labels and summaries can be incomplete or misleading when source coverage is sparse or blocked. <br>
Mitigation: Review the preserved source links and key excerpts before relying on conclusions or sharing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hugogu/opinion-scanner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hugogu) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Structured Markdown report with source links, sentiment labels, summary tables, keywords, findings, and disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include target names, public links, article summaries, sentiment labels, and dated report paths when the agent saves files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
