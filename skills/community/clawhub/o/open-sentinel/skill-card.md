## Description:

Transparent LLM proxy that monitors and enforces policies on AI agent behavior, evaluating responses against configurable rules for hallucinations, PII leaks, prompt injection, and workflow violations before they reach users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sentinel199](https://clawhub.ai/user/sentinel199)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to install, configure, and run Open Sentinel as an OpenAI-compatible proxy that evaluates LLM responses against policy rules before use in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install an external package and configure provider API keys.

Mitigation: Use a pinned and verified opensentinel package, install it in an isolated environment, and use limited-scope provider keys.

Risk: The default asynchronous judge may not prevent sensitive content, payment actions, or irreversible automated actions before downstream use.

Mitigation: Do not rely on the default async judge as the sole preventive control for high-stakes workflows; configure critical blocking paths and keep human approval for irreversible actions.

Risk: The artifact describes fail-open hook behavior, so policy evaluation failures or timeouts can allow requests to pass through.

Mitigation: Test policies under failure and timeout conditions, monitor traces, and add independent safeguards before routing regulated or highly sensitive traffic through the proxy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sentinel199/skills/open-sentinel)
- [Open Sentinel Homepage](https://github.com/open-sentinel/open-sentinel)
- [Open Sentinel Docs](https://github.com/open-sentinel/open-sentinel/tree/main/docs)
- [Open Sentinel PyPI Package](https://pypi.org/project/opensentinel)
- [Open Sentinel Issues](https://github.com/open-sentinel/open-sentinel/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter reports 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
