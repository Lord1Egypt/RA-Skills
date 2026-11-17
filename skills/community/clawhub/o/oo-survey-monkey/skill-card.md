## Description:

Read, create, and manage SurveyMonkey surveys, contacts, collectors, and responses through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected SurveyMonkey account can inspect surveys, contacts, collectors, responses, and rollups, and create surveys, contacts, contact lists, or public weblink collectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time CLI setup executes remote code, and the downloaded installer and exact installed release are outside the inspected artifact.

Mitigation: Review and verify a specific CLI release before allowing setup.

Risk: Startup synchronization may silently install additional agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 unless additional skills are intended.

Risk: The connected account may expose sensitive survey data, and write actions can create SurveyMonkey resources.

Mitigation: Connect only the intended account and retain confirmation of the exact payload and effect before writes.

## Reference(s):

- [SurveyMonkey API documentation](https://api.surveymonkey.com/v3/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs vary; inspect the live connector schema before each call.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
