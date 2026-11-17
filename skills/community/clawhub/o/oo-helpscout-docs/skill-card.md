## Description:

Search and read Help Scout Docs content using the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support and documentation teams use this skill to search and read Help Scout Docs articles, collections, categories, and sites through an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run a downloaded CLI installer without an approval or integrity check; the installer and hosted connector implementation are unverified.

Mitigation: Review and verify the installer, and approve CLI installation separately before running it.

Risk: Automatic agent-skill synchronization settings may affect local skills.

Mitigation: Review and verify the synchronization settings before enabling automatic setup.

Risk: The connected Help Scout account may expose data beyond the intended account context.

Mitigation: Connect only the Help Scout account intended for this work.

## Reference(s):

- [Help Scout](https://www.helpscout.com)
- [Help Scout Docs API documentation](https://developer.helpscout.com/docs-api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON results presented or summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Help Scout Docs content from search, list, and article retrieval actions.]

## Skill Version(s):

1.0.4 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
