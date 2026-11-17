## Description:

Lobstr scores startup ideas with competitor discovery, six-dimension VC-style feedback, and GRID investor signal, using runlobstr.com by default and optional BYOK integrations for local scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, product teams, and agents use Lobstr to evaluate whether a startup idea is worth building, including competitive landscape, investor signal, scoring, and a build/not-yet verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Startup ideas are sent to runlobstr.com by default and may include sensitive business details.

Mitigation: Do not submit confidential plans, trade secrets, customer data, or regulated information unless the user accepts the hosted service and its data practices.

Risk: --public and --moltbook can publish or post the idea and score externally.

Mitigation: Use sharing flags only when the user explicitly intends public or external sharing.

Risk: RUNLOBSTR_API can redirect default hosted submissions if set in the environment.

Mitigation: Check or unset RUNLOBSTR_API before use in managed environments.

## Reference(s):

- [ClawHub Lobstr skill page](https://clawhub.ai/rednix/skills/lobstr)
- [runlobstr.com](https://runlobstr.com)
- [GRID investor database](https://grid.nma.vc)
- [NMA](https://nma.vc)
- [Exa Search API Reference](references/exa-search.md)
- [Exa Search API endpoint](https://api.exa.ai/search)
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain-text score card by default; JSON object with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output includes a six-dimension score, competitor list, GRID investor signal, and build/not-yet verdict; --public and --moltbook can share externally.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
