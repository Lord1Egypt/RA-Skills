## Description:

Get the current Swatch Internet Time in beats (@000-@999) when users ask for Internet time, Swatch beats, beat time, /beats, or Swatch time conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kens-agents](https://clawhub.ai/user/kens-agents)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and power users use this skill through ClawHub or OpenClaw to get the current Swatch Internet Time or translate timestamps and locations into beat time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as '@ time' or 'current beats' may invoke the skill unexpectedly in ordinary chat.

Mitigation: Review trigger configuration before deployment and narrow or disable ambiguous phrases in environments where accidental invocation would be disruptive.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/kens-agents/skills/internet-time)
- [Project Homepage](https://github.com/swatchtime)
- [Swatch Internet Time](https://www.swatch.com/en-us/internet-time)
- [Reference Implementation](https://github.com/swatchtime/sample-code/blob/main/python/get_swatch_time.py)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Markdown-formatted bold Swatch Internet Time string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zero-padded @000-@999 beat value only.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
