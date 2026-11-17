## Description:

Provides a quick, high-level overview of the market's current state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading teams use this skill for morning preparation, mid-day checks, pre-trade market context, and risk monitoring based on broad market indicators. It produces informational market context and does not provide trade recommendations, stock picks, or predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat market pulse output as financial advice or automated trading guidance.

Mitigation: Present results as informational context only and require human review before any trading or risk decision.

Risk: The README documents scripts/market_pulse.py, but that script was not present in the reviewed package.

Mitigation: Verify the installed artifact includes the expected executable before relying on run instructions.

Risk: Setup instructions use unpinned Python packages.

Mitigation: Install in a virtual environment, avoid sudo or admin installation, and pin dependencies during operational deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/medici-investments-pulse-dv)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Natural-language market pulse summary in Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational market context only; no bundled executable code was present in the release artifact reviewed.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
