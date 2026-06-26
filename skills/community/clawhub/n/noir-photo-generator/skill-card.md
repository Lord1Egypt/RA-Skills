## Description: <br>
Generate dramatic film noir style portraits and scenes with AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative developers use this skill to generate film noir style image URLs from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the user-provided Neta/TalesOfAI token are sent to an external image service. <br>
Mitigation: Use only prompts and tokens appropriate for that service, avoid exposing tokens in shared terminals, CI logs, or recordings, and rotate any token that may have been disclosed. <br>
Risk: The skill depends on a user-provided API token and an external service endpoint. <br>
Mitigation: Confirm token availability and external service access before relying on the skill in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/noir-photo-generator) <br>
- [Publisher profile](https://clawhub.ai/user/blammectrappora) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text image URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Neta API token and sends prompts to the disclosed external image service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
