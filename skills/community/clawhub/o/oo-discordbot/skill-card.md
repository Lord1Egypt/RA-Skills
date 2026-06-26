## Description: <br>
Discord Bot (discord.com). Use this skill for ANY Discord Bot request: reading, creating, updating, and deleting Discord Bot data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Discord bot workflows through OOMOL-connected accounts, including reading Discord resources and creating, updating, or deleting channels, messages, roles, members, invites, threads, application commands, and related server objects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected Discord bot may have moderation or administration permissions over important servers. <br>
Mitigation: Use least-privilege Discord bot permissions and review the skill before installing it for high-impact servers. <br>
Risk: Some state-changing Discord operations are not tagged for confirmation even though the skill says untagged actions are safe reads. <br>
Mitigation: Manually confirm any prune, unban, pin, unpin, crosspost, delete, role, member, invite, or message-changing operation before execution. <br>
Risk: The skill depends on installing and running the oo CLI. <br>
Mitigation: Install the oo CLI only from a trusted source and prefer a verified installer or package-manager path over pipe-to-shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-discordbot) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Discord developer applications](https://discord.com/developers/applications) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
