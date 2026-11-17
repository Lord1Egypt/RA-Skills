## Description:

A small utility skill that greets users and demonstrates the ClawHub publish flow.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub publishers can use this demo skill to inspect a minimal skill folder structure and run a simple greeting command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running bundled shell scripts executes local commands from the artifact.

Mitigation: Review scripts/greet.sh before execution; for this release, server evidence indicates it only prints a greeting and performs no meaningful system changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and a small shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script prints a greeting and does not require inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
