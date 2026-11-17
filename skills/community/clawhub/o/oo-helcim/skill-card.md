## Description:

Operate Helcim through an OOMOL-connected account to retrieve, search, create, and update customer records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who use Helcim can retrieve and search customer records, create customers, and update existing records through their OOMOL-connected account. The skill requires confirmation of the exact payload and effect before customer changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill setup can execute downloaded software without separate approval or integrity checks.

Mitigation: Review and approve the CLI installation separately; inspect its bundled-agent-skill installation behavior before allowing setup commands.

Risk: The OOMOL connection mediates access to customer data.

Mitigation: Understand which connected account and customer data are accessible before using the skill.

Risk: Creating or updating a customer changes Helcim data.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [Helcim](https://www.helcim.com/)
- [Helcim API authentication documentation](https://devdocs.helcim.com/docs/authentication-with-the-helcim-api-and-helcimpayjs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer records; create and update actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
