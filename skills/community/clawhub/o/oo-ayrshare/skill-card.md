## Description: <br>
Ayrshare helps agents manage social posting workflows, including reading, creating, updating, validating, scheduling, and deleting posts through a connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate an Ayrshare-connected social posting account from an agent, including post publishing, validation, analytics, history lookup, profile access, updates, retries, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive Ayrshare actions can affect public or scheduled social media content. <br>
Mitigation: Review payloads carefully and require explicit user confirmation before publishing, updating, retrying, or deleting posts. <br>
Risk: The skill depends on an OOMOL-connected Ayrshare account and may fail when authentication, connection scope, app readiness, or billing is missing. <br>
Mitigation: Use the documented first-time setup or billing steps only after a command fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub Ayrshare skill page](https://clawhub.ai/oomol/skills/oo-ayrshare) <br>
- [Ayrshare homepage](https://www.ayrshare.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Ayrshare connector actions through the oo CLI when the agent has user approval and the account is connected.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
