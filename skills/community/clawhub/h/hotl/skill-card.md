## Description: <br>
Use the hotl CLI to search Google Hotels, compare prices, fetch hotel room/rate details, and return machine-readable hotel results from a terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[art22s](https://clawhub.ai/user/art22s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs terminal-based hotel search, price comparison, room or rate lookups, and structured hotel results for travel planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI may send hotel search details, including destinations, dates, filters, and entity keys, to Google Hotels or the CLI's backing service. <br>
Mitigation: Use the skill only for travel details that are appropriate to share externally; avoid sensitive personal or confidential business travel information. <br>
Risk: The workflow depends on a third-party PyPI package and the local hotl binary. <br>
Mitigation: Install hotl from a trusted Python environment and verify the command is available before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/art22s/hotl) <br>
- [Publisher profile](https://clawhub.ai/user/art22s) <br>
- [PyPI package: hotl](https://pypi.org/project/hotl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the hotl command-line binary; use --format json when structured hotel results are needed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
