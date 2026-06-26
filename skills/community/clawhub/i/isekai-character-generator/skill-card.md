## Description: <br>
Generates isekai and anime character images from text prompts through the Neta AI image generation API and returns a direct image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate isekai anime character art, original character concepts, light novel cover concepts, manga concept art, and character sheets from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to the external image service. <br>
Mitigation: Avoid private or sensitive prompt content and only use the skill if sharing those values with the external service is acceptable. <br>
Risk: Typing the Neta API token directly in shell commands can expose it through shell history, logs, or shared terminals. <br>
Mitigation: Pass the token from a protected environment variable or secret store and avoid logging commands that include credentials. <br>
Risk: Generated image availability and moderation outcomes depend on the external API service. <br>
Mitigation: Review generated outputs before use and handle API failures, moderation states, and timeouts in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/isekai-character-generator) <br>
- [Neta AI token and trial page](https://www.neta.art/open/) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text direct image URL, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports portrait, landscape, square, and tall aspect ratios, plus an optional reference image UUID for style inheritance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
