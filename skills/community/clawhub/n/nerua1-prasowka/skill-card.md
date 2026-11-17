## Description:

Generates a daily news portal as a single HTML file with fetched news and summaries across 18 categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather current news across AI, technology, science, markets, world, and Polish topics and generate a responsive daily HTML portal with concise article summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live news content can be rendered into HTML without safe escaping, which can allow browser-side script execution from a malicious article or URL.

Mitigation: Escape rendered article fields, validate article links to http/https, and add rel="noopener noreferrer" on external links before installation or publication.

Risk: Some artifact behavior uses hard-coded output paths beyond the documented workspace.

Mitigation: Restrict writes to documented workspace paths and make output locations configurable through the documented parameters.

Risk: Multiple generator scripts make it unclear which generation path is authoritative.

Mitigation: Clarify the supported generator entrypoint and remove or deprecate inconsistent alternatives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerua1/skills/nerua1-prasowka)
- [Publisher profile](https://clawhub.ai/user/nerua1)
- [Topic definitions](artifact/references/topics.md)
- [Source definitions](artifact/references/sources.md)
- [HTML format reference](artifact/references/format.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Single HTML file plus JSON state for seen article URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live web sources and local browser features such as theme, bookmark, and read-state storage.]

## Skill Version(s):

1.0.2 (source: release evidence; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
