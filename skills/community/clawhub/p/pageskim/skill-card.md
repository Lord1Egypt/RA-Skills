## Description:

PageSkim helps developers make websites readable by LLMs and agents at 10-50x fewer tokens by generating .llm.md sibling files, site indexes, build wiring, and CI validation for plain HTML, Astro, Next.js, Hugo, and Jekyll sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[venki0552](https://clawhub.ai/user/venki0552)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to add PageSkim generation, site indexing, build integration, and CI validation to static or pre-rendered websites so agents can read generated sibling files instead of raw HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Build and CI instructions may execute mutable third-party npm package or GitHub Action code.

Mitigation: Review before installing or using in CI; prefer pinning pageskim to a reviewed exact version or locked dependency, and pin the GitHub Action to a full commit SHA with minimal workflow permissions and limited secrets exposure.

## Reference(s):

- [PageSkim repository](https://github.com/venki0552/PageSkim)
- [PageSkim format spec](https://github.com/venki0552/PageSkim/blob/main/spec/SPEC.md)
- [PageSkim publisher guide](https://github.com/venki0552/PageSkim/blob/main/docs/integration.md)
- [PageSkim live playground](https://page-skim.vercel.app)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or propose .llm.md, .llm.json, split files, /.well-known/pageskim.json, build scripts, and CI validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
