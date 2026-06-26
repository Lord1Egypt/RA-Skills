## Description: <br>
Use when user input is vague, underspecified, lacks boundaries or acceptance criteria, or would benefit from being reframed into a more executable prompt before work begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lq434239](https://clawhub.ai/user/lq434239) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content authors, and agent users use this skill to turn vague or underspecified requests into clearer prompts with explicit goals, constraints, output format, and acceptance criteria before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rewrite ambiguous requests in a way that changes user intent. <br>
Mitigation: Keep the default confirmation flow for requests that could change files, spend money, publish content, or affect accounts. <br>
Risk: Casual phrases such as "just do it" may be treated as permission to use the rewritten prompt immediately. <br>
Mitigation: Use auto-apply only when the user clearly authorizes skipping confirmation. <br>


## Reference(s): <br>
- [Prompt Refinement Patterns](references/prompt-patterns.md) <br>
- [Prompt Refiner on ClawHub](https://clawhub.ai/lq434239/prompt-refiner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompt refinement with optional confirmation choice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a refined prompt and a recommendation to ask the user to choose between the original and refined prompt.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
