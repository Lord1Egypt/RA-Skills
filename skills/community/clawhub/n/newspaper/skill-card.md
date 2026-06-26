## Description: <br>
Render structured news content into a traditional newspaper-style HTML page with optional ComfyUI image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spootmu](https://clawhub.ai/user/spootmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn provided headlines, article bodies, and optional image prompts into a locally hosted newspaper-style HTML page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article text, titles, and generated HTML files may be accessible to other users or processes on the same machine. <br>
Mitigation: Avoid sensitive content in article fields and manage access to the local output directory and server port. <br>
Risk: Image prompts are sent to the configured ComfyUI endpoint when image generation is enabled. <br>
Mitigation: Use a trusted ComfyUI endpoint and omit sensitive details from image prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spootmu/newspaper) <br>
- [README.md](README.md) <br>
- [AGENT.md](AGENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [HTML, JSON, API calls, Guidance] <br>
**Output Format:** [JSON response containing a local URL to the rendered HTML page and optional image generation status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated HTML files locally and can send one image prompt per render request to the configured ComfyUI endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
