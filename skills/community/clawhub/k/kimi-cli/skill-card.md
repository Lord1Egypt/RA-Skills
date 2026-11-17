## Description:

Kimi Code CLI helps agents delegate complex coding tasks to Kimi CLI for code generation, refactoring, debugging, research implementation, and long-running development sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkman1w](https://clawhub.ai/user/walkman1w)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to prepare and run Kimi CLI coding sessions for larger implementation, refactoring, debugging, and proof-of-concept tasks. It is most relevant when a task needs a PTY-backed CLI workflow, a dedicated work directory, and ongoing session monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce or relay shell commands that may change local files or run unsafe operations.

Mitigation: Install and run it only in a controlled environment, review proposed commands before execution, and prefer a pinned, reviewed Kimi CLI version inside a virtual environment.

Risk: Untrusted task text or paths passed through the bundled runner could steer execution toward unintended files or commands.

Mitigation: Use a dedicated project directory, avoid passing untrusted prompts or paths, and keep the working directory constrained to the intended task.

Risk: Interactive background sessions can remain active after the task finishes.

Mitigation: Monitor active sessions and explicitly kill each Kimi session after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/walkman1w/skills/kimi-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/walkman1w)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON runner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow assumes Kimi CLI is installed and authenticated, uses PTY-backed execution, and recommends dedicated work directories with explicit timeouts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
