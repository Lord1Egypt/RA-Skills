## Description: <br>
Renders Mermaid diagrams to PNG images with Browser/Canvas and uploads and sends them to a configured Feishu conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and collaborators use this skill to turn Mermaid flowcharts, sequence diagrams, UML-style diagrams, and related visualizations into image messages for Feishu when native Mermaid rendering is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated diagram images to Feishu without a clear per-send confirmation step. <br>
Mitigation: Configure the agent to ask before each upload or send, and verify the intended recipient before delivery. <br>
Risk: Diagram images may contain sensitive architecture, workflow, or data-model details. <br>
Mitigation: Avoid sending sensitive diagrams unless the Feishu app, conversation, and audience are approved for that content. <br>
Risk: Feishu app credentials and recipient IDs enable message delivery to external conversations if misconfigured. <br>
Mitigation: Use a least-privilege Feishu app, store credentials outside the skill text, and validate the recipient ID before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/mermaid-to-feishu) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>
- [Mermaid browser bundle](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG image delivery to Feishu with supporting Markdown, code, shell command, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and a configured recipient ID; can use Browser/Canvas rendering or mermaid-cli where available.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
