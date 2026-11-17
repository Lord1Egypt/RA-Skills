## Description:

Manage projects, grants, milestones, updates, payouts, and invoices on the Karma protocol through the Karma REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheshmurthy](https://clawhub.ai/user/maheshmurthy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and update Karma projects, grants, milestones, project updates, endorsements, and team members, and to check payout status and invoice information through authenticated Karma API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Karma API key to a configurable endpoint if KARMA_API_URL is changed.

Mitigation: Keep KARMA_API_URL unset unless intentionally using a trusted Karma endpoint, and use a narrowly scoped Karma API key.

Risk: The skill can alter remote Karma project, grant, milestone, update, endorsement, and member records through authenticated actions.

Mitigation: Confirm requested record changes with the user before execution and review API responses for the affected project, grant, network, and reference.

Risk: Broad trigger wording may route payout, invoice, or project-management requests into authenticated API workflows.

Mitigation: Install only when the agent is expected to manage Karma records, and verify the intended action before sending authenticated requests.

## Reference(s):

- [Karma API Documentation](https://gapapi.karmahq.xyz/v2/docs/static/index.html)
- [ClawHub Skill Page](https://clawhub.ai/maheshmurthy/skills/karma-project-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated Karma API calls and asks the user to confirm project, grant, and milestone changes before execution.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
