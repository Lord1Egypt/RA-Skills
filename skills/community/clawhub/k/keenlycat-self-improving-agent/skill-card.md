## Description:

Continuously captures and applies learnings from errors, user corrections, successful tasks, and periodic reviews to improve agent performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keenlycat](https://clawhub.ai/user/keenlycat)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to capture errors, user corrections, successes, and insights as local learnings, then search and review those learnings before related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local learning logs may store task context and failed command details without strong consent, redaction, or integrity safeguards.

Mitigation: Review before installing, avoid wrapping commands that include secrets or confidential paths, and use opt-in capture with redaction, restrictive file permissions, and a clear review and deletion process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keenlycat/skills/keenlycat-self-improving-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, and local JSONL learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores captured learnings locally in JSONL when the bundled shell scripts are used.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
