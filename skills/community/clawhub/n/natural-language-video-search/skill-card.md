## Description: <br>
Semantic search over video files using Gemini embeddings, with indexing and natural-language retrieval for dashcam, security camera, or MP4 footage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssrajadh](https://clawhub.ai/user/ssrajadh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and video operators use this skill to index local footage, search it with natural-language descriptions, and extract matching clips. It is suited to dashcam, security, surveillance, and Tesla footage workflows where visual moments need to be found quickly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed footage, generated clips, GPS overlays, and location names may expose sensitive personal or location data. <br>
Mitigation: Use a limited API key or local backend for sensitive footage, avoid indexing broad private folders, and review clips before sharing. <br>
Risk: The skill depends on an external repository, runtime dependencies, and video-processing tools. <br>
Mitigation: Install only when the external repository and dependencies are trusted, and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssrajadh/natural-language-video-search) <br>
- [Project homepage](https://github.com/ssrajadh/sentrysearch) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local video indexes, trimmed clips, and optional telemetry-overlaid video files through the external sentrysearch tooling.] <br>

## Skill Version(s): <br>
0.2.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
