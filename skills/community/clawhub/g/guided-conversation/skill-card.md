## Description: <br>
Minimize user friction by asking up to 4 clarifying questions before executing actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szpili](https://clawhub.ai/user/szpili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill before action execution to clarify ambiguous requests, summarize the understood task, list assumptions, and decide whether confirmation is needed for higher-risk work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can allow an agent to proceed automatically on low-risk tasks after clarification. <br>
Mitigation: Review whether automatic low-risk progression fits the deployment environment and keep explicit confirmation enabled for destructive, financial, external, or account-changing actions. <br>
Risk: If a request remains ambiguous after four questions, the skill directs the agent to make a best-effort interpretation. <br>
Mitigation: Require the agent to state its assumptions and notify the user before proceeding when ambiguity remains. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szpili/guided-conversation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown conversational prompts, task summaries, and assumption lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asks up to 4 clarifying questions; high-risk actions still require confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
