## Description:

Generates McKinsey consulting-style multi-page HTML presentation decks with data-driven slide layouts, SVG charts, and source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinin2005](https://clawhub.ai/user/yinin2005)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a business topic and generate a consulting-style HTML slide deck with charts, citations, and presentation-ready layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger on broad presentation requests and directs the agent to perform external research, which may expose confidential business plans or client data.

Mitigation: Confirm the topic and data sensitivity with the user before research, avoid confidential inputs unless explicitly authorized, and prefer public or approved sources.

Risk: The workflow includes deployment of the completed presentation.

Mitigation: Require explicit user approval before running any deployment or publication step.

Risk: Generated presentations may contain stale, incorrect, or weakly supported claims if research quality is poor.

Mitigation: Use authoritative current sources, record source names, dates, and URLs, cite every data slide, and manually review claims before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinin2005/skills/mckinsey-presentation-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, SVG, citation tables, and deployment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current external research, source citations on data slides, screenshot verification, and manual confirmation before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
