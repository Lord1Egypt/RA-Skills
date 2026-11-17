## Description:

Daily health-article pipeline for WeChat public accounts that guides an agent through topic angle selection, recent-article deduplication, 2,000+ character article drafting, platform compliance self-checks, styled HTML generation, and article library updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meimei-shoulu](https://clawhub.ai/user/meimei-shoulu)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators of Chinese health or wellness WeChat public accounts use this skill to draft daily long-form posts, rotate article angles, avoid recent self-duplication, run platform compliance checks, generate styled HTML, and update a local article library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to remember local writing folders and can update persistent local HTML article libraries.

Mitigation: Confirm exact write paths before running the library script and review local file changes before publishing or reusing the generated library.

Risk: The skill includes off-platform WeChat payment and contact instructions for an upgraded package.

Mitigation: Treat payment and contact steps as an external transaction outside platform safeguards and do not share sensitive information through the agent.

Risk: Generated health and wellness articles may contain unsupported medical claims or platform-sensitive promotional language.

Mitigation: Apply the included compliance checklist and human review for medical claims, efficacy promises, extreme advertising terms, fabricated credentials, and direct off-platform promotion before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meimei-shoulu/skills/health-gzh-daily)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated article text, inline HTML, shell commands, and local HTML file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update a persistent local article library when the bundled script is run.]

## Skill Version(s):

1.2.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
