## Description:

Start every day focused with a morning briefing of overdue tasks, today's priorities, calendar overview, and context from recent meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused operators use this skill to ask an agent for a concise daily or weekly briefing based on local task lists, recent meeting notes, optional calendar context, and optional memory/profile files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may reveal sensitive tasks, meetings, calendar items, or memory/profile context in chat output.

Mitigation: Use explicit briefing commands only when the output audience is appropriate, and disable or remove access to memory, profile, or calendar sources that should not be summarized.

Risk: Broad trigger phrases may produce a briefing when the user did not intend to expose connected work context.

Mitigation: Prefer deliberate commands such as "briefing" or "daily briefing" and avoid invoking the skill while screen sharing unless the audience should see the briefing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-ai-daily-briefing)
- [Creator Homepage](https://jeffjhunter.com)
- [Complete Setup Guide](https://skillboss.co/skill.md)
- [Quick Start](artifact/examples/quick-start.md)
- [Example Output](artifact/examples/output-example.md)
- [Briefing Preferences Template](artifact/assets/PREFERENCES-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown daily briefing with structured sections and optional checklist-style items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single chat response; sections may be skipped when no relevant data exists.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
