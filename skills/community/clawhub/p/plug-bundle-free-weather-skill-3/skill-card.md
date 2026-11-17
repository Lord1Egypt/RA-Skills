## Description:

free-weath组合包 is a ClawHub plug bundle that combines four Lifestyle skills for weather lookup, game-building, text-game processing, and Apple Health-related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this bundle to coordinate several lifestyle-oriented skills into a single workflow that can collect weather information, help build games, process text-game content, and synchronize or handle health data. It is intended to reduce fragmented personal workflow management by routing work through the bundled skills and combining their outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the bundle combines broad read, write, and execute authority with vague scoping.

Mitigation: Install only after reviewing the requested permissions, and prefer separate narrowly scoped skills unless the publisher clarifies command and file boundaries.

Risk: The bundle may handle health data and API credentials.

Mitigation: Avoid sharing sensitive health data or credentials unless the workflow, storage behavior, and consent boundaries are clear and acceptable.

Risk: Bundled skills can combine outputs from multiple sources, which may make errors or unsafe actions harder to isolate.

Mitigation: Review generated commands, files, and recommendations before execution or deployment, especially when they affect local files or external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-free-weather-skill-3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, code snippets, and structured outputs such as JSON or CSV when supported by the underlying skills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require file access, command execution, API credentials, and user-provided weather, game, text, or health data depending on the bundled workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
