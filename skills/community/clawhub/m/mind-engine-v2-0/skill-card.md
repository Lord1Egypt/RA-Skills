## Description: <br>
A 7-stage thinking engine that turns an AI assistant into a structured reasoning partner for diagnosis, model matching, dialogue, hypothesis generation, verification, recommendations, and consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason989303](https://clawhub.ai/user/jason989303) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, decision-makers, and knowledge workers use this skill to structure complex questions into multi-step analysis, explore options conversationally, and receive methodology-tagged recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to activate on broad ordinary prompts, which can cause it to participate when a narrower or simpler response would be more appropriate. <br>
Mitigation: Configure the skill for explicit invocation or clear user confirmation before applying the full framework. <br>
Risk: The skill asks to update user memory after each dialogue, which may retain personal preferences, constraints, or sensitive context without clear consent. <br>
Mitigation: Require explicit approval before saving memories and avoid using the skill with sensitive personal or work documents unless retention behavior is reviewed. <br>


## Reference(s): <br>
- [Mind Engine README](README.md) <br>
- [Mind Engine skill definition](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/jason989303/mind-engine-v2-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured recommendation sections, methodology-tagged bullets, and optional follow-up questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask methodology-driven questions before producing recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
