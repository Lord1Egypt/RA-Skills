## Description: <br>
Predicts what is likely to happen from a user's query by thinking through which forecasting theories fit, then applying one or more from references/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runshengdu](https://clawhub.ai/user/runshengdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure near-future forecasts by selecting relevant forecasting theories, gathering current evidence, and producing separate theory-specific predictions with assumptions and confidence stated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecasting on private, confidential, or market-sensitive questions can expose search terms and research targets to external tools or websites. <br>
Mitigation: Use the skill only with information appropriate for live research, and avoid sensitive prompts unless external research disclosure is acceptable. <br>
Risk: Forecasts may be incorrect or overconfident if evidence is incomplete or assumptions are weak. <br>
Mitigation: Review the generated evidence notes, assumptions, confidence, and falsifiable conditions before relying on the forecast. <br>


## Reference(s): <br>
- [Source repository](https://github.com/runshengdu/predict-future-skill) <br>
- [Howard Marks - Finance Forecasting](references/finance_howard_marks.md) <br>
- [Hyman Minsky - Finance Forecasting](references/finance_hyman_minsky.md) <br>
- [Robert Shiller - Finance Forecasting](references/finance_robert_shiller.md) <br>
- [General Forecasting - Tetlock Superforecasting](references/general_Philip_Tetlock.md) <br>
- [International Relations - Bueno de Mesquita Game-Theoretic Forecasting](references/intl_bruce_bueno_de_mesquita.md) <br>
- [International Relations - Structural Realism](references/intl_structural_realism.md) <br>
- [International Relations - Schelling Strategy of Conflict and Coercion](references/intl_thomas_schelling.md) <br>
- [Clayton Christensen - Tech Forecasting](references/tech_clayton_christensen.md) <br>
- [Geoffrey Moore - Tech Forecasting](references/tech_geoffrey_moore.md) <br>
- [Paul Saffo - Tech Forecasting](references/tech_paul_saffo.md) <br>
- [Robert Shiller data](http://www.econ.yale.edu/~shiller/data.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files with structured forecast sections and source notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped run folders and keeps each selected theory's forecast separate.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
