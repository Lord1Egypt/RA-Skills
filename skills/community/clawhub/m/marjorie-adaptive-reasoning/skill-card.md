## Description: <br>
Automatically assess task complexity and adjust reasoning level. Triggers on every user message to evaluate whether extended thinking (reasoning mode) would improve response quality. Use this as a pre-processing step before answering complex questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill as a pre-response reasoning posture check to decide when a request warrants more deliberate analysis. It is intended for users who want complex planning, debugging, architecture, math, or high-stakes requests handled with deeper reasoning while keeping simple requests fast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic reasoning escalation can make some responses slower or more detailed than expected. <br>
Mitigation: Ask for a quick answer, disable the skill, or turn reasoning off when speed and brevity matter. <br>
Risk: The skill changes response style by adding a visual indicator when higher reasoning is active. <br>
Mitigation: Disable the skill in contexts that require clean output formatting or explicitly ask for no response indicators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/marjorie-adaptive-reasoning) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown instructions with scoring tables and response-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no files, credentials, network access, or code execution requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
