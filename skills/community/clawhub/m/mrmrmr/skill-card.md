## Description:

mrmrmr provides an LLM-powered automated Mendelian randomization workflow for causal discovery and causal validation in biomedical research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rqth123](https://clawhub.ai/user/rqth123)

### License/Terms of Use:

Apache 2.0

## Use Case:

Biomedical researchers, clinicians, and developers use this skill to run knowledge discovery from a disease or validate a specified exposure-outcome hypothesis with Mendelian randomization, GWAS data selection, sensitivity checks, and generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and biomedical query terms may be exposed through unsafe handling or external services.

Mitigation: Install and run in an isolated research environment, use disposable or scoped API tokens, avoid sensitive inputs, and confirm any configured OpenAI-compatible base URL before use.

Risk: The workflow can execute Python and R analysis code and may install or call external dependencies.

Mitigation: Review commands and dependency installation paths before execution, avoid curl-to-sh installers, and run with least privilege in a disposable environment.

Risk: LLM-derived biomedical interpretations and editable intermediate CSV files can produce misleading causal claims.

Mitigation: Require domain expert review of CSV intermediates, GWAS selections, MR assumptions, sensitivity checks, and generated reports before using results for decisions.

Risk: Disease, exposure, outcome, and analysis result data may be sent to external LLM or biomedical data services.

Mitigation: Use non-sensitive inputs, document data flow for users, disable synonym expansion when appropriate, or use a local LLM provider where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rqth123/skills/mrmrmr)
- [MRAgent paper](https://doi.org/10.1093/bib/bbaf140)
- [Zenodo experiment files](https://doi.org/10.5281/zenodo.14184396)
- [PyPI package](https://pypi.org/project/mragent/)
- [Hugging Face web demo](https://huggingface.co/spaces/xuwei1997/MRAgent)
- [OpenGWAS API](https://api.opengwas.io/)
- [STROBE-MR](https://www.strobe-mr.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result summaries; generated analysis artifacts include CSV tables and PDF reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Rscript, OPENAI_API_KEY, and optionally OPENGWAS_JWT; may use external LLM and biomedical data services.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; package version 0.2.5 in artifact frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
