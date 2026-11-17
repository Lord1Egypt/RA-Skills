## Description:

OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simbabuddy](https://clawhub.ai/user/simbabuddy)

### License/Terms of Use:


## Use Case:

Developers and technical users use OpenProse to execute, validate, and author `.prose` workflows that orchestrate multiple AI agents, route OpenProse commands, fetch reusable programs, and manage run state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted `.prose` programs can spawn agents, fetch remote workflows, and write persistent state.

Mitigation: Inspect workflows before running them, avoid remote or untrusted programs, and review requests for persistence, shell access, network access, or writes outside the current project.

Risk: PostgreSQL mode can expose `OPENPROSE_POSTGRES_URL` credentials to subagent sessions and logs.

Mitigation: Keep PostgreSQL disabled unless it is isolated securely, and use a dedicated database with limited-privilege credentials.

Risk: Persistent run state and agent memory can retain sensitive workflow outputs.

Mitigation: Avoid production secrets, review `.prose/runs/` and agent memory contents after sensitive runs, and clean state that should not persist.

## Reference(s):

- [OpenProse homepage](https://www.prose.md)
- [OpenProse ClawHub skill page](https://clawhub.ai/simbabuddy/skills/open-prose)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update `.prose/` run state, bindings, imports, and agent memory when executing workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
