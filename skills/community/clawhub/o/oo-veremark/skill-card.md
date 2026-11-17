## Description:

Use Veremark to review background-check requests and criteria, and create candidate check requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operators managing candidate background checks can use the skill to review available criteria and request status, retrieve results, and create new checks through Veremark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI dependency can install additional agent skills without clearly disclosing that effect.

Mitigation: Review and install a specific CLI release. Set OO_SKILLS_SYNC_DISABLED=1 for invocations where automatic changes to other agent skills are not wanted.

Risk: Candidate background-check data is processed through OOMOL and Veremark, while the hosted connector implementation and external installer contents are unverified.

Mitigation: Authorize only the access needed, review the CLI release before installing it, and confirm each new background-check request.

## Reference(s):

- [Veremark](https://www.veremark.com/)
- [Veremark API documentation](https://api.veremark.com/external/v1/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [CLI commands and JSON action results with concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
