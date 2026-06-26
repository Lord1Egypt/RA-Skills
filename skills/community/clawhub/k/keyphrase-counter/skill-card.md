## Description: <br>
Counts high-frequency phrases from text input and writes the top N results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askjda](https://clawhub.ai/user/askjda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run a command-line text-processing step that summarizes phrase frequency results into JSON or TXT output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill is presented as a local keyphrase counter, but the code includes undisclosed network features that can send local file contents to arbitrary endpoints. <br>
Mitigation: Review before installing and avoid running it with --url, --endpoint, or --payload, especially on sensitive files or internal networks, unless the publisher removes or clearly documents and constrains those behaviors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askjda/keyphrase-counter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files] <br>
**Output Format:** [Command output plus JSON or TXT file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top-N result count is controlled by the --top-k command-line argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
