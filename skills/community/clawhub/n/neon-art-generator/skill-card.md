## Description: <br>
AI neon art generator that transforms any subject into stunning neon-lit artwork via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to generate neon-styled images from text prompts for profile pictures, wallpapers, social media content, and digital art projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference IDs, and the Neta API token are sent to an external image generation service. <br>
Mitigation: Avoid confidential prompt content and use a revocable or limited-scope Neta token when possible. <br>
Risk: Passing tokens on the command line can expose them through shell history or process listings. <br>
Mitigation: Prefer short-lived tokens, clear shell history where appropriate, and avoid running the command on shared systems. <br>
Risk: Image generation depends on the external API and may fail, be moderated, or time out. <br>
Mitigation: Handle nonzero exits and missing URLs in calling workflows, and retry only after checking API status and prompt policy constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/neon-art-generator) <br>
- [Publisher profile](https://clawhub.ai/user/blammectrappora) <br>
- [Neta AI token and service page](https://www.neta.art/open/) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the script prints a direct image URL to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, accepts an optional size and reference image UUID, and polls the external image API until a URL is returned or the request times out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
