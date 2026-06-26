## Description: <br>
Pluggable AI report engine for generating AI, finance, and stock briefings from multiple public data sources with scoring, deduplication, LLM editing, rendering, scheduling, and optional delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx9826](https://clawhub.ai/user/llx9826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate recurring AI/CV, finance, and market reports from configured presets or user hints. It can render reports as HTML, Markdown, and optional PDF, with email or webhook delivery when explicitly configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User hints, report context, and fetched public-source data may be sent to a configured LLM provider. <br>
Mitigation: Use only approved LLM endpoints and avoid entering secrets, private portfolio details, or confidential business data in hints or configuration. <br>
Risk: Email and webhook delivery can forward generated reports to external recipients or arbitrary webhook URLs. <br>
Mitigation: Keep delivery disabled until recipients, webhook URLs, and channel permissions are reviewed and trusted. <br>
Risk: Generated HTML reports may include content derived from external sources. <br>
Mitigation: Review generated reports before forwarding or opening in sensitive environments, especially until the renderer sanitization behavior is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx9826/lunaclaw-brief) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/skill.yaml) <br>
- [Artifact usage guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated report files such as HTML, Markdown, and optional PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns report paths and issue metadata; optional email and webhook delivery require trusted configuration.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
