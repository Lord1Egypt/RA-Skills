## Description:

Langextract helps agents use Google's LangExtract Python library to extract structured data from unstructured text with source-text offsets, visual review, and Gemini, OpenAI, or Ollama models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to install and apply LangExtract for extracting grounded structured records from clinical, legal, literary, academic, and long-form documents, then save JSONL results and generate HTML visualizations for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes a curl-to-shell Ollama command.

Mitigation: Review the command first and prefer an official verified installer or inspected script before execution.

Risk: Hosted model use and examples involving medical, legal, confidential, or regulated documents can expose sensitive text to external providers.

Mitigation: Use approved providers and privacy terms, avoid sending regulated or confidential documents without authorization, and prefer local models for sensitive workflows.

Risk: API key setup and troubleshooting can reveal credentials if full environment values are printed or logged.

Mitigation: Use environment or secret-management tooling and avoid printing complete API keys in terminals, notebooks, logs, or shared artifacts.

Risk: Saved JSONL and HTML visualization outputs may contain sensitive source text and extracted entities.

Mitigation: Treat generated output files as sensitive, restrict access, and remove or encrypt them according to the data handling policy for the source documents.

Risk: Unpinned package upgrades and model choices can reduce reproducibility.

Mitigation: Use a virtual environment and pin package and model versions when repeatable extraction behavior is required.

## Reference(s):

- [LangExtract GitHub Repository](https://github.com/google/langextract)
- [LangExtract PyPI Project](https://pypi.org/project/langextract/)
- [LangExtract Paper DOI](https://doi.org/10.5281/zenodo.17015089)
- [LangExtract Examples](https://github.com/google/langextract/tree/main/examples)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with bash and Python code blocks; generated project outputs may include JSONL and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call hosted or local LLM providers and write extraction artifacts that can contain source document content.]

## Skill Version(s):

0.1.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
