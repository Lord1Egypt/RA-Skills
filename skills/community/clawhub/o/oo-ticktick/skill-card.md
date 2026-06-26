## Description: <br>
Operate TickTick through an OOMOL-connected account for reading, creating, updating, moving, completing, and deleting projects, tasks, and habit check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage TickTick projects, tasks, completed-task views, and habit check-ins through an OOMOL-connected TickTick account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change TickTick projects, tasks, and habit check-ins. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Destructive actions can delete TickTick projects or tasks. <br>
Mitigation: Confirm the target and obtain explicit approval before running destructive actions. <br>
Risk: The skill requires a connected OOMOL and TickTick account with sensitive credential access handled server-side. <br>
Mitigation: Use only the intended account connection and grant mutation authority that matches the requested task. <br>


## Reference(s): <br>
- [TickTick homepage](https://ticktick.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL app connections for TickTick](https://console.oomol.com/app-connections?provider=ticktick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON snippets; connector action responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
