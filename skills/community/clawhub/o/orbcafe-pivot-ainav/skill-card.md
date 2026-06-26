## Description: <br>
Build ORBCAFE advanced analytics interactions using CPivotTable/usePivotTable and voice navigation using CAINavProvider/useVoiceInput. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to implement ORBCAFE pivot-table analytics, preset management, and voice-navigation flows in application UI work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice navigation can send voice or transcript data to an ASR endpoint. <br>
Mitigation: Confirm the ASR endpoint contract, keep authentication outside source code, and provide clear user control over voice capture. <br>
Risk: Saved pivot presets may contain business-sensitive analytics structure or preferences. <br>
Mitigation: Choose server-side or local persistence based on preset sensitivity and document the persistence behavior for users. <br>


## Reference(s): <br>
- [Domain Patterns](references/domain-patterns.md) <br>
- [Pivot + AINav Guardrails](references/guardrails.md) <br>
- [Pivot + AINav Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript or TSX code snippets and concise operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes module choice, minimal implementation guidance, and one operational note.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
