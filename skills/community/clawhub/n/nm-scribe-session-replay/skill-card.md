## Description: <br>
Converts a Claude Code session JSONL file into an animated GIF terminal replay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn prior Claude Code sessions into animated GIF terminal replays for demos, pull requests, tutorials, or shared workflow evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads prior Claude session logs under ~/.claude/projects/, which may contain sensitive prompts, tool outputs, or project details. <br>
Mitigation: Choose the session deliberately and review the parsed content before rendering or sharing the replay. <br>
Risk: Generated GIFs can expose private or irrelevant session details when full sessions, tool output, or thinking content are included. <br>
Mitigation: Limit the replay to necessary turns, exclude tools or thinking unless needed, and manually redact sensitive content before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-session-replay) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file paths, command examples, and generated replay artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a temporary VHS tape and delegates GIF rendering to the configured scry:vhs-recording dependency.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
