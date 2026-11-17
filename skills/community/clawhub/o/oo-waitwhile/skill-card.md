## Description:

Waitwhile (waitwhile.com). Use this skill for ANY Waitwhile request — reading, creating, updating, and deleting data. Whenever a task involves Waitwhile, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read, search, create, update, and delete Waitwhile customer records, or list accessible locations, through their connected Waitwhile account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI installer code that has not been inspected.

Mitigation: Review and verify the CLI installer before allowing setup.

Risk: The documented startup synchronization can install additional agent skills.

Mitigation: Disable skill synchronization before first use if it is unwanted, using OO_SKILLS_SYNC_DISABLED as described in the publisher documentation.

Risk: Customer updates and deletions can change or remove Waitwhile records.

Mitigation: Require approval for customer changes and deletions, including confirmation of the exact target and effect.

## Reference(s):

- [Waitwhile API documentation](https://developers.waitwhile.com/docs/getting-started-with-the-waitwhile-api)
- [Waitwhile homepage](https://waitwhile.com)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [Structured JSON responses and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain customer or location records; write actions can change or delete customer data.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
