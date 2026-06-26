## Description: <br>
Coordinates multi-agent project work by routing ideas to Discord discussions, creating project threads, assigning initial agent tasks, and summarizing project status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project leads use this skill to coordinate multi-agent work through Discord by discussing ideas, initializing projects, assigning agent-specific tasks, and checking active project status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot token or channel configuration can be exposed through helper configuration output. <br>
Mitigation: Use a least-privilege bot token, redact configuration output before sharing it, and avoid storing secrets in project descriptions. <br>
Risk: Broad natural-language triggers can post messages or change project data in Discord unexpectedly. <br>
Mitigation: Prefer explicit /project:* commands and review the intended Discord-bound message before allowing the skill to send it. <br>
Risk: Project descriptions and task briefs can disclose confidential information to Discord channels or threads. <br>
Mitigation: Keep sensitive details out of project prompts and review every generated task brief before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexxxiong/inspirai-project) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API Calls] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or query Discord channels and threads when configured with a Discord bot token.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
