## Description: <br>
Generates realistic human-portrait images from text descriptions of pets using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate pet-to-human portrait images for creative portraits, gifts, and social media content from text prompts and optional style references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional reference identifiers are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid sensitive personal details in prompts or references, and confirm the agent asks before making external requests. <br>
Risk: The Neta API token can be exposed through command-line history, process listings, or logs when passed as a flag. <br>
Mitigation: Prefer an environment variable or secret manager in wrappers and avoid logging commands that include tokens. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/omactiengartelle/pet-to-human-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text URL on stdout, with errors printed to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and may poll the image-generation task until a result URL is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
