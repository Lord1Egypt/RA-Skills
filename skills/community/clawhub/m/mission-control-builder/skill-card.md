## Description:

Builds a personal OpenClaw mission-control dashboard with task management, memory browsing, calendar views, team tracking, and GitHub trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shukiclaw](https://clawhub.ai/user/shukiclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create a local Next.js dashboard for tracking tasks, browsing OpenClaw memories, viewing calendar data, managing team status, and surfacing GitHub trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated memory sync API can expose local OpenClaw memory excerpts if served beyond a trusted local environment.

Mitigation: Bind the dashboard to localhost or a private network, add authentication before enabling memory sync, and avoid deploying it publicly without access controls.

Risk: The memory sync route reads from an implicit local memory directory.

Mitigation: Make the memory directory explicitly configurable and document the selected path before running the dashboard.

Risk: Bulk memory excerpts may reveal sensitive personal or project information.

Mitigation: Return metadata or selected records by default, and expose full memory content only after user selection and review.

Risk: Unpinned npm dependencies can make setup less reproducible.

Mitigation: Pin package versions or commit a lockfile before sharing or deploying the generated dashboard.

## Reference(s):

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [Lucide Icons](https://lucide.dev)
- [Mission Control Builder on ClawHub](https://clawhub.ai/shukiclaw/skills/mission-control-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for a local dashboard; generated application behavior depends on the user's environment and any security hardening they add.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
