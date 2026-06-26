## Description: <br>
Audit OpenClaw agent tool exposure versus observed use, including broad or unused tool allowances, using an already-installed trusted local CLI that can emit Markdown or JSON summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit local OpenClaw agent tool configuration against observed tool usage and identify overly broad or unused tool access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local audit report may reveal local agent configuration, session paths, tool usage, or other sensitive operational details. <br>
Mitigation: Treat generated reports as sensitive and review them before sharing. <br>
Risk: The skill depends on a local openclaw-tool-audit binary or source checkout. <br>
Mitigation: Use it only with a trusted or verified local installation and avoid elevated execution unless required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON report output from the local audit CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill relies on a trusted local openclaw-tool-audit installation and may guide users to inspect local OpenClaw config and session data.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
