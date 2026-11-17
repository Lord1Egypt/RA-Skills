## Description:

Automate construction data processing using LLM (ChatGPT, Claude, LLaMA) to generate Python/Pandas scripts, extract data from documents, and create automated pipelines without deep programming knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction professionals, data analysts, and developers use this skill to turn project data, PDFs, BIM exports, cost estimates, and schedule files into structured analysis workflows using LLM-assisted Python/Pandas code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes a remote installer pattern that can execute mutable code on the user's machine.

Mitigation: Use official platform-specific Ollama installation steps, verify downloads, and avoid running `curl ... | sh` as written.

Risk: Construction, customer, cost, contract, or schedule data may be sensitive if submitted to online LLM services.

Mitigation: Use organization-approved tools and prefer local LLM workflows for confidential data.

Risk: Generated Python/Pandas code or analysis may be incorrect for a given project dataset.

Mitigation: Validate inputs and generated code before execution, review outputs against source data, and work on copies of important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/llm-data-automation)
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction)
- [DataDrivenConstruction homepage](https://datadrivenconstruction.io)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [Ollama](https://ollama.com)
- [LM Studio](https://lmstudio.ai)
- [Google Colab](https://colab.research.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured tables, Python code blocks, shell command snippets, and export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May offer Excel, CSV, or JSON export options when relevant.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
