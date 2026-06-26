## Description: <br>
Scans Markdown files in the current or specified directory and generates a structured digest with titles, sections, word counts, and summary totals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ithrael](https://clawhub.ai/user/ithrael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation teams use this skill to summarize Markdown work in a chosen folder into a quick daily report for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Markdown files in the current or specified folder and prints document metadata that may reveal sensitive workspace content. <br>
Mitigation: Run it against an explicit narrow directory in sensitive workspaces and review the generated digest before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ithrael/ithrael-daily-digest) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown report printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports top-level Markdown files in the selected directory, including extracted titles, second-level headings, word counts, and aggregate totals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
