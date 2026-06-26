## Description: <br>
Provides a health-industry AI application reference library with 62 task types, component checklists, compliance checkpoints, examples, and questionnaire-driven customization for content, design, marketing, operations, support, and training workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, marketing, operations, and training teams in health-related companies use this skill to structure AI-assisted work across copywriting, visual assets, video, packaging, website optimization, business tracking, customer support, and product training. It is also used to turn a company's current manual workflow questionnaire into a customized AI replacement plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to automatically install and load Universal Task OS when it is missing. <br>
Mitigation: Require explicit user or organization approval before installing or loading additional skills; use read-only reference mode when approval is absent. <br>
Risk: Customer names, order data, health information, credentials, or confidential business details may be entered while customizing workflows or support responses. <br>
Mitigation: Use only approved data, apply privacy and retention controls, avoid secrets and unnecessary personal data, and require human review before deployment. <br>
Risk: Health-industry marketing, education, and support outputs can become misleading, non-compliant, or unsupported if examples are reused without validation. <br>
Mitigation: Review outputs against applicable advertising, medical advertising, food safety, platform, evidence, and brand requirements before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/health-ai-applications) <br>
- [Health AI task catalog](references/health-ai-catalog.md) <br>
- [Health AI requirements checklist](references/health-ai-requirements.md) <br>
- [Examples index](references/exemplars.md) <br>
- [Traditional workflow questionnaire](references/traditional-workflow-questionnaire.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, checklists, structured plans, code/configuration snippets, and questionnaire-driven recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate in read-only reference mode when Universal Task OS is unavailable; generated outputs should be reviewed for legal, medical, privacy, and brand compliance before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
