## Description:

A minimal demo skill that greets the user and prints the current UTC timestamp.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishers use this skill to smoke-test a ClawHub publish and install round trip with a minimal command-only skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill proposes a shell command for execution.

Mitigation: Review the command before running it; the security evidence indicates it only prints a greeting and UTC timestamp.

## Reference(s):

- [Hello ClawHub Demo listing](https://clawhub.ai/terrycarter1985/skills/hello-clawhub-demo)
- [terrycarter1985 publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Markdown with a bash command and expected plain-text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints one greeting line with an ISO-8601 UTC timestamp.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
