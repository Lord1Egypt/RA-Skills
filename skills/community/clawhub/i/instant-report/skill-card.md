## Description: <br>
Instant Report generates professional industry, market, competitor, company, and comparison research reports from Chinese or English user requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianghaist](https://clawhub.ai/user/jianghaist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce structured industry research reports, company research reports, market analyses, competitor studies, and comparative analyses with cited sources and deliverable files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and report content may be processed through web research, subagents, and document-conversion workflows. <br>
Mitigation: Avoid confidential topics unless approved for those workflows, and review generated reports before distribution. <br>
Risk: The skill claims Chinese and English language matching, but security evidence notes it may still produce Chinese output. <br>
Mitigation: Confirm the required output language and translate or revise deliverables before use when English output is required. <br>
Risk: Generated research reports may contain stale, unsupported, or inconsistent market data. <br>
Mitigation: Require source URLs, data cutoff dates, independent source checks, and human review before relying on reports for business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianghaist/instant-report) <br>
- [Data Sources](references/data_sources.md) <br>
- [Report Structure](references/report_structure.md) <br>
- [Quality Checklist](references/quality_checklist.md) <br>
- [Style Guide](references/style_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown report with Mermaid chart syntax, DOCX and PDF files, and a source list with credibility ratings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include source URLs, data freshness notes, fact-checking output, and professional document formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
