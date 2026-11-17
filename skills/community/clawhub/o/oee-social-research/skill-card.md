## Description:

Conducts tiered social media research on X/Twitter and web sources, then compiles public discussion into structured briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odinbot33](https://clawhub.ai/user/odinbot33)

### License/Terms of Use:


## Use Case:

Agents and operators use this skill to gather public social discussion about a topic and produce a concise briefing with sentiment, narrative themes, notable posts, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be sent to third-party search and social endpoints.

Mitigation: Use only public, non-sensitive topics unless the operator accepts disclosure to those services.

Risk: Local cache, log, and briefing files may retain researched topics and collected results.

Mitigation: Review and clear `.cache`, `.logs`, and `.briefings` when topic retention is not desired.

Risk: Documented `--tier` and `--briefing` examples are not fully supported by the implementation.

Mitigation: Do not treat those options as privacy or retrieval controls until the implementation is updated and retested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odinbot33/skills/oee-social-research)
- [Publisher profile](https://clawhub.ai/user/odinbot33)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured text briefing with topic summary, sentiment counts, narrative themes, notable posts, links, and an optional saved briefing file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache results and write local logs and briefing files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
