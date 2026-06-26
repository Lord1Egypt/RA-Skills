## Description: <br>
Creates stylized 3D animated portrait images from text prompts by calling the Neta/Tales of AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate stylized portrait, avatar, headshot, family portrait, pet portrait, or character images from text prompts. It is useful when the agent should run a CLI workflow that submits a prompt to an external image-generation service and returns the generated image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference IDs, and generated-image requests are sent to the external Neta/Tales of AI service. <br>
Mitigation: Use the skill only when that provider is acceptable for the data being submitted, and avoid sensitive personal details or private reference IDs. <br>
Risk: Examples pass the Neta token on the command line, where it may be exposed through shell history or process listings. <br>
Mitigation: Use a short-lived or low-privilege token and handle command history, logs, and shared systems as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/pixar-portrait-generator) <br>
- [Neta AI token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI returns a plain image URL on stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and accepts size and reference-image options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
