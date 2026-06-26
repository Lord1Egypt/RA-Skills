## Description: <br>
Mecha Art Generator helps agents generate anime-style mecha artwork from text prompts through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate mecha-themed concept art, posters, cosplay references, fanart, and model-kit inspiration from text prompts, with optional size and style-reference controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta/TalesOfAI token are sent to api.talesofai.com. <br>
Mitigation: Use non-sensitive prompts, review the service terms, and use a revocable or limited-purpose token. <br>
Risk: Passing tokens on the command line can expose them through shell history or local process inspection. <br>
Mitigation: Prefer safer local token handling where possible and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/mecha-art-generator) <br>
- [Neta open platform](https://www.neta.art/open/) <br>
- [TalesOfAI image API](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text URL and Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct image URL after polling the remote image-generation API; requires a Neta API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
