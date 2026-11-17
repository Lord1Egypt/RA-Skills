## Description:

Build robust Laravel apps avoiding Eloquent traps, queue failures, and auth pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for concise Laravel guidance on Eloquent, controllers, queues, authentication, Blade templates, and Artisan commands so they can avoid common framework pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Laravel commands may affect databases, queues, cached configuration, or production environments.

Mitigation: Confirm the target environment and database impact before applying migrations, tinker saves, queue worker commands, or production commands using --force.

Risk: Framework guidance can be misapplied when the application's Laravel version, middleware stack, or deployment model differs from the examples.

Mitigation: Review recommendations against the application's codebase, tests, and deployment process before making changes.

## Reference(s):

- [ClawHub Laravel skill page](https://clawhub.ai/ivangdavila/skills/laravel)
- [Eloquent Traps](artifact/eloquent.md)
- [Controller Traps](artifact/controllers.md)
- [Queue Traps](artifact/queues.md)
- [Auth Traps](artifact/auth.md)
- [Blade Traps](artifact/blade.md)
- [Artisan Traps](artifact/artisan.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Laravel project context; metadata indicates php and composer are expected on linux, darwin, or win32.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
