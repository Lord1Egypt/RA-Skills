## Description: <br>
Helps agents diagnose knowing-doing gaps and turn stated lessons, plans, or intentions into a concrete Knowing-Doing Audit with a next action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to coach individuals or teams through analysis paralysis, repeated lessons without behavior change, and claims of learning that need behavioral evidence. It produces a diagnostic audit that identifies missing knowledge components and a small next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives directive behavioral coaching and could be misused to shame or pressure people. <br>
Mitigation: Apply it diagnostically with user consent, and frame the result as a missing knowledge component rather than a character judgment. <br>
Risk: The audit can produce misleading conclusions when the barrier is a real external constraint. <br>
Mitigation: Check for external constraints such as capital, regulation, or waiting for a trigger before using the Knowing-Doing Audit. <br>


## Reference(s): <br>
- [Primary sources](references/sources.md) <br>
- [Wang Yangming's Longchang Enlightenment, 1508](examples/wang-yangming-longchang-enlightenment-1508.md) <br>
- [Implementation Intentions: Strong Effects of Simple Plans](https://doi.org/10.1037/0003-066X.54.7.493) <br>
- [A New Look at Habits and the Habit-Goal Interface](https://doi.org/10.1037/0033-295X.114.4.843) <br>
- [Do Things That Don't Scale](http://paulgraham.com/ds.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit with structured prompts and next-action fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask step-by-step follow-up questions and stop for user input in coaching mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
