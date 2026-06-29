## Description: <br>
Browse hookify rule catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to browse and install pre-built Hookify rules for git safety, Python quality, security gates, workflow enforcement, and performance guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Hookify rule files can warn or block future agent actions in a project. <br>
Mitigation: Review each .claude/hookify.*.local.md file before creating it, start with warn rules before block rules, and remove or disable rules that interfere with normal work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-hookify-rule-catalog) <br>
- [Hookify homepage](https://github.com/athola/claude-night-market/tree/master/plugins/hookify) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and rule file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rule selection and installation guidance; installed rules may create or update .claude/hookify.*.local.md files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
