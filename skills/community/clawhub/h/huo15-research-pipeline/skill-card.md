## Description: <br>
Automates a six-phase research workflow from topic scoping through literature discovery, synthesis, experiment design, analysis, and paper drafting with human checkpoints and local OpenClaw output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to run a structured, human-reviewed research pipeline for a supplied topic and produce phase notes plus a draft academic paper through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and topics are sent through the configured OpenClaw LLM service, which may expose sensitive or proprietary research material depending on provider settings. <br>
Mitigation: Avoid confidential topics unless the configured LLM/provider settings are acceptable for that data. <br>
Risk: The shell workflow writes generated research files under the user's OpenClaw home directory. <br>
Mitigation: Invoke the workflow explicitly and review the configured output path before using it in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-research-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown files with terminal prompts and log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes phase outputs under $HOME/.openclaw/agents/main/agent/kb/raw/research-{topic}-{date}/ and pauses for human confirmation between phases.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter is 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
