## Description: <br>
Generate and optimize clinical trial subject inclusion/exclusion criteria to balance scientific rigor with recruitment feasibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical trial protocol teams and life-science researchers use this skill to draft, optimize, analyze, and benchmark eligibility criteria for protocol design, enrollment feasibility, recruitment strategy, and competitive eligibility review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send target, drug, company, indication, or trial queries to external PatSnap MCP services or web-search providers. <br>
Mitigation: Use only data your organization permits to share with those services, and avoid confidential protocol drafts, unpublished strategy, patient data, or proprietary study materials. <br>
Risk: Generated eligibility criteria and feasibility estimates can influence clinical trial design decisions. <br>
Mitigation: Have qualified clinical, regulatory, and safety reviewers validate all proposed criteria, rationales, and enrollment assumptions before protocol use. <br>
Risk: The artifact includes CLI commands that read and write local JSON files. <br>
Mitigation: Run commands in a controlled workspace and review input and output paths before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/inclusion-criteria-gen) <br>
- [AIPOCH publisher profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Criteria templates](references/criteria_templates.json) <br>
- [Optimization guidelines](references/optimization_guidelines.md) <br>
- [Common pitfalls](references/common_pitfalls.md) <br>
- [Regulatory guidance](references/regulatory_guidance.md) <br>
- [Feasibility data](references/feasibility_data.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON criteria, analysis, optimization, or benchmark report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI and Python API flows can read criteria JSON input and write generated report JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
