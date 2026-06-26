## Description: <br>
Guides an agent to use the LangExtract Python library to extract source-grounded structured data from unstructured text and generate JSONL results and HTML review visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to install and configure LangExtract, design extraction prompts and examples, run structured extraction over text or document URLs, and review source-grounded results. It is aimed at extraction workflows for clinical, legal, academic, news, and long-document analysis where traceability to source text matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive documents may be sent to external model providers during extraction. <br>
Mitigation: Use only approved providers and environments for sensitive data, and prefer local Ollama for private documents. <br>
Risk: API keys may be exposed through environment setup or local .env files. <br>
Mitigation: Store keys in a secret manager or protected environment variables, and keep .env files out of version control. <br>
Risk: Generated JSONL and HTML review files may contain sensitive source text or extracted data. <br>
Mitigation: Review generated files, restrict access, and keep sensitive outputs out of version control. <br>
Risk: The installation guide includes a remote Ollama installer script. <br>
Mitigation: Inspect remote installer scripts or use an organization-approved installation source before running them. <br>


## Reference(s): <br>
- [LangExtract GitHub](https://github.com/google/langextract) <br>
- [LangExtract PyPI](https://pypi.org/project/langextract/) <br>
- [LangExtract paper DOI](https://doi.org/10.5281/zenodo.17015089) <br>
- [Installation guide](guides/01-installation.md) <br>
- [Quickstart guide](guides/02-quickstart.md) <br>
- [Advanced usage guide](guides/03-advanced-usage.md) <br>
- [Troubleshooting guide](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with Python and shell command examples; runtime outputs may include JSONL and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and may use Gemini, OpenAI, or local Ollama model configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
