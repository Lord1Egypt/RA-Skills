## Description:

Accesses and analyzes Hevy fitness tracking data, including workouts, routines, and exercise templates, through command-line guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nsampre](https://clawhub.ai/user/nsampre)

### License/Terms of Use:


## Use Case:

Agents and users with Hevy Pro use this skill to retrieve, export, and analyze workouts, routines, and exercise templates through hevycli commands. The skill supports read-only fitness data workflows such as workout history review, JSON export, and progress analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide access to personal Hevy fitness account data.

Mitigation: Use it only when the user is comfortable granting hevycli access to their Hevy account, and limit retrieved output to the data needed for the task.

Risk: API keys or sensitive request details may be exposed through config display, debug output, chat, logs, or terminal history.

Mitigation: Avoid printing or sharing API keys, use debug output only when necessary, and rotate the Hevy API key if it is exposed.

Risk: Installing an unpinned latest CLI release can change behavior without review.

Mitigation: Prefer a reviewed pinned version when operational consistency matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nsampre/skills/hevycli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, analysis]

**Output Format:** [Markdown guidance with inline shell commands and optional table or JSON CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Hevy account data access; command outputs may include personal fitness data.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
