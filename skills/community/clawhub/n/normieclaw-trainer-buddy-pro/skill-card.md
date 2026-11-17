## Description:

Trainer Buddy Pro helps an agent generate personalized workouts from equipment photos and user goals, track workout history and PRs, adapt programming around reported injuries, and provide concise form guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill as a chat-based fitness coach for workout planning, workout logging, progressive overload tracking, PR summaries, and injury-aware exercise substitutions. Developers can also use the included configuration, examples, backup script, and dashboard specification to extend the local workout-tracking workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal fitness, body, and injury information that may be sensitive.

Mitigation: Keep workout and profile data local by default, restrict file permissions, and avoid sharing logs or profiles outside the user's context.

Risk: The optional dashboard path can extend local fitness data into a cloud database.

Mitigation: Do not enable the Supabase or dashboard flow without explicit user consent, strong per-user row-level security, and clear deletion and retention controls.

Risk: The included backup script is not reliable enough to depend on without review.

Mitigation: Review, fix, and test the backup script before using it for user data preservation.

Risk: The package overstates its security posture compared with the server security review.

Mitigation: Present the release as requiring review before installation and rely on the server security summary rather than marketing-style audit claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-trainer-buddy-pro)
- [README](artifact/README.md)
- [Security audit](artifact/SECURITY.md)
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Workout generation example](artifact/examples/workout-generation.md)
- [Progress tracking example](artifact/examples/progress-tracking.md)
- [Form coaching example](artifact/examples/form-check.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON fitness data such as profiles, workout logs, PR history, and configuration files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
