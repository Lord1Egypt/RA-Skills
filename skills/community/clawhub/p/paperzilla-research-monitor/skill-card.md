## Description: <br>
Monitors and discusses research papers from one Paperzilla project using the pz CLI inside OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pors](https://clawhub.ai/user/pors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, research engineers, and teams using Paperzilla use this skill to triage one project's feed, discuss selected papers, and generate recurring weekday briefs tied to their work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an already authenticated Paperzilla CLI and may deliver briefs through Telegram/OpenClaw. <br>
Mitigation: Before installing or running it, confirm that pz is the official Paperzilla CLI, that it is authenticated to the intended account, and that Telegram/OpenClaw delivery targets the intended destination. <br>
Risk: Recurring briefs retain paper IDs that were already included so later runs can avoid repeats. <br>
Mitigation: For sensitive projects, ask the host or publisher how to inspect or clear the retained brief history. <br>


## Reference(s): <br>
- [Paperzilla CLI documentation](https://docs.paperzilla.ai/guides/cli) <br>
- [Paperzilla Monitor ClawHub release](https://clawhub.ai/pors/paperzilla-research-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown chat responses with Paperzilla metadata, summaries, recommendations, and inline CLI command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paper identifiers used for feed triage, feedback, and recurring brief history.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
