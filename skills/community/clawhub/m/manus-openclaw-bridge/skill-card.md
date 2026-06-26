## Description: <br>
Connect OpenClaw to Manus task APIs for chat-driven image generation, document/slides jobs, task polling, output collection, and messaging-surface return flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t0nyren](https://clawhub.ai/user/t0nyren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to route explicit Manus requests from chat surfaces into Manus task APIs, poll for completion, collect generated files, and return images, documents, slides, or concise status summaries to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The slides JSON-to-PPTX conversion path may fetch remote assets and write files outside the documented safety limits. <br>
Mitigation: Review the converter before installation and avoid running it on untrusted Manus output until HTTPS Manus-host allowlisting, redirect revalidation, size limits, and safe filename handling are enforced. <br>
Risk: The skill depends on a Manus API key and endpoint configured on the local machine. <br>
Mitigation: Use a dedicated Manus API key, protect the local config file, and install only when the Manus endpoint and publisher are trusted. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/t0nyren/manus-openclaw-bridge) <br>
- [Publisher Profile](https://clawhub.ai/user/t0nyren) <br>
- [Manus API Documentation](https://open.manus.im/docs) <br>
- [Setup](references/setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Chat Patterns](references/chat-patterns.md) <br>
- [Feishu Return](references/feishu-return.md) <br>
- [Slides Handling](references/slides.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON, files] <br>
**Output Format:** [Markdown guidance with bash, Python, Node.js, JSON, and generated file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local environment configuration for Manus API credentials and can save downloaded Manus outputs under the skill workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
