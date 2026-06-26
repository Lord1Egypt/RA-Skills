## Description: <br>
Recommends curated Nano Banana Pro image-generation prompts and prompt templates from a large community library based on a user's image or content needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DophinL](https://clawhub.ai/user/DophinL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, designers, and developers use this skill to find, preview, and adapt image-generation prompts for portraits, products, social media, posters, article illustrations, and other content needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill refreshes prompt data from a mutable live source, which can change recommendations over time. <br>
Mitigation: Install only if you trust the YouMind-OpenLab source, scope network access and file writes where possible, and review downloaded references when reproducibility matters. <br>
Risk: Prompt recommendations may include preview media loaded from external URLs. <br>
Mitigation: Avoid fetching or sending preview media from unexpected domains, and use environments where outbound media access can be reviewed or restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DophinL/nano-banana-pro-prompts-recommend) <br>
- [YouMind Nano Banana Pro prompt gallery](https://youmind.com/nano-banana-pro-prompts?utm_source=nano-banana-pro-prompts-recommend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with prompt previews, source links, optional image references, and setup commands for refreshing local prompt data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are capped at three prompts per request and include attribution to YouMind.com when presenting prompts.] <br>

## Skill Version(s): <br>
1.5.9 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
