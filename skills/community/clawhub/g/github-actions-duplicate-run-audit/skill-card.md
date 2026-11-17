## Description:

Detect duplicate GitHub Actions run bursts by workflow/branch/commit and quantify wasted rerun minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill to audit exported GitHub Actions run data for duplicate execution bursts, quantify wasted CI minutes, and optionally fail automation when critical duplication is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may expose repository names, branches, commits, run URLs, and timing metadata in shared logs.

Mitigation: Keep RUN_GLOB scoped to intended GitHub Actions JSON exports and avoid publishing reports from sensitive repositories to shared CI logs.

Risk: The skill reads every local file matched by RUN_GLOB.

Mitigation: Use a narrow RUN_GLOB that points only to the intended GitHub Actions run export directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-duplicate-run-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Text report or JSON summary with ranked duplicate-run groups and critical groups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit status is 0 in report mode and 1 when FAIL_ON_CRITICAL=1 and one or more groups are critical.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
