## Description:

Calculate MACD from price data. Use when computing MACD/signal/histogram from a price series, spotting crossovers, reading momentum, or planning MACD-based entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to compute MACD, signal line, histogram, and EMA values from supplied price data. It also provides educational momentum, crossover, histogram, and strategy guidance for interpreting MACD outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV filename handling in calculate-file can allow local code execution when filenames or paths come from untrusted sources.

Mitigation: Review and fix filename handling before using calculate-file with external or untrusted paths; use only trusted local files until then.

Risk: The skill provides direct trading actions without a risk disclosure.

Mitigation: Use outputs as educational technical-analysis guidance only, not financial advice; require human review before acting on trading suggestions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/macd)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal output with tabular numeric values and explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash 4+ and python3 standard library; calculation commands require enough price observations for the selected slow and signal periods.]

## Skill Version(s):

2.0.4 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
