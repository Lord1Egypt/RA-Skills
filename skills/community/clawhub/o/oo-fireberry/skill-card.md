## Description:

Use this skill for any Fireberry request—including reading, creating, updating, and deleting data—instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Fireberry through their connected account to read, create, update, delete, and query Fireberry account and contact records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can run an unverified remote installer script.

Mitigation: Review setup before use and install a verified CLI yourself instead of allowing automatic remote-script execution.

Risk: The connected account gives the skill access to Fireberry data, including actions that create, update, or delete records.

Mitigation: Connect only the permissions needed and approve the exact payload and target before writes or deletions.

## Reference(s):

- [Fireberry REST API documentation](https://developers.fireberry.com/reference/getting-started-with-rest-api)
- [Fireberry](https://www.fireberry.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text summaries, shell commands, and JSON record data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Fireberry account or contact data and proposed record changes.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
