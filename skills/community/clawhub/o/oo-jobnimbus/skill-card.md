## Description: <br>
JobNimbus (jobnimbus.com). Use this skill for ANY JobNimbus request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to read, create, and update JobNimbus contacts and jobs through an OOMOL-connected JobNimbus account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL to broker access to the user's JobNimbus account. <br>
Mitigation: Install and use it only when the user trusts OOMOL and has connected the intended JobNimbus account. <br>
Risk: Create and update actions can change JobNimbus CRM records. <br>
Mitigation: Inspect the live action schema and confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Connection, scope, credential, or billing failures can block actions. <br>
Mitigation: Use first-time setup or recovery steps only after a command fails with the matching authentication, connection, scope, credential, or billing error. <br>


## Reference(s): <br>
- [JobNimbus homepage](https://www.jobnimbus.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-jobnimbus) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
