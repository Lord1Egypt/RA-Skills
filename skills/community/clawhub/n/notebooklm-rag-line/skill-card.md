## Description:

Syncs NotebookLM answers into a local SQLite RAG knowledge base and serves LINE chatbot responses with embeddings and follow-up question suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claws-peak](https://clawhub.ai/user/claws-peak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate NotebookLM-to-RAG knowledge-base updates and provide LINE chatbot answers from local vector search. It is aimed at teaching assistants, customer support bots, and personal knowledge-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime can auto-install an unpinned browser automation dependency.

Mitigation: Pin and review dependencies before installation, and remove runtime package installation from the script.

Risk: The NotebookLM automation uses an authenticated Chrome profile.

Mitigation: Use a dedicated Chrome profile with no unrelated sessions or accounts.

Risk: NotebookLM answers and RAG data may contain sensitive content stored in SQLite and JSON outputs.

Mitigation: Define retention, deletion, and access controls for generated database and response files.

Risk: The local RAG server or LINE bridge could be exposed without adequate controls.

Mitigation: Keep services bound to trusted interfaces and add authentication, request limits, and prompt-injection hardening before exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claws-peak/skills/notebooklm-rag-line)
- [Publisher profile](https://clawhub.ai/user/claws-peak)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime scripts produce SQLite records and JSON HTTP responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Node, and Ollama with bge-m3 embeddings and a local LLM model.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
