## Description:

Moss Skill-9 installs and configures upstream internet data tools for social platforms, video sites, GitHub, RSS, and web pages so an agent can call those tools directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwzh](https://clawhub.ai/user/jiangwzh)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to install, check, and configure platform access channels, then run upstream tools for web, social, video, repository, job, and feed retrieval tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unverified remote tooling with broad local tool access.

Mitigation: Install only after reviewing the upstream repository, prefer pinned or audited releases, and run commands in a constrained environment.

Risk: The skill may require live account cookies or proxy credentials for platform access.

Mitigation: Do not paste personal cookies or proxy passwords into agent chat; use dedicated low-privilege accounts and verify exactly what credentials will be stored.

Risk: Cookie-based access can expose accounts or trigger platform account enforcement.

Mitigation: Use dedicated accounts where possible and avoid storing sensitive cookies beyond the minimum needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangwzh/skills/moss-skill-9)
- [Publisher profile](https://clawhub.ai/user/jiangwzh)
- [agent-reach installation archive](https://github.com/Panniantong/agent-reach/archive/main.zip)
- [Cookie-Editor browser extension](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific commands and configuration guidance for upstream tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
