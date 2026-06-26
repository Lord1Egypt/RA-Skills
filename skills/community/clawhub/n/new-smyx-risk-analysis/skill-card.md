## Description: <br>
Analyzes video or images to identify falls, abnormal behavior, and possible health-risk signals, then returns structured risk reports, warnings, recommendations, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, care teams, and developers use this skill to submit video or image files, media URLs, or streams for high-risk behavior and health-risk analysis. The skill can also query cloud-stored historical analysis reports associated with the current internal user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive videos, images, analysis metadata, and identity-linked report history may be sent to the vendor service. <br>
Mitigation: Use only with media and report history that are approved for vendor processing, and avoid sensitive household, medical, or surveillance footage unless retention and access controls are understood. <br>
Risk: The skill can create or reuse a local identity and store service tokens in the workspace data directory. <br>
Mitigation: Run it in a controlled workspace, restrict access to generated data, and review or remove stored identity and token data after use. <br>
Risk: Risk analysis output may affect safety or health decisions but is not a substitute for professional security or medical assessment. <br>
Mitigation: Treat results as advisory, require human review for alerts, and escalate urgent safety or health concerns to qualified responders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/new-smyx-risk-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Risk classification standards and alert levels](references/risk_categories.md) <br>
- [API interface documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown text with JSON-like structured analysis results and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk labels, confidence-style levels, recommendations, report export links, and paginated history listings returned by the vendor service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
