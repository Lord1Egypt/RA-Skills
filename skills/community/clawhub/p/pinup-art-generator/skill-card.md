## Description: <br>
Generate classic 1950s pin-up art, retro glamour illustrations, vintage poster portraits, mid-century advertising art, and Gil Elvgren style pinup girls via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate vintage pin-up, retro glamour, poster portrait, and mid-century advertising-style image outputs from text prompts. It is intended for creative image generation workflows that can use a Neta API token and optional reference image UUID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, task metadata, and the Neta/TalesOfAI API token are sent to a third-party remote image service. <br>
Mitigation: Install only when that data sharing is acceptable, and avoid submitting sensitive prompts or reference identifiers. <br>
Risk: The required API token could be exposed through shared shell history, logs, or CI output. <br>
Mitigation: Use a limited-purpose token and avoid placing real secrets in commands or environments that are logged or shared. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/pinup-art-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/blammectrappora) <br>
- [Neta API Token Page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text image URL on stdout, with progress and error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a text prompt, size option, required Neta API token, and optional reference image UUID; returns a direct image URL when the remote image job completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
