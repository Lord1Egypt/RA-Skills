## Description: <br>
Generate eerie liminal space images, dreamcore backgrounds, and backrooms-style scenes from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, writers, and developers use this skill to generate liminal space, dreamcore, backrooms-style, and atmospheric background images from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image IDs, and the Neta API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive prompt content, and pass the token through shell environment expansion such as "$NETA_TOKEN". <br>
Risk: A long-lived API token could be exposed if typed directly into shell history or shared logs. <br>
Mitigation: Store the token in an environment variable or a local secret manager and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/liminal-space-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/omactiengartelle) <br>
- [Neta API token page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, guidance] <br>
**Output Format:** [Command-line invocation that returns a direct image URL as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Neta API token; supports size selection and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
