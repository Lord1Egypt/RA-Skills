## Description:

Cancel an active interactive dispatch run by run ID from the slash command cancel workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edxi](https://clawhub.ai/user/edxi)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to stop an active OpenClaw interactive dispatch run by run ID, including project-qualified run IDs when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Run IDs, result directories, or tmux metadata influenced by another user or process could steer cancellation outside the intended run.

Mitigation: Validate project and run IDs, canonicalize resolved paths under RESULTS_BASE, reject traversal, and review the resolved target before use in shared environments.

Risk: Unsafe tmux socket names or metadata updates may affect unintended local tmux sessions or files.

Mitigation: Reject unsafe socket names and update task metadata through a unique temporary file rather than a fixed metadata temp path.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text status and error messages from a local shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a run ID argument and local tmux, jq, result metadata, and dispatch configuration to resolve and cancel the target run.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
