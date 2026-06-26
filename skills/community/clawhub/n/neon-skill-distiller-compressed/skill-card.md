## Description: <br>
Same skill compression power in half the context - 975 tokens vs 2,500. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to compress verbose skill instructions into smaller Markdown while preserving core behavior and reporting compression trade-offs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or append local calibration or output files in the workspace. <br>
Mitigation: Use dry-run or review generated files before accepting changes when workspace modifications are not desired. <br>
Risk: External model provider configuration can expose sensitive credentials if API keys are used in an untrusted environment. <br>
Mitigation: Avoid setting external provider API keys unless the execution environment is trusted and credentials are scoped appropriately. <br>
Risk: Skill compression can remove context or reduce behavioral fidelity if the result is accepted without review. <br>
Mitigation: Review the compressed Markdown, removed-content summary, and reported functionality estimate before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/leegitw/neon-skill-distiller-compressed) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/leegitw) <br>
- [Project homepage](https://github.com/live-neon/skills/tree/main/skill-distiller/compressed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with optional local JSONL calibration records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append calibration metrics under .learnings/skill-distiller/calibration.jsonl and can produce compressed skill Markdown.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
