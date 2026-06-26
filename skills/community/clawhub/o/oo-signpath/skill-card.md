## Description: <br>
SignPath lets an agent inspect SignPath action schemas, list signing policies, check signing request status, and submit fast hash-signing requests through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users who manage SignPath signing workflows use this skill to inspect live connector schemas, submit fast hash-signing requests, poll signing request status, and list visible signing policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit SignPath signing requests, including fast hash-signing requests, even though the available action list is not explicitly tagged as write-capable. <br>
Mitigation: Require explicit user confirmation of the exact payload, signing policy, project, and expected effect before running fast_sign_hash. <br>
Risk: The skill depends on sensitive SignPath credentials through the connected OOMOL account. <br>
Mitigation: Use the existing OOMOL connection flow, avoid requesting or exposing raw credentials, and only revisit setup when an auth or connection error occurs. <br>


## Reference(s): <br>
- [ClawHub SignPath skill page](https://clawhub.ai/oomol/oo-signpath) <br>
- [SignPath homepage](https://signpath.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated OOMOL account with SignPath connected; connector responses may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
