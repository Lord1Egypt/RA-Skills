## Description:

Audits the DSA problem bank for coverage gaps and proposes new YAML entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining the Gauntlet DSA problem bank use this skill to audit category coverage against manifest counts and prepare proposed YAML problem entries for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed problem entries could be inaccurate, incomplete, or misaligned with the existing problem bank.

Mitigation: Keep the generated report in review mode and require a human to approve any YAML additions before merging.

Risk: The workflow assumes the Gauntlet plugin layout and supporting scripts are present.

Mitigation: Confirm the expected plugin directory, problem manifest, and curation script before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-gauntlet-curate)
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with YAML proposal examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human approval is required before proposed problem entries are merged into the problem bank.]

## Skill Version(s):

1.9.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
