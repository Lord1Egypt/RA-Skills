## Description: <br>
Helps an agent audit arguments by rewriting premises and conclusions, checking structural, linguistic, cognitive, and rhetorical fallacy patterns, and separating failed inference from the truth of the underlying claim. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent evaluate persuasive arguments, identify fallacy patterns, and explain what evidence or inference would actually support a conclusion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may be used in authenticated administrative workflows where sensitive actions require explicit intent. <br>
Mitigation: Use authenticated access only when those actions are intended, and keep confirmation and dry-run gates in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/logical-fallacies) <br>
- [Sources](references/sources.md) <br>
- [Tversky and Kahneman Linda Problem Example](examples/tversky-kahnemans-linda-problem-1983.md) <br>
- [Aristotle, Sophistical Refutations](https://classics.mit.edu/Aristotle/sophist_refut.html) <br>
- [Stanford Encyclopedia of Philosophy: Fallacies](https://plato.stanford.edu/entries/fallacies/) <br>
- [Tversky and Kahneman 1983](https://doi.org/10.1037/0033-295X.90.4.293) <br>
- [Tversky and Kahneman 1974](https://doi.org/10.1126/science.185.4157.1124) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured fallacy audit with findings, verdict, and repair guidance] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
