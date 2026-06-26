## Description: <br>
Generate photorealistic impossible scenes and anti-physics landscapes powered by AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate surreal or impossible scene imagery for wallpapers, concept art, book covers, album art, posters, fantasy worldbuilding, and print-on-demand artwork from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image identifiers, and the Neta API token are sent to an external provider. <br>
Mitigation: Do not include secrets, private data, or confidential imagery in prompts or references; only install and run the skill if external provider use is acceptable. <br>
Risk: Passing the API token directly on the command line can expose it through shell history or process listings. <br>
Mitigation: Store the token in an environment variable or secret manager and pass it from that protected location when invoking the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/impossible-scene-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Plain text URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct generated image URL after polling the external image-generation API; requires a Neta API token and accepts optional size and reference-image parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
