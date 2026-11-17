## Description:

Dropcontact (dropcontact.com). Use this skill for ANY Dropcontact request — reading, creating, and updating data. Whenever a task involves Dropcontact, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit contacts for Dropcontact enrichment and retrieve enrichment results through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes downloaded CLI installation code, and an installer for additional skills may also be involved.

Mitigation: Review and install the CLI separately before allowing the skill to run.

Risk: Submitted contacts are processed through OOMOL and Dropcontact.

Mitigation: Confirm which contacts will be processed and retain the required approval before submitting them.

## Reference(s):

- [Dropcontact API documentation](https://developer.dropcontact.com/)
- [Dropcontact homepage](https://www.dropcontact.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses may include execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
