## Description: <br>
Route4Me helps agents read, create, and delete Route4Me optimization data through an OOMOL-connected Route4Me account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to operate a connected Route4Me account, including listing optimizations, creating route optimization problems, and deleting selected optimization problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a connected Route4Me account, including actions that create or delete optimization data. <br>
Mitigation: Review the proposed payload and effect before write actions, and require explicit user approval before destructive actions. <br>
Risk: First-time setup may run oo CLI installer or authentication commands. <br>
Mitigation: Run setup commands only when they are intentionally needed to resolve an authentication, connection, or missing-CLI failure. <br>
Risk: The skill depends on OOMOL-managed Route4Me credentials. <br>
Mitigation: Install it only when the user trusts OOMOL and wants the agent to access the connected Route4Me account. <br>


## Reference(s): <br>
- [Route4Me homepage](https://route4me.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Route4Me ClawHub listing](https://clawhub.ai/oomol/oo-route4me) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect action schemas before running Route4Me connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
