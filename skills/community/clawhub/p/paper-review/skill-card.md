## Description: <br>
Review academic papers for correctness, quality, and novelty using OpenJudge's multi-stage pipeline, with support for PDF files, LaTeX source packages, and BibTeX verification across 10 disciplines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloml0326](https://clawhub.ai/user/helloml0326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to run OpenJudge's multi-stage academic paper review pipeline for manuscript critique, correctness checks, venue-aware review scoring, and optional reference verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper contents, references, or manuscript metadata may be processed by configured external model and bibliography services. <br>
Mitigation: Use approved providers or endpoints, and do not submit confidential, embargoed, or unpublished manuscripts unless that use is authorized. <br>
Risk: Model API keys and custom endpoints are required for normal operation. <br>
Mitigation: Prefer environment variables or restricted API keys, avoid printing secrets in terminals, and verify custom base URLs before use. <br>
Risk: The skill depends on the OpenJudge and LiteLLM package chain and on the selected provider's behavior. <br>
Mitigation: Install only in trusted environments and review dependency and provider trust requirements before deployment. <br>


## Reference(s): <br>
- [Paper Review Skill Reference](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/helloml0326/paper-review) <br>
- [LiteLLM providers](https://docs.litellm.ai/docs/providers) <br>
- [OpenAI models](https://platform.openai.com/docs/models) <br>
- [Anthropic models](https://docs.anthropic.com/en/docs/about-claude/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review report and BibTeX verification summary, with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include review scores, correctness findings, criticality assessment, safety or format results, and reference verification status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
