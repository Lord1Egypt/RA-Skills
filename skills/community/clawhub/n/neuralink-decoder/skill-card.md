## Description: <br>
Simulates and decodes neural spike activity into cursor movement (BCI). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AadiPapp](https://clawhub.ai/user/AadiPapp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and learners use this skill to run a local synthetic BCI simulation that generates neural spike counts and decodes them into virtual cursor movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script imports numpy, but no dependency file is included. <br>
Mitigation: Install numpy only from a trusted package source if the runtime environment does not already provide it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AadiPapp/neuralink-decoder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and console text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python simulation and prints decoded velocity, cursor position, and angle error.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
