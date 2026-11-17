## Description:

Plan, orchestrate, and adversarially verify parallel AI coding agents - a dynamic multi-agent workflow engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suraj1235](https://clawhub.ai/user/suraj1235)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, run, and review parallel multi-agent coding workflows through a local Open Dynamic Workflows daemon. It is suited to tasks that can be split into independent subtasks and need adversarial verification before results are trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run a mutable external daemon with model credentials and local workspace authority.

Mitigation: Use a pinned, reviewed ODW commit or release, install in a restricted environment, and run the daemon only for repositories where that authority is acceptable.

Risk: Provider API keys may be exposed if handled carelessly during setup or daemon execution.

Mitigation: Keep provider API keys in the environment or local ODW configuration and avoid exposing them during dependency installation.

Risk: The daemon bridge writes plan.json in the working directory during planning.

Mitigation: Check for existing plan.json files before planning and review generated plans before execution.

## Reference(s):

- [Open Dynamic Workflows GitHub repository](https://github.com/Suraj1235/open-dynamic-workflows)
- [ClawHub skill page](https://clawhub.ai/suraj1235/skills/open-dynamic-workflows)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON workflow results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite plan.json when planning through the daemon bridge.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
