## Description:

Reference tool for blockchain and crypto that covers introductory concepts, formulas, regulations, risks, instruments, strategies, glossary terms, and due diligence checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and blockchain practitioners use this skill to retrieve concise launchpad reference material and checklists for blockchain workflows. Reviewers should account for the bundled nested skill that can maintain a local launchpad datastore.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a nested skill with persistent local data operations that are not described by the top-level reference-tool summary.

Mitigation: Review the package before installation and remove or clearly document the nested skill if local datastore behavior is intended.

Risk: The nested skill can delete and export locally stored Launchpad entries.

Mitigation: Run it only in an appropriate workspace, review configured data paths, and avoid storing sensitive information in the Launchpad datastore.

Risk: Reference content about blockchain, regulation, and risk can be generic or incomplete.

Mitigation: Treat the output as a quick reference and verify regulatory, financial, or security decisions against authoritative sources.

## Reference(s):

- [Launchpad Skill Page](https://clawhub.ai/ckchzh/skills/launchpad)
- [Publisher Profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown reference content from shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top-level commands emit reference documentation; the bundled nested skill can also create, delete, configure, and export local files under the configured Launchpad data directory.]

## Skill Version(s):

2.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
