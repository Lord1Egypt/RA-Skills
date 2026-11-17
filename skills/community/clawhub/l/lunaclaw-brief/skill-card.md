## Description:

Ai Cv Weekly is a pluggable AI report engine that generates multi-source technology, finance, and stock briefings with scoring, deduplication, LLM editing, rendering, scheduling, and delivery support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx9826](https://clawhub.ai/user/llx9826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate recurring AI/CV, financial, and market briefings from configured data sources, optionally routing user hints to a suitable preset and delivering the resulting report by email or webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manipulated source material or user hints may be reflected in generated HTML reports.

Mitigation: Use trusted sources and avoid opening or forwarding generated HTML from untrusted material until HTML escaping and sanitization are fixed.

Risk: Custom preset creation can influence YAML files written by the skill.

Mitigation: Avoid custom preset creation until preset names are strictly validated, and review generated preset YAML before reuse.

Risk: Reports, user hints, and summaries may be sent to configured LLM, SMTP, or webhook services.

Mitigation: Use only trusted LLM and delivery configurations, and avoid submitting confidential material unless those services are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx9826/skills/lunaclaw-brief)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, PDF, Configuration]

**Output Format:** [Generated report files plus JSON-compatible paths and issue metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally send generated HTML reports through configured SMTP email or webhook channels.]

## Skill Version(s):

4.0.0 (source: evidence.release.version, target metadata, artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
