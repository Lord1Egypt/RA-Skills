## Description: <br>
Product Review Panel Skill convenes a structured multi-expert panel to review Product Requirements Documents or product proposals and return a GO, NO-GO, or CONDITIONAL GO verdict with dissent preserved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpsean](https://clawhub.ai/user/cpsean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and product teams use this skill to stress-test written PRDs or product proposals across product, UX, and business-model dimensions before committing engineering resources. It is intended for critical review and decision support, not brainstorming, technical architecture review, or user research synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PRDs or private document links may be read by the runtime during review. <br>
Mitigation: Use approved environments for confidential material and redact sensitive details before sharing documents or links. <br>
Risk: Language-based panel selection can apply a China-oriented review frame when the conversation is in Chinese. <br>
Mitigation: Ask explicitly for the international panel or another review frame when that perspective is preferred. <br>
Risk: Persona-style expert perspectives may be mistaken for statements by real individuals. <br>
Mitigation: Keep the mandatory disclaimer visible and treat the output as interpretive decision support rather than endorsement. <br>
Risk: An opinionated verdict may over-influence product decisions when PRD evidence is incomplete. <br>
Mitigation: Validate the verdict against user research, business metrics, and the skill's stated failure signals before committing resources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cpsean/product-review-panel-skill) <br>
- [Skill definition](SKILL.md) <br>
- [Information gap check workflow](references/workflows/information-gap-check.md) <br>
- [PRD classification workflow](references/workflows/prd-classification.md) <br>
- [Verdict logic workflow](references/workflows/verdict-logic.md) <br>
- [Disclaimer template](references/templates/disclaimer.md) <br>
- [Output structure template](references/templates/output-structure.md) <br>
- [Chinese expert personas](references/personas/experts-cn.md) <br>
- [International expert personas](references/personas/experts-intl.md) <br>
- [The Closer persona](references/personas/closer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown review with a disclaimer, intake questions, panel discussion, final verdict, dissent, and failure signals.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual output selected by conversation language; no numeric scoring; always includes a final verdict and dissent section.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
