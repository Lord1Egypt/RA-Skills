## Description:

Designs a Web MVP for making SKILL.md capabilities usable by non-technical users through upload, conversational parameter collection, dynamic UI rendering, and an agent execution loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and product builders use this skill to plan an MVP that turns command-line skills into a web-based experience for non-technical users. It produces an implementation-oriented architecture, API outline, phased delivery checklist, validation plan, and risk boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The planned platform executes uploaded or third-party skills, which can create security exposure if shipped without execution controls.

Mitigation: Require authentication, per-skill ownership checks, sandboxed per-run execution, restricted tools and network access, credential isolation, path validation, audit logs, quotas, and explicit warnings before executing uploaded skills.

Risk: The skill is a planning reference, so generated implementation guidance may be incomplete or unsafe if treated as production-ready.

Mitigation: Use the output as a reviewed design starting point and complete security, operational, and product review before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/interactive-skills-platform-mvp)
- [Project Homepage](https://github.com/wangzhiming1999/oliver-skill)
- [Claude Agent SDK Reference](https://github.com/anthropics/anthropic-sdk-python)
- [felo-skills Repository](https://github.com/Felo-Inc/felo-skills)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with architecture notes, API sketches, phased checklists, test cases, and risk guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default response language is Chinese unless the user requests otherwise.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
