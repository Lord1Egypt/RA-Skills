## Description: <br>
Oraclaw Ensemble combines predictions from multiple LLMs, models, or sources into a consensus prediction weighted by historical accuracy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to combine two or more model, agent, or analyst predictions into a weighted consensus and identify high disagreement before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the paid OraClaw service may send model predictions, forecasts, or analyst inputs outside the local agent environment. <br>
Mitigation: Install only if OraClaw's data handling and billing terms meet requirements; avoid confidential inputs unless approved. <br>
Risk: A high-disagreement ensemble result may be unreliable for immediate action. <br>
Mitigation: Flag high entropy results and require review before acting on the consensus. <br>


## Reference(s): <br>
- [OraClaw Ensemble homepage](https://oraclaw.dev/ensemble) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Structured consensus result with prediction, weights, entropy, and individual contributions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and uses a paid external service with a stated free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
