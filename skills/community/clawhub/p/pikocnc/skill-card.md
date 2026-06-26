## Description: <br>
Provides a PikoCNC G-code reference for interpreting commands, tracking modal state, validating CNC program structure, and designing CNC simulator or interpreter logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midware](https://clawhub.ai/user/midware) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, CNC programmers, and machining workflow reviewers use this skill as a PikoCNC G-code reference for program structure, command behavior, modal state handling, validation, and simulator or interpreter planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or unverified G-code can cause unsafe CNC machine motion, tool crashes, damaged workpieces, or operator risk. <br>
Mitigation: Compare any generated program with official PikoCNC documentation, simulate or dry-run it, confirm units, coordinates, tool table, clearances, spindle and coolant behavior, and treat unknown commands as errors unless a trained operator approves them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/midware/pikocnc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with G-code examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference-only output; generated G-code or machining instructions require operator review, simulation, and dry-run validation before machine use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
