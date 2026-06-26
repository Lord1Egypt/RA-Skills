## Description: <br>
Create AI-generated movie posters, film posters, and cinema artwork from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate poster-style image assets from short text descriptions, with optional size presets and reference image identifiers for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Poster prompts and optional reference identifiers are sent to the external TalesOfAI API. <br>
Mitigation: Avoid including private, personal, regulated, or confidential information in prompts or reference identifiers. <br>
Risk: The skill requires an API token and the artifact demonstrates passing it on the command line. <br>
Mitigation: Use shell environment expansion or a secret manager where possible, and avoid storing raw tokens in shared command history, logs, or scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/movie-poster-generator) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, a text prompt, and optional size or reference image parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
