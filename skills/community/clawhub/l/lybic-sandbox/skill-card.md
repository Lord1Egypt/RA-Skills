## Description: <br>
Lybic Sandbox is a cloud sandbox built for agents and automation workflows, letting agents create disposable cloud computers, automate desktop or Android GUIs, execute code and commands, manage files, expose HTTP services, and observe or stop runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AEnjoy](https://clawhub.ai/user/AEnjoy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to control Lybic cloud sandboxes for isolated code execution, GUI automation, Android automation, file processing, web service testing, and project or sandbox lifecycle management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can create and control Lybic cloud sandboxes, including GUI actions and process execution. <br>
Mitigation: Install only for workflows that require sandbox control, use least-privileged Lybic credentials, and monitor or stop runs when needed. <br>
Risk: Credentials are required through LYBIC_ORG_ID and LYBIC_API_KEY. <br>
Mitigation: Provide credentials through environment variables or a secret manager and never commit real credentials to source files or examples. <br>
Risk: The skill can download files into sandboxes and process them. <br>
Mitigation: Validate downloaded files before processing and avoid using untrusted inputs in sensitive workflows. <br>
Risk: HTTP port mappings can expose sandbox services through public URLs. <br>
Mitigation: Expose only intended services, require authentication where appropriate, and remove mappings when work is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AEnjoy/lybic-sandbox) <br>
- [Publisher Profile](https://clawhub.ai/user/AEnjoy) <br>
- [Lybic Homepage](https://lybic.ai) <br>
- [Lybic Python SDK Docs](https://docs.lybic.cn/en/sdk/python) <br>
- [Lybic Action Space Docs](https://docs.lybic.cn/en/sandbox/action) <br>
- [Lybic Code Execution Docs](https://docs.lybic.cn/en/sandbox/code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include async Python examples, environment variable setup, sandbox action payloads, and cleanup guidance.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
