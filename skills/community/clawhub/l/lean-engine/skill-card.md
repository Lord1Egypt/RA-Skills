## Description:

Run QuantConnect LEAN backtests and manage US equity algorithm development, including algorithm setup, data preparation, configuration, result review, and Interactive Brokers-oriented deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative engineers use this skill to prepare and run LEAN algorithmic trading backtests, manage US equity data, edit backtest configuration, inspect results, and plan Interactive Brokers deployment settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can touch LEAN trading configuration that may contain sensitive broker settings or credentials.

Mitigation: Use it in an isolated project or VM, avoid live broker configs with Interactive Brokers credentials, keep a minimal backtest-only config, and back up LEAN config files before using helper scripts.

Risk: Setup and data workflows may download dependencies or market data from external sources.

Mitigation: Prefer pinned dependencies, review downloaded packages and data sources, and avoid elevated privileges during setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cylqqqcyl/skills/lean-engine)
- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- [Data download reference](references/data-download.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples; helper scripts produce LEAN configuration and data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires dotnet, Python, LEAN_ROOT, DOTNET_ROOT, and PYTHONNET_PYDLL; network access may be used for dependency and market data downloads.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
