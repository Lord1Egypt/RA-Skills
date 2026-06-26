## Description: <br>
Everhour lets agents operate Everhour through an OOMOL-connected account for time tracking, timers, users, projects, tasks, and team time records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to manage Everhour time tracking through an OOMOL-connected Everhour account, including listing projects and tasks, creating time records, and starting or stopping timers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback setup path can ask the agent to run a remotely downloaded oo CLI installer script in a shell. <br>
Mitigation: Review the official installer or install guide before running it, and only use setup steps after an action fails because the CLI, authentication, or connection is missing. <br>
Risk: Everhour write actions can create time records or start and stop timers. <br>
Mitigation: Confirm the exact payload and expected Everhour change with the user before allowing write actions. <br>
Risk: The skill requires connecting Everhour through OOMOL and relies on sensitive credentials handled server-side. <br>
Mitigation: Install only if OOMOL is trusted for the intended Everhour workspace and the connected account has appropriate access. <br>


## Reference(s): <br>
- [Everhour homepage](https://everhour.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-everhour) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the oo CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, OOMOL sign-in, and an Everhour connection for live actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
