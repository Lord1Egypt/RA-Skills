## Description:

Generates browser-ready HTML presentation files by splitting supplied speech or presentation content into logical slides with a minimalist Jobs-style layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidong](https://clawhub.ai/user/qidong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn presentation text or speech content into a navigable HTML slide deck that can be opened in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentations can execute injected browser script when untrusted content is included in slide text.

Mitigation: Review generated HTML before use, avoid hosting it on a sensitive origin, and prefer escaping slide text and validating color options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidong/skills/ppt-generator-template)
- [Publisher profile](https://clawhub.ai/user/qidong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and generated HTML presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML should be treated as active browser content when sourced from untrusted input.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
