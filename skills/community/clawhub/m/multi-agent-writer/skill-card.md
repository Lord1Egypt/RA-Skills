## Description:

Helps agents run a three-stage writing workflow that finds recent topics, drafts articles or social media content, and reviews revisions against scored writing criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonelake](https://clawhub.ai/user/gonelake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate topical articles and social posts, configure LLM-backed writing runs, and inspect JSON or Markdown outputs from its review loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer pulls mutable remote code, installs Python dependencies, and registers into user-level agent skill directories.

Mitigation: Review the repository and installer before use, prefer a pinned commit, and install into a single intended agent environment.

Risk: Prompts and topics may be sent to external search or LLM providers during production writing runs.

Mitigation: Avoid confidential topics or secrets in prompts and use approved providers, credentials, and network settings.

Risk: User-level skill registration and uninstall scripts modify local agent directories and the ~/.skills/multi-agent project path.

Mitigation: Run installation and removal commands from a reviewed checkout and confirm target paths before execution.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/gonelake/skills/multi-agent-writer)
- [Publisher profile](https://clawhub.ai/user/gonelake)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python snippets; generated runs can produce JSON, Markdown, and TSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create output.json, output.md, and experiments.tsv when the installed project is run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
