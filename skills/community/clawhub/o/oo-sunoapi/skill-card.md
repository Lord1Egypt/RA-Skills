## Description: <br>
SunoAPI lets an agent operate the SunoAPI connector through OOMOL's oo CLI for reading account data and submitting music, lyrics, MIDI, cover, video, and audio transformation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with an OOMOL-connected SunoAPI account use this skill to inspect live action schemas, submit SunoAPI generation or transformation jobs, and retrieve task details or account credit status without handling raw API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit credit-consuming SunoAPI generation, upload, conversion, extension, and transformation actions. <br>
Mitigation: Inspect the live schema, confirm the exact payload and likely credit use with the user before running write actions, and stop when account credits are insufficient. <br>
Risk: The skill depends on the local oo CLI installation and the OOMOL-connected SunoAPI credential flow. <br>
Mitigation: Install only from the documented OOMOL CLI installer, review the install command before running it, and use OOMOL server-side credentials instead of exposing raw SunoAPI tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-sunoapi) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [SunoAPI Homepage](https://sunoapi.org) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; connector actions return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL account, a connected SunoAPI API key, and user confirmation for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
