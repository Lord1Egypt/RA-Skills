## Description:

Probe-first deep research - low-cost snippet reconnaissance before committing to full searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkm123](https://clawhub.ai/user/lkm123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other external users use this skill to run structured web research that probes search snippets first, aligns on a plan, then performs deeper source-backed synthesis. It is suited to research questions where cost control, source quality, confidence labeling, and explicit uncertainty handling matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command and file-editing authority beyond its core research workflow.

Mitigation: Review the skill before installation, run it in a constrained workspace, and remove Bash/Edit permissions when they are not required.

Risk: The skill can persist research-state files during long or multi-agent sessions.

Mitigation: Ask for explicit notice before file writes and verify the target workspace does not contain sensitive or unrelated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkm123/skills/probe-first-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plans, probe findings, source-backed reports, confidence labels, and methodology notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a research-state Markdown file during longer or multi-agent research sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
