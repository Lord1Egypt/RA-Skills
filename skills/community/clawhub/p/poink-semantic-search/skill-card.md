## Description:

Builds and queries local document knowledge bases with semantic and hybrid search across PDF, Markdown, TXT, DOCX, ODT, and FODT files using the poink CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szemroda](https://clawhub.ai/user/szemroda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search, ingest, organize, and inspect local document collections with the poink CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses poink-cli to process local documents, so broad indexing paths may include sensitive folders.

Mitigation: Review target paths before indexing and avoid sensitive folders unless that is explicit intent.

Risk: Installing an external CLI package can introduce supply-chain drift in controlled environments.

Mitigation: Review or pin the poink-cli package version where reproducibility or change control is required.

## Reference(s):

- [Poink Repository](https://github.com/szemroda/poink)
- [Poink README](https://github.com/szemroda/poink#readme)
- [ClawHub Skill Page](https://clawhub.ai/szemroda/skills/poink-semantic-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of the poink CLI, including JSON output for non-interactive agent execution and text output for user-facing commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
