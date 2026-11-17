## Description:

Distill OpenClaw daily memory, session transcripts, and newly generated report files into new knowledge points and deeper knowledge leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to distill local memory files, session logs, daily notes, summaries, and generated reports into evidence-backed knowledge points and leads for further study.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local memory, session logs, notes, and reports, and may surface sensitive conclusions in its generated Markdown output.

Mitigation: Install only when that local access is acceptable, and review the generated Markdown file before reusing or sharing it.

## Reference(s):

- [Output Templates](references/output-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/knowledge-distillation)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Shell commands]

**Output Format:** [Dated Markdown file with structured sections for input summary, new knowledge points, knowledge leads, and distillation conclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script creates a draft that the agent completes from reviewed local source material.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, clawhub.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
