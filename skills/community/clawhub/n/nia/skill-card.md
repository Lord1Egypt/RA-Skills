## Description:

Index and search code repositories, documentation, research papers, HuggingFace datasets, local folders, and packages with Nia AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arlanrakh](https://clawhub.ai/user/arlanrakh)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use Nia to index, search, and retrieve grounded context from repositories, documentation, papers, datasets, local folders, package sources, and saved contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local folder indexing can upload broad local code and text files to Nia.

Mitigation: Review folder contents before indexing and exclude secrets, credentials, private keys, generated artifacts, and unrelated files.

Risk: Database import and preview commands can send connection details and selected database content to Nia.

Mitigation: Use read-only, short-lived database credentials and restrict queries to the minimum rows and columns needed.

Risk: The guided setup path uses an unpinned `npx ...@latest` command.

Mitigation: Prefer a pinned or otherwise verified setup package before installing or running setup tooling.

Risk: The Nia API key is read from `~/.config/nia/api_key`.

Mitigation: Set restrictive file permissions for the API key file and rotate the key if it may have been exposed.

## Reference(s):

- [Nia homepage](https://trynia.ai)
- [Nia documentation](https://docs.trynia.ai/)
- [ClawHub Nia skill page](https://clawhub.ai/arlanrakh/skills/nia)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include retrieved source snippets, search results, research summaries, dependency analysis, and code-advisor responses from Nia.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
