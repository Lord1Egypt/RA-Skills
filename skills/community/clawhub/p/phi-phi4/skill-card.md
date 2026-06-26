## Description: <br>
Guides agents through installing and using Microsoft Phi-family models with the ollama-herd local fleet router on low-RAM, cross-platform devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up ollama-herd, route Phi models across local devices, and call local chat, monitoring, image, speech, and embedding APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local router exposes broader model, image, speech, embedding, and monitoring APIs than a single Phi shortcut. <br>
Mitigation: Install only when the broader ollama-herd router is intended, review the package source, and keep the service bound to trusted interfaces. <br>
Risk: Prompts, uploaded files or audio, and fleet logs may contain sensitive data. <br>
Mitigation: Use an isolated Python environment where practical and treat ~/.fleet-manager logs and submitted content as sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/phi-phi4) <br>
- [ollama-herd PyPI Project](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup and API usage examples; model downloads require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
