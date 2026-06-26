## Description: <br>
Guides users through installing the Maton API Plan browser-capture Chrome extension and using exported or relay-fetched matonPlan JSON with API Gateway to suggest Maton OAuth connectors based on browsing activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robert0812](https://clawhub.ai/user/robert0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install or pair the Maton browser-capture extension, ingest matonPlan JSON from downloads or a local relay, and decide which Maton API Gateway OAuth connectors to add with user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browsing-derived summaries and connector suggestions can reveal sensitive activity. <br>
Mitigation: Exclude sensitive origins, install from the Chrome Web Store when possible, and share exported matonPlan data only when comfortable with agent analysis. <br>
Risk: OAuth connector setup can affect accounts and data access. <br>
Mitigation: Require clear user approval before opening or completing any Maton OAuth connector flow. <br>
Risk: The local relay may expose recent browser-derived exports if left enabled or unprotected. <br>
Mitigation: Enable the relay only when needed, use a relay token, and protect MATON_API_KEY and relay credentials. <br>


## Reference(s): <br>
- [Maton browse plan homepage](https://github.com/Robert0812/maton-browse-plan) <br>
- [Maton API Plan Chrome Web Store listing](https://chromewebstore.google.com/detail/dgecpbbjdgiindogaboidejihbmkhnai) <br>
- [API Gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [matonPlan JSON Schema](artifact/maton-plan.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON field references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May analyze matonPlan JSON and local relay responses; requires MATON_API_KEY for API Gateway operations.] <br>

## Skill Version(s): <br>
1.3.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
