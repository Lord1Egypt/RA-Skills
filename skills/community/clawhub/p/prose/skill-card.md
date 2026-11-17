## Description:

OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mondilo1](https://clawhub.ai/user/mondilo1)

### License/Terms of Use:


## Use Case:

Developers and automation teams use Prose to run, compile, and author .prose workflows that orchestrate multi-agent sessions, manage workflow state, and produce reusable automation artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote .prose programs can be fetched and executed as powerful workflows.

Mitigation: Treat .prose files like code and run remote programs only after reviewing and trusting their source.

Risk: Persistent project, user, or custom agent memory can retain workflow context beyond a single run.

Mitigation: Prefer local filesystem state for normal use and review or disable project, user, or custom persistence before deployment.

Risk: Database-backed state can expose credentials or sensitive data if used with real secrets or production systems.

Mitigation: Avoid production databases and real secrets; use dedicated, limited-privilege databases when database-backed state is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mondilo1/skills/prose)
- [Publisher profile](https://clawhub.ai/user/mondilo1)
- [OpenProse homepage](https://www.prose.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and optional .prose files or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist workflow state in .prose files or configured databases when execution modes require it.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
