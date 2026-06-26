## Description: <br>
Compile legacy documentation on internet into agent-native memory context using the Moltext. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UditAkhourii](https://clawhub.ai/user/UditAkhourii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Moltext to compile web documentation for tools, libraries, or applications into dense Markdown context that can be read back into an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an npm package and fetches documentation URLs supplied by the user. <br>
Mitigation: Install it only in environments where npm package installation and outbound documentation fetching are acceptable. <br>
Risk: Compiled documentation may include incorrect, untrusted, or sensitive source content before it is reintroduced into an agent workflow. <br>
Mitigation: Review generated context files before use, and avoid compiling private or sensitive sources unless the data flow is understood. <br>
Risk: Optional LLM-based flows can require API credentials. <br>
Mitigation: Use raw mode when possible, and use scoped API keys when credentials are needed. <br>


## Reference(s): <br>
- [Moltext ClawHub release](https://clawhub.ai/UditAkhourii/moltext) <br>
- [OpenClaw documentation](https://docs.molt.bot/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to install and run the moltext CLI, then read the generated Markdown context file.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
