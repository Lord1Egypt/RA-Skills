## Description:

Verify data integrity with hashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to validate data integrity, automate hash checks, and report verification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for HASH_API_KEY without explaining its purpose or handling requirements.

Mitigation: Confirm whether the key is required, keep it out of committed files and logs, and provide secret-handling guidance before use.

Risk: The documented command references scripts/hash_verifier.py, but no executable script is included in the artifact.

Mitigation: Verify the required verifier implementation is supplied and reviewed before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-hash-verifier)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced verifier command is expected to return JSON verification results.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
