## Description: <br>
Helps users assess life satisfaction across eight dimensions, check burnout signals, reflect quarterly, adjust habits, and generate an interactive HTML life-balance report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run a structured life audit, identify imbalanced areas, watch for burnout, and turn self-assessment into practical next steps. It supports personal quarterly reviews, habit resets, and local HTML reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive life, burnout, finance, and reflection data may be saved in browser history by the local HTML report. <br>
Mitigation: Use the report only on trusted devices, avoid entering unnecessary sensitive details, and clear local browser history for the report when it is no longer needed. <br>
Risk: The report template loads Chart.js from a third-party CDN. <br>
Mitigation: Prefer a release that bundles Chart.js locally before using the report with sensitive personal data. <br>


## Reference(s): <br>
- [人生轮盘 8 维度评估指南](references/dimensions.md) <br>
- [Interactive HTML report template](assets/report-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown guidance and generated interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTML report can store assessment history locally in the browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
