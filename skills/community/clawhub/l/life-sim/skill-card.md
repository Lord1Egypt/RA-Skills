## Description: <br>
Life Sim is a Chinese-language interactive life-simulation skill that starts from a user's counterfactual prompt and narrates an alternate path with period-specific details, choice points, and an ending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-meng-xin](https://clawhub.ai/user/chen-meng-xin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to explore counterfactual life choices through a Chinese-language interactive narrative. The skill helps an agent infer the user's core question, build a historically grounded alternate life path, offer 3-5 meaningful choice points, and close with a concise ending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad common phrases such as "假如" or "如果当初," which may be disruptive if the user did not intend to start the simulation. <br>
Mitigation: Narrow activation wording or require an explicit start phrase before deploying in contexts where accidental activation would interrupt normal conversation. <br>
Risk: The skill uses personalization and cultural assumptions to infer a user's likely behavior, which may not fit every user. <br>
Mitigation: Keep inferences tentative, accept user corrections immediately, and avoid treating the narrative as factual prediction or psychological assessment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chen-meng-xin/life-sim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese-language Markdown narrative with interactive choice prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Second-person narrative output, typically with 3-5 choice points and a final recap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
