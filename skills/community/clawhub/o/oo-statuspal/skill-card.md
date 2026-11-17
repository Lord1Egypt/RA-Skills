## Description:

Search and read StatusPal status pages, services, and incidents through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to retrieve current status page information, configured services, and incident details from a connected StatusPal account. An agent can summarize this data to answer StatusPal questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions can run a remote CLI installer without prior approval; the external installer and connector implementation were unavailable for verification.

Mitigation: Review the CLI installer and its automatic skill-installation behavior before installing, and approve local changes explicitly.

Risk: Connecting StatusPal entrusts OOMOL with access to that account.

Mitigation: Confirm that you intend to grant OOMOL access to the StatusPal account before connecting it.

## Reference(s):

- [StatusPal homepage](https://www.statuspal.io)
- [StatusPal API documentation](https://www.statuspal.io/api-docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [StatusPal data returned as JSON and summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
