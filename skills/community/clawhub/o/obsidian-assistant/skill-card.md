## Description:

Obsidian Assistant helps Obsidian users learn and maintain vault habits, answer setup-specific questions, extract reusable templates or macros, and diagnose vault organization issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltryee](https://clawhub.ai/user/ltryee)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users and knowledge workers use this skill to receive personalized vault guidance, generate reusable notes or automation assets, and diagnose organization problems using their recorded vault structure, tags, plugins, and workflow habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a long-lived local profile of the user's Obsidian vault path, folder structure, tags, plugins, workflow habits, and pain points.

Mitigation: Install only when that persistent profiling is acceptable; redact sensitive paths or command output before sharing them, and review or clear references/habit-patterns.md when those details should not be reused.

## Reference(s):

- [README](README.md)
- [Obsidian Concepts Reference](references/obsidian-concepts.md)
- [Habit Patterns Profile](references/habit-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/ltryee/skills/obsidian-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Dataview or Templater code blocks, JSON macro configuration, and file or template recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the local habit profile and template files when new user workflow information is confirmed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
