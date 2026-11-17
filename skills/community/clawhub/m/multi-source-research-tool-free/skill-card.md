## Description: <br>
Integrates web search, academic platforms, social media, and news sources to deduplicate research material, classify source credibility, and produce structured research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, individual researchers, analysts, and developers use this skill to gather material from multiple online source classes, remove overlapping results, label credibility, and generate a structured Markdown report for a single research topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts can expose confidential project names, personal data, or sensitive internal questions to external search and content sources. <br>
Mitigation: Avoid sensitive or personal terms unless external lookup is intended; narrow prompts and redact confidential details before using the skill. <br>
Risk: Broad activation can cause unrelated analysis requests to be handled as internet research tasks. <br>
Mitigation: Limit activation to explicit research, source-gathering, literature-review, news, or public-opinion analysis requests. <br>
Risk: Generated reports may contain incorrect, outdated, or misleading claims from collected sources. <br>
Mitigation: Review high-impact findings against primary sources and use the credibility labels as review prompts rather than guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-source-research-tool-free) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with source statistics, credibility labels, configuration examples, and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition focuses on one research topic at a time and does not export PDF or Word reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
