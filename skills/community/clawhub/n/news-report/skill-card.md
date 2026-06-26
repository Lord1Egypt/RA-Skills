## Description: <br>
Collects news from multiple search engines, guides LLM analysis, and generates a self-contained dark-dashboard HTML report for a requested keyword or topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather recent search snippets for a topic, ask an LLM to organize them into structured report data, and generate a self-contained HTML news analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and generated reports may be sent to external services or shared through Feishu. <br>
Mitigation: Avoid sensitive topics or confidential report content, and review delivery destinations before sending or sharing the generated HTML. <br>
Risk: Generated HTML is built from web and LLM-derived fields and may contain unsafe or misleading content. <br>
Mitigation: Review the HTML locally before distribution and prefer a fixed version that escapes or sanitizes report fields. <br>
Risk: The fetch script disables TLS certificate verification when requesting search pages. <br>
Mitigation: Use a fixed version that restores TLS verification before relying on fetched results in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/news-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON report data, and self-contained HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches search-result snippets, depends on LLM-created report JSON, and writes an HTML report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
