## Description: <br>
Generates kawaii and chibi-style artwork from text prompts through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request cute kawaii artwork, profile pictures, stickers, character concepts, and wallpapers from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, optional reference UUIDs, and the Neta API token to api.talesofai.com. <br>
Mitigation: Avoid sensitive or confidential prompts, and pass the token through a controlled secret mechanism such as an environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/kawaii-art-generator) <br>
- [Neta Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with status messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; accepts an image prompt, optional size, and optional reference UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
