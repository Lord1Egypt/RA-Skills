## Description: <br>
Multi-agent collaborative industry research for OpenClaw that assigns research roles, runs parallel sub-agent research with optional Codex, Gemini, and Claude CLI augmentation, reviews quality iteratively, merges findings, and outputs a structured Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shineliang](https://clawhub.ai/user/shineliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to coordinate multiple sub-agents for industry research, cross-validate findings with optional external AI CLIs, review report quality, and merge results into a structured Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move or delete broad workspace files during cleanup. <br>
Mitigation: Run it in a dedicated empty workspace and choose archive instead of delete during cleanup. <br>
Risk: Research content may be sent to external AI CLI tools under local accounts by default. <br>
Mitigation: Set RESEARCH_CROSS_MODEL=none or restrict RESEARCH_CLI_TOOLS for confidential, regulated, client, or internal topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shineliang/multi-agent-industry-research) <br>
- [Project homepage](https://github.com/shineliang/industry-research-skill) <br>
- [CLI cross-validation protocol](references/cross-validation.md) <br>
- [OpenClaw tool mapping reference](references/tool-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and status updates with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-topic research folders and may call external AI CLI tools depending on configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
