## Description:

Exports public Douyin search, creator-post, comment, and hot-list data as JSON for content planning, marketing research, and traffic analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content teams use this skill to map natural-language Douyin data requests to Node.js CLI commands for public keyword search, creator post export, comment retrieval, and hot-list lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei token and Douyin query inputs to www.guaikei.com.

Mitigation: Use a limited token where possible, avoid sensitive search terms, and review the skill before installation.

Risk: The security evidence reports misleading authentication-error behavior compared with the skill's own neutral-error policy.

Mitigation: Treat authentication failures cautiously and do not rely on runtime error text as policy-compliant guidance.

Risk: The skill saves result exports locally.

Mitigation: Delete exported logs when no longer needed and avoid storing sensitive research queries or results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-json-comments-export)
- [Guaikei token and help site](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with Node.js command examples; CLI stdout is JSON and exports may be saved as JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; individual requests are documented with a maximum limit of 10000 records.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
