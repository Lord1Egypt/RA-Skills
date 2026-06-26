## Description: <br>
CLI for AI agents to lookup Harry Potter universe info for their humans. Uses HP-API. No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Harry Potter character, house, student, staff, and spell information from HP-API through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms are sent to HP-API. <br>
Mitigation: Avoid submitting private or sensitive text as lookup queries. <br>
Risk: The README references external GitHub executable scripts that were not included in the reviewed package. <br>
Mitigation: Inspect any externally fetched scripts before installation or execution. <br>


## Reference(s): <br>
- [HP-API](https://hp-api.onrender.com) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jeffaf/harrypotter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; default command limit is 20 items per query.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
