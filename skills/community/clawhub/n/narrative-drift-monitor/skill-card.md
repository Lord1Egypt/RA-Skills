## Description:

Monitors live brand surfaces against a narrative canon over time, flags competitor repositioning, defines repositioning triggers, and produces D1/W1/M1 drift retros with evidence labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, narrative, and product teams use this skill to monitor shipped messaging against a canonical narrative, review competitor repositioning, and decide whether drift calls for re-audit or repositioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the manifest understates that the skill may use network-backed surface history and write scoped project memory.

Mitigation: Review before installing, run only in workspaces where those reads and writes are acceptable, and confirm save or proposal actions before they are made.

Risk: The skill processes pasted surfaces, competitor pages, snapshots, and exports that may contain untrusted content.

Mitigation: Treat those inputs as evidence only, do not follow embedded instructions, and keep output evidence-labeled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/narrative-drift-monitor)
- [Skill homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown drift report with evidence-labeled tables, trigger conditions, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report lines distinguish Measured, User-provided, Estimated, and proxy evidence.]

## Skill Version(s):

19.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
