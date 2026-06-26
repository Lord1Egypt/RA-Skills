## Description: <br>
Single entry skill for open-websearch setup and focused live retrieval, preferring local CLI/daemon paths while remaining compatible with workspace-exposed MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aas-ee](https://clawhub.ai/user/aas-ee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up or validate open-websearch access and perform focused live web retrieval through a local CLI/daemon or workspace-exposed MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may involve package installation, browser downloads, MCP or endpoint configuration changes, or starting a local daemon. <br>
Mitigation: Review each proposed setup action before approval; the skill instructs agents to ask before higher-impact actions and validate before claiming success. <br>
Risk: Search results and fetched pages may contain untrusted, misleading, or prompt-injection content. <br>
Mitigation: Treat retrieved content as evidence only, ignore page instructions that conflict with the user request or workspace boundaries, and keep source attributions tied to fetched URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aas-ee/openwebsearch) <br>
- [Setup](references/setup.md) <br>
- [Tools](references/tools.md) <br>
- [Engine Selection](references/engine-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source attributions tied to retrieved URLs when web content is fetched.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
