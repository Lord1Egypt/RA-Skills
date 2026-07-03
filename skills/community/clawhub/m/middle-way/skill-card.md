## Description: <br>
Helps an agent analyze binary-framed decisions by identifying each pole's failure modes and choosing a situation-dependent position that avoids both false balance and ideological extremes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and decision-makers use this skill when a decision or debate is framed as a binary but needs a principled middle position based on context, constraints, and failure-mode analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bias responses toward seeking a middle position even when evidence clearly favors one side. <br>
Mitigation: Apply the documented fit check first and decline the middle-way lens when the choice is genuinely binary or one side is clearly correct on the evidence. <br>
Risk: A middle-way framing can be misused as split-the-difference reasoning or false balance. <br>
Mitigation: Require explicit failure-mode analysis for both poles and state why the selected position fits the specific situation. <br>
Risk: The lens can be used to avoid timely commitment when urgency requires choosing a side and iterating. <br>
Mitigation: Use the skill's not-when guardrail for urgent decisions and name a review trigger when a middle position is appropriate. <br>


## Reference(s): <br>
- [Primary Sources - middle-way](references/sources.md) <br>
- [Method in Action: Zhongyong and the Third Way Debate](examples/zisi-zhongyong-third-way-debate.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/middle-way) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with a structured analysis template and optional coaching questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; output depends on the user's decision context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
