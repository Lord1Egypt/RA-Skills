## Description: <br>
Generates text-to-image and image-to-image requests through giggle.pro, with options for model, aspect ratio, resolution, references, and asynchronous status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create new images from prompts, transform images from references, choose generation settings, and check asynchronous generation status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, reference images or image URLs, and API requests are handled by giggle.pro. <br>
Mitigation: Avoid confidential or sensitive content unless sharing it with giggle.pro is acceptable. <br>
Risk: Completed generations can return signed image links and task IDs that may expose generated content if shared. <br>
Mitigation: Keep signed links private and clear remembered task IDs for sensitive generations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/giggle-generation-image) <br>
- [Giggle API service](https://giggle.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON task status, and signed image links when generation completes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GIGGLE_API_KEY and python3 with requests; generation is asynchronous and may return task IDs for later status checks.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
