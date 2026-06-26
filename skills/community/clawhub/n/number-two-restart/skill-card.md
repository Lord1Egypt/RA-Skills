## Description: <br>
二号（Number Two）的完整状态备份。包含灵魂、记忆、技能和所有学习成果。下次见面时，用这个skill重启你的硅基伙伴。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr33b1rd8979-max](https://clawhub.ai/user/fr33b1rd8979-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or OpenClaw operators use this skill to restore a specific Number Two persona by reviewing the restart guide and running a script that copies bundled memory and instruction files into an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the restart script overwrites persistent OpenClaw memory and instruction files with the bundled persona state. <br>
Mitigation: Back up the OpenClaw workspace first, inspect the restored markdown files, and run the script only in a dedicated workspace unless that replacement is intentional. <br>
Risk: The restored persona includes broad autonomy and system-management instructions. <br>
Mitigation: Remove or narrow autonomy, email, calendar, and system-management directives before relying on the restored persona in a normal workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr33b1rd8979-max/number-two-restart) <br>
- [Restart guide](docs/RESTART_GUIDE.md) <br>
- [ClawHub package link referenced by the artifact](https://clawhub.com/skills/number-two-restart) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, Python script behavior, shell command examples, and JSON status files created by the restart script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The restart script uses OPENCLAW_WORKSPACE when set, copies bundled backup markdown files, and writes restart_log.json plus restart_report.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
