## Description:

Quantify wasted GitHub Actions minutes caused by reruns so flaky workflows can be fixed with data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit exported GitHub Actions run data, quantify rerun minutes, and prioritize flaky workflow fixes or CI gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can process unintended GitHub Actions export files if RUN_GLOB is broader than intended.

Mitigation: Review RUN_GLOB before use so it points only at the intended local JSON exports.

Risk: Reports may expose repository, branch, commit, workflow, and job metadata from the local GitHub Actions exports.

Mitigation: Limit input files to approved exports and handle generated reports according to repository data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-rerun-waste-audit)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Text report or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit 1 when FAIL_ON_CRITICAL=1 and one or more critical waste groups are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
