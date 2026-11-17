## Description:

Habit Coach acts as an AI accountability partner that helps users build, track, and sustain habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record daily habit check-ins, review habit progress and streaks, and draft new habit-building plans with accountability-oriented guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit entries are saved locally and may contain personal routine or health-related details.

Mitigation: Avoid entering highly sensitive personal or health information unless local JSON storage is acceptable.

Risk: The documentation asks users to install requests even though the current script does not need it.

Mitigation: Skip the dependency installation unless a future version of the script actually imports and requires requests.

## Reference(s):

- [Habit Coach Guide](references/habit_coach_guide.md)
- [Atomic Habits framework](https://jamesclear.com/atomic-habits)
- [awesome-openclaw-usecases Habit Tracker](https://github.com/hesamsheikh/awesome-openclaw-usecases)
- [Reddit AI habit tracker discussion](https://www.reddit.com/r/productivity/comments/ai_habit_tracker/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command use may write habit records to a local JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
