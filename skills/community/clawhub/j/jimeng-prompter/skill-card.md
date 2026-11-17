## Description:

Jimeng Prompter helps agents interview users and produce optimized Jimeng AI prompts for Seedance video and Seedream image generation, including model routing, style guidance, prompt calibration, and local preference-memory controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyface0](https://clawhub.ai/user/sallyface0)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and prompt engineers use this skill to turn rough image or video ideas into Jimeng-ready prompts, parameters, storyboard guidance, negative prompts, and iteration advice. It is intended for normal ClawHub release use, with local preference memory reviewed before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cross-session visual preference memory needs review because the bundled memory reference still describes automatic preference updates despite consent promises elsewhere.

Mitigation: Before relying on the skill, review or disable references/evolution-memory.md, require an explicit yes before every preference write, and periodically inspect or delete stored preferences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sallyface0/skills/jimeng-prompter)
- [Publisher profile](https://clawhub.ai/user/sallyface0)
- [Privacy Policy](PRIVACY.md)
- [Evolution Memory Reference](references/evolution-memory.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured prompt blocks, tables, and parameter recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jimeng model routing, prompt text, negative prompts, timeline segments, storyboard tables, concept-image prompt guidance, and local preference-memory notices.]

## Skill Version(s):

3.1.0 (source: server release evidence, frontmatter, and CHANGELOG released 2026-07-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
