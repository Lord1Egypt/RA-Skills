## Description: <br>
Assists with creating, scripting, organizing, debugging, and packaging Garry's Mod addons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzmjlrt](https://clawhub.ai/user/lzmjlrt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and addon creators use this skill to plan Garry's Mod addon structure, write Lua scripts, reason about client and server realms, debug common Lua errors, and prepare addons for distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lua code generated for autorun or server-side folders could affect live Garry's Mod behavior if used without review. <br>
Mitigation: Review generated Lua and test it in-game or in a non-production server before placing it in autorun or server-side addon folders. <br>
Risk: Broad trigger wording may cause the skill to activate more often than necessary. <br>
Mitigation: Confirm that the current task is specifically about Garry's Mod, GMod Lua, addon structure, packaging, or debugging before relying on the skill. <br>
Risk: Guessed Garry's Mod API URLs may lead to missing or incorrect documentation. <br>
Mitigation: Use the Garry's Mod wiki index or search for the exact API term instead of constructing API documentation URLs manually. <br>


## Reference(s): <br>
- [Lua Folder Structure](references/addon-structure.md) <br>
- [Common Errors](references/common-error.md) <br>
- [States / Realms](references/state-exp.md) <br>
- [Garry's Mod Wiki](https://wiki.facepunch.com/gmod) <br>
- [ClawHub release page](https://clawhub.ai/lzmjlrt/gmod-addon-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Lua code, addon structure examples, and command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Lua and addon placement guidance should be reviewed before use in a live Garry's Mod server or autorun folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
