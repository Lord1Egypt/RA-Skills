## Description: <br>
Uses the MiniMax Coding Plan API for web search and image understanding when an agent needs current information, source lookup, image description, image analysis, or text extraction from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MirrorProMax](https://clawhub.ai/user/MirrorProMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to route web-search requests and image-understanding requests to MiniMax Coding Plan tools. It is suited for answering current-information questions, finding source material, describing images, analyzing image content, and extracting text from supported image formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a live-looking MiniMax API credential. <br>
Mitigation: Prefer a release that requires the user to provide their own declared API key and rotate or revoke any exposed credential before deployment. <br>
Risk: The skill runs an unpinned external MCP package at runtime. <br>
Mitigation: Pin and review the runtime package version before installation or execution. <br>
Risk: Search terms, image URLs, or local images can be sent to MiniMax. <br>
Mitigation: Warn users before sending sensitive queries or images and avoid processing confidential data unless the data-sharing path is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MirrorProMax/minimax-cp-search) <br>
- [Publisher profile](https://clawhub.ai/user/MirrorProMax) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text responses from MiniMax MCP tools, with command-line usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries, image URLs, and local images may be sent to MiniMax during use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
