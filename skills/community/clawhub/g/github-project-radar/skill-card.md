## Description:

GitHub Project Radar helps Chinese-speaking users deduplicate, tier, test, and record GitHub repository candidates for personal use, publishing, validation, or archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Content creators, researchers, operators, and developers who collect GitHub repository links use this skill to normalize repository identities, detect duplicates, assign review tiers, decide next actions, and maintain a local candidate table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-back could update the wrong local candidate table or record an unintended change.

Mitigation: Review the target candidate table path and proposed row changes before allowing write-back.

Risk: Installation tests for candidate repositories could execute untrusted code.

Mitigation: Require explicit confirmation before any installation test, test one repository at a time, and record the command source plus rollback plan before execution.

Risk: A repository could be promoted to use or publish based on incomplete evidence.

Mitigation: Check at least three stated evidence criteria before assigning the use or publish tier.

## Reference(s):

- [Review checklist](references/review-checklist.md)
- [Candidate table template](assets/candidate-table-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown candidate records and candidate-table updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include repository identity, canonical URL, duplicate status, summary, rationale, tier, next action, and review notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
