## Description: <br>
Operates JSONBin.io through an OOMOL-connected account for reading, creating, updating, and deleting bins without handling raw API tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to operate JSONBin.io records through the OOMOL connector, including reading bins and performing confirmed create, update, and delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create and update actions can change remote JSONBin.io data. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Delete actions can remove remote JSONBin.io bins. <br>
Mitigation: Confirm the target bin and obtain explicit approval before running destructive actions. <br>
Risk: The skill operates through the user's OOMOL-connected JSONBin.io account. <br>
Mitigation: Use setup flows only after an authentication or connection failure, and avoid handling raw API tokens directly. <br>


## Reference(s): <br>
- [JSONBin.io homepage](https://jsonbin.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-jsonbin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
