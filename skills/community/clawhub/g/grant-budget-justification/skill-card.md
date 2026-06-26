## Description: <br>
Generate narrative budget justifications for NIH/NSF applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External grant writers, research administrators, and investigators use this skill to draft narrative budget justifications for personnel, equipment, supplies, and travel in NIH or NSF proposal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script can overwrite a user-chosen output path. <br>
Mitigation: Run it in a project workspace and choose a new or disposable output path before execution. <br>
Risk: Budget details may include sensitive proposal information that persists in output files. <br>
Mitigation: Store generated files only in intended workspace locations and review them before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/grant-budget-justification) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown narrative budget justification, with optional file output from the local Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an output file to a user-chosen path.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
