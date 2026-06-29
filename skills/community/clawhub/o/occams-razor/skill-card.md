## Description: <br>
Helps an agent rank competing explanations, designs, or diagnoses by first checking evidence fit and then preferring the option with the fewest unsupported assumptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users apply this skill when comparing two or more plausible hypotheses, designs, diagnoses, or incident explanations. It guides the agent through a Parsimony Audit that checks evidence fit, counts unsupported assumptions, and names what evidence would overturn the preference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be misused to choose a simpler explanation that does not fit all known evidence. <br>
Mitigation: Require the fit gate before comparing simplicity, and reject any candidate that drops known evidence. <br>
Risk: The skill's output can be mistaken for proof rather than a prior for where to look first. <br>
Mitigation: State the preferred candidate as provisional and include the specific observation that would overturn it. <br>
Risk: Assumption counts can become biased toward the user's preferred answer. <br>
Mitigation: Count unsupported assumptions consistently across candidates and call out asymmetric counting as a rationalization risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/occams-razor) <br>
- [Sources - occams-razor](references/sources.md) <br>
- [Method in Action: Wegener and Continental Drift (1912)](examples/wegener-continental-drift-1912.md) <br>
- [Stanford Encyclopedia of Philosophy: William of Ockham](https://plato.stanford.edu/entries/ockham/) <br>
- [Encyclopaedia Britannica: Occam's razor](https://www.britannica.com/topic/Occams-razor) <br>
- [USGS: Plate tectonics](https://www.usgs.gov/programs/earthquake-hazards/plate-tectonics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a structured Parsimony Audit template and step-by-step coaching prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve the fit gate, assumption-count comparison, over-shave check, and overturning-evidence statement.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
