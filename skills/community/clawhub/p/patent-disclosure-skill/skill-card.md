## Description:

China patents skill for mining patent points, drafting China patent disclosures, converting disclosures into application documents, searching CNIPA bibliographic records, explaining patents, briefing examination-policy changes, and assisting office-action responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomestwei](https://clawhub.ai/user/handsomestwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, patent practitioners, and technical teams use this skill to draft and iterate China patent disclosures, produce application document sets from completed disclosures, run CNIPA publication searches, explain patent documents, prepare policy briefs, and draft office-action response materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles potentially confidential patent material while some helpers can make web or browser requests.

Mitigation: Use only trusted inputs and approved networks; avoid processing untrusted URLs and do not enable online embeddings for confidential matters unless the provider and data policy are acceptable.

Risk: Local browser and SVG-related helpers may process untrusted content.

Mitigation: Keep temporary browser/SVG serving on loopback, avoid untrusted SVG files, and review generated files before relying on them.

Risk: Dependency behavior can vary across user environments.

Mitigation: Pin dependencies in the deployment environment and review the optional browser, Obsidian, CAD, and embedding setup before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomestwei/skills/patent-disclosure-skill)
- [AgentSkills layout](https://agentskills.io)
- [Python](https://www.python.org/)
- [Playwright](https://playwright.dev/)
- [Obsidian CLI](https://help.obsidian.md/cli)
- [CNIPA publication search](http://epub.cnipa.gov.cn/)
- [Patent disclosure reference schemas](skills/patent-disclosure/references/schemas/README.md)
- [Patent application schema references](skills/patent-application/references/schemas/README.md)
- [Patent docket phase model](skills/patent-docket/references/phase_machine.md)
- [Patent reader output format](skills/patent-reader/references/patent_obsidian_format.md)
- [Patent examination policy sources](skills/patent-exam-policy/references/sources.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown, JSON/YAML configuration, shell commands, generated document files, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes user-facing outputs under workspace output directories; some workflows can generate Word documents, patent figures, Obsidian notes, and search reports.]

## Skill Version(s):

4.5.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
