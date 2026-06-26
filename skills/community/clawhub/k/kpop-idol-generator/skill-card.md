## Description: <br>
Generate k-pop idol style portraits and kpop photocard aesthetic images from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate K-pop idol style portraits, photocard images, and Korean fashion portrait concepts from plain text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image UUIDs, and the API token are sent to the third-party Neta/TalesOfAI service. <br>
Mitigation: Use the skill only with prompts and references suitable for that service, avoid confidential inputs, and use a limited-scope token where possible. <br>
Risk: Examples pass the API token as a command-line argument, which may expose it through shell history or process listings. <br>
Mitigation: Prefer short-lived or limited-scope tokens and avoid sharing command transcripts or logs that include token values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/kpop-idol-generator) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls] <br>
**Output Format:** [Plain text image URL on stdout with progress messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, accepts text prompts, optional image size, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
