## Description: <br>
Searches WebSim's public asset library for images, audio, music, sound effects, videos, and 3D models, then returns direct download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upintheairsheep](https://clawhub.ai/user/upintheairsheep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and agents use this skill to find reusable media assets for games, prototypes, presentations, and creative projects. It is useful when a user needs candidate files with filenames, MIME types, relevance scores, and direct public download URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to WebSim's external asset search service. <br>
Mitigation: Avoid sensitive project names, private filenames, client data, and confidential prompts in search queries. <br>
Risk: Returned assets are community-provided third-party files that may not be reviewed for license, safety, or suitability. <br>
Mitigation: Review each asset and its source context before downloading, embedding, or redistributing it. <br>
Risk: The artifact states that no public rate-limit headers are known for the API. <br>
Mitigation: Use modest pagination and avoid large parallel request bursts. <br>


## Reference(s): <br>
- [OpenAssetSearch on ClawHub](https://clawhub.ai/upintheairsheep/open-asset-search) <br>
- [Publisher profile](https://clawhub.ai/user/upintheairsheep) <br>
- [WebSim asset search API endpoint](https://websim.com/api/v1/search/assets) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown or JSON summaries containing filenames, MIME types, relevance scores, and direct asset URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports query, result limit, pagination offset, and media-type filtering for image, audio, video, or model assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
