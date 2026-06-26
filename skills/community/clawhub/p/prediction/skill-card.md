## Description: <br>
Forecast uncertain outcomes with base rates, reference classes, calibration loops, and explicit scorekeeping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and agents use this skill to turn uncertain planning or prediction prompts into auditable forecasts with resolution rules, numeric probabilities, update triggers, and later scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local forecast memory can preserve old forecasts, assumptions, or preferences under ~/prediction/. <br>
Mitigation: Use explicit-request activation when desired, and periodically review or delete ~/prediction/ content that should no longer influence future answers. <br>
Risk: Forecasts can be misleading when a question lacks a clear deadline, threshold, or resolution source. <br>
Mitigation: Define a resolvable question and resolution rule before assigning a probability, and abstain or lower confidence when critical evidence is missing. <br>


## Reference(s): <br>
- [Prediction release page](https://clawhub.ai/ivangdavila/prediction) <br>
- [Prediction skill homepage](https://clawic.com/skills/prediction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local forecast-memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local forecast notes under ~/prediction/ when the user chooses recurring forecast memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
