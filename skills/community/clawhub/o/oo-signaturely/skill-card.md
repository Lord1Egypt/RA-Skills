## Description:

Manage Signaturely folders by listing, retrieving, creating, and renaming them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can manage Signaturely folders by listing folders, retrieving folder details, creating folders, or renaming them through a connected account. Folder creation and renaming change account data and require confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changing third-party installer code; the supplied evidence does not verify the downloaded installer or exact CLI release.

Mitigation: Review setup instructions, install a reviewed version-verified CLI yourself, and decide whether its automatic bundled-skill synchronization is acceptable before setup.

Risk: Connecting Signaturely entrusts authenticated connector requests and account credentials to OOMOL.

Mitigation: Connect only an account you intend to use and review the connection before authorizing it.

Risk: Creating or renaming folders changes Signaturely account data.

Mitigation: Keep the required confirmation step and review the exact action and payload before running it.

## Reference(s):

- [Signaturely](https://signaturely.com/)
- [Signaturely API documentation](https://docs.signaturely.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text]

**Output Format:** [Structured connector requests and responses with brief explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Folder creation and rename operations require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
