## Description: <br>
Publish markdown and return share links using curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and technical documentation authors use this skill to publish rendered Markdown documents with Mermaid diagrams, KaTeX, and code blocks, then retrieve a shareable link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published Markdown may expose secrets, customer data, private architecture notes, or internal documents through a shareable link. <br>
Mitigation: Review content before publishing, avoid sensitive material unless approved for external sharing, and use expires_hours when temporary access is intended. <br>
Risk: A missing share_url indicates the publish request did not complete as expected. <br>
Mitigation: Treat responses without share_url as errors and inspect the full JSON response before sharing or retrying. <br>


## Reference(s): <br>
- [AutEng Markdown publishing documentation](https://auteng.ai/llms.txt) <br>
- [AutEng publish-markdown API endpoint](https://auteng.ai/api/tools/docs/publish-markdown/) <br>
- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/markdown-publish-share) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON response handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes supplied Markdown to AutEng and expects a response containing share_url; optional title and expires_hours fields are supported.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and VERSION.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
