## Description: <br>
Explain how to connect NovelAI to OpenClaw through a local OpenAI-compatible shim for local adaptor configuration, model selection, and OpenClaw `base_url` setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askkumptenchen](https://clawhub.ai/user/askkumptenchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a local NovelAI adaptor endpoint, choose supported text or image models, and keep NovelAI credentials in local configuration rather than chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install or run an unverified local adaptor package. <br>
Mitigation: Verify the package source, maintainer, repository, and release history before installation, and require user approval before running install commands. <br>
Risk: NovelAI credentials may be exposed if pasted into chat or included inline in commands. <br>
Mitigation: Keep credentials in the local configuration flow only and avoid inline secrets in command examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askkumptenchen/novelai-openclaw-adaptor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local-only credential handling guidance, supported model names, and OpenClaw base_url configuration details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
