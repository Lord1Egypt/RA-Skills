## Description:

ModelSpy helps agents verify OpenAI-compatible endpoints by using behavioral probes to infer the underlying model and report ranked candidates with confidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3378925604-a11y](https://clawhub.ai/user/3378925604-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether API proxies, reseller endpoints, or OpenAI-compatible services appear to be serving the model they claim. It guides endpoint probing, confidence-based interpretation, and follow-up checks when evidence is inconclusive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a downloaded executable while supplying an API key.

Mitigation: Use a dedicated low-limit test key, prefer environment-variable or safer secret passing when available, and verify the executable through checksums or signatures before running it.

Risk: Proxy mirrors or untrusted download paths can expose users to tampered binaries.

Mitigation: Prefer trusted release sources and avoid proxy mirrors unless the user explicitly trusts the mirror.

Risk: Model identity results are probabilistic and may be inconclusive when confidence is low or candidates are close.

Mitigation: Treat low-confidence or close-ranked results as insufficient evidence, run multiple probe rounds, and avoid making binary claims from a single run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3378925604-a11y/skills/modelspy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON or HTML reports from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an endpoint base URL, model name, and API key; supports confidence-ranked results and consistency verdicts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
