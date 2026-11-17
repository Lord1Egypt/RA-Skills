## Description:

Run LangChain AI pipelines locally and offline with Ollama and phi4-mini for coding, DevOps, chat, and document-grounded queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manojrammurthy](https://clawhub.ai/user/manojrammurthy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local LangChain and Ollama workflows for code generation, shell command guidance, chat, and document-grounded Q&A without cloud API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies globally or with elevated privileges can broaden the impact of dependency or packaging issues.

Mitigation: Install the skill in a controlled virtual environment and avoid running pip with elevated privileges.

Risk: Offline and privacy behavior depends on the local Ollama configuration and the model endpoint used.

Mitigation: Verify that Ollama is configured to use only local models and local endpoints before processing sensitive prompts or documents.

Risk: Unpinned LangChain and Ollama package versions can reduce reproducibility and supply-chain control.

Mitigation: Pin and review dependency versions before deploying the skill in a managed or production environment.

Risk: The documentation advertises a rag mode, but the interactive mode configuration does not list rag as a selectable mode.

Mitigation: Review mode configuration before relying on document-grounded Q&A workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manojrammurthy/skills/openclaw-skill-langchain-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text streamed from a local CLI, including code blocks or shell commands when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode selects coding, devops, chat, or rag; the local model defaults to phi4-mini.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
