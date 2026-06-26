## Description: <br>
Generate professional podcast cover art and show artwork for Spotify, Apple Podcasts, YouTube Music, Amazon Music, and Overcast using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, indie podcasters, podcast networks, and show hosts use this skill to turn plain-language show descriptions into directory-ready podcast cover artwork. It is also useful for developers or agents that need a CLI workflow returning a generated image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the podcast-cover prompt, optional reference image UUID, and Neta token to api.talesofai.com. <br>
Mitigation: Avoid sensitive prompt content, review the external service before use, and only run the skill when sharing that data with the service is acceptable. <br>
Risk: Passing the API token directly on the command line can expose it through shell history, logs, or CI output. <br>
Mitigation: Prefer expanding the token from a shell variable and rotate the token if it may have been recorded. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/podcast-cover-generator) <br>
- [Neta Open](https://www.neta.art/open/) <br>
- [Neta API Service](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URL on stdout with progress messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt, a Neta API token, and optional size or reference image UUID arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
