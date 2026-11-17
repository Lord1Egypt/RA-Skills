## Description:

Executes multi-step deep research with the OpenAI Responses API, including question decomposition, evidence gathering with optional web search, contradiction tracking, and final cited report synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanglechen](https://clawhub.ai/user/guanglechen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to run structured research workflows for complex or high-stakes topics and produce auditable plan, findings, and report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and prompts may be sent to the configured OpenAI-compatible API and, when enabled, web-search providers.

Mitigation: Avoid confidential topics unless those providers are approved; use --disable-web-search for internal-data-only runs and --dry-run for local workflow tests.

Risk: A custom OPENAI_BASE_URL can route requests through an untrusted compatible gateway.

Mitigation: Set OPENAI_BASE_URL only to a trusted endpoint, or omit it to use the default OpenAI client configuration.

Risk: Unpinned SDK dependency resolution can affect reproducibility.

Mitigation: Review or pin the OpenAI SDK dependency before controlled or repeatable deployments.

## Reference(s):

- [Research Quality Rubric](references/research-quality.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON artifacts, raw text logs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a run directory with run_meta.json, plan.json, plan_raw.txt, findings.json, research_raw.json, and report.md; supports dry-run, web-search disablement, model selection, concurrency, and token limits.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
