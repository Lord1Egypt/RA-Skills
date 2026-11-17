## Description:

Adds new language translations to customer service knowledge base templates, syncs them to Feishu Wiki, and creates a GitHub issue to document the change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operations teams use this skill to add translated customer-service KB templates, propagate updates to Feishu Wiki, and document the change through a GitHub issue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials for Feishu and GitHub could be exposed or over-permissioned.

Mitigation: Keep credentials in environment variables or a secret manager, and prefer fine-grained GitHub tokens limited to issue creation.

Risk: The workflow can change external systems and local repository state.

Mitigation: Require preview and confirmation before Feishu updates, GitHub issue creation, document deletion or recreation, and git commits.

Risk: Translated KB content may introduce inaccurate or locale-inappropriate customer-service guidance.

Mitigation: Review translated text for tone, locale conventions, placeholders, links, and formatting before syncing or committing.

## Reference(s):

- [Feishu Wiki API Reference](references/feishu-api.md)
- [ClawHub release page](https://clawhub.ai/terrycarter1985/skills/multilingual-kb-update)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit local KB markdown, call Feishu and GitHub APIs, and create a local git commit when credentials and confirmation are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
