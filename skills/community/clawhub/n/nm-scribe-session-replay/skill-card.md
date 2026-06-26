## Description: <br>
Converts a Claude Code session JSONL file into an animated GIF terminal replay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to convert selected Claude Code session logs into animated GIF terminal replays for pull requests, tutorials, workflow demos, and visual evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can list and read local Claude Code session logs, which may include secrets, customer data, internal URLs, tokens, tool output, or private discussion. <br>
Mitigation: Install only if comfortable granting that access, review generated GIFs before sharing, and prefer narrow options such as --turns and --show user,assistant. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/athola/nm-scribe-session-replay) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown/text responses with command examples, generated VHS tape files, and animated GIF outputs through the scry dependency] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Claude Code JSONL session logs and should use narrow filters such as --turns and --show to limit exposed content.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
