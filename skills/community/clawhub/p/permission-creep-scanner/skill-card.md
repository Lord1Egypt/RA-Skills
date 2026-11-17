## Description:

Helps detect permission creep in AI agent skills by flagging when a skill's actual code accesses resources beyond what its declared purpose requires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review AI agent skills for permission creep, including mismatches between declared purpose and actual access to files, environment variables, network calls, subprocesses, and sensitive paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides heuristic review guidance rather than sandbox enforcement.

Mitigation: Manually review its findings before relying on them, especially for skills that handle credentials, broad filesystem access, network calls, or shell execution.

Risk: Static and heuristic permission analysis can miss dynamically loaded code, obfuscated paths, or indirect access through libraries.

Mitigation: Use the audit as an initial signal and perform deeper manual code review for high-stakes or sensitive deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/permission-creep-scanner)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured permission audit with declared scope, actual access list, mismatch flags, risk rating, and recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
