## Description: <br>
Korean-language pension and retirement-planning skill that routes common National Pension, IRP, pension savings, severance pay, basic pension, FIRE, and retirement simulation requests into concise guidance and estimate outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Korean-speaking users use this skill to estimate retirement-related amounts, compare pension account options, understand Korean pension systems, and identify when official government or pension sources should be checked. It is intended for informational planning support, not investment, legal, tax, or individualized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce retirement, pension, severance, and tax-related estimates that may be outdated or incorrect for a user's specific situation. <br>
Mitigation: Treat outputs as estimates and verify current amounts, eligibility, and rules with official NPS, My Pension, government, or qualified professional sources before acting. <br>
Risk: Users may share sensitive identity, income, asset, or login information while seeking personalized pension estimates. <br>
Mitigation: Do not provide full resident-registration numbers, passwords, login sessions, or unnecessary income and asset details; approve any external lookup before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sw326/pension-guide) <br>
- [Intent router](references/intent_router.md) <br>
- [Output templates](references/output_templates.md) <br>
- [Source tiers](references/source_tiers.md) <br>
- [National Pension Service](https://www.nps.or.kr) <br>
- [My Pension](https://csa.nps.or.kr) <br>
- [Financial Supervisory Service](https://www.fss.or.kr) <br>
- [Ministry of Employment and Labor](https://www.moel.go.kr) <br>
- [Korean Law Information Center](https://www.law.go.kr) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Calculations, Shell commands] <br>
**Output Format:** [Markdown with tables, concise explanations, estimate summaries, and occasional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mandatory informational disclaimers and directs users to official sources for exact pension amounts and current rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
