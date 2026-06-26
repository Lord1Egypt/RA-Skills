## Description: <br>
Log and review options trades with trend analysis and exportable position reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this local command-line utility to record options-related notes, review recent activity, search logs, and export stored entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says this is a local text logger branded as an options-trading tool, with unclear scope and persistent storage of potentially sensitive inputs. <br>
Mitigation: Review the artifact before installing, treat it as a local logger rather than a full options analysis tool, and avoid entering account credentials, secrets, or sensitive trading details. <br>
Risk: The script stores command inputs in ~/.local/share/options and includes those logs in local searches and exports. <br>
Mitigation: Use non-sensitive entries, review exported JSON, CSV, or text files before sharing them, and delete local logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/options) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [BytesAgain feedback](https://bytesagain.com/feedback/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command-line examples and local export files in JSON, CSV, or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/options.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
