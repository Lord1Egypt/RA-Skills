## Description: <br>
Generates custom brand mascots and cartoon characters from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to request mascot or cartoon character images for brands, teams, schools, gaming groups, and content channels. The skill is useful when an agent needs to turn a written mascot concept into an image-generation request and return the resulting image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta/TalesOfAI API token are sent to an external image-generation service. <br>
Mitigation: Use only appropriate prompts and reference IDs for that service, avoid highly confidential brand material, and confirm users are comfortable sharing the token and request data externally. <br>
Risk: API tokens passed on the command line can be exposed through shell history, logs, or shared terminal output. <br>
Mitigation: Avoid committing or sharing tokens, clear shell history where needed, and prefer a controlled local execution environment for generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/mascot-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [TalesOfAI API service](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports square, portrait, landscape, and tall image sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
