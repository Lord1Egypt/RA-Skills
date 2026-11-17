## Description:

Control OpenCode to execute development tasks. Provides session management and task execution capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongxh13](https://clawhub.ai/user/gongxh13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use OCC to delegate coding tasks to OpenCode, manage OpenCode sessions, and continue task execution from a CLI or external workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently runs npm install with unpinned dependencies during normal use.

Mitigation: Install and review dependencies before use; prefer a release with a lockfile, pinned dependency versions, and no automatic install step.

Risk: The skill can start and control an OpenCode session that works in the current directory.

Mitigation: Run it only from the intended project directory and review the requested task before allowing OpenCode to modify files.

Risk: Session prompts and replies are sent to local OpenCode session APIs.

Mitigation: Avoid sending secrets or sensitive project data unless the local OpenCode environment is approved for that data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the OpenCode CLI in PATH and may start a local OpenCode server for session operations.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact scripts/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
