## Description: <br>
ImageKit helps an agent list, inspect, purge, and delete ImageKit media assets through the OOMOL ImageKit connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage ImageKit media library assets from an agent session, including search, metadata lookup, cache purge, purge status checks, and file deletion with confirmation controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad ImageKit prompts could be interpreted as permission to take account-impacting actions. <br>
Mitigation: Treat the trigger narrowly and confirm the exact payload and intended effect before approving write, purge, or delete actions. <br>
Risk: The skill requires sensitive ImageKit-connected credentials through the OOMOL account connection. <br>
Mitigation: Install it only for users who intend to manage ImageKit resources and keep credential handling inside the configured OOMOL connection. <br>
Risk: Destructive actions can permanently delete files or purge cached content. <br>
Mitigation: Require explicit user approval for destructive targets and verify identifiers or URLs before execution. <br>


## Reference(s): <br>
- [ImageKit homepage](https://imagekit.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-imagekit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON when actions are run with the oo CLI --json flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
