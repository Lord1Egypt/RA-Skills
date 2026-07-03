## Description: <br>
Diagnoses decisions where losses, reference points, framing, or probability weighting are distorting choices, then guides the agent through expected-value checks, reframing, and a final rationale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to analyze risk decisions, pricing reactions, negotiation stalls, insurance choices, and product adoption patterns where loss aversion or prospect-theory effects may be changing the choice. It is intended to help an agent compute expected value, test alternate reference points, and document when loss aversion should be respected or overridden. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce persuasive decision guidance for consequential financial, negotiation, product, or policy choices. <br>
Mitigation: Review the expected-value calculation, reference point, probability estimates, and stakes classification before relying on the recommendation. <br>
Risk: Loss-aversion debiasing is inappropriate when the downside is genuinely catastrophic or irreversible. <br>
Mitigation: Use the skill's fit check and respect asymmetric caution for catastrophic or irreversible losses. <br>


## Reference(s): <br>
- [Sources - loss-aversion-prospect-theory](artifact/references/sources.md) <br>
- [Method in Action: Kahneman and Tversky's 1979 Prospect Theory](artifact/examples/kahneman-and-tversky-1979-prospect-theory.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/loss-aversion-prospect-theory) <br>
- [Publisher profile](https://clawhub.ai/user/deciqai) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with a structured decision-analysis template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input in coach mode before completing the analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
