## Description:

Automates DOI extraction and academic library download workflows for books and articles using institutional access when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and run academic download workflows, extract DOIs, and preserve citation metadata for materials they are authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for institutional credentials and supports bulk academic access without enough safety boundaries or disclosure.

Mitigation: Use only accounts and materials the operator is authorized to access, follow applicable institutional and publisher terms, and review each automated workflow before running it.

Risk: Library credentials may be exposed through shell history or shared execution environments.

Mitigation: Use secure secret handling, avoid typing credentials directly into shared shells, and remove credentials from the environment after use.

Risk: The Playwright/Node helper and unpinned dependency ranges increase review and supply-chain risk before automated downloads are trusted.

Mitigation: Review the helper script, pin dependency versions, and run the downloader in an isolated environment before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-anne-library)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded files and metadata in a local output directory when run with authorized access.]

## Skill Version(s):

1.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
