## Description: <br>
Automatically scores each user request for complexity and adjusts the agent's reasoning depth before responding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent builders use this skill to have an agent evaluate prompt complexity and choose quick, standard, or deeper reasoning for complex work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic deeper reasoning can make quick-answer workflows slower and more token-intensive. <br>
Mitigation: Install it only when automatic reasoning-depth selection is desired, and document how users can opt out or disable it for quick answers. <br>
Risk: Reasoning indicators may change the visible response style. <br>
Mitigation: Review the indicator behavior before deployment and disable the skill where strict output formatting is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/maske-adaptive-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Text or Markdown responses with optional reasoning indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append reasoning indicators for prompts assessed as complex.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
