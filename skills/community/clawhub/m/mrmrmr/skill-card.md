## Description: <br>
LLM-powered automated Mendelian Randomization for causal discovery in biomedical research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rqth123](https://clawhub.ai/user/rqth123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Biomedical researchers and clinicians use this skill to discover or validate exposure-outcome causal relationships with Mendelian randomization, PubMed literature review, OpenGWAS data selection, and LLM-written interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run generated R code and Python eval on model, API, or CSV-derived data. <br>
Mitigation: Run only with trusted inputs in a constrained workspace; prefer a reviewed version that replaces eval with safe parsing and invokes fixed R scripts with argument lists. <br>
Risk: Weak validation of GWAS IDs, paths, and generated analysis inputs can affect biomedical analysis results or file writes. <br>
Mitigation: Validate GWAS IDs and paths before execution, use an isolated output directory, and review intermediate CSV files and reports before relying on conclusions. <br>
Risk: The Streamlit demo can expose analysis execution paths to untrusted users if deployed publicly. <br>
Mitigation: Do not expose the demo to untrusted users; keep it local or behind access controls with non-sensitive API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rqth123/mrmrmr) <br>
- [MRAgent README](artifact/mrmrmr/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [MRAgent paper](https://doi.org/10.1093/bib/bbaf140) <br>
- [MRAgent PyPI package](https://pypi.org/project/mragent/) <br>
- [MRAgent Zenodo artifacts](https://doi.org/10.5281/zenodo.14184396) <br>
- [MRAgent web demo](https://huggingface.co/spaces/xuwei1997/MRAgent) <br>
- [OpenGWAS API](https://api.opengwas.io/) <br>
- [STROBE-MR](https://www.strobe-mr.org/) <br>
- [MRlap](https://github.com/n-mounier/MRlap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, PDF reports, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output includes a JSON summary, CSV intermediates, plots, and PDF reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, Rscript, OPENAI_API_KEY, and optionally OPENGWAS_JWT; outputs are written under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
