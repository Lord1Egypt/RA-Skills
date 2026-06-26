## Description: <br>
Personal Development System is a unified self-improvement and productivity operating system that helps an agent support goals, projects, tasks, reviews, energy management, habit building, systems thinking, and project breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starsbottle](https://clawhub.ai/user/starsbottle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to maintain a local plaintext productivity system for planning, prioritization, habits, reviews, overload resets, and task breakdown. The skill is intended for personal productivity workflows stored under ~/productivity/ after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can maintain local plaintext productivity notes that may contain preferences, priorities, commitments, and work-style details. <br>
Mitigation: Create or update ~/productivity/ content only after explicit user confirmation, and avoid storing sensitive information unless the user deliberately chooses to save it. <br>
Risk: Setup or migration may restructure existing productivity notes. <br>
Mitigation: Review exact ~/productivity/ paths first, back up existing notes, preserve legacy files during migration, and delete old folders only after the user verifies the migrated content. <br>
Risk: Burnout and energy-management material could be mistaken for medical or mental-health care. <br>
Mitigation: Present burnout material as self-help productivity guidance and direct users to qualified professional support for medical or mental-health concerns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/starsbottle/pd) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Productivity System Template](artifact/system-template.md) <br>
- [Migration Guide](artifact/migration.md) <br>
- [Feel-Good Productivity Framework](artifact/feel-good-framework.md) <br>
- [Habit System](artifact/habits.md) <br>
- [Burnout Prevention Guide](artifact/burnout-prevention.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance, planning structures, local plaintext Markdown notes, and routing snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local ~/productivity/ files only after explicit user confirmation; no external network requests are described.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and target metadata; artifact frontmatter reports 2.7.0 and artifact local metadata reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
