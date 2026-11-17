## Description:

Learn Graph helps an agent guide users through systematic learning of a new field by collaboratively mapping concepts, uses, prerequisite relationships, high-value nodes, accessible entry points, and a goal-sized learning path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-evan](https://clawhub.ai/user/li-evan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and learning-focused agents use this skill when someone wants to understand a new field, choose where to start, plan a systematic learning path, or decide what level of coverage is enough for a specific goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce less useful output when it continues in Chinese for a user expecting another language.

Mitigation: Have the agent adapt responses to the user's language preference while preserving the knowledge-graph learning workflow.

Risk: Learning paths can be misleading if the agent assumes the user already knows prerequisite concepts.

Mitigation: Ask the user to confirm uncertain prior knowledge before treating it as known, and adjust the concept map accordingly.

## Reference(s):

- [ClawHub Learn Graph skill page](https://clawhub.ai/li-evan/skills/learn-graph)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or conversational text with concept maps, learning paths, questions, and prerequisite guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, shell commands, API calls, or file outputs are requested by the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
