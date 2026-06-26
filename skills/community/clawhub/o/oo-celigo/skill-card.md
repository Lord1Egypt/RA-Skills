## Description: <br>
Celigo (celigo.com). Use this skill for ANY Celigo request: reading, creating, and updating data through an OOMOL-connected Celigo account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to inspect Celigo resources and run Celigo connector actions through an OOMOL-connected account. It supports connection, export, flow, import, and token metadata workflows while prompting schema checks before action payloads are built. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an OOMOL-connected Celigo account and may expose account-scoped Celigo data through connector responses. <br>
Mitigation: Install it only for users who need Celigo account access, and review requested Celigo actions and payloads before approval. <br>
Risk: Actions tagged write or destructive can change, remove, or overwrite Celigo data if run with an incorrect payload. <br>
Mitigation: Fetch the live action schema first, confirm the exact target and payload with the user, and require explicit approval before write or destructive actions. <br>


## Reference(s): <br>
- [Celigo skill page](https://clawhub.ai/oomol/oo-celigo) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Celigo homepage](https://www.celigo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; command responses may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
