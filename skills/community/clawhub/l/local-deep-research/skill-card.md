## Description: <br>
Performs multi-cycle, iterative deep research on complex topics using a local LDR service, providing detailed reports with citations and source tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eplt](https://clawhub.ai/user/eplt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research-focused users use this skill to run comprehensive research, literature reviews, competitive intelligence, and iterative source-backed investigations through a locally hosted LDR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and credentials are sent to the configured LDR service. <br>
Mitigation: Keep LDR_BASE_URL and LDR_LOGIN_URL on localhost or another trusted host, and use a dedicated low-privilege LDR account. <br>
Risk: The script sources ~/.config/local_deep_research/config/.env when present, which may expose variables in that file to the skill. <br>
Mitigation: Review that .env file before use and keep unrelated secrets out of it. <br>
Risk: Local document search modes can include private local content in research results. <br>
Mitigation: Avoid local document search modes unless private local content is intended to be included. <br>


## Reference(s): <br>
- [LDR API Reference](references/api.md) <br>
- [LDR Skill Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown research reports with JSON job metadata, status updates, source lists, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include citations, source tracking, progress state, and local document source references when the configured LDR search mode includes local content.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
