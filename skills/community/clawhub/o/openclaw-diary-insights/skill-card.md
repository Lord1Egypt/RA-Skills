## Description: <br>
Extracts thought cards, mood timelines, growth-dimension scores, and knowledge-graph data from local diary files, then generates an interactive local visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smorzandos](https://clawhub.ai/user/smorzandos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Journal users and personal knowledge-management users use this skill to analyze local diary Markdown files, extract personal insights and mood trends, and produce local HTML and JSON outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads diary folders and optional identity files, then creates derived summaries that may contain sensitive personal information. <br>
Mitigation: Install only if you are comfortable with that access, review the configured storage.path before running, and treat generated HTML, data.js, and JSON outputs as sensitive. <br>
Risk: The generated visualization may load third-party CDN scripts or fonts when opened in a browser. <br>
Mitigation: Avoid opening the generated page online unless you accept those CDN requests; use local assets or an offline review flow for stronger privacy. <br>


## Reference(s): <br>
- [OpenClaw Diary Insights on ClawHub](https://clawhub.ai/smorzandos/openclaw-diary-insights) <br>
- [Diary System homepage](https://github.com/openclaw-community/diary-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance plus generated JavaScript, JSON, and HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local diary Markdown and optional identity files; writes local insights HTML, data.js, and JSON backup files under ~/write_me/02notes/insights/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
