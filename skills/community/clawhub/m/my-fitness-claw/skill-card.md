## Description:

My Fitness Claw lets users log meals in natural language, estimate macros and selected micronutrients, persist local nutrition history, and view progress in a browser dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serg010101](https://clawhub.ai/user/serg010101)

### License/Terms of Use:


## Use Case:

External users use this OpenClaw skill to log meals in chat, maintain local macro and micronutrient records, receive progress insights, and view daily nutrition status in a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal and nutrition history may include sensitive health-adjacent personal data and is saved in multiple local files.

Mitigation: Use explicit meal-log commands, keep the workspace private, and sanitize nutrition, memory, mirror, and insight files before publishing or sharing.

Risk: The browser dashboard loads an unpinned third-party Chart.js script.

Mitigation: Pin or bundle the dashboard dependency and review the dashboard asset before relying on it in a managed environment.

Risk: The workspace-root HTTP server instruction can expose more local files than the dashboard needs.

Mitigation: Prefer the offline dashboard or serve only the dashboard asset directory instead of the workspace root.

Risk: Dashboard rendering can display meal, insight, or food-memory content supplied through chat logs.

Mitigation: Sanitize displayed values and prefer safe DOM text APIs before using the dashboard with untrusted or shared data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/serg010101/skills/my-fitness-claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with JSON, JavaScript, and Markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists meal logs, targets, common-food notes, dashboard mirror data, and generated insights in local workspace files.]

## Skill Version(s):

1.7.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
