## Description:

Audits the DSA problem bank for coverage gaps and proposes new YAML entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining a DSA problem bank use this skill to compare category coverage with the manifest, identify gaps, and prepare YAML problem entries for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coverage report may miss or misstate gaps if referenced problem-bank materials are missing or out of date.

Mitigation: Confirm the manifest, problem files, and analysis script are available, then review the category counts and existing problems.

Risk: Proposed problem entries could be inaccurate or misleading.

Mitigation: Have a human review each proposal and validate it against the problem schema before adding it to the bank.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-gauntlet-problem-bank)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Markdown coverage report with YAML problem entry proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposals are for human review and validation before inclusion in the problem bank.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
