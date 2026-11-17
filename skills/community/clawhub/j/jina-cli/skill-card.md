## Description:

Reads web content and searches the web using Jina AI Reader API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read URLs, extract web pages or social media posts into LLM-friendly content, run web searches, and configure Jina CLI output behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-line install command pipes a remote installer directly into a shell.

Mitigation: Download and inspect the installer first, or use a pinned and verified release before installing.

Risk: Cookie forwarding can expose session credentials or private browsing context to the service path.

Mitigation: Do not pass real session cookies, confidential documents, internal URLs, or regulated data unless the service path is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackfeng0614-prog/skills/jina-cli)
- [Install script referenced by the skill](https://raw.githubusercontent.com/geekjourneyx/jina-cli/main/scripts/install.sh)
- [Jina Reader API endpoint](https://r.jina.ai/)
- [Jina Search API endpoint](https://s.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples; command results may be JSON, Markdown, plain text, HTML, or screenshot URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can batch process URL lists and save extracted content to files when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
