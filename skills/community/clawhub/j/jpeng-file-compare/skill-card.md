## Description: <br>
Compare two files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to compare files from a command-line workflow and return structured comparison results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for COMPARE_API_KEY without explaining what service uses it or whether file contents are transmitted. <br>
Mitigation: Do not provide the API key or use sensitive files until the publisher documents the key purpose, network behavior, and data handling. <br>
Risk: The documented command references scripts/file_compare.py, but the artifact does not include that script. <br>
Mitigation: Require the publisher to supply the missing script and review it before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-file-compare) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration] <br>
**Output Format:** [JSON comparison results with shell command and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes a success flag and data object, and requires COMPARE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
