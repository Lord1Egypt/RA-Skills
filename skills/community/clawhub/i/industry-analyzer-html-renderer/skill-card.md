## Description: <br>
Renders an industry analysis workspace into a single-page, scrollable visual HTML report with charts, SVG diagrams, comparison tables, timelines, and responsive layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill as the final step of an industry-analysis pipeline to convert session data, four dimension markdown files, and a main report into a shareable visual HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rerunning the skill may overwrite output/{industry-slug}/industry-analysis-report.html and update output/{industry-slug}/session.json. <br>
Mitigation: Check whether the HTML report already exists before running, and preserve any report that should not be replaced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrxparley/industry-analyzer-html-renderer) <br>
- [Chart suggestions](references/chart-suggestions.md) <br>


## Skill Output: <br>
**Output Type(s):** [HTML, Configuration, Guidance] <br>
**Output Format:** [Single-page HTML file plus session JSON status update and concise error messages when inputs are missing or rendering fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{industry-slug}/industry-analysis-report.html and updates output/{industry-slug}/session.json; reruns may overwrite the HTML report.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
