## Description:

Builds, optimizes, and reviews React and Next.js applications with TypeScript and Tailwind CSS, including project scaffolding, component generation, bundle analysis, performance optimization, accessibility, and frontend code quality review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers and engineering teams use this skill to scaffold React or Next.js projects, generate typed components and hooks, analyze bundle size, and apply accessibility and performance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project files and component code can introduce unwanted changes if run directly in a working project.

Mitigation: Use dry-run modes when available and review generated files before keeping them.

Risk: Generated package manifests and next-step commands can lead users to install dependency versions without review.

Mitigation: Review and pin dependency versions before running npm install.

Risk: Reference examples include persisted auth state patterns that are unsuitable for sensitive production tokens.

Mitigation: Avoid storing auth tokens in localStorage; prefer server-managed HttpOnly secure cookies or keep sensitive tokens out of persistent browser storage.

## Reference(s):

- [Senior Frontend ClawHub Skill Page](https://clawhub.ai/felix-antonio-sl/skills/kv-senior-frontend)
- [Frontend Best Practices](references/frontend_best_practices.md)
- [Next.js Optimization Guide](references/nextjs_optimization_guide.md)
- [React Patterns](references/react_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, TSX, JSON, and bash code blocks; scripts may create workspace files or JSON bundle reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run modes for scaffolding and component generation; bundle analysis can emit JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
