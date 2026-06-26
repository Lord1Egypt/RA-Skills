## Description: <br>
Info Vivid renders structured data into dark-themed SVG/HTML bar charts and Pillow-based PNG longform reports for reporting, ranking, and monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TODD-9527](https://clawhub.ai/user/TODD-9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn JSON datasets into browser-viewable bar charts or PNG reports for monitoring reports, daily or weekly updates, rankings, and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad visualization prompts may route to this skill even when the user did not intend to generate a chart or report. <br>
Mitigation: Confirm the intended dataset and output type before using the skill for broad requests such as "visualize data". <br>
Risk: Sensitive data supplied for visualization may be written into generated HTML/SVG or PNG report files. <br>
Mitigation: Only provide datasets intended for report generation, and review generated files before sharing or archiving them. <br>


## Reference(s): <br>
- [Info Vivid ClawHub listing](https://clawhub.ai/TODD-9527/info-vivid) <br>
- [SVG chart output screenshot](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-01-svg-chart.png) <br>
- [Longform report output screenshot](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-02-longform-report.png) <br>
- [JSON to output screenshot](https://raw.githubusercontent.com/TODD-9527/skill-assets/main/screenshots/info-vivid-03-json-to-output.png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, Python snippets, and shell commands; generated artifacts are HTML/SVG or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SVG/HTML generation uses Python standard library code; PNG report generation requires Pillow and can optionally copy output to an archive path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
