## Description:

Scans ClawHub skills before installation to detect malicious code, obfuscated payloads, and social engineering using pattern matching, deobfuscation, and optional LLM intent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sypsyp97](https://clawhub.ai/user/sypsyp97)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit ClawHub skills before installation or after local installation. It reports suspicious patterns, decoded payload indicators, and manual LLM-review prompts for questionable code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is heuristic and can miss unsupported file types or novel attack patterns, which may make safe results look stronger than they are.

Mitigation: Treat scan results as triage, manually review unsupported files and suspicious reports, and do not rely on the tool as a complete security verifier.

Risk: Suspicious code excerpts may be copied to /tmp for manual LLM review, exposing private or proprietary skill content on the local system.

Mitigation: Avoid running the skill on private or proprietary skills until the temporary export behavior is fixed, and delete retained suspicious-code report files after review.

## Reference(s):

- [341 Malicious ClawHub Skills Incident](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security)
- [ClawHub Skill Page](https://clawhub.ai/sypsyp97/skills/openclaw-skill-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text report with shell command examples and manual review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write suspicious-code excerpts to /tmp for manual LLM review when suspicious content is found.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
