## Description:

Command-line JSON processor. Extract, filter, transform JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a quick reference for installing jq and composing command-line filters to extract, reshape, summarize, and pretty-print JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing jq from an untrusted package or binary source could introduce supply-chain risk.

Mitigation: Install jq through a trusted package manager or from a trusted download source.

Risk: jq filters can expose, transform, or print sensitive JSON fields in command output.

Mitigation: Review jq commands before running them on sensitive JSON and avoid printing secrets or regulated data.

## Reference(s):

- [jq downloads](https://jqlang.org/download/)
- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/jq)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise jq installation, usage, flag, filter, and example guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
