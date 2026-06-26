## Description: <br>
Generates Mermaid diagrams and renders them as PNG images, with optional upload to Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xx235300](https://clawhub.ai/user/xx235300) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and documentation authors use this skill to turn requested workflows, architectures, timelines, and other structured ideas into Mermaid diagrams and rendered PNG assets. It can also help prepare diagram images for Feishu documents when the user approves an upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering user-controlled Mermaid through browser HTML that loads Mermaid from a CDN can expose diagram content to browser and network handling risks. <br>
Mitigation: Render only trusted or reviewed diagram text, keep confidential diagrams local, and avoid CDN-backed rendering when the environment requires strict data isolation. <br>
Risk: Optional Feishu uploads or remote rendering fallbacks can send diagram content to external services. <br>
Mitigation: Require explicit user approval before uploads or remote fallback rendering, and do not send confidential diagrams to external services. <br>


## Reference(s): <br>
- [Mermaid Syntax Guide](references/syntax-guide.md) <br>
- [Mermaid Diagram Patterns](references/diagram-patterns.md) <br>
- [Mermaid Official Documentation](https://mermaid.nodejs.cn/) <br>
- [Mermaid Live Editor](https://mermaid.live/) <br>
- [Mermaid CDN](https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks and PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a local HTML path for browser screenshot rendering and may produce a Feishu media token when upload is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
