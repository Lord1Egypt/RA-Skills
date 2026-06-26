## Description: <br>
Merge lines from multiple files side by side, creating columnar output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to combine corresponding lines from separate local text files into aligned, tabular output for comparison or downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files passed to the tool are read locally and their contents are printed in the output. <br>
Mitigation: Do not pass sensitive files unless their contents are intended to appear in the output. <br>
Risk: The documented delimiter and serial-merge options are unsupported in this version. <br>
Mitigation: Use the default tab-separated parallel merge behavior, or update and verify the script before relying on those options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/paste-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints merged local file contents to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
