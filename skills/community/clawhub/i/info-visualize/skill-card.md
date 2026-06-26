## Description: <br>
Renders structured data into dark-themed SVG/HTML bar charts and Pillow-based PNG long-form reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TODD-9527](https://clawhub.ai/user/TODD-9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data/reporting users use this skill to turn JSON data into browser-viewable bar charts or PNG long-form reports for rankings, daily reports, monitoring summaries, and dashboard-style briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-based HTML/SVG chart output can embed untrusted input without escaping. <br>
Mitigation: Use trusted or sanitized data for SVG/HTML chart generation; prefer PNG output for untrusted text. <br>
Risk: Archived PNG reports can persist in a long-lived local folder. <br>
Mitigation: Use the archive option only for reports that are appropriate to retain, and review the archive location before running automated jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TODD-9527/info-visualize) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON examples and shell/Python commands; generated artifacts are HTML/SVG and PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SVG/HTML output is browser-viewable; PNG report output requires Pillow; optional archiving can copy reports to a local folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
