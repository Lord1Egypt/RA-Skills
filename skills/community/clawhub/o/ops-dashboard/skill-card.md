## Description: <br>
Gather operational signals (disk usage, git status, recent commits, and resources) so you can answer "How is the Clawdy infrastructure doing?" without manually running multiple checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to generate a local snapshot of workspace health before deployments, updates, or support work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface workspace health metadata, including git status, recent commit summaries, changed file paths, directory names and sizes, disk usage, and system load. <br>
Mitigation: Run it only in workspaces where that operational metadata is appropriate to expose in an agent conversation. <br>


## Reference(s): <br>
- [Ops Dashboard reference](references/ops-dashboard.md) <br>
- [ClawHub skill page](https://clawhub.ai/CrimsonDevil333333/ops-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON reports from the local CLI, with Markdown guidance in agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local workspace disk usage, git status, recent commits, load averages, and top-level directory sizes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
