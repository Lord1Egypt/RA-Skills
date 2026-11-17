## Description:

Two-agent iterative vibe-coding loop for OpenClaw that has one sub-agent build an app or artifact while a second analyst inspects code, previews frontend UI in a browser when applicable, runs small functional checks, and feeds concrete fixes back until the result matches the target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocketship4545-a11y](https://clawhub.ai/user/rocketship4545-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate an iterative generator and analyst workflow for UI-heavy apps, prototypes, landing pages, dashboards, and API-backed frontend work where visual and functional behavior matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may edit project files, install dependencies, start local previews, use browser automation, take screenshots, and run tests.

Mitigation: Review proposed actions and generated changes as with any coding assistant workflow, especially in projects that contain credentials or connect to live services.

Risk: A frontend result may be accepted without adequate visual review if browser inspection cannot be completed or is skipped.

Mitigation: Require the analyst role to preview the app in a browser, capture screenshots when useful, test key interactions, and clearly report any blocker that prevents visual inspection.

Risk: The generator and analyst loop can continue after progress stalls or revisions start regressing accepted work.

Mitigation: Stop the loop when the analyst accepts the result, the user says to stop, a blocker appears, or feedback repeats without meaningful improvement.

## Reference(s):

- [Loop Patterns](references/loop-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/rocketship4545-a11y/skills/match-loop)
- [ClawHub Publisher Profile](https://clawhub.ai/user/rocketship4545-a11y)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with role prompts, feedback packets, command suggestions, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshot paths, preview URLs, test commands, and acceptance status when used in a frontend review loop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
