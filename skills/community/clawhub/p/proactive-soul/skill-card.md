## Description: <br>
Gives your agent an inner life - proactive daily dispatches, persistent intellectual threads, and genuine pushback when it disagrees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobgourley](https://clawhub.ai/user/bobgourley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users install this skill to give an agent persistent intellectual continuity, proactive daily outreach, and a defined pushback style. It is intended for agents configured with QMD, cron scheduling, and a private messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads broad workspace, memory, and vault content before dispatches. <br>
Mitigation: Limit QMD indexing to intended paths and keep sensitive vaults or files out of the index unless they should inform dispatches. <br>
Risk: The skill changes persistent workspace behavior by patching AGENTS.md and creating CURIOSITY.md. <br>
Mitigation: Review the AGENTS.md patch before enabling; to remove the behavior, uninstall the skill, delete CURIOSITY.md, and revert the AGENTS.md additions. <br>
Risk: The skill sends scheduled unprompted messages through the configured messaging channel. <br>
Mitigation: Use a private channel, confirm the four cron jobs are desired, and disable those cron jobs to pause outbound dispatches. <br>
Risk: The skill has no strong runtime consent gate for its persistent authority. <br>
Mitigation: Enable it only after explicit user approval of the workspace changes, indexed paths, messaging channel, and pause/removal process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobgourley/proactive-soul) <br>
- [Publisher profile](https://clawhub.ai/user/bobgourley) <br>
- [Project homepage](https://github.com/bobgourley/proactive-soul) <br>
- [README](README.md) <br>
- [Proactive outreach protocol](references/proactive-protocol.md) <br>
- [Pushback protocol](references/pushback-protocol.md) <br>
- [Intellectual character](references/intellectual-character.md) <br>
- [Knowledge core](references/Knowledge_Core.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update AGENTS.md and CURIOSITY.md when enabled, and may send scheduled outbound messages through the configured channel.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
