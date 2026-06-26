## Description: <br>
Mee6 operations via Discord message tool (channel=discord). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilmn25](https://clawhub.ai/user/ilmn25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent send explicit Mee6 bot commands in Discord for level checks, XP changes, role creation, plugin toggles, and prefix updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send Discord commands that change Mee6 roles, plugins, prefixes, or XP. <br>
Mitigation: Use a least-privileged Discord token or bot account, restrict it to intended servers and channels, keep Discord action gating enabled, and require explicit confirmation for role, plugin, prefix, or XP-changing commands. <br>
Risk: Mee6 commands could be sent in the wrong context if the agent treats unrelated Discord work as Mee6 work. <br>
Mitigation: Send Mee6 commands only when the user explicitly requests interaction with the Mee6 bot; use the generic Discord skill for unrelated Discord actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilmn25/mee6) <br>
- [Publisher profile](https://clawhub.ai/user/ilmn25) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Discord command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Discord token and explicit user intent before sending Mee6 commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
