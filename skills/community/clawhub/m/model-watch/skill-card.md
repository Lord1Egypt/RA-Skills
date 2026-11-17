## Description:

Benchmark AI API models over time and detect quality degradation with standardized reasoning, coding, writing, instruction-following, and hallucination checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run repeatable benchmark prompts against AI API model outputs, store score history locally, and identify potential quality regressions over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented GitHub default-branch install command can fetch code that differs from the reviewed release artifact.

Mitigation: Install from a pinned commit, signed release, or reviewed package artifact before operational use.

Risk: Submitted model outputs are saved locally in ~/.hermes/model-watch-history.json.

Mitigation: Avoid submitting sensitive prompts, responses, customer data, credentials, or other confidential content.

Risk: Benchmark scores use simple keyword and length heuristics, so results can be incomplete or misleading for model quality decisions.

Mitigation: Review scored outputs manually and calibrate benchmark prompts and thresholds before relying on alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/model-watch)
- [Project homepage](https://github.com/minirr890112-byte/model-watch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON alert output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores benchmark history locally at ~/.hermes/model-watch-history.json.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.2.0 and pyproject.toml lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
